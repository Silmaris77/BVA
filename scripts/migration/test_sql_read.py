"""
Test SQL Read - Sprawdza czy dane są poprawnie zapisane w SQL
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data.repositories import UserRepository
from database.models import User
from database.connection import session_scope


def test_sql_read(username: str):
    """Test odczytu użytkownika z SQL"""
    print("="*60)
    print(f"🧪 TESTING SQL READ FOR USER: {username}")
    print("="*60)
    
    # Test 1: Direct SQL query
    print("\n📊 Test 1: Direct SQL Query")
    try:
        with session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            
            if user:
                print(f"✅ User found in database!")
                print(f"   - ID: {user.id}")
                print(f"   - User ID: {user.user_id}")
                print(f"   - Username: {user.username}")
                print(f"   - XP: {user.xp}")
                print(f"   - DegenCoins: {user.degencoins}")
                print(f"   - Level: {user.level}")
                print(f"   - Degen Type: {user.degen_type}")
                print(f"   - Joined: {user.joined_date}")
                print(f"   - Last Login: {user.last_login}")
            else:
                print(f"❌ User not found!")
                return False
    except Exception as e:
        print(f"❌ SQL query failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Repository with SQL backend
    print("\n📊 Test 2: UserRepository with SQL Backend")
    try:
        repo = UserRepository(backend="sql")
        
        if not repo.sql_available:
            print(f"❌ SQL backend not available in repository!")
            return False
        
        user_data = repo.get(username)
        
        if user_data:
            print(f"✅ User loaded via Repository!")
            print(f"   - XP: {user_data.get('xp', 0)}")
            print(f"   - DegenCoins: {user_data.get('degencoins', 0)}")
            print(f"   - Level: {user_data.get('level', 1)}")
        else:
            print(f"❌ User not found via Repository!")
            return False
    except Exception as e:
        print(f"❌ Repository read failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Compare JSON vs SQL
    print("\n📊 Test 3: JSON vs SQL Comparison")
    try:
        json_repo = UserRepository(backend="json")
        sql_repo = UserRepository(backend="sql")
        
        json_data = json_repo.get(username)
        sql_data = sql_repo.get(username)
        
        if json_data and sql_data:
            # Compare basic fields
            fields_to_compare = ['xp', 'degencoins', 'level', 'user_id']
            all_match = True
            
            for field in fields_to_compare:
                json_val = str(json_data.get(field, 'N/A'))
                sql_val = str(sql_data.get(field, 'N/A'))
                
                match = json_val == sql_val
                symbol = "✅" if match else "❌"
                
                print(f"   {symbol} {field}: JSON={json_val}, SQL={sql_val}")
                
                if not match:
                    all_match = False
            
            if all_match:
                print(f"\n✅ All fields match!")
            else:
                print(f"\n⚠️  Some fields don't match")
        else:
            print(f"❌ Could not load data for comparison")
            return False
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60)
    
    return True


def list_all_users_in_sql():
    """Wyświetla wszystkich użytkowników w SQL"""
    print("="*60)
    print("📋 ALL USERS IN SQL DATABASE")
    print("="*60)
    
    try:
        with session_scope() as session:
            users = session.query(User).all()
            
            if users:
                print(f"\nTotal users: {len(users)}\n")
                print(f"{'#':<4} {'Username':<20} {'XP':<8} {'Coins':<10} {'Level':<6}")
                print("-"*60)
                
                for idx, user in enumerate(users, 1):
                    print(f"{idx:<4} {user.username:<20} {user.xp:<8} {user.degencoins:<10} {user.level:<6}")
            else:
                print("\n❌ No users found in database")
    except Exception as e:
        print(f"\n❌ Failed to list users: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test SQL read functionality")
    parser.add_argument("username", nargs="?", default="Max", help="Username to test (default: Max)")
    parser.add_argument("--list", action="store_true", help="List all users in SQL")
    
    args = parser.parse_args()
    
    if args.list:
        list_all_users_in_sql()
    else:
        success = test_sql_read(args.username)
        sys.exit(0 if success else 1)
