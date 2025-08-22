"""
Moduł do zarządzania strukturą kursu BrainVenture Academy.
Zawiera funkcje do ładowania danych o blokach, kategoriach i lekcjach z pliku JSON.
"""

import json
import os
from typing import Dict, List, Any, Optional

def load_course_structure() -> Dict[str, Any]:
    """
    Ładuje strukturę kursu z pliku JSON.
    
    Returns:
        Dict zawierający bloki, kategorie i lekcje
    """
    # Ścieżka do pliku z strukturą kursu
    current_dir = os.path.dirname(__file__)
    course_file_path = os.path.join(current_dir, "course_structure.json")
    
    try:
        with open(course_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {course_file_path}")
        return {"blocks": {}, "categories": {}, "lessons": {}}
    except json.JSONDecodeError:
        print(f"Błąd: Nieprawidłowa struktura JSON w pliku {course_file_path}")
        return {"blocks": {}, "categories": {}, "lessons": {}}

def get_blocks() -> Dict[int, Dict[str, Any]]:
    """
    Pobiera informacje o blokach tematycznych kursu.
    
    Returns:
        Dict z blokami kursu
    """
    course_data = load_course_structure()
    blocks = course_data.get("blocks", {})
    
    # Konwertuj klucze na int
    return {int(k): v for k, v in blocks.items()}

def get_categories() -> Dict[int, Dict[str, Any]]:
    """
    Pobiera informacje o kategoriach umiejętności.
    
    Returns:
        Dict z kategoriami kursu
    """
    course_data = load_course_structure()
    categories = course_data.get("categories", {})
    
    # Konwertuj klucze na int
    return {int(k): v for k, v in categories.items()}

def get_lessons_for_category(category_id: int) -> List[Dict[str, str]]:
    """
    Pobiera listę lekcji dla danej kategorii.
    
    Args:
        category_id: ID kategorii
        
    Returns:
        Lista lekcji z ID i tytułami
    """
    course_data = load_course_structure()
    lessons = course_data.get("lessons", {})
    
    return lessons.get(str(category_id), [])

def get_category_info(category_id: int) -> Optional[Dict[str, Any]]:
    """
    Pobiera szczegółowe informacje o kategorii.
    
    Args:
        category_id: ID kategorii
        
    Returns:
        Dict z informacjami o kategorii lub None jeśli nie znaleziono
    """
    categories = get_categories()
    return categories.get(category_id)

def get_block_info(block_id: int) -> Optional[Dict[str, Any]]:
    """
    Pobiera szczegółowe informacje o bloku.
    
    Args:
        block_id: ID bloku
        
    Returns:
        Dict z informacjami o bloku lub None jeśli nie znaleziono
    """
    blocks = get_blocks()
    return blocks.get(block_id)

def get_all_lesson_ids() -> List[str]:
    """
    Pobiera listę wszystkich ID lekcji w kursie.
    
    Returns:
        Lista ID wszystkich lekcji
    """
    course_data = load_course_structure()
    lessons = course_data.get("lessons", {})
    
    all_lesson_ids = []
    for category_lessons in lessons.values():
        for lesson in category_lessons:
            all_lesson_ids.append(lesson["id"])
    
    return all_lesson_ids

def get_lessons_by_block(block_id: int) -> Dict[int, List[Dict[str, str]]]:
    """
    Pobiera wszystkie lekcje należące do danego bloku.
    
    Args:
        block_id: ID bloku
        
    Returns:
        Dict z kategoriami i ich lekcjami z danego bloku
    """
    block_info = get_block_info(block_id)
    if not block_info:
        return {}
    
    block_categories = block_info.get("categories", [])
    result = {}
    
    for category_id in block_categories:
        lessons = get_lessons_for_category(category_id)
        if lessons:
            result[category_id] = lessons
    
    return result

def search_lessons(query: str) -> List[Dict[str, Any]]:
    """
    Wyszukuje lekcje po tytule.
    
    Args:
        query: Tekst do wyszukania
        
    Returns:
        Lista lekcji pasujących do zapytania wraz z informacją o kategorii
    """
    course_data = load_course_structure()
    lessons = course_data.get("lessons", {})
    categories = get_categories()
    
    results = []
    query_lower = query.lower()
    
    for category_id_str, category_lessons in lessons.items():
        category_id = int(category_id_str)
        category_info = categories.get(category_id, {})
        
        for lesson in category_lessons:
            if query_lower in lesson["title"].lower():
                results.append({
                    "lesson": lesson,
                    "category_id": category_id,
                    "category_name": category_info.get("name", "Nieznana kategoria")
                })
    
    return results

def get_course_statistics() -> Dict[str, int]:
    """
    Zwraca podstawowe statystyki kursu.
    
    Returns:
        Dict ze statystykami kursu
    """
    course_data = load_course_structure()
    
    blocks_count = len(course_data.get("blocks", {}))
    categories_count = len(course_data.get("categories", {}))
    
    total_lessons = 0
    lessons = course_data.get("lessons", {})
    for category_lessons in lessons.values():
        total_lessons += len(category_lessons)
    
    return {
        "blocks": blocks_count,
        "categories": categories_count,
        "lessons": total_lessons
    }

# Funkcje pomocnicze dla zachowania kompatybilności z istniejącym kodem
def get_lessons_data() -> Dict[int, List[Dict[str, str]]]:
    """
    Pobiera wszystkie lekcje w formacie kompatybilnym z starym kodem.
    
    Returns:
        Dict z lekcjami indeksowanymi przez ID kategorii
    """
    course_data = load_course_structure()
    lessons = course_data.get("lessons", {})
    
    # Konwertuj klucze na int
    return {int(k): v for k, v in lessons.items()}

def validate_course_structure() -> bool:
    """
    Sprawdza poprawność struktury kursu.
    
    Returns:
        True jeśli struktura jest prawidłowa, False w przeciwnym razie
    """
    try:
        course_data = load_course_structure()
        
        # Sprawdź czy istnieją wymagane sekcje
        required_sections = ["blocks", "categories", "lessons"]
        for section in required_sections:
            if section not in course_data:
                print(f"Błąd: Brakuje sekcji '{section}' w strukturze kursu")
                return False
        
        # Sprawdź czy kategorie mają przypisane bloki
        blocks = course_data["blocks"]
        categories = course_data["categories"]
        
        for category_id, category_info in categories.items():
            block_id = category_info.get("block")
            if str(block_id) not in blocks:
                print(f"Błąd: Kategoria {category_id} odwołuje się do nieistniejącego bloku {block_id}")
                return False
        
        # Sprawdź czy bloki mają prawidłowe kategorie
        for block_id, block_info in blocks.items():
            for category_id in block_info.get("categories", []):
                if str(category_id) not in categories:
                    print(f"Błąd: Blok {block_id} odwołuje się do nieistniejącej kategorii {category_id}")
                    return False
        
        print("Struktura kursu jest prawidłowa")
        return True
        
    except Exception as e:
        print(f"Błąd podczas walidacji struktury kursu: {e}")
        return False

if __name__ == "__main__":
    # Test funkcji
    print("=== Test modułu course_data ===")
    
    # Załaduj i wyświetl statystyki
    stats = get_course_statistics()
    print(f"Statystyki kursu: {stats}")
    
    # Sprawdź strukturę
    validate_course_structure()
    
    # Test wyszukiwania
    search_results = search_lessons("dopamina")
    print(f"Wyniki wyszukiwania 'dopamina': {len(search_results)} lekcji")
    for result in search_results:
        print(f"  - {result['lesson']['title']} (Kategoria: {result['category_name']})")
