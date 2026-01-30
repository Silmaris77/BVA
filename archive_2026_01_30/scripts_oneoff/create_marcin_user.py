"""
Dodaj użytkownika Marcin do bazy SQL
"""
from database.connection import session_scope
from database.models import User
from datetime import datetime

username = "Marcin"

try:
    with session_scope() as session:
        # Sprawdź czy już istnieje
        existing = session.query(User).filter_by(username=username).first()
        
        if existing:
            print(f"✅ Użytkownik '{username}' już istnieje (ID: {existing.user_id})")
        else:
            # Stwórz użytkownika
            new_user = User(
                username=username,
                password_hash="haslo123",  # Placeholder
                degen_type="Architect",  # Z users_data.json
                xp=0,
                degencoins=0,
                level=1,
                joined_date=datetime.now().date(),
                test_taken=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            session.add(new_user)
            session.commit()
            
            print(f"✅ Utworzono użytkownika '{username}' (ID: {new_user.user_id})")
            
except Exception as e:
    print(f"❌ Błąd: {e}")
    import traceback
    traceback.print_exc()
