"""
Test Dual-Write Mode
Sprawdza czy zapisy idą jednocześnie do JSON i SQL
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data.repositories import UserRepository, BusinessGameRepository


def test_dual_write_user():
    """Test dual-write dla user data"""
    print("="*80)
    print("🔄 TEST DUAL-WRITE MODE - USER DATA")
    print("="*80)
    
    # Create repository (should auto-detect dual-write mode from config)
    repo = UserRepository()
    
    # Test user
    test_username = "dual_write_test_user"
    
    print(f"\n📋 Step 1: Creating test user '{test_username}'...")
    
    test_user = {
        'user_id': '00000000-0000-0000-0000-000000000001',
        'password': 'hashed_password',
        'xp': 1000,
        'degencoins': 5000,
        'level': 5,
        'joined_date': '2025-10-24',
        'last_login': '2025-10-24 07:52:00',
        'test_taken': True,
        'degen_type': 'Test Degen',
        'completed_lessons': ['lesson1', 'lesson2'],
        'badges': [],
        'badge_data': {},
        'lesson_progress': {},
        'recent_activities': [],
        'inspirations': {'read': [], 'favorites': []},
        'business_games': {}
    }
    
    # Save using repository (should write to both JSON and SQL)
    print(f"   💾 Saving user via Repository...")
    success = repo.save(test_username, test_user)
    
    if not success:
        print(f"   ❌ Save failed!")
        return False
    
    print(f"   ✅ Save successful!")
    
    # Verify in JSON
    print(f"\n📋 Step 2: Verifying in JSON...")
    json_repo = UserRepository(backend="json")
    json_data = json_repo.get(test_username)
    
    if json_data:
        print(f"   ✅ Found in JSON - XP: {json_data.get('xp')}, Coins: {json_data.get('degencoins')}")
    else:
        print(f"   ❌ NOT found in JSON!")
        return False
    
    # Verify in SQL
    print(f"\n📋 Step 3: Verifying in SQL...")
    sql_repo = UserRepository(backend="sql")
    sql_data = sql_repo.get(test_username)
    
    if sql_data:
        print(f"   ✅ Found in SQL - XP: {sql_data.get('xp')}, Coins: {sql_data.get('degencoins')}")
    else:
        print(f"   ❌ NOT found in SQL!")
        return False
    
    # Compare
    print(f"\n📋 Step 4: Comparing JSON vs SQL...")
    
    fields_to_check = ['xp', 'degencoins', 'level', 'user_id']
    all_match = True
    
    for field in fields_to_check:
        json_val = str(json_data.get(field))
        sql_val = str(sql_data.get(field))
        
        match = json_val == sql_val
        symbol = "✅" if match else "❌"
        
        print(f"   {symbol} {field}: JSON={json_val}, SQL={sql_val}")
        
        if not match:
            all_match = False
    
    # Update test
    print(f"\n📋 Step 5: Testing UPDATE (dual-write)...")
    
    test_user['xp'] = 2000
    test_user['degencoins'] = 10000
    
    print(f"   💾 Updating XP to 2000, Coins to 10000...")
    success = repo.save(test_username, test_user)
    
    if not success:
        print(f"   ❌ Update failed!")
        return False
    
    # Verify update in both
    json_data_updated = json_repo.get(test_username)
    sql_data_updated = sql_repo.get(test_username)
    
    json_xp = json_data_updated.get('xp') if json_data_updated else None
    sql_xp = sql_data_updated.get('xp') if sql_data_updated else None
    
    print(f"   JSON XP after update: {json_xp}")
    print(f"   SQL XP after update: {sql_xp}")
    
    if json_xp == 2000 and sql_xp == 2000:
        print(f"   ✅ Both updated correctly!")
    else:
        print(f"   ❌ Update mismatch!")
        all_match = False
    
    # Cleanup
    print(f"\n📋 Step 6: Cleanup (deleting test user)...")
    repo.delete(test_username)
    
    print("\n" + "="*80)
    if all_match:
        print("✅ DUAL-WRITE TEST PASSED - User Data")
    else:
        print("❌ DUAL-WRITE TEST FAILED - User Data")
    print("="*80)
    
    return all_match


def test_dual_write_business_game():
    """Test dual-write dla business games"""
    print("\n" + "="*80)
    print("🔄 TEST DUAL-WRITE MODE - BUSINESS GAMES")
    print("="*80)
    
    bg_repo = BusinessGameRepository()
    
    # Use existing user
    test_username = "Max"
    scenario_type = "consulting"
    
    print(f"\n📋 Step 1: Loading existing business game for '{test_username}'...")
    
    # Get current data
    json_repo = BusinessGameRepository(backend="json")
    current_game = json_repo.get(test_username, scenario_type)
    
    if not current_game:
        print(f"   ❌ No business game found!")
        return False
    
    print(f"   ✅ Found game - Money: {current_game.get('money')}")
    
    # Modify money
    original_money = current_game.get('money', 0)
    new_money = original_money + 500
    
    print(f"\n📋 Step 2: Updating money from {original_money} to {new_money}...")
    
    current_game['money'] = new_money
    
    # Save via repository (should dual-write)
    success = bg_repo.save(test_username, scenario_type, current_game)
    
    if not success:
        print(f"   ❌ Save failed!")
        return False
    
    print(f"   ✅ Save successful!")
    
    # Verify in JSON
    print(f"\n📋 Step 3: Verifying in JSON...")
    json_data = json_repo.get(test_username, scenario_type)
    
    if json_data:
        json_money = json_data.get('money')
        print(f"   ✅ Found in JSON - Money: {json_money}")
    else:
        print(f"   ❌ NOT found in JSON!")
        return False
    
    # Verify in SQL
    print(f"\n📋 Step 4: Verifying in SQL...")
    sql_repo = BusinessGameRepository(backend="sql")
    sql_data = sql_repo.get(test_username, scenario_type)
    
    if sql_data:
        sql_money = sql_data.get('money')
        print(f"   ✅ Found in SQL - Money: {sql_money}")
    else:
        print(f"   ❌ NOT found in SQL!")
        return False
    
    # Compare
    print(f"\n📋 Step 5: Comparing JSON vs SQL...")
    
    match = json_money == sql_money == new_money
    
    if match:
        print(f"   ✅ Both have correct value: {new_money}")
    else:
        print(f"   ❌ Mismatch - JSON: {json_money}, SQL: {sql_money}, Expected: {new_money}")
    
    # Restore original value
    print(f"\n📋 Step 6: Restoring original money value ({original_money})...")
    current_game['money'] = original_money
    bg_repo.save(test_username, scenario_type, current_game)
    
    print("\n" + "="*80)
    if match:
        print("✅ DUAL-WRITE TEST PASSED - Business Games")
    else:
        print("❌ DUAL-WRITE TEST FAILED - Business Games")
    print("="*80)
    
    return match


def main():
    """Run all dual-write tests"""
    print("\n" + "="*80)
    print("🚀 DUAL-WRITE MODE TEST SUITE")
    print("="*80)
    
    # Check config
    config_file = Path(__file__).parent.parent.parent / "config" / "migration_config.json"
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(f"\n📋 Configuration:")
    print(f"   dual_write_enabled: {config.get('dual_write_enabled')}")
    print(f"   enable_dual_write: {config.get('feature_flags', {}).get('enable_dual_write')}")
    print(f"   enable_sql_write: {config.get('feature_flags', {}).get('enable_sql_write')}")
    
    if not config.get('dual_write_enabled'):
        print(f"\n❌ Dual-write is NOT enabled in config!")
        return False
    
    print(f"\n✅ Dual-write is enabled - starting tests...\n")
    
    # Run tests
    test1_passed = test_dual_write_user()
    test2_passed = test_dual_write_business_game()
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"User Data Test:       {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Business Games Test:  {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("="*80)
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL DUAL-WRITE TESTS PASSED!")
        print("\n✅ Dual-write mode is working correctly.")
        print("   - All saves go to both JSON and SQL")
        print("   - Data stays synchronized")
        print("   - Ready for gradual rollout")
        return True
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("   Check the errors above and fix before continuing.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
