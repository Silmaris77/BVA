import json

# Load old lesson
with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', encoding='utf-8') as f:
    old_data = json.load(f)

# Load new v2.0 lesson
with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', encoding='utf-8') as f:
    new_data = json.load(f)

# Copy sections from old learning/tabs[0]/sections to new nauka/tabs[0]/sections
old_sections = old_data['sections']['learning']['tabs'][0]['sections']
new_data['nauka']['tabs'][0]['sections'] = old_sections

print(f'Skopiowano {len(old_sections)} sekcji z zakładki "Tekst"')

# Save updated v2.0
with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print('✅ Zaktualizowano sekcję nauka w pliku v2.0!')
