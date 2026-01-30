import json

# Wczytaj obie wersje
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# Pobierz case studies z v1.0
case_studies_data = v1.get('sections', {}).get('practical_exercises', {}).get('case_studies', {})

if case_studies_data and 'studies' in case_studies_data:
    # Dodaj do v2.0 w sekcji nauka
    v2['nauka']['case_studies'] = case_studies_data['studies']
    
    print(f"✅ Dodano {len(case_studies_data['studies'])} case studies do sekcji nauka w v2.0!")
    
    # Pokaż tytuły
    print("\nCase studies:")
    for i, cs in enumerate(case_studies_data['studies'], 1):
        print(f"{i}. {cs.get('title', 'Bez tytułu')}")
else:
    print("❌ Nie znaleziono case studies w v1.0")

# Zapisz
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'w', encoding='utf-8') as f:
    json.dump(v2, f, ensure_ascii=False, indent=2)

print("\n✅ Zapisano v2.0!")
print("\nKompletna struktura nauka:")
for key in v2['nauka'].keys():
    value = v2['nauka'][key]
    if isinstance(value, dict):
        if 'sekcje' in value:
            print(f"- {key}: {len(value['sekcje'])} sekcji")
        elif 'karty' in value:
            print(f"- {key}: {len(value['karty'])} kart")
        else:
            print(f"- {key}")
    elif isinstance(value, list):
        print(f"- {key}: {len(value)} elementów")
    else:
        print(f"- {key}")
