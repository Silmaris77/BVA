"""
Aktualizuje scenario_id w game_state dla użytkownika Carl
"""

from database.models import User, BusinessGame
from database.connection import session_scope
import json

username = "Carl"

try:
    with session_scope() as session:
        # Find user
        user = session.query(User).filter_by(username=username).first()
        
        if not user:
            print(f"❌ Użytkownik '{username}' nie istnieje w SQL")
        else:
            # Find FMCG game
            fmcg_game = session.query(BusinessGame).filter_by(
                user_id=user.user_id,
                scenario_type="fmcg"
            ).first()
            
            if not fmcg_game:
                print(f"❌ Użytkownik '{username}' nie ma gry FMCG")
            else:
                # Get extra_data
                extra_data = fmcg_game.extra_data or {}
                
                # Check current scenario_id
                current_scenario = extra_data.get("scenario_id", "BRAK")
                print(f"📊 Obecne scenario_id: {current_scenario}")
                
                # Add scenario_id to game_state if missing
                if "scenario_id" not in extra_data:
                    extra_data["scenario_id"] = "fmcg_heinz_food_service_v1"
                    print(f"✅ Dodano scenario_id do top-level")
                
                # Update fmcg_state scenario_id
                if isinstance(extra_data, dict):
                    # Check all possible locations
                    for key in ["fmcg_state", "game_state"]:
                        if key in extra_data and isinstance(extra_data[key], dict):
                            extra_data[key]["scenario_id"] = "fmcg_heinz_food_service_v1"
                            print(f"✅ Zaktualizowano scenario_id w {key}")
                
                # Save
                fmcg_game.extra_data = extra_data
                session.commit()
                
                print(f"✅ SUKCES - Zaktualizowano scenario_id dla '{username}'")
                print(f"   Teraz produkty Heinz powinny wyświetlać się poprawnie")
                
except Exception as e:
    print(f"❌ BŁĄD: {e}")
    import traceback
    traceback.print_exc()
