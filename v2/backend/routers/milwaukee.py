from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import sys
import os

# Dodaj ścieżkę do głównego katalogu projektu, aby zaimportować utils
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from utils.milwaukee_recommender import MilwaukeeRecommender
from v2.backend import schemas
from v2.backend.database import get_db
from v2.backend.auth import get_current_active_user

router = APIRouter(
    prefix="/tools/milwaukee",
    tags=["milwaukee"],
    responses={404: {"description": "Not found"}},
)

# Inicjalizacja rekomendera (singleton-like)
recommender = MilwaukeeRecommender()

@router.get("/context-questions")
async def get_context_questions():
    """Zwraca pytania do kroku 1: Kontekst"""
    return recommender.questions.get('context_questions', {})

@router.post("/match-application", response_model=List[schemas.MilwaukeeAppMatch])
async def match_application(context: schemas.MilwaukeeContext):
    """Krok 2: Dopasuj aplikacje na podstawie kontekstu"""
    # Konwersja Pydantic model do dict
    ctx_dict = context.dict()
    matches = recommender.match_application(ctx_dict)
    
    results = []
    for app_id, score, reason in matches:
        details = recommender.get_application_details(app_id)
        results.append({
            "app_id": app_id,
            "score": score,
            "reason": reason,
            "details": details
        })
    
    return results

@router.get("/discovery-questions/{client_type}", response_model=List[schemas.DiscoveryQuestion])
async def get_discovery_questions(client_type: str):
    """Krok 3: Pytania pogłębiające dla typu klienta"""
    questions = recommender.get_discovery_questions(client_type)
    if not questions:
        return []
    
    # Standaryzacja ID (recommender może nie zwracać ID, więc generujemy)
    standardized = []
    for idx, q in enumerate(questions, 1):
        q_id = q.get('id', f'q_{idx}')
        standardized.append({
            "id": q_id,
            "question": q.get('question', ''),
            "type": q.get('type', 'choice'),
            "options": q.get('options'),
            "scale": q.get('scale'),
            "purpose": q.get('purpose')
        })
        
    return standardized

@router.post("/recommendation", response_model=schemas.RecommendationPackage)
async def get_recommendation(
    request: schemas.RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: schemas.UserStats = Depends(get_current_active_user) # Require auth
):
    """Krok 4: Generowanie pełnej rekomendacji i zapis wyniku"""
    
    # 1. Scoring produktów
    product_scores = recommender.calculate_product_scores(request.answers)
    
    # 2. Buduj pakiet
    package = recommender.build_recommendation_package(request.app_id, product_scores)
    
    # 3. Zapisz wynik (Persistence)
    try:
        from v2.backend import models
        import json
        
        tool_result = models.ToolResult(
            user_id=current_user.user_id,
            tool_id="milwaukee_advisor",
            input_data=request.json(),
            output_data=json.dumps(package) # Zapisujemy tylko core package
        )
        db.add(tool_result)
        
        # 4. Dodaj ActivityLog i XP
        activity = models.ActivityLog(
            user_id=current_user.user_id,
            activity_type="tool_used",
            description=f"Użyto narzędzia Milwaukee: {request.app_id}",
            xp_awarded=50,
            metadata_json={"tool": "milwaukee", "app_id": request.app_id}
        )
        db.add(activity)
        
        # 5. Update User Stats
        user = db.query(models.User).filter(models.User.user_id == current_user.user_id).first()
        if user:
            user.xp = (user.xp or 0) + 50
            # Simple level up logic (e.g. every 1000 XP)
            user.level = 1 + (user.xp // 1000)
            
        db.commit()
    except Exception as e:
        print(f"Error saving result: {e}")
        # Nie blokujemy response jeśli zapis się nie uda
    
    # 6. Dodaj skrypty, ROI, case studies
    app_data = recommender.get_application_details(request.app_id)
    persuasion = recommender.get_persuasion_script(request.app_id)
    roi = recommender.get_roi_calculator(request.app_id)
    cases = recommender.get_case_studies(request.app_id)
    
    return {
        "package": package,
        "persuasion_script": persuasion,
        "roi_calculator": roi,
        "case_studies": cases
    }
