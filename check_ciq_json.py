import json

filepath = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('✅ JSON poprawny!')
    print(f'Tytuł: {data.get("title")}')
    print(f'ID: {data.get("id")}')
    print(f'Główne klucze: {", ".join(data.keys())}')
    
except json.JSONDecodeError as e:
    print(f'❌ Błąd JSON w linii {e.lineno}, kolumna {e.colno}')
    print(f'Komunikat: {e.msg}')
    print(f'Pozycja: {e.pos}')
    
    # Pokaż fragment z błędem
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start = max(0, e.pos - 100)
    end = min(len(content), e.pos + 100)
    print('\nFragment z błędem:')
    print(repr(content[start:end]))
    print(' ' * (e.pos - start) + '^--- błąd tutaj')
