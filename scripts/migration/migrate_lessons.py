"""
Migrate Lessons Data - JSON → SQL
Migruje completed_lessons, lesson_progress, lesson_access
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for emoji
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from data.repositories.lesson_repository import LessonRepository


def migrate_user_lessons(username: str, dry_run: bool = True):
    """
    Migruje dane lekcji użytkownika z JSON do SQL
    
    Args:
        username: Nazwa użytkownika
        dry_run: Jeśli True, tylko walidacja (bez zapisu do SQL)
    
    Returns:
        bool: True jeśli sukces
    """
    
    print("="*80)
    print(f"📚 LESSON MIGRATION: {username}")
    print(f"   Mode: {'DRY RUN (no writes)' if dry_run else 'LIVE MIGRATION'}")
    print("="*80)
    
    # 1. Load JSON data
    print("\n📋 Step 1: Loading lessons from JSON...")
    
    users_file = project_root / "users_data.json"
    try:
        with open(users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    except Exception as e:
        print(f"   ❌ Error loading JSON: {e}")
        return False
    
    if username not in users_data:
        print(f"   ❌ User {username} not found in JSON")
        return False
    
    user_data = users_data[username]
    
    # 2. Extract lesson data
    completed_lessons = user_data.get('completed_lessons', [])
    lesson_progress = user_data.get('lesson_progress', {})
    lesson_access = user_data.get('lesson_access', {})
    
    print(f"   ✅ Completed lessons: {len(completed_lessons)}")
    print(f"   ✅ Lesson progress: {len(lesson_progress)} lessons")
    print(f"   ✅ Lesson access: {len(lesson_access)} lessons")
    
    if not completed_lessons and not lesson_progress and not lesson_access:
        print(f"\n   ℹ️  No lesson data to migrate for {username}")
        return True
    
    # 3. Validate data
    print("\n📋 Step 2: Validating data...")
    
    # Pokaż co zostanie zmigrowane
    if completed_lessons:
        print(f"\n   📗 Completed lessons ({len(completed_lessons)}):")
        for lesson in completed_lessons[:5]:  # Pierwsze 5
            print(f"      ✓ {lesson}")
        if len(completed_lessons) > 5:
            print(f"      ... and {len(completed_lessons) - 5} more")
    
    if lesson_progress:
        print(f"\n   📊 Lesson progress ({len(lesson_progress)} lessons):")
        for lesson_id, progress in list(lesson_progress.items())[:3]:  # Pierwsze 3
            sections = [k.replace('_completed', '') for k in progress.keys() if k.endswith('_completed') and progress[k]]
            print(f"      ✓ {lesson_id}: {len(sections)} sections completed")
        if len(lesson_progress) > 3:
            print(f"      ... and {len(lesson_progress) - 3} more")
    
    if lesson_access:
        granted_count = sum(1 for has_access in lesson_access.values() if has_access)
        print(f"\n   🔑 Lesson access: {granted_count}/{len(lesson_access)} granted")
    
    # 4. Migrate to SQL (if not dry-run)
    if not dry_run:
        print("\n📋 Step 3: Migrating to SQL...")
        
        repo = LessonRepository(backend="sql")
        repo._ensure_sql_initialized()  # Force SQL initialization
        
        if not repo.sql_available:
            print("   ❌ SQL not available!")
            return False
        
        try:
            # Migrate completed lessons
            if completed_lessons:
                print(f"\n   📗 Migrating {len(completed_lessons)} completed lessons...")
                for lesson_id in completed_lessons:
                    if not repo.add_completed_lesson(username, lesson_id):
                        print(f"      ⚠️  Failed to migrate completed lesson: {lesson_id}")
            
            # Migrate lesson progress
            if lesson_progress:
                print(f"\n   📊 Migrating lesson progress for {len(lesson_progress)} lessons...")
                for lesson_id, progress in lesson_progress.items():
                    # Znajdź wszystkie sekcje (intro, content, etc.)
                    sections = set()
                    for key in progress.keys():
                        if key.endswith('_completed') or key.endswith('_xp_awarded'):
                            section_name = key.replace('_completed', '').replace('_xp_awarded', '')
                            sections.add(section_name)
                    
                    for section_name in sections:
                        section_data = {
                            f"{section_name}_xp_awarded": progress.get(f"{section_name}_xp_awarded", False),
                            f"{section_name}_completed": progress.get(f"{section_name}_completed", False),
                            f"{section_name}_xp": progress.get(f"{section_name}_xp", 0),
                            f"{section_name}_degencoins": progress.get(f"{section_name}_degencoins", 0),
                            f"{section_name}_timestamp": progress.get(f"{section_name}_timestamp"),
                        }
                        
                        if not repo.save_lesson_progress(username, lesson_id, section_name, section_data):
                            print(f"      ⚠️  Failed to migrate progress: {lesson_id}/{section_name}")
            
            # Migrate lesson access
            if lesson_access:
                print(f"\n   🔑 Migrating lesson access for {len(lesson_access)} lessons...")
                for lesson_id, has_access in lesson_access.items():
                    if not repo.set_lesson_access(username, lesson_id, has_access):
                        print(f"      ⚠️  Failed to migrate access: {lesson_id}")
            
            print(f"\n   ✅ Migration successful!")
            
        except Exception as e:
            print(f"\n   ❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # 5. Verify migration
        print("\n📋 Step 4: Verifying migration...")
        
        try:
            # Verify completed lessons
            sql_completed = repo.get_completed_lessons(username)
            print(f"\n   📗 Completed lessons: {len(completed_lessons)} JSON → {len(sql_completed)} SQL")
            if set(completed_lessons) != set(sql_completed):
                print(f"      ⚠️  Mismatch!")
                print(f"      Missing in SQL: {set(completed_lessons) - set(sql_completed)}")
                print(f"      Extra in SQL: {set(sql_completed) - set(completed_lessons)}")
            else:
                print(f"      ✅ Match!")
            
            # Verify lesson progress (sample check)
            for lesson_id in list(lesson_progress.keys())[:2]:
                sql_progress = repo.get_lesson_progress(username, lesson_id)
                json_progress = lesson_progress[lesson_id]
                
                # Sprawdź kilka kluczy
                for key in ['intro_completed', 'content_completed']:
                    json_val = json_progress.get(key)
                    sql_val = sql_progress.get(key)
                    if json_val != sql_val:
                        print(f"      ⚠️  Progress mismatch for {lesson_id}.{key}: {json_val} vs {sql_val}")
            
            print(f"\n   ✅ Verification complete")
            
        except Exception as e:
            print(f"\n   ⚠️  Verification error: {e}")
    
    print("\n" + "="*80)
    if dry_run:
        print("✅ DRY RUN COMPLETE - No changes made")
        print(f"   Ready to migrate lesson data for {username}")
    else:
        print("✅ MIGRATION COMPLETE")
        print(f"   Lesson data migrated successfully for {username}")
    print("="*80)
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate lesson data from JSON to SQL')
    parser.add_argument('username', help='Username to migrate')
    parser.add_argument('--migrate', action='store_true', help='Actually perform migration (default is dry-run)')
    
    args = parser.parse_args()
    
    dry_run = not args.migrate
    
    success = migrate_user_lessons(args.username, dry_run=dry_run)
    
    sys.exit(0 if success else 1)
