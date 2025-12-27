import json

# Wczytaj lekcję
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'r', encoding='utf-8') as f:
    lesson = json.load(f)

print("📋 Obecna struktura:")
print(f"  - sections keys: {list(lesson['sections'].keys())}")
print(f"  - exercises keys: {list(lesson.get('exercises', {}).keys())}")

# Przenieś exercises do sections.practical_exercises
if 'exercises' in lesson:
    print("\n✅ Przenoszę exercises → sections.practical_exercises...")
    
    # Utwórz sekcję practical_exercises
    lesson['sections']['practical_exercises'] = {
        "case_studies": lesson['exercises']['case_studies']
    }
    
    # Usuń starą sekcję exercises z root level
    del lesson['exercises']
    
    print("✅ Przeniesiono!")
else:
    print("❌ Brak sekcji exercises")

# Zapisz
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'w', encoding='utf-8') as f:
    json.dump(lesson, f, ensure_ascii=False, indent=2)

# Weryfikuj
print("\n🔍 Weryfikacja...")
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'r', encoding='utf-8') as f:
    test = json.load(f)
    print(f"✅ JSON valid")
    print(f"sections keys: {list(test['sections'].keys())}")
    print(f"Has practical_exercises: {'practical_exercises' in test['sections']}")
    print(f"Has exercises (old): {'exercises' in test}")
    
    if 'practical_exercises' in test['sections']:
        print(f"practical_exercises keys: {list(test['sections']['practical_exercises'].keys())}")
