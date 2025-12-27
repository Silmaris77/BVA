#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Poprawka struktury praktyka zgodnie z template V2
"""

import json

v1_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json'
v2_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json'

# Wczytaj oba pliki
with open(v1_path, 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(v2_path, 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# Pobierz dane z v1.0
practical = v1['sections']['practical_exercises']
exercises = practical.get('exercises', {})
case_studies = practical.get('case_studies', {})
ai_exercises = practical.get('ai_exercises', {})
closing_quiz = practical.get('closing_quiz', {})

# Utwórz poprawną strukturę praktyka zgodną z template V2
v2['praktyka'] = {
    # CWICZENIA - tablica obiektów (nie obiekt z sekcje!)
    "cwiczenia": [],
    
    # CASE STUDIES (opcjonalne)
    "case_studies": case_studies.get('studies', []),
    
    # WYZWANIE AI (opcjonalne)
    "wyzwanie": {
        "title": "💪 Challenge - Dynamiczne case studies",
        "description": "AI wygeneruje dla Ciebie unikalny przypadek komunikacyjny do rozwiązania",
        "generator_prompt": "Wygeneruj przypadek komunikacyjny w kontekście Conversational Intelligence",
        "difficulty": "medium"
    },
    
    # CWICZENIA AI - scenarios zamiast cwiczenia
    "cwiczenia_ai": {
        "title": ai_exercises.get('title', '🤖 Ćwiczenia AI'),
        "description": ai_exercises.get('description', ''),
        "scenarios": []
    },
    
    # QUIZ KONCOWY - pytania zamiast questions
    "quiz_koncowy": {
        "title": closing_quiz.get('title', '📝 Quiz Końcowy'),
        "description": closing_quiz.get('description', ''),
        "passing_score": 70,
        "pytania": []
    }
}

# Przekształć exercises.sections w tablicę obiektów cwiczenia
if 'sections' in exercises:
    for i, section in enumerate(exercises['sections'], 1):
        cwiczenie = {
            "id": i,
            "title": section.get('title', f'Ćwiczenie {i}'),
            "type": "practical",
            "description": section.get('title', ''),
            "instructions": section.get('content', ''),
            "time_required": "15-20 min"
        }
        v2['praktyka']['cwiczenia'].append(cwiczenie)

# Przekształć ai_exercises.exercises w scenarios
if 'exercises' in ai_exercises:
    for i, ex in enumerate(ai_exercises['exercises'], 1):
        scenario = {
            "id": i,
            "title": ex.get('title', f'Scenariusz {i}'),
            "description": ex.get('title', ''),
            "ai_role": "Ekspert Conversational Intelligence",
            "user_task": ex.get('content', {}).get('exercise_prompt', ''),
            "full_content": ex.get('content', {})
        }
        v2['praktyka']['cwiczenia_ai']['scenarios'].append(scenario)

# Przekształć closing_quiz.questions w pytania
if 'questions' in closing_quiz:
    for q in closing_quiz['questions']:
        pytanie = {
            "id": q.get('id'),
            "pytanie": q.get('question', ''),
            "opcje": q.get('options', []),
            "poprawna": q.get('correct', 0),
            "wyjaśnienie": q.get('explanation', '')
        }
        v2['praktyka']['quiz_koncowy']['pytania'].append(pytanie)

# Zapisz
with open(v2_path, 'w', encoding='utf-8') as f:
    json.dump(v2, f, ensure_ascii=False, indent=2)

print("✅ POPRAWIONO STRUKTURĘ PRAKTYKA")
print(f"\n📊 Struktura praktyka (zgodna z V2 template):")
print(f"- cwiczenia: {len(v2['praktyka']['cwiczenia'])} elementów (tablica)")
print(f"- case_studies: {len(v2['praktyka']['case_studies'])} elementów")
print(f"- wyzwanie: ✅ (obiekt)")
print(f"- cwiczenia_ai.scenarios: {len(v2['praktyka']['cwiczenia_ai']['scenarios'])} scenariuszy")
print(f"- quiz_koncowy.pytania: {len(v2['praktyka']['quiz_koncowy']['pytania'])} pytań")
