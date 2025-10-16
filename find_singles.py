with open('views/tools.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Szukaj linii które mają tylko JEDNO """ (nie parę)
single_triple_lines = []
for i, line in enumerate(lines):
    count = line.count('"""')
    if count == 1:  # Nieparna liczba na jednej linii - może być otwarcie lub zamknięcie
        single_triple_lines.append((i+1, line.strip()))

print(f"Znaleziono {len(single_triple_lines)} linii z pojedynczym '\"\"\"'")
print("\nLinietworzy pary z innymi lub są nieparzystą liczbą:")
for line_num, content in single_triple_lines:
    print(f"Linia {line_num}: {content[:100]}")
