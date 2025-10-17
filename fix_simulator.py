"""
Skrypt do usunięcia uszkodzonej sekcji symulatora z tools.py
"""

file_path = r"c:\Users\pksia\Dropbox\BVA\views\tools.py"

# Czytamy cały plik
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Oryginalny plik: {len(lines)} linii")

# Usuwamy linie 3712-4838 (indeksy 3711-4837 w Pythonie - 0-based)
# Linia 3712 to pierwsza do usunięcia, linia 4838 to ostatnia
start_line = 3711  # 3712 w edytorze (1-based)
end_line = 4838    # 4838 w edytorze (1-based) 

new_lines = lines[:start_line] + lines[end_line:]

print(f"Nowy plik: {len(new_lines)} linii")
print(f"Usunięto: {len(lines) - len(new_lines)} linii")

# Zapisujemy
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Usunięto uszkodzoną sekcję symulatora")
