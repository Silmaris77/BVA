"""
Usuń custom permissions z użytkownika mil2
Aby używał TYLKO systemu tagów (resource_tags.json)
"""

from database.models import User
from database.connection import session_scope

with session_scope() as session:
    user = session.query(User).filter_by(username='mil2').first()
    
    if user:
        print(f"=== PRZED ZMIANĄ ===")
        print(f"Username: {user.username}")
        print(f"Company: {user.company}")
        print(f"Permissions: {user.permissions}")
        
        # Usuń permissions - będzie używał systemu tagów
        user.permissions = None
        session.commit()
        
        print(f"\n=== PO ZMIANIE ===")
        print(f"Username: {user.username}")
        print(f"Company: {user.company}")
        print(f"Permissions: {user.permissions}")
        print("\n✅ Teraz mil2 używa TYLKO systemu tagów z resource_tags.json")
    else:
        print("❌ Nie znaleziono użytkownika mil2")
