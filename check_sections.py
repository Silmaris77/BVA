import json

# Load old lesson
with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', encoding='utf-8') as f:
    data = json.load(f)

# Get sections from Tekst tab
sections = data['sections']['learning']['tabs'][0]['sections']
print(f'Liczba sekcji w zakładce Tekst: {len(sections)}\n')

for i, s in enumerate(sections):
    print(f'{i+1}. {s["title"]}')
