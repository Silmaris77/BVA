with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Liczba linii: {len(lines)}")
print("\nOstatnie 10 linii:")
for i in range(max(0, len(lines)-10), len(lines)):
    print(f"{i+1:4d}: {repr(lines[i])}")
