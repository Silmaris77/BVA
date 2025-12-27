import json

with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'r', encoding='utf-8') as f:
    lesson = json.load(f)

print("✅ JSON valid!")
print(f"\n📋 Struktura:")
print(f"  sections keys: {list(lesson['sections'].keys())}")
print(f"  practical_exercises keys: {list(lesson['sections']['practical_exercises'].keys())}")

if 'closing_quiz' in lesson['sections']['practical_exercises']:
    quiz = lesson['sections']['practical_exercises']['closing_quiz']
    print(f"\n✅ Quiz końcowy istnieje!")
    print(f"  Liczba pytań: {len(quiz['questions'])}")
    print(f"\n📝 Przykładowe pytanie #1:")
    print(f"  Q: {quiz['questions'][0]['question']}")
    print(f"  Odpowiedzi: {len(quiz['questions'][0]['options'])}")
else:
    print("\n❌ Brak quizu końcowego")
