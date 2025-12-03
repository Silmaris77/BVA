"""
Permissions Helper - Zarządzanie uprawnieniami użytkowników
Sprawdza dostęp do treści i narzędzi na podstawie company templates
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import streamlit as st


# Cache dla szablonów firm
_company_templates_cache = None


def load_company_templates() -> Dict[str, Any]:
    """Ładuje szablony firm z config/company_templates.json"""
    global _company_templates_cache
    
    if _company_templates_cache is None:
        config_path = Path(__file__).parent.parent / "config" / "company_templates.json"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                _company_templates_cache = json.load(f)
        else:
            # Fallback - domyślne uprawnienia
            _company_templates_cache = {
                "_default": {
                    "content": {
                        "lessons": None,
                        "tests": None,
                        "business_games": {"scenarios": None, "types": None},
                        "inspirations": None
                    },
                    "tools": {
                        "dashboard": True,
                        "profile": True,
                        "learn": True,
                        "inspirations": True,
                        "practice": True,
                        "business_games": True,
                        "shop": True,
                        "admin_panel": False,
                        "personality_tests": True,
                        "rankings": True,
                        "notes": True
                    },
                    "ranking": {
                        "scope": "global",
                        "visible_in_global": True
                    }
                }
            }
    
    return _company_templates_cache


def get_user_permissions(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pobiera uprawnienia użytkownika
    
    Args:
        user_data: Dane użytkownika z session_state lub SQL
    
    Returns:
        Dict z uprawnieniami (content, tools, ranking)
    """
    # Jeśli użytkownik ma custom permissions - użyj ich
    if user_data.get('permissions'):
        return user_data['permissions']
    
    # Jeśli użytkownik ma company - załaduj szablon
    company = user_data.get('company')
    if company:
        templates = load_company_templates()
        if company in templates:
            return templates[company]
    
    # Fallback - domyślne uprawnienia (wszystko dostępne)
    templates = load_company_templates()
    return templates.get('_default', {})


def has_access_to_tool(tool_name: str, user_data: Optional[Dict[str, Any]] = None) -> bool:
    """
    Sprawdza czy użytkownik ma dostęp do narzędzia
    
    Args:
        tool_name: Nazwa narzędzia (dashboard, profile, learn, etc.)
        user_data: Dane użytkownika (jeśli None - pobiera z session_state)
    
    Returns:
        bool: True jeśli użytkownik ma dostęp
    """
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    permissions = get_user_permissions(user_data)
    tools = permissions.get('tools', {})
    
    # Domyślnie wszystko dostępne (jeśli nie określono inaczej)
    return tools.get(tool_name, True)


def has_access_to_lesson(lesson_id: str, user_data: Optional[Dict[str, Any]] = None) -> bool:
    """
    Sprawdza czy użytkownik ma dostęp do lekcji
    
    Args:
        lesson_id: ID lekcji
        user_data: Dane użytkownika
    
    Returns:
        bool: True jeśli ma dostęp
    """
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    permissions = get_user_permissions(user_data)
    allowed_lessons = permissions.get('content', {}).get('lessons')
    
    # Jeśli None - wszystkie dostępne
    if allowed_lessons is None:
        return True
    
    # Sprawdź czy lekcja jest na liście
    return lesson_id in allowed_lessons


def has_access_to_test(test_id: str, user_data: Optional[Dict[str, Any]] = None) -> bool:
    """Sprawdza dostęp do testu"""
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    permissions = get_user_permissions(user_data)
    allowed_tests = permissions.get('content', {}).get('tests')
    
    if allowed_tests is None:
        return True
    
    return test_id in allowed_tests


def has_access_to_business_game_scenario(scenario_id: str, user_data: Optional[Dict[str, Any]] = None) -> bool:
    """Sprawdza dostęp do scenariusza Business Games"""
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    permissions = get_user_permissions(user_data)
    bg = permissions.get('content', {}).get('business_games', {})
    allowed_scenarios = bg.get('scenarios')
    
    if allowed_scenarios is None:
        return True
    
    return scenario_id in allowed_scenarios


def has_access_to_business_game_type(game_type: str, user_data: Optional[Dict[str, Any]] = None) -> bool:
    """Sprawdza dostęp do typu gry Business Games (FMCG, Consulting, etc.)"""
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    permissions = get_user_permissions(user_data)
    bg = permissions.get('content', {}).get('business_games', {})
    allowed_types = bg.get('types')
    
    if allowed_types is None:
        return True
    
    return game_type in allowed_types


def has_access_to_inspiration_category(category: str, user_data: Optional[Dict[str, Any]] = None) -> bool:
    """Sprawdza dostęp do kategorii inspiracji"""
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    permissions = get_user_permissions(user_data)
    allowed_categories = permissions.get('content', {}).get('inspirations')
    
    if allowed_categories is None:
        return True
    
    return category in allowed_categories


def filter_accessible_items(items: List[Any], access_checker, id_field: str = 'id', 
                            user_data: Optional[Dict[str, Any]] = None) -> List[Any]:
    """
    Filtruje listę elementów według uprawnień
    
    Args:
        items: Lista elementów do przefiltrowania
        access_checker: Funkcja sprawdzająca dostęp (np. has_access_to_lesson)
        id_field: Nazwa pola z ID elementu
        user_data: Dane użytkownika
    
    Returns:
        List: Przefiltrowana lista
    """
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    return [
        item for item in items
        if access_checker(item.get(id_field), user_data)
    ]


def get_ranking_scope(user_data: Optional[Dict[str, Any]] = None) -> str:
    """
    Pobiera tryb rankingu dla użytkownika
    
    Args:
        user_data: Dane użytkownika
    
    Returns:
        str: 'none', 'company', lub 'global'
    """
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    permissions = get_user_permissions(user_data)
    return permissions.get('ranking', {}).get('scope', 'global')


def is_visible_in_global_ranking(user_data: Optional[Dict[str, Any]] = None) -> bool:
    """
    Sprawdza czy użytkownik jest widoczny w globalnym rankingu
    
    Args:
        user_data: Dane użytkownika
    
    Returns:
        bool: True jeśli widoczny
    """
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    permissions = get_user_permissions(user_data)
    return permissions.get('ranking', {}).get('visible_in_global', True)


def get_company_display_name(company_code: str) -> str:
    """Pobiera pełną nazwę firmy z kodu"""
    templates = load_company_templates()
    if company_code in templates:
        return templates[company_code].get('display_name', company_code)
    return company_code


def get_available_companies() -> List[Dict[str, str]]:
    """
    Pobiera listę dostępnych firm dla admina
    
    Returns:
        List[Dict]: Lista firm z kodem i nazwą
    """
    templates = load_company_templates()
    companies = []
    
    for code, template in templates.items():
        if code != '_default':  # Pomijamy default
            companies.append({
                'code': code,
                'name': template.get('display_name', code)
            })
    
    return sorted(companies, key=lambda x: x['name'])
