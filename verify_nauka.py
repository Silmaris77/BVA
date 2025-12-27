import json

data = json.load(open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', encoding='utf-8'))

print('✅ JSON poprawny!')
sections = data['nauka']['tabs'][0]['sections']
print(f'\nSekcje w zakładce Teoria: {len(sections)}\n')

for i, s in enumerate(sections):
    print(f'{i+1}. {s["title"]}')
