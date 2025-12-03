"""
Usuwa grę FMCG dla użytkownika Carl (zachowuje konto)
"""

from database.models import User, BusinessGame
from database.connection import session_scope

username = "Carl"

try:
    with session_scope() as session:
        # Find user
        user = session.query(User).filter_by(username=username).first()
        
        if not user:
            print(f"❌ Użytkownik '{username}' nie istnieje w SQL")
        else:
            print(f"✅ Znaleziono użytkownika '{username}' (user_id: {user.user_id})")
            
            # Find FMCG game
            fmcg_game = session.query(BusinessGame).filter_by(
                user_id=user.user_id,
                scenario_type="fmcg"
            ).first()
            
            if not fmcg_game:
                print(f"ℹ️  Użytkownik '{username}' nie ma gry FMCG w SQL")
            else:
                print(f"🗑️  Usuwam grę FMCG dla użytkownika '{username}'...")
                session.delete(fmcg_game)
                session.commit()
                print(f"✅ SUKCES - Gra FMCG usunięta dla '{username}'")
                print(f"   Teraz przy następnym wejściu do scenariusza Heinz zostanie stworzona nowa gra z cleanup")
                
except Exception as e:
    print(f"❌ BŁĄD: {e}")
    import traceback
    traceback.print_exc()
