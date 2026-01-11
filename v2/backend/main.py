import sys
import os

# Dodaj katalog główny projektu do ścieżki Pythona, aby umożliwić importy z v2.backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import bcrypt

# Używamy pełnych ścieżek importu, zakładając uruchomienie z root dir
from v2.backend.database import get_db, engine, SessionLocal
from v2.backend import models, schemas
from v2.backend import auth 

# Utworzenie tabel
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BrainVentureAcademy API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:8501", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routery
# Routery
from v2.backend.routers import milwaukee, lessons
app.include_router(milwaukee.router)
app.include_router(lessons.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- DATA SEEDING ---
def init_lessons(db: Session):
    """Seed initial lessons if table is empty"""
    try:
        # Check if table exists and has data
        if db.query(models.Lesson).count() == 0:
            print("Seeding initial lessons...")
            lessons_data = [
                models.Lesson(
                    id="intro-1",
                    title="Wprowadzenie do Akademii",
                    description="Poznaj misję BVA i dowiedz się, jak korzystać z platformy.",
                    category="Onboarding",
                    video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", 
                    thumbnail_url="/images/lessons/intro.jpg",
                    duration=300,
                    xp_reward=50,
                    difficulty="Beginner",
                    order=1
                ),
                 models.Lesson(
                    id="strat-1",
                    title="Podstawy Strategii Błękitnego Oceanu",
                    description="Jak unikać konkurencji i tworzyć nowe rynki.",
                    category="Strategia",
                    video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
                    thumbnail_url="/images/lessons/strategy.jpg",
                    duration=600,
                    xp_reward=150,
                    difficulty="Intermediate",
                    order=2
                ),
                 models.Lesson(
                    id="tool-1",
                    title="Obsługa Narzędzi Milwaukee",
                    description="Naucz się dobierać idealny zestaw narzędzi dla klienta.",
                    category="Narzędzia",
                    video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
                    duration=450,
                    xp_reward=100,
                    difficulty="Beginner",
                    order=3
                ),
                models.Lesson(
                    id="exec-1",
                    title="Zarządzanie Zespołem Sprzedażowym",
                    description="Techniki motywacyjne dla liderów.",
                    category="Leadership",
                    video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
                    duration=900,
                    xp_reward=300,
                    difficulty="Expert",
                    order=4
                )
            ]
            for l in lessons_data:
                db.merge(l) # merge prevents primary key errors if partly seeded
            db.commit()
    except Exception as e:
        print(f"Seeding failed: {e}")

def init_users(db: Session):
    """Seed initial admin user if not exists"""
    try:
        user = db.query(models.User).filter(models.User.username == "admin").first()
        if not user:
            print("Creating admin user...")
            hashed_password = auth.get_password_hash("admin123")
            admin_user = models.User(
                username="admin",
                email="admin@bva.pl",
                full_name="Administrator",
                hashed_password=hashed_password,
                is_active=True,
                role="admin",
                xp=0,
                level=1,
                streak_days=0
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
    except Exception as e:
        print(f"Error checking/seeding users: {e}")

@app.on_event("startup")
def on_startup():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Inicjalizacja danych
    db = SessionLocal()
    try:
        init_lessons(db)
        init_users(db)
    finally:
        db.close()
    
# --- Funkcje Pomocnicze ---
def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        return False

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# --- Endpointy ---

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    password_valid = False
    
    if user.password_hash:
        if verify_password(form_data.password, user.password_hash):
            password_valid = True
        elif user.password_hash == form_data.password:
            password_valid = True
    
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserStats)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

@app.put("/users/me", response_model=schemas.UserStats)
async def update_user_me(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Re-fetch user to ensure attachment to current db session
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.company is not None:
        user.company = user_update.company
    if user_update.avatar_url is not None:
        user.avatar_url = user_update.avatar_url
    if user_update.degen_type is not None:
        current_user.degen_type = user_update.degen_type
    if user_update.preferences is not None:
        current_user.preferences = user_update.preferences
    
    db.add(current_user)
    db.refresh(user)
    return user

@app.get("/users/{username}/stats", response_model=schemas.UserPublic)
async def get_user_stats(username: str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{username}/activities", response_model=list[schemas.ActivityLog])
async def get_user_activities(username: str, limit: int = 5, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    activities = db.query(models.ActivityLog).filter(
        models.ActivityLog.user_id == user.user_id
    ).order_by(models.ActivityLog.timestamp.desc()).limit(limit).all()
    
    return activities

@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "2.0.0", "db": "connected"}
