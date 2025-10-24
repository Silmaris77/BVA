"""
Test Repository System - Prosty test warstwy abstrakcji
"""

import sys
from pathlib import Path

# Dodaj główny katalog do PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data.repositories import UserRepository


def test_user_repository():
    """Test podstawowych operacji UserRepository"""
    
    print("="*60)
    print("🧪 TESTING USER REPOSITORY")
    print("="*60)
    
    # Inicjalizacja repository
    repo = UserRepository()
    
    print(f"\n1. Backend: {repo.backend}")
    print(f"2. JSON file: {repo.json_file_path}")
    print(f"3. SQL available: {repo.sql_available}")
    
    # Test get
    print("\n--- Testing GET ---")
    test_username = "Max"
    user_data = repo.get(test_username)
    
    if user_data:
        print(f"✅ User '{test_username}' found!")
        print(f"   - XP: {user_data.get('xp', 0)}")
        print(f"   - DegenCoins: {user_data.get('degencoins', 0)}")
        print(f"   - Level: {user_data.get('level', 1)}")
        
        # Sprawdź business_games
        if "business_games" in user_data:
            print(f"   - Business Games: {list(user_data['business_games'].keys())}")
        elif "business_game" in user_data:
            print(f"   - Business Game (old format): Found")
    else:
        print(f"❌ User '{test_username}' not found")
    
    # Test get_all
    print("\n--- Testing GET_ALL ---")
    all_users = repo.get_all()
    print(f"✅ Total users: {len(all_users)}")
    print(f"   Usernames: {list(all_users.keys())[:5]}...")  # First 5
    
    # Test exists
    print("\n--- Testing EXISTS ---")
    exists = repo.exists(test_username)
    print(f"✅ User '{test_username}' exists: {exists}")
    
    # Test count
    print("\n--- Testing COUNT ---")
    count = repo.count()
    print(f"✅ Total users count: {count}")
    
    # Test validation
    print("\n--- Testing VALIDATION ---")
    if user_data:
        is_valid, error = repo.validate_user_data(user_data)
        print(f"✅ User data valid: {is_valid}")
        if not is_valid:
            print(f"   Error: {error}")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    try:
        test_user_repository()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
