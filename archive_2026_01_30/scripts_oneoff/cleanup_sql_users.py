"""
Cleanup SQL - usuwa użytkowników z SQL, których nie ma w JSON
Synchronizuje SQL z aktualnym stanem JSON
"""

import json
from database.connection import session_scope
from database.models import User, BusinessGame

def cleanup_sql_users():
    """Usuwa z SQL użytkowników, których nie ma w JSON"""
    
    # 1. Wczytaj aktualnych użytkowników z JSON
    with open("users_data.json", "r", encoding="utf-8") as f:
        json_users = json.load(f)
    
    valid_usernames = set(json_users.keys())
    
    print("="*60)
    print("🧹 CLEANUP SQL DATABASE")
    print("="*60)
    print(f"\n✅ Valid users in JSON: {len(valid_usernames)}")
    print(f"   {sorted(valid_usernames)}")
    
    # 2. Pobierz wszystkich użytkowników z SQL
    with session_scope() as session:
        sql_users = session.query(User).all()
        
        print(f"\n📊 Users in SQL: {len(sql_users)}")
        
        # 3. Znajdź użytkowników do usunięcia
        to_delete = []
        for user in sql_users:
            if user.username not in valid_usernames:
                to_delete.append(user)
        
        print(f"\n🗑️  Users to DELETE from SQL: {len(to_delete)}")
        for user in to_delete:
            print(f"   ✗ {user.username} (user_id={user.user_id})")
        
        if not to_delete:
            print("\n✅ SQL is already clean - no users to delete")
            return
        
        # 4. Usuń użytkowników
        print(f"\n🔄 Deleting {len(to_delete)} users...")
        
        for user in to_delete:
            # Najpierw usuń powiązane business games RĘCZNIE
            games = session.query(BusinessGame).filter_by(user_id=user.user_id).all()
            print(f"   🗑️  {user.username}: {len(games)} business game(s)")
            
            for game in games:
                # Usuń game (cascade usunie employees, contracts, transactions, stats)
                session.delete(game)
            
            # Potem usuń użytkownika
            session.delete(user)
        
        session.commit()
        
        print(f"\n✅ CLEANUP COMPLETE")
        print(f"   Deleted: {len(to_delete)} users")
        print(f"   Remaining: {len(sql_users) - len(to_delete)} users")
        
        # 5. Weryfikacja
        remaining = session.query(User).all()
        print(f"\n📊 Verification:")
        print(f"   SQL users after cleanup: {len(remaining)}")
        for user in remaining:
            games_count = session.query(BusinessGame).filter_by(user_id=user.user_id).count()
            print(f"   ✓ {user.username} ({games_count} games)")


if __name__ == "__main__":
    cleanup_sql_users()
