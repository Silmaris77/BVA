"""
Test SQL Integration - sprawdza czy dane lekcji działają z SQL
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data.repositories import LessonRepository

print("="*60)
print("🧪 TEST SQL INTEGRATION - LESSONS")
print("="*60)

# Test dla każdego użytkownika
users = ['admin', 'Piotr', 'Pawel']

repo = LessonRepository()

for username in users:
    print(f"\n{'='*60}")
    print(f"👤 USER: {username}")
    print(f"{'='*60}")
    
    # 1. Completed Lessons
    completed = repo.get_completed_lessons(username)
    print(f"\n1️⃣  Completed Lessons: {len(completed)}")
    for lesson in completed:
        print(f"   ✓ {lesson}")
    
    # 2. Lesson Progress
    print(f"\n2️⃣  Lesson Progress:")
    if username == 'admin':
        lessons_to_check = ['0. Wprowadzenie do neuroprzywództwa', '2. Chemia mózgu']
    elif username == 'Piotr':
        lessons_to_check = ['0. Wprowadzenie do neuroprzywództwa']
    else:  # Pawel
        lessons_to_check = ['3. Model SCARF']
    
    for lesson_id in lessons_to_check:
        progress = repo.get_lesson_progress(username, lesson_id)
        if progress:
            sections = [k.replace('_completed', '') for k in progress.keys() if k.endswith('_completed') and progress[k]]
            print(f"   ✓ {lesson_id}: {len(sections)} sections")
            for section in sections[:3]:
                print(f"      - {section}")
    
    # 3. Lesson Access
    access = repo.get_lesson_access(username)
    granted = sum(1 for has_access in access.values() if has_access)
    print(f"\n3️⃣  Lesson Access: {granted}/{len(access)} granted")

print(f"\n{'='*60}")
print(f"✅ TEST COMPLETE")
print(f"{'='*60}")

# Test zapisu
print(f"\n{'='*60}")
print(f"🔬 TEST WRITE OPERATIONS")
print(f"{'='*60}")

test_username = "admin"
test_lesson = "TEST_LESSON_DELETE_ME"

print(f"\n1️⃣  Test: Add completed lesson...")
success = repo.add_completed_lesson(test_username, test_lesson)
print(f"   {'✅' if success else '❌'} Add: {success}")

print(f"\n2️⃣  Test: Verify completed lesson...")
completed = repo.get_completed_lessons(test_username)
found = test_lesson in completed
print(f"   {'✅' if found else '❌'} Found in list: {found}")

print(f"\n3️⃣  Test: Add lesson progress...")
progress_data = {
    "intro_xp_awarded": True,
    "intro_completed": True,
    "intro_xp": 10,
    "intro_degencoins": 0,
    "intro_timestamp": "2025-10-29 01:00:00"
}
success = repo.save_lesson_progress(test_username, test_lesson, "intro", progress_data)
print(f"   {'✅' if success else '❌'} Save: {success}")

print(f"\n4️⃣  Test: Verify lesson progress...")
progress = repo.get_lesson_progress(test_username, test_lesson)
has_intro = progress.get('intro_completed', False)
print(f"   {'✅' if has_intro else '❌'} Has intro_completed: {has_intro}")

print(f"\n5️⃣  Test: Set lesson access...")
success = repo.set_lesson_access(test_username, test_lesson, True)
print(f"   {'✅' if success else '❌'} Set access: {success}")

print(f"\n6️⃣  Test: Verify lesson access...")
access = repo.get_lesson_access(test_username)
has_access = access.get(test_lesson, False)
print(f"   {'✅' if has_access else '❌'} Has access: {has_access}")

print(f"\n{'='*60}")
print(f"✅ ALL TESTS COMPLETE")
print(f"{'='*60}")
print(f"\nℹ️  Note: Test data (TEST_LESSON_DELETE_ME) left in database")
print(f"   You can manually delete it if needed")
