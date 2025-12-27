import json
import sys

filepath = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json'

print(f"Sprawdzam plik: {filepath}")
print("=" * 60)

try:
    # Próba 1: Standardowy load
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('✅ JSON poprawny!')
    print(f'Tytuł: {data.get("title")}')
    print(f'ID: {data.get("id")}')
    print(f'Główne klucze ({len(data.keys())}):')
    for key in data.keys():
        print(f'  - {key}')
    
except json.JSONDecodeError as e:
    print(f'❌ Błąd JSON!')
    print(f'  Linia: {e.lineno}')
    print(f'  Kolumna: {e.colno}')
    print(f'  Komunikat: {e.msg}')
    print(f'  Pozycja w pliku: {e.pos}')
    
    # Analiza kontekstu błędu
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pokaż 5 linii przed i po błędzie
    lines = content.split('\n')
    error_line = e.lineno - 1  # Python liczy od 0
    
    print('\n' + '=' * 60)
    print('KONTEKST BŁĘDU (5 linii przed i po):')
    print('=' * 60)
    
    start = max(0, error_line - 5)
    end = min(len(lines), error_line + 6)
    
    for i in range(start, end):
        marker = '>>> ' if i == error_line else '    '
        print(f'{marker}{i+1:4d}: {lines[i]}')
    
    # Pokaż fragment z błędem
    print('\n' + '=' * 60)
    print('FRAGMENT TEKSTU WOKÓŁ BŁĘDU:')
    print('=' * 60)
    
    start_pos = max(0, e.pos - 200)
    end_pos = min(len(content), e.pos + 200)
    fragment = content[start_pos:end_pos]
    
    # Pokaż pozycję błędu w fragmencie
    error_in_fragment = e.pos - start_pos
    print(repr(fragment))
    print(' ' * error_in_fragment + '^--- BŁĄD TUTAJ (pozycja ' + str(e.pos) + ')')
    
    sys.exit(1)
