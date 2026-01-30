import json

# Wczytaj obie wersje
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# Sprawdź strukturę v1.0 - szukam podcast i fiszki
v1_tabs = v1.get('sections', {}).get('learning', {}).get('tabs', [])

print("=== TABS W v1.0 ===")
for tab in v1_tabs:
    tab_id = tab.get('id')
    tab_title = tab.get('title')
    print(f"\nTab: {tab_id} - {tab_title}")
    print(f"Klucze: {list(tab.keys())}")
    
    # Jeśli to podcast lub fiszki, pokaż szczegóły
    if tab_id in ['podcast', 'fiszki']:
        print(f"\nZnaleziono {tab_id}!")
        print(json.dumps(tab, indent=2, ensure_ascii=False)[:500])

# Znajdź podcast w v1.0
podcast_tab = next((t for t in v1_tabs if t.get('id') == 'podcast'), None)
fiszki_tab = next((t for t in v1_tabs if t.get('id') == 'fiszki'), None)

# Dodaj do v2.0
if podcast_tab:
    print("\n\n=== DODAJĘ PODCAST ===")
    v2['nauka']['podcast'] = {
        'title': podcast_tab.get('title', '🎧 Podcast'),
        'description': podcast_tab.get('description', ''),
        'url': podcast_tab.get('url', ''),
        'transcript': podcast_tab.get('transcript', '')
    }
    print(f"✓ Podcast: {podcast_tab.get('title')}")

if fiszki_tab:
    print("\n=== DODAJĘ FISZKI ===")
    v2['nauka']['fiszki'] = {
        'title': fiszki_tab.get('title', '🃏 Fiszki'),
        'description': fiszki_tab.get('description', ''),
        'karty': fiszki_tab.get('karty', [])
    }
    print(f"✓ Fiszki: {len(fiszki_tab.get('karty', []))} kart")

# Zapisz
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'w', encoding='utf-8') as f:
    json.dump(v2, f, ensure_ascii=False, indent=2)

print("\n✅ Dodano podcast i fiszki do v2.0!")
print("\nStruktura nauka po zmianach:")
for key in v2['nauka'].keys():
    print(f"- {key}")
