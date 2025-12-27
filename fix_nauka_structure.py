import json

# Wczytaj v2.0
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Przekształć strukturę nauka z tabs[] na płaską strukturę
tabs = data['nauka']['tabs']

# Nowa struktura
new_nauka = {}

# Tab "teoria" -> "tekst" z kluczem "sekcje"
teoria_tab = next((t for t in tabs if t['id'] == 'teoria'), None)
if teoria_tab and 'sections' in teoria_tab:
    new_nauka['tekst'] = {
        'sekcje': [
            {
                'tytul': section['title'],
                'tresc': section['content']
            }
            for section in teoria_tab['sections']
        ]
    }

# Tab "narzedzia" - jeśli ma content, dodaj jako osobny klucz
narzedzia_tab = next((t for t in tabs if t['id'] == 'narzedzia'), None)
# Póki co placeholder, więc pomijamy

# Tab "video" - przekształć na strukturę oczekiwaną przez kod
video_tab = next((t for t in tabs if t['id'] == 'video'), None)
if video_tab:
    new_nauka['video'] = {
        'title': video_tab.get('title', 'Video'),
        'description': 'Materiały wideo - w przygotowaniu',
        'url': ''  # Placeholder
    }

# Zastąp starą strukturę nową
data['nauka'] = new_nauka

# Zapisz
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Przekształcono strukturę nauka z tabs[] na płaską strukturę!")
print("\nNowa struktura nauka:")
print(f"- tekst: {len(new_nauka.get('tekst', {}).get('sekcje', []))} sekcji")
print(f"- video: {'✓' if 'video' in new_nauka else '✗'}")
