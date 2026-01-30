with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Liczymy nawiasy w całym pliku
open_braces = 0
close_braces = 0

depth = 0
max_depth = 0

for i, char in enumerate(content):
    if char == '{':
        open_braces += 1
        depth += 1
        if depth > max_depth:
            max_depth = depth
    elif char == '}':
        close_braces += 1
        depth -= 1
        if depth < 0:
            print(f"BŁĄD: Za dużo nawiasów zamykających na pozycji {i}")
            print(f"Fragment: {repr(content[max(0, i-50):i+50])}")
            break

print(f"Nawiasy otwierające {{: {open_braces}")
print(f"Nawiasy zamykające }}: {close_braces}")
print(f"Różnica: {open_braces - close_braces}")
print(f"Maksymalna głębokość zagnieżdżenia: {max_depth}")
print(f"Końcowa głębokość: {depth}")

if depth != 0:
    print(f"\n⚠️  PROBLEM: Końcowa głębokość powinna wynosić 0, ale wynosi {depth}")
    if depth > 0:
        print(f"   Brakuje {depth} nawiasów zamykających }}")
    else:
        print(f"   Za dużo nawiasów zamykających (nadmiar: {-depth})")
