with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Usuń ostatnią linię (dodatkowy nawias})
with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'w', encoding='utf-8') as f:
    f.writelines(lines[:-1])

print(f"Usunięto ostatnią linię. Teraz jest {len(lines)-1} linii.")
