"""
Test dostępu mil2 do lekcji - diagnoza systemu tagów
"""

from database.models import User
from database.connection import session_scope
from utils.resource_access import get_resource_tags, has_access_to_resource, get_company_info
from data.lessons import load_lessons

# Załaduj lekcje
lessons = load_lessons()

# Pobierz użytkownika mil2
with session_scope() as session:
    user = session.query(User).filter_by(username='mil2').first()
    user_data = user.to_dict()

print("=== UŻYTKOWNIK MIL2 ===")
print(f"Company: {user_data.get('company')}")
print(f"Permissions: {user_data.get('permissions')}")

# Sprawdź info o firmie Milwaukee
company_info = get_company_info('Milwaukee')
print(f"\n=== FIRMA MILWAUKEE ===")
print(f"Info: {company_info}")
print(f"Exclude General: {company_info.get('exclude_general') if company_info else 'N/A'}")

print("\n=== ANALIZA DOSTĘPU DO LEKCJI ===")
accessible_count = 0
inaccessible_count = 0

for lesson_id, lesson in lessons.items():
    tags = get_resource_tags('lessons', lesson_id)
    has_access = has_access_to_resource('lessons', lesson_id, user_data)
    
    if has_access:
        accessible_count += 1
        print(f"OK  {lesson_id:50s} | Tagi: {tags}")
    else:
        inaccessible_count += 1
        print(f"NO  {lesson_id:50s} | Tagi: {tags}")

print(f"\n=== PODSUMOWANIE ===")
print(f"Dostępne: {accessible_count}")
print(f"Niedostępne: {inaccessible_count}")
print(f"Razem: {len(lessons)}")

print("\n=== OCZEKIWANY WYNIK ===")
print("Mil2 powinien widzieć TYLKO lekcje z tagiem 'Milwaukee'")
print("Lekcje z tagiem 'General' powinny być NIEDOSTĘPNE (exclude_general=true)")
