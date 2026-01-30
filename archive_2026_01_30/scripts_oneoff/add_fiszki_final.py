import json

# Wczytaj obie wersje
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# Znajdź fiszki w v1.0
flashcards_data = v1.get('sections', {}).get('practical_exercises', {}).get('flashcards', {})

if flashcards_data and 'cards' in flashcards_data:
    # Przekształć strukturę z front/back na przod/tyl
    karty = []
    for card in flashcards_data['cards']:
        karty.append({
            'przod': card.get('front', ''),
            'tyl': card.get('back', ''),
            'kategoria': card.get('category', ''),
            'trudnosc': card.get('difficulty', '')
        })
    
    # Dodaj do v2.0
    v2['nauka']['fiszki'] = {
        'title': flashcards_data.get('title', '🃏 Fiszki'),
        'description': flashcards_data.get('description', ''),
        'karty': karty
    }
    
    print(f"✅ Dodano {len(karty)} fiszek do v2.0!")
    
    # Pokaż przykład
    if karty:
        print(f"\nPrzykładowa fiszka:")
        print(f"Przód: {karty[0]['przod'][:60]}...")
        print(f"Tył: {karty[0]['tyl'][:60]}...")
else:
    print("❌ Nie znaleziono fiszek w v1.0")

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
