"""
Resource Access Helper - System tagowania i dostępu do zasobów
Zarządza dostępem na podstawie tagów company zamiast sztywnych list
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import streamlit as st


# Cache dla tagów zasobów
_resource_tags_cache = None


def clear_resource_tags_cache():
    """
    Czyści cache tagów zasobów.
    Przydatne po manualnej edycji resource_tags.json.
    """
    global _resource_tags_cache
    _resource_tags_cache = None


def load_resource_tags(force_reload: bool = False) -> Dict[str, Any]:
    """
    Ładuje tagi zasobów z config/resource_tags.json
    
    Args:
        force_reload: Jeśli True, wymusza ponowne załadowanie z pliku (ignoruje cache)
    """
    global _resource_tags_cache
    
    # W trybie development ZAWSZE ładuj na świeżo (komentarz poniżej dla produkcji)
    force_reload = True  # DEV MODE - wyłączyć w produkcji dla performance
    
    if _resource_tags_cache is None or force_reload:
        config_path = Path(__file__).parent.parent / "config" / "resource_tags.json"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                _resource_tags_cache = json.load(f)
        else:
            # Fallback - domyślnie wszystko jako General
            _resource_tags_cache = {
                "companies": [
                    {"code": "General", "display_name": "Ogólne", "color": "#6c757d"}
                ],
                "lessons": {},
                "business_games_scenarios": {},
                "business_games_types": {},
                "inspirations_categories": {}
            }
    
    return _resource_tags_cache


def save_resource_tags(tags_data: Dict[str, Any]) -> bool:
    """Zapisuje zmodyfikowane tagi zasobów"""
    global _resource_tags_cache
    
    try:
        config_path = Path(__file__).parent.parent / "config" / "resource_tags.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(tags_data, f, indent=2, ensure_ascii=False)
        _resource_tags_cache = tags_data
        return True
    except Exception as e:
        print(f"Error saving resource tags: {e}")
        return False


def get_resource_tags(resource_type: str, resource_id: str) -> List[str]:
    """
    Pobiera tagi dla danego zasobu
    
    Args:
        resource_type: 'lessons', 'business_games_scenarios', 'business_games_types', 'inspirations_categories'
        resource_id: ID zasobu
    
    Returns:
        Lista tagów company (np. ['General', 'Warta'])
    """
    tags = load_resource_tags()
    resource_dict = tags.get(resource_type, {})
    return resource_dict.get(resource_id, ["General"])


def set_resource_tags(resource_type: str, resource_id: str, company_tags: List[str]) -> bool:
    """
    Ustawia tagi dla zasobu
    
    Args:
        resource_type: Typ zasobu
        resource_id: ID zasobu
        company_tags: Lista tagów do przypisania
    
    Returns:
        bool: True jeśli zapisano pomyślnie
    """
    tags = load_resource_tags()
    
    if resource_type not in tags:
        tags[resource_type] = {}
    
    tags[resource_type][resource_id] = company_tags
    return save_resource_tags(tags)


def has_access_to_resource(resource_type: str, resource_id: str, user_data: Optional[Dict[str, Any]] = None) -> bool:
    """
    Sprawdza czy użytkownik ma dostęp do zasobu na podstawie tagów
    
    Args:
        resource_type: Typ zasobu
        resource_id: ID zasobu
        user_data: Dane użytkownika
    
    Returns:
        bool: True jeśli ma dostęp
    """
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    # Pobierz company użytkownika (TYLKO NOWY SYSTEM TAGÓW)
    user_company = user_data.get('company', 'General')
    
    # Pobierz tagi zasobu
    resource_tags = get_resource_tags(resource_type, resource_id)
    
    # Sprawdź czy grupa użytkownika wyklucza zasoby "General"
    company_info = get_company_info(user_company)
    exclude_general = company_info.get('exclude_general', False) if company_info else False
    
    # Jeśli grupa wyklucza General:
    # 1. Zasób NIE MOŻE mieć tagu "General"
    # 2. Zasób MUSI mieć tag użytkownika
    if exclude_general:
        if "General" in resource_tags:
            return False  # Zawiera General - BRAK DOSTĘPU
        return user_company in resource_tags
    
    # Standardowo: zasób ma tag "General" lub tag użytkownika - dostęp
    return "General" in resource_tags or user_company in resource_tags


def get_accessible_resources(resource_type: str, user_data: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Zwraca listę ID zasobów dostępnych dla użytkownika
    
    Args:
        resource_type: Typ zasobu
        user_data: Dane użytkownika
    
    Returns:
        Lista ID zasobów
    """
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    tags = load_resource_tags()
    resource_dict = tags.get(resource_type, {})
    
    accessible = []
    for resource_id, resource_tags in resource_dict.items():
        if has_access_to_resource(resource_type, resource_id, user_data):
            accessible.append(resource_id)
    
    return accessible


def get_all_companies() -> List[Dict[str, str]]:
    """
    Pobiera listę wszystkich firm/grup
    
    Returns:
        Lista dict z code, display_name, description, color
    """
    tags = load_resource_tags()
    return tags.get('companies', [])


def get_company_info(company_code: str) -> Optional[Dict[str, str]]:
    """Pobiera informacje o firmie/grupie"""
    companies = get_all_companies()
    for company in companies:
        if company['code'] == company_code:
            return company
    return None


def filter_resources_by_tags(resources: List[Any], resource_type: str, 
                             id_field: str = 'id', 
                             user_data: Optional[Dict[str, Any]] = None) -> List[Any]:
    """
    Filtruje listę zasobów według dostępu użytkownika
    
    Args:
        resources: Lista zasobów (dict/objects)
        resource_type: Typ zasobu
        id_field: Nazwa pola z ID
        user_data: Dane użytkownika
    
    Returns:
        Przefiltrowana lista
    """
    if user_data is None:
        user_data = st.session_state.get('user_data', {})
    
    return [
        resource for resource in resources
        if has_access_to_resource(
            resource_type, 
            resource.get(id_field) if isinstance(resource, dict) else getattr(resource, id_field),
            user_data
        )
    ]


def get_resources_by_company(resource_type: str, company_code: str) -> List[str]:
    """
    Zwraca listę ID zasobów przypisanych do danej firmy
    
    Args:
        resource_type: Typ zasobu
        company_code: Kod firmy
    
    Returns:
        Lista ID zasobów
    """
    tags = load_resource_tags()
    resource_dict = tags.get(resource_type, {})
    
    resources = []
    for resource_id, resource_tags in resource_dict.items():
        if company_code in resource_tags:
            resources.append(resource_id)
    
    return resources
