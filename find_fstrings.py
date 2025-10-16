with open('views/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Znajdź wszystkie f""" w pliku
fstring_triple = []
pos = 0
while True:
    pos = content.find('f"""', pos)
    if pos == -1:
        break
    line_num = content[:pos].count('\n') + 1
    fstring_triple.append((pos, line_num))
    pos += 4

print(f"Znaleziono {len(fstring_triple)} wystąpień 'f\"\"\"'")

# Pokaż wszystkie
print("\nWszystkie wystąpienia f\"\"\" (pozycja, linia):")
for i, (pos, line_num) in enumerate(fstring_triple):
    context_start = max(0, pos - 20)
    context_end = min(len(content), pos + 60)
    context = content[context_start:context_end].replace('\n', '\\n')
    print(f"{i+1}. Linia {line_num}: ...{context}...")
