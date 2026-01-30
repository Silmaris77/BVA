"""
Refaktoryzacja struktury MILWAUKEE_JSS_Rules_of_Engagement.json
do formatu zgodnego z lesson.py (structure jak Module 2)
"""

import json
import os

# Ścieżki
LESSON_PATH = 'data/lessons/MILWAUKEE_JSS_Rules_of_Engagement.json'

# Wczytaj obecną strukturę
with open(LESSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded lesson: {data['title']}")
print(f"Learning sections: {len(data.get('learning_sections', []))}")
print(f"Case studies: {len(data.get('case_studies', []))}")
print(f"Closing quiz: {len(data.get('closing_quiz', []))}")
print(f"Main quiz: {len(data.get('main_quiz', []))}")

# Przekształć strukturę
new_data = {}

# Kopiuj metadane (wszystko oprócz learning_sections, case_studies, quizów)
exclude_keys = ['learning_sections', 'case_studies', 'closing_quiz', 'main_quiz']
for key in data.keys():
    if key not in exclude_keys:
        new_data[key] = data[key]

# Utwórz nową strukturę sections.learning.sections (jak Module 2)
new_data['sections'] = {
    'learning': {
        'sections': data['learning_sections']  # Przenieś learning_sections tutaj
    }
}

# Dodaj practical_exercises (case_studies + closing_quiz)
new_data['practical_exercises'] = {
    'case_studies': data['case_studies'],
    'closing_quiz': data['closing_quiz']
}

# Dodaj main_quiz bezpośrednio (jak Module 2)
new_data['closing_quiz'] = data['main_quiz']  # Module 2 nazywa to "closing_quiz"

print("\nNowa struktura:")
print(f"- sections.learning.sections: {len(new_data['sections']['learning']['sections'])}")
print(f"- practical_exercises.case_studies: {len(new_data['practical_exercises']['case_studies'])}")
print(f"- practical_exercises.closing_quiz: {len(new_data['practical_exercises']['closing_quiz'])}")
print(f"- closing_quiz (main): {len(new_data['closing_quiz'])}")

# Zapisz nową strukturę
with open(LESSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Zapisano refaktoryzowaną lekcję: {LESSON_PATH}")
