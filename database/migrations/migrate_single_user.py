"""
Migrate Single User - Test Migration Script
Migruje pojedynczego użytkownika z JSON do SQL
"""

import sys
from pathlib import Path

# Dodaj główny katalog do PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data.repositories import UserRepository
from database.connection import init_database


def migrate_single_user(username: str, dry_run: bool = True):
    """
    Migruje pojedynczego użytkownika z JSON do SQL
    
    Args:
        username: Nazwa użytkownika do migracji
        dry_run: Jeśli True, tylko symulacja (nie zapisuje do SQL)
    
    Returns:
        bool: True jeśli sukces
    """
    print("="*60)
    print(f"🔄 MIGRATING USER: {username}")
    print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE MIGRATION'}")
    print("="*60)
    
    # Initialize database
    if not dry_run:
        init_database()
        print("✅ Database initialized")
    
    # Create repository (JSON mode)
    repo = UserRepository(backend="json")
    
    # Load user from JSON
    print(f"\n📖 Loading user from JSON...")
    user_data = repo.get(username)
    
    if not user_data:
        print(f"❌ User '{username}' not found in JSON!")
        return False
    
    print(f"✅ User loaded from JSON")
    print(f"   - XP: {user_data.get('xp', 0)}")
    print(f"   - DegenCoins: {user_data.get('degencoins', 0)}")
    print(f"   - Level: {user_data.get('level', 1)}")
    
    # Show business_games info
    if "business_games" in user_data:
        print(f"   - Business Games: {list(user_data['business_games'].keys())}")
    elif "business_game" in user_data:
        print(f"   - Business Game (old format): Found")
    
    # Validate data
    print(f"\n🔍 Validating data...")
    is_valid, error = repo.validate_user_data(user_data)
    
    if not is_valid:
        print(f"❌ Validation failed: {error}")
        return False
    
    print(f"✅ Data is valid")
    
    if dry_run:
        print(f"\n✅ DRY RUN COMPLETE - No changes made")
        print(f"   To actually migrate, run with --migrate flag")
        return True
    
    # Save to SQL
    print(f"\n💾 Saving to SQL database...")
    
    # Temporarily switch to SQL backend
    sql_repo = UserRepository(backend="sql")
    
    if not sql_repo.sql_available:
        print(f"❌ SQL backend not available!")
        return False
    
    success = sql_repo._save_to_sql(username, user_data)
    
    if success:
        print(f"✅ User migrated to SQL successfully!")
        
        # Verify
        print(f"\n🔍 Verifying migration...")
        sql_user_data = sql_repo._get_from_sql(username)
        
        if sql_user_data:
            print(f"✅ User found in SQL database")
            print(f"   - XP: {sql_user_data.get('xp', 0)}")
            print(f"   - DegenCoins: {sql_user_data.get('degencoins', 0)}")
            print(f"   - Level: {sql_user_data.get('level', 1)}")
            
            # Basic comparison
            json_xp = user_data.get('xp', 0)
            sql_xp = sql_user_data.get('xp', 0)
            
            if json_xp == sql_xp:
                print(f"✅ Data matches!")
            else:
                print(f"⚠️  Warning: XP mismatch (JSON: {json_xp}, SQL: {sql_xp})")
        else:
            print(f"❌ User not found in SQL after migration!")
            return False
    else:
        print(f"❌ Failed to migrate user to SQL!")
        return False
    
    print("\n" + "="*60)
    print("✅ MIGRATION COMPLETE")
    print("="*60)
    
    return True


def test_sql_connection():
    """Testuje połączenie z SQL"""
    print("="*60)
    print("🔌 TESTING SQL CONNECTION")
    print("="*60)
    
    try:
        from database.connection import get_database_info
        info = get_database_info()
        
        print(f"\nDatabase Type: {info['type']}")
        print(f"Database URL: {info['url']}")
        print(f"Driver: {info['driver']}")
        print(f"Dialect: {info['dialect']}")
        print("\n✅ SQL connection OK")
        return True
    except Exception as e:
        print(f"\n❌ SQL connection failed: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate single user from JSON to SQL")
    parser.add_argument("username", nargs="?", default="Max", help="Username to migrate (default: Max)")
    parser.add_argument("--migrate", action="store_true", help="Actually perform migration (default is dry-run)")
    parser.add_argument("--test-connection", action="store_true", help="Just test SQL connection")
    
    args = parser.parse_args()
    
    if args.test_connection:
        test_sql_connection()
        sys.exit(0)
    
    dry_run = not args.migrate
    
    if dry_run:
        print("\n⚠️  RUNNING IN DRY-RUN MODE")
        print("   No changes will be made to SQL database")
        print("   Use --migrate flag to actually migrate\n")
    else:
        print("\n⚠️  LIVE MIGRATION MODE")
        print("   This will write data to SQL database!\n")
        confirm = input(f"Are you sure you want to migrate user '{args.username}'? (yes/no): ")
        if confirm.lower() != "yes":
            print("Migration cancelled.")
            sys.exit(0)
    
    try:
        success = migrate_single_user(args.username, dry_run=dry_run)
        
        if success:
            print(f"\n✅ Migration {'simulated' if dry_run else 'completed'} successfully!")
            sys.exit(0)
        else:
            print(f"\n❌ Migration failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
