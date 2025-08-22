# BADGE SYSTEM - STEP 3: Data Migration Utilities
# ================================================

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from utils.achievements import load_user_data, save_user_data
from config.settings import BADGES, BADGE_CATEGORIES, BADGE_TIERS

class BadgeDataMigrator:
    """
    Utility class for migrating badge data to the new Step 3 format
    """
    
    def __init__(self):
        self.migration_log = []
        self.backup_created = False
    
    def migrate_all_users(self, create_backup: bool = True) -> Dict[str, Any]:
        """
        Migruj dane odznak dla wszystkich użytkowników
        
        Args:
            create_backup: Czy utworzyć backup przed migracją
        
        Returns:
            Dict z wynikami migracji
        """
        if create_backup:
            self.create_backup()
        
        migration_results = {
            'success': True,
            'migrated_users': [],
            'failed_users': [],
            'total_users': 0,
            'total_badges_migrated': 0,
            'errors': []
        }
        
        try:
            # Załaduj wszystkich użytkowników
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                all_users_data = json.load(f)
            
            migration_results['total_users'] = len(all_users_data)
            
            for username, user_data in all_users_data.items():
                try:
                    user_result = self.migrate_user_data(username, user_data)
                    
                    if user_result['success']:
                        migration_results['migrated_users'].append({
                            'username': username,
                            'badges_migrated': user_result['badges_migrated'],
                            'changes_made': user_result['changes_made']
                        })
                        migration_results['total_badges_migrated'] += user_result['badges_migrated']
                    else:
                        migration_results['failed_users'].append({
                            'username': username,
                            'error': user_result['error']
                        })
                        migration_results['errors'].append(f"User {username}: {user_result['error']}")
                        
                except Exception as e:
                    error_msg = f"Failed to migrate user {username}: {str(e)}"
                    migration_results['failed_users'].append({
                        'username': username,
                        'error': error_msg
                    })
                    migration_results['errors'].append(error_msg)
            
            # Zapisz log migracji
            self.save_migration_log(migration_results)
            
        except Exception as e:
            migration_results['success'] = False
            migration_results['errors'].append(f"Critical error: {str(e)}")
        
        return migration_results
    
    def migrate_user_data(self, username: str, user_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Migruj dane odznak dla pojedynczego użytkownika
        
        Args:
            username: Nazwa użytkownika
            user_data: Opcjonalne dane użytkownika (jeśli już załadowane)
        
        Returns:
            Dict z wynikami migracji użytkownika
        """
        if user_data is None:
            user_data = load_user_data(username)
        
        if not user_data:
            return {'success': False, 'error': 'User data not found'}
        
        migration_result = {
            'success': True,
            'badges_migrated': 0,
            'changes_made': [],
            'error': None
        }
        
        try:
            # Sprawdź czy już ma nowy format
            if 'badge_data' in user_data and isinstance(user_data['badge_data'], dict):
                migration_result['changes_made'].append("Already in new format")
                return migration_result
            
            # Pobierz stare odznaki
            old_badges = user_data.get('badges', [])
            
            # Utwórz nową strukturę
            new_badge_data = {
                'badges': {},
                'badge_progress': {},
                'badge_stats': {
                    'total_earned': 0,
                    'categories_completed': [],
                    'current_streak': 0,
                    'highest_tier_earned': None,
                    'total_badge_xp': 0,
                    'last_badge_earned': None,
                    'earning_rate': 0.0
                }
            }
            
            # Migruj każdą odznakę
            for badge_id in old_badges:
                if badge_id in BADGES:
                    badge_info = BADGES[badge_id]
                    
                    # Oblicz XP z uwzględnieniem tier multiplier
                    base_xp = badge_info.get('xp_reward', 0)
                    tier = badge_info.get('tier', 'bronze')
                    multiplier = BADGE_TIERS.get(tier, {}).get('multiplier', 1.0)
                    xp_earned = int(base_xp * multiplier)
                    
                    new_badge_data['badges'][badge_id] = {
                        'earned': True,
                        'earned_date': user_data.get('joined_date', datetime.now().strftime('%Y-%m-%d')),
                        'xp_earned': xp_earned,
                        'tier': tier,
                        'conditions_met': ['migrated_from_old_format'],
                        'progress_when_earned': 100,
                        'context': {'migration': True, 'original_format': True}
                    }
                    
                    migration_result['badges_migrated'] += 1
                else:
                    migration_result['changes_made'].append(f"Removed invalid badge: {badge_id}")
            
            # Oblicz postęp dla nie-zdobytych odznak
            self._calculate_initial_progress(user_data, new_badge_data)
            
            # Oblicz statystyki
            new_badge_data['badge_stats'] = self._calculate_migrated_stats(new_badge_data, user_data)
            
            # Zapisz nowe dane
            user_data['badge_data'] = new_badge_data
            
            # Zachowaj stary format dla kompatybilności
            user_data['badges'] = list(new_badge_data['badges'].keys())
            
            # Zapisz zmiany
            if save_user_data(username, user_data):
                migration_result['changes_made'].append("Successfully migrated to new format")
                migration_result['changes_made'].append(f"Preserved {len(old_badges)} badges")
            else:
                migration_result['success'] = False
                migration_result['error'] = "Failed to save migrated data"
            
        except Exception as e:
            migration_result['success'] = False
            migration_result['error'] = str(e)
        
        # Dodaj do logu
        self.migration_log.append({
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'result': migration_result
        })
        
        return migration_result
    
    def create_backup(self) -> bool:
        """
        Utwórz backup danych przed migracją
        
        Returns:
            bool: Sukces tworzenia backup
        """
        try:
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
            backup_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                f'users_data_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
            
            with open(file_path, 'r', encoding='utf-8') as source:
                with open(backup_path, 'w', encoding='utf-8') as backup:
                    backup.write(source.read())
            
            self.backup_created = True
            print(f"✅ Backup created: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create backup: {str(e)}")
            return False
    
    def validate_migration(self, username: str) -> Dict[str, Any]:
        """
        Waliduj migrację użytkownika
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            Dict z wynikami walidacji
        """
        user_data = load_user_data(username)
        
        if not user_data:
            return {'valid': False, 'error': 'User not found'}
        
        validation = {
            'valid': True,
            'issues': [],
            'statistics': {},
            'recommendations': []
        }
        
        # Sprawdź obecność nowego formatu
        if 'badge_data' not in user_data:
            validation['valid'] = False
            validation['issues'].append("Missing new badge_data structure")
            validation['recommendations'].append("Run migration for this user")
            return validation
        
        badge_data = user_data['badge_data']
        
        # Sprawdź strukturę
        required_keys = ['badges', 'badge_progress', 'badge_stats']
        for key in required_keys:
            if key not in badge_data:
                validation['valid'] = False
                validation['issues'].append(f"Missing required key: {key}")
        
        # Sprawdź zgodność ze starym formatem
        old_badges = set(user_data.get('badges', []))
        new_badges = set(badge_data.get('badges', {}).keys())
        
        if old_badges != new_badges:
            validation['issues'].append("Mismatch between old and new badge lists")
            validation['recommendations'].append("Synchronize badge lists")
        
        # Sprawdź XP
        total_badge_xp = badge_data.get('badge_stats', {}).get('total_badge_xp', 0)
        if total_badge_xp == 0 and len(new_badges) > 0:
            validation['issues'].append("No badge XP calculated")
            validation['recommendations'].append("Recalculate badge XP")
        
        # Statystyki
        validation['statistics'] = {
            'total_badges': len(new_badges),
            'badges_with_progress': len(badge_data.get('badge_progress', {})),
            'total_badge_xp': total_badge_xp,
            'migration_date': self._extract_migration_date(badge_data)
        }
        
        return validation
    
    def _calculate_initial_progress(self, user_data: Dict[str, Any], badge_data: Dict[str, Any]):
        """Oblicz początkowy postęp dla nie-zdobytych odznak"""
        from utils.achievements import check_badge_condition
        
        for badge_id, badge_info in BADGES.items():
            if badge_id not in badge_data['badges']:
                # Sprawdź czy warunki są spełnione
                try:
                    condition_met = check_badge_condition(badge_id, user_data, {})
                    if condition_met:
                        # Odznaka powinna być zdobyta - dodaj ją
                        base_xp = badge_info.get('xp_reward', 0)
                        tier = badge_info.get('tier', 'bronze')
                        multiplier = BADGE_TIERS.get(tier, {}).get('multiplier', 1.0)
                        xp_earned = int(base_xp * multiplier)
                        
                        badge_data['badges'][badge_id] = {
                            'earned': True,
                            'earned_date': datetime.now().strftime('%Y-%m-%d'),
                            'xp_earned': xp_earned,
                            'tier': tier,
                            'conditions_met': ['auto_detected_during_migration'],
                            'progress_when_earned': 100,
                            'context': {'migration': True, 'auto_detected': True}
                        }
                    else:
                        # Oblicz częściowy postęp
                        progress = self._estimate_badge_progress(badge_id, badge_info, user_data)
                        if progress > 0:
                            badge_data['badge_progress'][badge_id] = {
                                'progress': progress,
                                'conditions_status': {'estimated': True},
                                'last_updated': datetime.now().isoformat(),
                                'migration_estimated': True
                            }
                except:
                    # W przypadku błędu, pomiń tę odznakę
                    continue
    
    def _estimate_badge_progress(self, badge_id: str, badge_info: Dict[str, Any], user_data: Dict[str, Any]) -> float:
        """Oszacuj postęp odznaki podczas migracji"""
        # Podstawowe heurystyki dla oszacowania postępu
        
        if badge_id == 'welcome':
            return 100 if user_data.get('user_id') else 0
        
        elif badge_id == 'first_lesson':
            return 100 if len(user_data.get('completed_lessons', [])) > 0 else 0
        
        elif badge_id == 'first_degen_test':
            return 100 if user_data.get('test_taken', False) else 0
        
        elif 'lesson' in badge_id and 'requirement' in badge_info:
            requirement = badge_info['requirement']
            if isinstance(requirement, int):
                completed = len(user_data.get('completed_lessons', []))
                return min(100, (completed / requirement) * 100)
        
        elif 'xp' in badge_id:
            current_xp = user_data.get('xp', 0)
            if badge_id == 'xp_collector':
                target_xp = 1000
            elif badge_id == 'xp_master':
                target_xp = 5000
            else:
                target_xp = 1000
            return min(100, (current_xp / target_xp) * 100)
        
        elif badge_id == 'login_streak_3':
            return min(100, (user_data.get('login_streak', 0) / 3) * 100)
        
        elif badge_id == 'login_streak_7':
            return min(100, (user_data.get('login_streak', 0) / 7) * 100)
        
        elif badge_id == 'profile_complete':
            fields = ['degen_type', 'avatar', 'theme']
            completed_fields = sum(1 for field in fields if user_data.get(field))
            return (completed_fields / len(fields)) * 100
        
        return 0
    
    def _calculate_migrated_stats(self, badge_data: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Oblicz statystyki podczas migracji"""
        earned_badges = badge_data['badges']
        
        stats = {
            'total_earned': len(earned_badges),
            'categories_completed': [],
            'current_streak': 0,
            'highest_tier_earned': None,
            'total_badge_xp': 0,
            'last_badge_earned': None,
            'earning_rate': 0.0
        }
        
        if not earned_badges:
            return stats
        
        # Oblicz całkowite XP
        stats['total_badge_xp'] = sum(badge.get('xp_earned', 0) for badge in earned_badges.values())
        
        # Znajdź najwyższy tier
        tiers = [badge.get('tier', 'bronze') for badge in earned_badges.values()]
        tier_order = ['bronze', 'silver', 'gold', 'platinum', 'diamond']
        highest_tier_index = max((tier_order.index(tier) for tier in tiers if tier in tier_order), default=0)
        stats['highest_tier_earned'] = tier_order[highest_tier_index]
        
        # Sprawdź ukończone kategorie
        for category_id in BADGE_CATEGORIES.keys():
            category_badges = [badge_id for badge_id, badge_info in BADGES.items() 
                             if badge_info.get('category') == category_id]
            earned_in_category = [badge_id for badge_id in category_badges if badge_id in earned_badges]
            
            if len(earned_in_category) == len(category_badges):
                stats['categories_completed'].append(category_id)
        
        # Oszacuj earning rate
        joined_date = user_data.get('joined_date')
        if joined_date:
            try:
                join_date = datetime.strptime(joined_date, '%Y-%m-%d')
                days_since_join = (datetime.now() - join_date).days
                if days_since_join > 0:
                    stats['earning_rate'] = len(earned_badges) / days_since_join
            except:
                pass
        
        return stats
    
    def _extract_migration_date(self, badge_data: Dict[str, Any]) -> Optional[str]:
        """Wyciągnij datę migracji z danych odznak"""
        for badge_info in badge_data.get('badges', {}).values():
            context = badge_info.get('context', {})
            if context.get('migration'):
                return badge_info.get('earned_date')
        return None
    
    def save_migration_log(self, migration_results: Dict[str, Any]):
        """Zapisz log migracji"""
        log_data = {
            'migration_timestamp': datetime.now().isoformat(),
            'migration_results': migration_results,
            'detailed_log': self.migration_log,
            'backup_created': self.backup_created
        }
        
        try:
            log_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                f'badge_migration_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
            
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            print(f"📝 Migration log saved: {log_path}")
            
        except Exception as e:
            print(f"❌ Failed to save migration log: {str(e)}")

def run_migration(create_backup: bool = True) -> Dict[str, Any]:
    """
    Uruchom migrację danych odznak
    
    Args:
        create_backup: Czy utworzyć backup
    
    Returns:
        Dict z wynikami migracji
    """
    migrator = BadgeDataMigrator()
    
    print("🚀 Starting badge data migration...")
    print("=" * 50)
    
    results = migrator.migrate_all_users(create_backup)
    
    print("\n📊 Migration Summary:")
    print(f"Total users: {results['total_users']}")
    print(f"Successfully migrated: {len(results['migrated_users'])}")
    print(f"Failed migrations: {len(results['failed_users'])}")
    print(f"Total badges migrated: {results['total_badges_migrated']}")
    
    if results['errors']:
        print(f"\n❌ Errors ({len(results['errors'])}):")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")
        if len(results['errors']) > 5:
            print(f"  ... and {len(results['errors']) - 5} more")
    
    print(f"\n✅ Migration {'completed successfully' if results['success'] else 'completed with errors'}")
    
    return results

if __name__ == "__main__":
    # Uruchom migrację jeśli skrypt jest wywołany bezpośrednio
    run_migration()
