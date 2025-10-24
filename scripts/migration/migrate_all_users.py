"""
Batch Migration Script - Wszystkich użytkowników do SQL
Migruje zarówno user data jak i business_games

Fazy:
1. Dry-run - walidacja wszystkich użytkowników
2. Migration - migracja w fazach (5 → 15 → reszta)
3. Verification - porównanie JSON vs SQL
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data.repositories import UserRepository, BusinessGameRepository


class BatchMigration:
    """Batch migration manager"""
    
    def __init__(self):
        self.users_file = Path(__file__).parent.parent.parent / "users_data.json"
        self.user_repo_json = UserRepository(backend="json")
        self.user_repo_sql = UserRepository(backend="sql")
        self.bg_repo_json = BusinessGameRepository(backend="json")
        self.bg_repo_sql = BusinessGameRepository(backend="sql")
        
        self.stats = {
            'total_users': 0,
            'users_with_bg': 0,
            'validation_passed': 0,
            'validation_failed': 0,
            'migration_success': 0,
            'migration_failed': 0,
            'verification_passed': 0,
            'verification_failed': 0,
            'failed_users': []
        }
    
    def load_all_users(self) -> Dict[str, dict]:
        """Ładuje wszystkich użytkowników z JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading users: {e}")
            return {}
    
    def dry_run(self, usernames: List[str] = None) -> bool:
        """
        Dry run - walidacja użytkowników bez zapisu
        
        Args:
            usernames: Lista użytkowników do walidacji (None = wszyscy)
        
        Returns:
            True jeśli wszystko OK
        """
        print("="*80)
        print("🧪 DRY RUN - VALIDATION")
        print("="*80)
        
        users = self.load_all_users()
        
        if usernames is None:
            usernames = list(users.keys())
        
        self.stats['total_users'] = len(usernames)
        
        print(f"\n📋 Validating {len(usernames)} users...\n")
        
        for idx, username in enumerate(usernames, 1):
            print(f"[{idx}/{len(usernames)}] {username:<20}", end=" ")
            
            user_data = users.get(username)
            if not user_data:
                print(f"❌ Not found in JSON")
                self.stats['validation_failed'] += 1
                self.stats['failed_users'].append((username, "not_found"))
                continue
            
            # Validate user data
            if not self.user_repo_json.validate_user_data(user_data):
                print(f"❌ Invalid user data")
                self.stats['validation_failed'] += 1
                self.stats['failed_users'].append((username, "invalid_user_data"))
                continue
            
            # Check business games
            has_bg = 'business_games' in user_data and user_data['business_games']
            
            if has_bg:
                self.stats['users_with_bg'] += 1
                
                # Validate each business game
                bg_valid = True
                for scenario_type, game_data in user_data['business_games'].items():
                    if not self.bg_repo_json._validate_business_game_data(game_data):
                        print(f"❌ Invalid BG: {scenario_type}")
                        self.stats['validation_failed'] += 1
                        self.stats['failed_users'].append((username, f"invalid_bg_{scenario_type}"))
                        bg_valid = False
                        break
                
                if not bg_valid:
                    continue
            
            # All good
            xp = user_data.get('xp', 0)
            coins = user_data.get('degencoins', 0)
            bg_count = len(user_data.get('business_games', {}))
            
            print(f"✅ XP:{xp:>6} Coins:{coins:>8} BG:{bg_count}")
            self.stats['validation_passed'] += 1
        
        # Summary
        print("\n" + "="*80)
        print("📊 DRY RUN SUMMARY")
        print("="*80)
        print(f"Total users:          {self.stats['total_users']}")
        print(f"✅ Validation passed: {self.stats['validation_passed']}")
        print(f"❌ Validation failed: {self.stats['validation_failed']}")
        print(f"Users with BG:        {self.stats['users_with_bg']}")
        
        if self.stats['failed_users']:
            print(f"\n❌ Failed users:")
            for username, reason in self.stats['failed_users']:
                print(f"   - {username}: {reason}")
        
        print("="*80)
        
        return self.stats['validation_failed'] == 0
    
    def migrate_users(self, usernames: List[str], phase_name: str = "Migration") -> bool:
        """
        Migruje użytkowników do SQL
        
        Args:
            usernames: Lista użytkowników do migracji
            phase_name: Nazwa fazy (dla logów)
        
        Returns:
            True jeśli wszystko OK
        """
        print("="*80)
        print(f"🚀 {phase_name.upper()}")
        print("="*80)
        
        users = self.load_all_users()
        
        print(f"\n📋 Migrating {len(usernames)} users...\n")
        
        for idx, username in enumerate(usernames, 1):
            print(f"[{idx}/{len(usernames)}] {username:<20}", end=" ")
            
            user_data = users.get(username)
            if not user_data:
                print(f"❌ Not found")
                self.stats['migration_failed'] += 1
                continue
            
            try:
                # Migrate user data
                success = self.user_repo_sql._save_to_sql(username, user_data)
                
                if not success:
                    print(f"❌ User migration failed")
                    self.stats['migration_failed'] += 1
                    continue
                
                # Migrate business games
                bg_count = 0
                if 'business_games' in user_data and user_data['business_games']:
                    for scenario_type, game_data in user_data['business_games'].items():
                        bg_success = self.bg_repo_sql._save_to_sql(username, scenario_type, game_data)
                        
                        if bg_success:
                            bg_count += 1
                        else:
                            print(f"⚠️  BG {scenario_type} failed")
                
                xp = user_data.get('xp', 0)
                coins = user_data.get('degencoins', 0)
                
                print(f"✅ XP:{xp:>6} Coins:{coins:>8} BG:{bg_count}")
                self.stats['migration_success'] += 1
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.stats['migration_failed'] += 1
                import traceback
                traceback.print_exc()
        
        # Summary
        print("\n" + "="*80)
        print(f"📊 {phase_name.upper()} SUMMARY")
        print("="*80)
        print(f"Total users:          {len(usernames)}")
        print(f"✅ Migration success: {self.stats['migration_success']}")
        print(f"❌ Migration failed:  {self.stats['migration_failed']}")
        print("="*80)
        
        return self.stats['migration_failed'] == 0
    
    def verify_migration(self, usernames: List[str]) -> bool:
        """
        Weryfikuje migrację - porównuje JSON vs SQL
        
        Args:
            usernames: Lista użytkowników do weryfikacji
        
        Returns:
            True jeśli wszystko się zgadza
        """
        print("="*80)
        print("🔍 VERIFICATION - JSON vs SQL")
        print("="*80)
        
        print(f"\n📋 Verifying {len(usernames)} users...\n")
        
        mismatches = []
        
        for idx, username in enumerate(usernames, 1):
            print(f"[{idx}/{len(usernames)}] {username:<20}", end=" ")
            
            # Load from both sources
            json_data = self.user_repo_json.get(username)
            sql_data = self.user_repo_sql.get(username)
            
            if not json_data:
                print(f"❌ Not in JSON")
                self.stats['verification_failed'] += 1
                continue
            
            if not sql_data:
                print(f"❌ Not in SQL")
                self.stats['verification_failed'] += 1
                continue
            
            # Compare key fields
            fields_match = True
            fields_to_check = ['xp', 'degencoins', 'level', 'user_id']
            
            for field in fields_to_check:
                json_val = str(json_data.get(field))
                sql_val = str(sql_data.get(field))
                
                if json_val != sql_val:
                    mismatches.append((username, field, json_val, sql_val))
                    fields_match = False
            
            # Check business games
            json_bg = self.bg_repo_json.get_all_scenarios(username)
            sql_bg = self.bg_repo_sql.get_all_scenarios(username)
            
            bg_match = len(json_bg) == len(sql_bg)
            
            if fields_match and bg_match:
                print(f"✅ Match (BG:{len(sql_bg)})")
                self.stats['verification_passed'] += 1
            else:
                print(f"⚠️  Mismatch")
                self.stats['verification_failed'] += 1
        
        # Summary
        print("\n" + "="*80)
        print("📊 VERIFICATION SUMMARY")
        print("="*80)
        print(f"Total users:            {len(usernames)}")
        print(f"✅ Verification passed: {self.stats['verification_passed']}")
        print(f"❌ Verification failed: {self.stats['verification_failed']}")
        
        if mismatches:
            print(f"\n⚠️  Field mismatches:")
            for username, field, json_val, sql_val in mismatches[:10]:  # Show first 10
                print(f"   - {username}.{field}: JSON={json_val}, SQL={sql_val}")
            
            if len(mismatches) > 10:
                print(f"   ... and {len(mismatches) - 10} more")
        
        print("="*80)
        
        return self.stats['verification_failed'] == 0
    
    def save_report(self, phase_name: str):
        """Zapisuje raport z migracji"""
        report_file = Path(__file__).parent / f"migration_report_{phase_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'phase': phase_name,
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Report saved: {report_file.name}")


