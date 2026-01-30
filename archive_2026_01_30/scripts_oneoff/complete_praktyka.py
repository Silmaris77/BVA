#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Uzupełnienie sekcji praktyka o AI exercises i closing quiz
"""

import json
import sys

# Ścieżki do plików
v1_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json'
v2_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json'

# Wczytaj oba pliki
with open(v1_path, 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(v2_path, 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# Pobierz AI exercises z v1.0
ai_exercises = v1['sections']['practical_exercises'].get('ai_exercises', {})
closing_quiz = v1['sections']['practical_exercises'].get('closing_quiz', {})

print("=== AI EXERCISES w v1.0 ===")
print(f"Klucze: {list(ai_exercises.keys())}")
if 'exercises' in ai_exercises:
    print(f"Liczba exercises: {len(ai_exercises['exercises'])}")
    for i, ex in enumerate(ai_exercises['exercises'], 1):
        print(f"  {i}. {ex.get('title', 'Bez tytułu')} (ID: {ex.get('id', 'brak')})")

print("\n=== CLOSING QUIZ w v1.0 ===")
print(f"Klucze: {list(closing_quiz.keys())}")
if 'questions' in closing_quiz:
    print(f"Liczba pytań: {len(closing_quiz['questions'])}")

# Dodaj AI exercises do praktyka.ai_cwiczenia
if 'praktyka' not in v2:
    v2['praktyka'] = {}

# Struktura AI ćwiczeń
v2['praktyka']['ai_cwiczenia'] = {
    'tytul': ai_exercises.get('title', '🤖 Ćwiczenia AI'),
    'opis': ai_exercises.get('description', ''),
    'config': ai_exercises.get('config', {}),
    'cwiczenia': ai_exercises.get('exercises', [])
}

# Dodaj closing quiz do praktyka.quiz_koncowy
v2['praktyka']['quiz_koncowy'] = {
    'tytul': closing_quiz.get('title', '🎯 Quiz końcowy'),
    'opis': closing_quiz.get('description', ''),
    'pytania': closing_quiz.get('questions', [])
}

# Zapisz
with open(v2_path, 'w', encoding='utf-8') as f:
    json.dump(v2, f, ensure_ascii=False, indent=2)

print(f"\n✅ Dodano {len(ai_exercises.get('exercises', []))} AI ćwiczeń")
print(f"✅ Dodano quiz końcowy z {len(closing_quiz.get('questions', []))} pytaniami")
print("\n✅ Sekcja praktyka kompletna!")

print("\nStruktura praktyka:")
print(f"- cwiczenia: {len(v2['praktyka']['cwiczenia']['sekcje'])} sekcji")
print(f"- case_studies: {len(v2['praktyka']['case_studies'])} elementów")
print(f"- ai_case_studies: {len(v2['praktyka']['ai_case_studies'].get('scenarios', []))} scenariuszy")
print(f"- ai_cwiczenia: {len(v2['praktyka']['ai_cwiczenia']['cwiczenia'])} ćwiczeń")
print(f"- quiz_koncowy: {len(v2['praktyka']['quiz_koncowy']['pytania'])} pytań")
