"""
Fix struktura practical_exercises w lekcji Conversational Intelligence
Problem: practical_exercises jest w sections.learning.tabs zamiast na najwyższym poziomie
"""

import json
import os

# Ścieżka do pliku
lesson_path = r"C:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json"

# Backup
backup_path = lesson_path.replace('.json', '_backup_pre_fix.json')

print(f"Czytam lekcję: {lesson_path}")

with open(lesson_path, 'r', encoding='utf-8') as f:
    lesson = json.load(f)

# Backup
print(f"Tworzę backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(lesson, f, ensure_ascii=False, indent=2)

print(f"\n=== OBECNA STRUKTURA ===")
print(f"Klucze na najwyższym poziomie: {list(lesson.keys())}")

# Sprawdź czy practical_exercises jest na najwyższym poziomie
if 'practical_exercises' in lesson:
    print(f"✓ practical_exercises JUŻ jest na najwyższym poziomie")
    print(f"  Klucze: {list(lesson['practical_exercises'].keys())}")
else:
    print(f"✗ practical_exercises NIE jest na najwyższym poziomie")
    
    # Szukaj w sections (obok learning)
    if 'sections' in lesson:
        sections = lesson['sections']
        
        # practical_exercises jest na tym samym poziomie co learning
        if 'practical_exercises' in sections:
            print(f"  ✓ Znalazłem practical_exercises w sections (sibling of learning)!")
            practical_data = sections['practical_exercises']
            practical_found = True
            
            if practical_found and practical_data:
                print(f"\n=== PRZENOSZĘ PRACTICAL_EXERCISES ===")
                
                # Sprawdź strukturę
                print(f"practical_exercises ma klucze: {list(practical_data.keys())}")
                
                # Wyciągnij case_studies
                case_studies_data = practical_data.get('case_studies', {})
                if isinstance(case_studies_data, dict) and 'studies' in case_studies_data:
                    case_studies = case_studies_data['studies']
                    print(f"✓ Wyciągam {len(case_studies)} case studies z case_studies.studies")
                else:
                    case_studies = []
                    print(f"⚠ Nie znaleziono case_studies.studies")
                
                # Wyciągnij closing_quiz
                closing_quiz = None
                if 'closing_quiz' in practical_data:
                    cq_data = practical_data['closing_quiz']
                    if isinstance(cq_data, dict) and 'questions' in cq_data:
                        closing_quiz = cq_data['questions']
                        print(f"✓ Wyciągam {len(closing_quiz)} pytań z closing_quiz.questions")
                    elif isinstance(cq_data, list):
                        closing_quiz = cq_data
                        print(f"✓ Znalazłem {len(closing_quiz)} pytań w closing_quiz")
                
                # Utwórz nową strukturę practical_exercises
                new_practical_exercises = {}
                
                if case_studies:
                    new_practical_exercises['case_studies'] = case_studies
                
                if closing_quiz:
                    new_practical_exercises['closing_quiz'] = closing_quiz
                
                # Dodaj na najwyższy poziom
                lesson['practical_exercises'] = new_practical_exercises
                
                # Usuń ze sections (żeby nie duplikować)
                del lesson['sections']['practical_exercises']
                print(f"✓ Usunięto practical_exercises z sections")
                
                print(f"\n=== NOWA STRUKTURA ===")
                print(f"Klucze na najwyższym poziomie: {list(lesson.keys())}")
                print(f"Klucze w practical_exercises: {list(lesson['practical_exercises'].keys())}")
                
                if 'case_studies' in lesson['practical_exercises']:
                    print(f"  case_studies: {len(lesson['practical_exercises']['case_studies'])} elementów")
                
                if 'closing_quiz' in lesson['practical_exercises']:
                    print(f"  closing_quiz: {len(lesson['practical_exercises']['closing_quiz'])} pytań")
                
                # Zapisz
                print(f"\n=== ZAPISUJĘ ===")
                with open(lesson_path, 'w', encoding='utf-8') as f:
                    json.dump(lesson, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Naprawiono strukturę!")
                print(f"\n📌 Backup: {backup_path}")
                print(f"📝 Zaktualizowany plik: {lesson_path}")
                print(f"\nTeraz zakładka PRAKTYKA powinna być widoczna w aplikacji!")
        else:
            print(f"✗ Nie znalazłem practical_exercises w sections")
            print(f"  Klucze w sections: {list(sections.keys())}")
    else:
        print(f"✗ Brak sections w strukturze")

