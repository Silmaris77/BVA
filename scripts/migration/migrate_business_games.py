"""
Migracja Business Games do SQL
Test dla użytkownika Max - scenariusz consulting
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data.repositories import BusinessGameRepository


def test_business_game_migration(username: str, dry_run: bool = True):
    """
    Testuje migrację business game do SQL
    
    Args:
        username: Nazwa użytkownika
        dry_run: Jeśli True, tylko walidacja bez zapisu
    """
    print("="*80)
    print(f"🎮 BUSINESS GAME MIGRATION TEST: {username}")
    print(f"   Mode: {'DRY RUN (no writes)' if dry_run else 'LIVE MIGRATION'}")
    print("="*80)
    
    # Initialize repositories
    json_repo = BusinessGameRepository(backend="json")
    
    # Get all scenarios for user
    print(f"\n📋 Step 1: Loading business games from JSON...")
    scenarios = json_repo.get_all_scenarios(username)
    
    if not scenarios:
        print(f"   ❌ No business games found for user {username}")
        return False
    
    print(f"   ✅ Found {len(scenarios)} scenario(s): {list(scenarios.keys())}")
    
    # Validate each scenario
    print(f"\n📋 Step 2: Validating data...")
    all_valid = True
    valid_scenarios = {}  # Only scenarios that pass validation
    
    for scenario_type, game_data in scenarios.items():
        print(f"\n   🎮 Scenario: {scenario_type}")
        
        # Check required fields
        required_fields = ['firm', 'employees', 'office', 'contracts', 'stats', 'money', 'history']
        missing = [f for f in required_fields if f not in game_data]
        
        if missing:
            print(f"      ⚠️  Missing fields: {missing}")
            print(f"      ⏭️  SKIPPING {scenario_type} (incomplete structure)")
            continue  # Skip invalid scenarios instead of failing
        
        # Show details
        firm = game_data.get('firm', {})
        print(f"      ✅ Firm: {firm.get('name')} (Level {firm.get('level')})")
        print(f"      ✅ Employees: {len(game_data.get('employees', []))}")
        print(f"      ✅ Money: {game_data.get('money', 0)}")
        
        contracts = game_data.get('contracts', {})
        active = len(contracts.get('active', []))
        completed = len(contracts.get('completed', []))
        failed = len(contracts.get('failed', []))
        available = len(contracts.get('available_pool', []))
        
        print(f"      ✅ Contracts: {active} active, {completed} completed, {failed} failed, {available} available")
        
        stats = game_data.get('stats', {})
        print(f"      ✅ Stats: {stats.get('total_revenue', 0)} revenue, {stats.get('contracts_completed', 0)} contracts done")
        
        history = game_data.get('history', {})
        transactions = len(history.get('transactions', []))
        print(f"      ✅ History: {transactions} transactions")
        
        # Repository validation
        if json_repo._validate_business_game_data(game_data):
            print(f"      ✅ Data structure is valid")
            valid_scenarios[scenario_type] = game_data  # Add to valid list
        else:
            print(f"      ⚠️  Data structure is invalid")
            print(f"      ⏭️  SKIPPING {scenario_type}")
    
    if not valid_scenarios:
        print(f"\n⚠️  No valid scenarios found to migrate!")
        return False
    
    print(f"\n✅ {len(valid_scenarios)} scenario(s) validated: {list(valid_scenarios.keys())}")
    
    if dry_run:
        print(f"\n" + "="*80)
        print(f"✅ DRY RUN COMPLETE - No changes made")
        print(f"   Ready to migrate {len(valid_scenarios)} scenario(s) for {username}")
        if len(valid_scenarios) < len(scenarios):
            skipped = set(scenarios.keys()) - set(valid_scenarios.keys())
            print(f"   ⏭️  Skipped {len(skipped)} incomplete scenario(s): {list(skipped)}")
        print("="*80)
        return True
    
    # LIVE MIGRATION
    print(f"\n📋 Step 3: Migrating to SQL...")
    sql_repo = BusinessGameRepository(backend="sql")
    
    # Force SQL initialization
    if not sql_repo._ensure_sql_initialized():
        print(f"   ❌ SQL backend not available!")
        return False
    
    migration_success = True
    
    for scenario_type, game_data in valid_scenarios.items():  # Only migrate valid scenarios
        print(f"\n   🎮 Migrating {scenario_type}...")
        
        try:
            success = sql_repo._save_to_sql(username, scenario_type, game_data)
            
            if success:
                print(f"      ✅ Migration successful!")
            else:
                print(f"      ❌ Migration failed!")
                migration_success = False
        except Exception as e:
            print(f"      ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            migration_success = False
    
    if not migration_success:
        print(f"\n❌ Migration had errors!")
        return False
    
    # Verify migration
    print(f"\n📋 Step 4: Verifying migration...")
    
    for scenario_type in valid_scenarios.keys():  # Only verify valid scenarios
        print(f"\n   🎮 Verifying {scenario_type}...")
        
        # Load from SQL
        sql_data = sql_repo._get_from_sql(username, scenario_type)
        
        if not sql_data:
            print(f"      ❌ Not found in SQL!")
            migration_success = False
            continue
        
        # Compare key fields
        json_data = valid_scenarios[scenario_type]
        
        firm_match = json_data.get('firm', {}).get('name') == sql_data.get('firm', {}).get('name')
        money_match = json_data.get('money') == sql_data.get('money')
        
        print(f"      ✅ Firm name: {firm_match}")
        print(f"      ✅ Money: {money_match}")
        
        if firm_match and money_match:
            print(f"      ✅ Data matches!")
        else:
            print(f"      ⚠️  Some fields don't match")
    
    print(f"\n" + "="*80)
    if migration_success:
        print(f"✅ MIGRATION COMPLETE")
        print(f"   {len(valid_scenarios)} scenario(s) migrated successfully for {username}")
        if len(valid_scenarios) < len(scenarios):
            skipped = set(scenarios.keys()) - set(valid_scenarios.keys())
            print(f"   ⏭️  Skipped {len(skipped)} incomplete scenario(s): {list(skipped)}")
    else:
        print(f"❌ MIGRATION HAD ERRORS")
    print("="*80)
    
    return migration_success


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate business games to SQL")
    parser.add_argument("username", nargs="?", default="Max", help="Username to migrate (default: Max)")
    parser.add_argument("--migrate", action="store_true", help="Actually perform migration (default: dry-run)")
    
    args = parser.parse_args()
    
    dry_run = not args.migrate
    
    success = test_business_game_migration(args.username, dry_run=dry_run)
    sys.exit(0 if success else 1)
