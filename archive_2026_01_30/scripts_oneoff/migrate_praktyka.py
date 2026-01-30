import json

# Wczytaj obie wersje
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# Pobierz practical_exercises z v1.0
practical = v1.get('sections', {}).get('practical_exercises', {})

print("=== STRUKTURA PRACTICAL_EXERCISES W v1.0 ===")
for key in practical.keys():
    print(f"\n{key}:")
    if isinstance(practical[key], dict):
        print(f"  Klucze: {list(practical[key].keys())}")
        if 'sections' in practical[key]:
            print(f"  Liczba sections: {len(practical[key]['sections'])}")
        if 'studies' in practical[key]:
            print(f"  Liczba studies: {len(practical[key]['studies'])}")
        if 'cards' in practical[key]:
            print(f"  Liczba cards: {len(practical[key]['cards'])}")

# Struktura praktyka dla v2.0
# Według kodu aplikacji praktyka może mieć podobną strukturę jak nauka
# Stwórzmy płaską strukturę z kluczami praktycznymi

praktyka_v2 = {}

# 1. Exercises (ćwiczenia praktyczne)
if 'exercises' in practical:
    exercises = practical['exercises']
    praktyka_v2['cwiczenia'] = {
        'title': exercises.get('title', 'Ćwiczenia praktyczne'),
        'description': exercises.get('description', ''),
        'sekcje': [
            {
                'tytul': section['title'],
                'tresc': section['content']
            }
            for section in exercises.get('sections', [])
        ]
    }
    print(f"\n✅ Dodano {len(exercises.get('sections', []))} ćwiczeń")

# 2. Case studies (już dodane do nauki, ale możemy dodać też tutaj)
if 'case_studies' in practical:
    cs_data = practical['case_studies']
    praktyka_v2['case_studies'] = cs_data.get('studies', [])
    print(f"✅ Dodano {len(cs_data.get('studies', []))} case studies")

# 3. Generated case studies
if 'generated_case_studies' in practical:
    gen_cs = practical['generated_case_studies']
    praktyka_v2['ai_case_studies'] = {
        'title': gen_cs.get('title', 'Case Studies z AI'),
        'description': gen_cs.get('description', ''),
        'scenarios': gen_cs.get('scenarios', [])
    }
    print(f"✅ Dodano {len(gen_cs.get('scenarios', []))} AI case studies")

# 4. Final exercises
if 'final_exercises' in practical:
    final = practical['final_exercises']
    if 'exercises' in final:
        praktyka_v2['cwiczenia_finalne'] = final['exercises']
        print(f"✅ Dodano {len(final['exercises'])} ćwiczeń finalnych")

# 5. Final AI exercises
if 'final_ai_exercises' in practical:
    final_ai = practical['final_ai_exercises']
    if 'exercises' in final_ai:
        praktyka_v2['ai_cwiczenia'] = final_ai['exercises']
        print(f"✅ Dodano {len(final_ai['exercises'])} ćwiczeń AI")

# Zapisz do v2.0
v2['praktyka'] = praktyka_v2

with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'w', encoding='utf-8') as f:
    json.dump(v2, f, ensure_ascii=False, indent=2)

print("\n✅ Zapisano sekcję praktyka do v2.0!")
print("\nStruktura praktyka:")
for key in v2['praktyka'].keys():
    value = v2['praktyka'][key]
    if isinstance(value, dict):
        if 'sekcje' in value:
            print(f"- {key}: {len(value['sekcje'])} sekcji")
        elif 'scenarios' in value:
            print(f"- {key}: {len(value['scenarios'])} scenariuszy")
        else:
            print(f"- {key}: {list(value.keys())}")
    elif isinstance(value, list):
        print(f"- {key}: {len(value)} elementów")
    else:
        print(f"- {key}")
