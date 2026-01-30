import json

# Prębuję załadować plik ignorując błąd
with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Sprawdzę ile jest nawiasów otwierających i zamykających
print("Analiza nawiasów:")
print(f"{{ : {content.count('{')}")
print(f"}} : {content.count('}')}")
print(f"Różnica: {content.count('{') - content.count('}')}")

# Spróbuję znaleźć gdzie kończy się główny obiekt JSON
depth = 0
main_object_end = None

for i, char in enumerate(content):
    if char == '{':
        depth += 1
    elif char == '}':
        depth -= 1
        if depth == 0 and main_object_end is None:
            main_object_end = i
            # Policz liczbę linii do tej pozycji
            lines_before = content[:i].count('\n') + 1
            print(f"\nGłówny obiekt JSON zamyka się w pozycji {i} (linia ~{lines_before})")
            print(f"Ostatnie 100 znaków przed zamknięciem:")
            print(repr(content[max(0, i-100):i+50]))
            break

if depth != 0:
    print(f"\n⚠️  Niezbalansowane nawiasy! Końcowa głębokość: {depth}")
