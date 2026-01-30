import json

# Wczytaj v2.0
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Dodaj pole icon do każdego taba w nauce
for tab in data['nauka']['tabs']:
    if tab['id'] == 'teoria':
        tab['icon'] = '📚'
    elif tab['id'] == 'narzedzia':
        tab['icon'] = '🧰'
    elif tab['id'] == 'video':
        tab['icon'] = '🎬'

# Zapisz
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Dodano pole 'icon' do wszystkich tabs w sekcji nauka!")
print("\nStruktura tabs po zmianie:")
for tab in data['nauka']['tabs']:
    print(f"- {tab['title']} (icon: {tab.get('icon', 'BRAK')})")
