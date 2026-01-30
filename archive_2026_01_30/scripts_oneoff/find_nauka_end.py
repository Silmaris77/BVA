with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Znajdź sekcję nauka
nauka_start = None
for i, line in enumerate(lines):
    if '  "nauka": {' in line:
        nauka_start = i
        print(f"Sekcja 'nauka' zaczyna się w linii {i+1}")
        break

# Szukaj gdzie kończy się sekcja nauka (na tym samym poziomie wcięcia co początek)
if nauka_start:
    depth = 0
    for i in range(nauka_start, len(lines)):
        line = lines[i]
        
        for char in line:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    print(f"Sekcja 'nauka' kończy się w linii {i+1}: {repr(line)}")
                    print(f"\nNastępna linia ({i+2}): {repr(lines[i+1])}")
                    print(f"Następna linia ({i+3}): {repr(lines[i+2]) if i+2 < len(lines) else 'BRAK'}")
                    break
        
        if depth == 0:
            break
