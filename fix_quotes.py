import json

# Wczytaj plik
with open('data/lessons/11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Zamień polskie cudzysłowy na zwykłe
original_content = content
content = content.replace('„', '"').replace('"', '"')

# Policz ile zamian zostało dokonanych
changes_start = original_content.count('„')
changes_end = original_content.count('"')
print(f'Zamieniono {changes_start} otwierających i {changes_end} zamykających polskich cudzysłowów')

# Zapisz poprawiony plik
with open('data/lessons/11. Od słów do zaufania - Conversational Intelligence.json', 'w', encoding='utf-8') as f:
    f.write(content)

print('Zapisano poprawiony plik')

# Sprawdź czy JSON jest teraz poprawny
try:
    lesson = json.loads(content)
    print('JSON jest teraz poprawny!')
    print('Podsumowanie zostało zaktualizowane')
except json.JSONDecodeError as e:
    print(f'Nadal błąd JSON: {e}')