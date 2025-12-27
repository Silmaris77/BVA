with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Dla każdej linii, policz nawiasy kumulatywnie
depth = 0
for i, line in enumerate(lines):
    line_open = line.count('{')
    line_close = line.count('}')
    depth += line_open - line_close
    
    # Pokaż linie gdzie depth zmniejsza się do pewnych wartości
    if i+1 in [296, 297, 298, 299, 300, 621, 622, 623, 624]:
        print(f"Linia {i+1}: depth={depth:2d}  open={line_open}  close={line_close}  | {line.strip()[:80]}")

print(f"\nKońcowa głębokość: {depth}")
print(f"Brakuje {depth} nawiasów }}" if depth > 0 else "OK")
