import json

# Wczytaj obie wersje
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# Pobierz taby z v1.0
v1_tabs = v1.get('sections', {}).get('learning', {}).get('tabs', [])

# Znajdź podcast i fiszki
podcast_tab = next((t for t in v1_tabs if t.get('id') == 'podcast'), None)
video_tab = next((t for t in v1_tabs if t.get('id') == 'video'), None)

# Sprawdź strukturę
if podcast_tab:
    print("=== PODCAST TAB ===")
    print(f"Klucze: {list(podcast_tab.keys())}")
    if 'sections' in podcast_tab:
        print(f"Liczba sekcji: {len(podcast_tab['sections'])}")
        if podcast_tab['sections']:
            first = podcast_tab['sections'][0]
            print(f"Pierwsza sekcja - klucze: {list(first.keys())}")
            print(f"Title: {first.get('title', 'BRAK')[:80]}")

# Podcast - przekształć sections[] na strukturę oczekiwaną przez kod
if podcast_tab and 'sections' in podcast_tab and len(podcast_tab['sections']) > 0:
    first_section = podcast_tab['sections'][0]
    v2['nauka']['podcast'] = {
        'title': first_section.get('title', '🎧 Podcast'),
        'description': first_section.get('description', ''),
        'url': first_section.get('url', ''),
        'transcript': first_section.get('transcript', ''),
        'content': first_section.get('content', '')  # Dodaj content jeśli istnieje
    }
    print(f"\n✅ Dodano podcast")

# Video - przekształć sections[] na sekcje do nauki
if video_tab and 'sections' in video_tab:
    # Jeśli video ma sections, przekształć je tak samo jak tekst
    v2['nauka']['video'] = {
        'sekcje': [
            {
                'tytul': section['title'],
                'tresc': section['content']
            }
            for section in video_tab['sections']
        ]
    }
    print(f"✅ Dodano video ({len(video_tab['sections'])} sekcji)")

# Szukaj fiszek w v1.0 - może są w sections.exercises?
if 'sections' in v1 and 'exercises' in v1['sections']:
    exercises = v1['sections']['exercises']
    print(f"\n=== EXERCISES ===")
    print(f"Klucze: {list(exercises.keys())}")
    
    if 'flashcards' in exercises:
        flashcards = exercises['flashcards']
        v2['nauka']['fiszki'] = {
            'title': '🃏 Fiszki',
            'description': flashcards.get('description', 'Kluczowe pojęcia do zapamiętania'),
            'karty': flashcards.get('cards', [])
        }
        print(f"✅ Dodano fiszki ({len(flashcards.get('cards', []))} kart)")

# Zapisz
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'w', encoding='utf-8') as f:
    json.dump(v2, f, ensure_ascii=False, indent=2)

print("\n✅ Zaktualizowano v2.0!")
print("\nStruktura nauka:")
for key in v2['nauka'].keys():
    value = v2['nauka'][key]
    if isinstance(value, dict):
        if 'sekcje' in value:
            print(f"- {key}: {len(value['sekcje'])} sekcji")
        elif 'karty' in value:
            print(f"- {key}: {len(value['karty'])} kart")
        else:
            print(f"- {key}")
    else:
        print(f"- {key}")
