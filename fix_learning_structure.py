import json

# Wczytaj plik
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'r', encoding='utf-8') as f:
    lesson = json.load(f)

# Sprawdź obecną strukturę
print("Obecna struktura sections.learning:", type(lesson['sections']['learning']))

# Jeśli learning to array - zamień na object z kluczem 'sections'
if isinstance(lesson['sections']['learning'], list):
    print("✅ Learning to array - przekształcam na object...")
    sections_array = lesson['sections']['learning']
    lesson['sections']['learning'] = {
        "sections": sections_array
    }
    print(f"✅ Przekształcono: learning.sections ma teraz {len(sections_array)} elementów")
else:
    print("❌ Learning NIE jest array - struktura nieoczekiwana")
    print(lesson['sections']['learning'])

# Zapisz
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'w', encoding='utf-8') as f:
    json.dump(lesson, f, ensure_ascii=False, indent=2)

# Weryfikuj
print("\n🔍 Weryfikacja...")
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'r', encoding='utf-8') as f:
    test = json.load(f)
    print(f"✅ Plik valid JSON")
    print(f"sections.learning type: {type(test['sections']['learning'])}")
    if 'sections' in test['sections']['learning']:
        print(f"✅ sections.learning.sections istnieje ({len(test['sections']['learning']['sections'])} elementów)")
    else:
        print("❌ sections.learning.sections NIE istnieje")
