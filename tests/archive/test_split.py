with open('views/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Znajdź wszystkie """ w pliku
triple_quotes = []
pos = 0
while True:
    pos = content.find('"""', pos)
    if pos == -1:
        break
    triple_quotes.append(pos)
    pos += 3

print(f"Znaleziono {len(triple_quotes)} wystąpień '\"\"\"'")
print(f"Czy parzysta liczba: {len(triple_quotes) % 2 == 0}")

# Pokaż ostatnie 20
print("\nOstatnie 20 wystąpień (pozycja, linia):")
for i, pos in enumerate(triple_quotes[-20:]):
    line_num = content[:pos].count('\n') + 1
    context_start = max(0, pos - 40)
    context_end = min(len(content), pos + 43)
    context = content[context_start:context_end].replace('\n', '\\n')
    print(f"{i+1}. Pozycja {pos}, linia {line_num}: ...{context}...")
