"""
Dodaj użytkownika admin do bazy SQL z company=Milwaukee
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.models import User
from database.connection import session_scope
import uuid
from datetime import datetime

def add_admin_user():
    """Dodaj użytkownika admin do SQL"""
    
    print("🔧 Dodawanie użytkownika admin do bazy SQL")
    print("=" * 60)
    
    with session_scope() as session:
        # Sprawdź czy admin już istnieje
        existing = session.query(User).filter_by(username='admin').first()
        
        if existing:
            print(f"⊙ Użytkownik 'admin' już istnieje")
            print(f"  Current company: {existing.company}")
            
            # Aktualizuj company jeśli nie jest ustawione
            if existing.company != 'Milwaukee':
                existing.company = 'Milwaukee'
                session.commit()
                print(f"  ✓ Zaktualizowano company na 'Milwaukee'")
            else:
                print(f"  ✓ Company już ustawione na 'Milwaukee'")
            
        else:
            # Utwórz nowego użytkownika admin
            new_admin = User(
                user_id=str(uuid.uuid4()),
                username='admin',
                password_hash='admin',  # W produkcji zahashować!
                company='Milwaukee',
                permissions=None,  # Użyje szablonu Milwaukee
                account_created_by='system',
                xp=0,
                level=1,
                degencoins=0,
                test_taken=False,
                joined_date=datetime.now().date()
            )
            
            session.add(new_admin)
            session.commit()
            print(f"  ✓ Utworzono użytkownika 'admin' z company='Milwaukee'")
    
    print("=" * 60)
    print("✅ Gotowe!")
    print("\nTeraz:")
    print("1. Zatrzymaj aplikację Streamlit (Ctrl+C)")
    print("2. Uruchom ponownie: .\\run.bat")
    print("3. Zaloguj się jako admin")
    print("4. Lekcja Milwaukee powinna być dostępna!")

if __name__ == "__main__":
    try:
        add_admin_user()
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
