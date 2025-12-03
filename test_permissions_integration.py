"""
Test integracji systemu uprawnień opartego na firmach
Sprawdza czy filtrowanie działa poprawnie we wszystkich views
"""

import sys
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from database.connection import session_scope
from data.repositories.user_repository import UserRepository
from database.models import User
from utils.permissions import (
    has_access_to_lesson,
    has_access_to_business_game_scenario,
    has_access_to_business_game_type,
    has_access_to_inspiration_category,
    has_access_to_tool,
    get_ranking_scope,
    is_visible_in_global_ranking,
    load_company_templates
)

def test_permissions_integration():
    """Test kompletnej integracji systemu uprawnień"""
    
    print("=" * 60)
    print("TEST INTEGRACJI SYSTEMU UPRAWNIEŃ")
    print("=" * 60)
    
    # Wczytaj szablony
    templates = load_company_templates()
    print(f"\n✓ Załadowano {len(templates)} szablonów firm")
    
    # Test dla każdej firmy
    test_companies = ['Warta', 'Heinz', 'Milwaukee']
    
    for company in test_companies:
        print(f"\n{'=' * 60}")
        print(f"FIRMA: {company}")
        print(f"{'=' * 60}")
        
        # Utwórz testowego użytkownika
        test_username = f"test_{company.lower()}_integration"
        
        try:
            with session_scope() as session:
                user_repo = UserRepository(session)
                
                # Usuń jeśli istnieje
                from database.models import User as UserModel
                existing = session.query(UserModel).filter_by(username=test_username).first()
                if existing:
                    session.delete(existing)
                    session.commit()
                
                # Utwórz nowego użytkownika
                template = templates.get(company, {})
                from database.models import User as UserModel
                user = UserModel(
                    username=test_username,
                    password_hash="test_hash",
                    company=company,
                    permissions=template,
                    account_created_by="test_script"
                )
                session.add(user)
                session.commit()
                
                print(f"✓ Utworzono użytkownika: {test_username}")
                
                # Pobierz dane użytkownika
                from database.models import User as UserModel
                user = session.query(UserModel).filter_by(username=test_username).first()
                user_data = user.to_dict()
                
                # TEST 1: Lekcje
                print(f"\n📚 TEST: Dostęp do lekcji")
                lesson_ids = template.get('content', {}).get('lessons', [])
                print(f"   Uprawnienia: {len(lesson_ids)} lekcji")
                
                # Test pierwszej lekcji (jeśli jest)
                if lesson_ids:
                    test_lesson = lesson_ids[0]
                    has_access = has_access_to_lesson(test_lesson, user_data)
                    print(f"   ✓ Dostęp do '{test_lesson}': {has_access}")
                    
                    # Test lekcji spoza uprawnień
                    fake_lesson = "nonexistent_lesson_xyz"
                    no_access = not has_access_to_lesson(fake_lesson, user_data)
                    print(f"   ✓ Brak dostępu do '{fake_lesson}': {no_access}")
                
                # TEST 2: Business Games - scenariusze
                print(f"\n🎮 TEST: Business Games - scenariusze")
                bg_scenarios = template.get('content', {}).get('business_games', {}).get('scenarios', [])
                print(f"   Uprawnienia: {len(bg_scenarios)} scenariuszy")
                
                if bg_scenarios:
                    test_scenario = bg_scenarios[0]
                    has_access = has_access_to_business_game_scenario(test_scenario, user_data)
                    print(f"   ✓ Dostęp do scenariusza '{test_scenario}': {has_access}")
                
                # TEST 3: Business Games - typy
                print(f"\n🎮 TEST: Business Games - typy kontraktów")
                bg_types = template.get('content', {}).get('business_games', {}).get('types', [])
                print(f"   Uprawnienia: {len(bg_types)} typów")
                
                for bg_type in bg_types:
                    has_access = has_access_to_business_game_type(bg_type, user_data)
                    print(f"   ✓ Dostęp do typu '{bg_type}': {has_access}")
                
                # TEST 4: Inspiracje
                print(f"\n💡 TEST: Inspiracje - kategorie")
                insp_categories = template.get('content', {}).get('inspirations', [])
                print(f"   Uprawnienia: {len(insp_categories)} kategorii")
                
                if insp_categories:
                    test_category = insp_categories[0]
                    has_access = has_access_to_inspiration_category(test_category, user_data)
                    print(f"   ✓ Dostęp do kategorii '{test_category}': {has_access}")
                
                # TEST 5: Narzędzia
                print(f"\n🛠️ TEST: Narzędzia")
                tools = template.get('tools', {})
                for tool_name, accessible in tools.items():
                    has_access = has_access_to_tool(tool_name, user_data)
                    status = "✓" if has_access == accessible else "✗"
                    print(f"   {status} '{tool_name}': {has_access} (oczekiwano: {accessible})")
                
                # TEST 6: Rankingi
                print(f"\n🏆 TEST: Rankingi")
                ranking_scope = get_ranking_scope(user_data)
                expected_scope = template.get('ranking', {}).get('scope', 'none')
                scope_match = ranking_scope == expected_scope
                status = "✓" if scope_match else "✗"
                print(f"   {status} Scope: {ranking_scope} (oczekiwano: {expected_scope})")
                
                visible_global = is_visible_in_global_ranking(user_data)
                expected_visible = template.get('ranking', {}).get('visible_in_global', False)
                visible_match = visible_global == expected_visible
                status = "✓" if visible_match else "✗"
                print(f"   {status} Widoczny w globalnym: {visible_global} (oczekiwano: {expected_visible})")
                
                # CLEANUP
                session.delete(user)
                session.commit()
                print(f"\n✓ Usunięto użytkownika testowego: {test_username}")
                
        except Exception as e:
            print(f"\n✗ BŁĄD dla {company}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 60}")
    print("TEST ZAKOŃCZONY")
    print(f"{'=' * 60}\n")

if __name__ == "__main__":
    test_permissions_integration()
