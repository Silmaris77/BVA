import json
import re

# Wczytaj plik
with open('data/lessons/11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Lista problemów do naprawienia
fixes = [
    ('Zamień \\"musisz\\" na „co możemy zrobić razem?"', 'Zamień &quot;musisz&quot; na &quot;co możemy zrobić razem?&quot;'),
    ('zapytaj: „Czego dziś najbardziej potrzebujemy jako zespół?"', 'zapytaj: &quot;Czego dziś najbardziej potrzebujemy jako zespół?&quot;'),
    ('„Dotarcie do następnego poziomu wielkości zależy od jakości kultury,<br>która zależy od jakości relacji,<br>a te – od jakości rozmów."', '&quot;Dotarcie do następnego poziomu wielkości zależy od jakości kultury,<br>która zależy od jakości relacji,<br>a te – od jakości rozmów.&quot;'),
]

# Wykonaj poprawki
for old_text, new_text in fixes:
    if old_text in content:
        content = content.replace(old_text, new_text)
        print(f'Poprawiono: {old_text[:50]}...')
    else:
        print(f'Nie znaleziono: {old_text[:50]}...')

# Zapisz poprawiony plik
with open('data/lessons/11. Od słów do zaufania - Conversational Intelligence.json', 'w', encoding='utf-8') as f:
    f.write(content)

print('Zapisano poprawiony plik')

# Sprawdź czy JSON jest teraz poprawny
try:
    lesson = json.loads(content)
    print('✅ JSON jest teraz poprawny!')
    print('✅ Podsumowanie zostało zaktualizowane')
except json.JSONDecodeError as e:
    print(f'❌ Nadal błąd JSON: {e}')
    print(f'Pozycja błędu: {e.pos}')
    
    # Znajdź problematyczny fragment
    lines = content.split('\n')
    char_count = 0
    for i, line in enumerate(lines):
        if char_count + len(line) >= e.pos:
            print(f'Błąd na linii {i+1}')
            error_pos_in_line = e.pos - char_count
            start = max(0, error_pos_in_line - 50)
            end = min(len(line), error_pos_in_line + 50)
            print(f'Fragment: {repr(line[start:end])}')
            break
        char_count += len(line) + 1  # +1 for newline