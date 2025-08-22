import json
from config.settings import LESSONS_FILE_PATH # Upewnij się, że ta ścieżka jest zdefiniowana

_lesson_data_cache = None

def load_all_lessons_data():
    global _lesson_data_cache
    if _lesson_data_cache is None:
        try:
            with open(LESSONS_FILE_PATH, 'r', encoding='utf-8') as f:
                _lesson_data_cache = json.load(f)
        except FileNotFoundError:
            print(f"Error: Lessons file not found at {LESSONS_FILE_PATH}")
            _lesson_data_cache = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {LESSONS_FILE_PATH}")
            _lesson_data_cache = {}
        except Exception as e:
            print(f"An unexpected error occurred while loading lessons: {e}")
            _lesson_data_cache = {}
    return _lesson_data_cache

def get_lesson_title(lesson_id: str) -> str:
    lessons_data = load_all_lessons_data()
    lesson_info = lessons_data.get(lesson_id)
    # Sprawdź różne możliwe struktury metadanych lekcji
    if lesson_info:
        if 'metadata' in lesson_info and 'title' in lesson_info['metadata']:
            return lesson_info['metadata']['title']
        elif 'title' in lesson_info: # Alternatywna lokalizacja tytułu
            return lesson_info['title']
    return lesson_id # Zwróć ID jeśli tytuł nie został znaleziony
