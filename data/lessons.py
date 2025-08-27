import os
import json

def load_lessons():
    """Load all lessons from the data/lessons directory."""
    lessons_dir = os.path.join(os.path.dirname(__file__), 'lessons')
    lessons = {}

    if not os.path.exists(lessons_dir):
        print(f"Error: Lessons directory not found at {lessons_dir}")
        return {}

    for i, filename in enumerate(sorted(os.listdir(lessons_dir))):
        if filename.endswith('.json') and not filename.startswith('lesson_template'):
            try:
                with open(os.path.join(lessons_dir, filename), 'r', encoding='utf-8') as file:
                    lesson_data = json.load(file)
                    # Użyj unikalnego ID, dodając indeks dla duplikatów
                    lesson_id = os.path.splitext(filename)[0]  # Nazwa pliku (bez rozszerzenia)
                    if " copy" in lesson_id:
                        # Zamień "example_lesson copy" na "example_lesson_copy" dla lepszej obsługi
                        lesson_id = lesson_id.replace(" copy", "_copy")
                    if lesson_id in lessons:
                        # Jeśli ID już istnieje, dodaj indeks
                        lesson_id = f"{lesson_id}_{i}"
                    lessons[lesson_id] = lesson_data
                    print(f"Loaded lesson: {lesson_id}")
            except Exception as e:
                print(f"Error loading lesson {filename}: {e}")

    print(f"Total lessons loaded: {len(lessons)}")
    return lessons