def main():
    """Main migration flow"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch migrate users to SQL")
    parser.add_argument("--phase", type=int, choices=[0, 1, 2, 3], default=0,
                       help="Migration phase: 0=dry-run, 1=first 5, 2=next 15, 3=rest")
    parser.add_argument("--users", nargs="+", help="Specific users to migrate")
    parser.add_argument("--verify", action="store_true", help="Verify migration only")
    
    args = parser.parse_args()
    
    migration = BatchMigration()
    
    # Get all users
    all_users = list(migration.load_all_users().keys())
    
    print(f"\n📊 Total users in JSON: {len(all_users)}\n")
    
    # Determine which users to process
    if args.users:
        target_users = args.users
        phase_name = f"custom_{len(target_users)}_users"
    elif args.phase == 0:
        # Dry run - all users
        target_users = all_users
        phase_name = "dry_run"
    elif args.phase == 1:
        # Phase 1: First 5 users
        target_users = all_users[:5]
        phase_name = "phase_1_first_5"
    elif args.phase == 2:
        # Phase 2: Next 15 users (6-20)
        target_users = all_users[5:20]
        phase_name = "phase_2_next_15"
    elif args.phase == 3:
        # Phase 3: Rest (21+)
        target_users = all_users[20:]
        phase_name = "phase_3_rest"
    else:
        target_users = all_users
        phase_name = "all_users"
    
    print(f"🎯 Target: {len(target_users)} users")
    print(f"📋 Phase: {phase_name}\n")
    
    # Verification only
    if args.verify:
        success = migration.verify_migration(target_users)
        migration.save_report(f"{phase_name}_verify")
        sys.exit(0 if success else 1)
    
    # Phase 0: Dry run
    if args.phase == 0:
        success = migration.dry_run(target_users)
        migration.save_report(phase_name)
        
        if success:
            print("\n✅ Dry run passed! Ready for migration.")
            print("\nNext steps:")
            print("  python scripts/migration/migrate_all_users.py --phase 1  # Migrate first 5")
            print("  python scripts/migration/migrate_all_users.py --phase 2  # Migrate next 15")
            print("  python scripts/migration/migrate_all_users.py --phase 3  # Migrate rest")
        else:
            print("\n❌ Dry run failed! Fix issues before migration.")
        
        sys.exit(0 if success else 1)
    
    # Migration phases 1-3
    print(f"\n⚠️  LIVE MIGRATION - Phase {args.phase}")
    print(f"This will migrate {len(target_users)} users to SQL.")
    
    response = input("\nContinue? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("❌ Migration cancelled")
        sys.exit(0)
    
    # Run migration
    success = migration.migrate_users(target_users, phase_name)
    
    if success:
        print("\n✅ Migration successful! Running verification...")
        migration.verify_migration(target_users)
    
    migration.save_report(phase_name)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
