import json

# Załaduj lekcję
with open('data/lessons/11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    lesson = json.load(f)

quiz = lesson['intro']['quiz_samodiagnozy']
print(f"Quiz ma {len(quiz['questions'])} pytań")
print("\nSprawdzam correct_answer w każdym pytaniu:")

for i, q in enumerate(quiz['questions']):
    correct_answer = q.get('correct_answer', 'BRAK')
    print(f"Pytanie {i+1}: correct_answer = {correct_answer}")

# Sprawdź czy wszystkie mają None/BRAK
all_none = all(q.get('correct_answer') is None for q in quiz['questions'])
print(f"\nCzy wszystkie pytania mają correct_answer = None? {all_none}")