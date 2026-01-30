with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Znajdź gdzie zaczyna się "podsumowanie":
podsumowanie_line = None
for i, line in enumerate(lines):
    if '  "podsumowanie": {' in line:
        podsumowanie_line = i
        print(f"Znaleziono 'podsumowanie' w linii {i+1}: {line.strip()}")

if podsumowanie_line:
    # Policz głębokość zagnieżdżenia od tej linii
    depth = 0
    start_line = podsumowanie_line
    
    # Przechodź przez linie od początku sekcji podsumowanie
    for i in range(start_line, len(lines)):
        line = lines[i]
        
        # Policz nawiasy w tej linii
        for char in line:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                
                # Jeśli depth spadł do 0, oznacza to koniec sekcji podsumowanie
                if depth == 0:
                    print(f"\nKoniec sekcji 'podsumowanie' w linii {i+1}: {line.strip()}")
                    print(f"Następna linia ({i+2}): {lines[i+1].strip() if i+1 < len(lines) else 'BRAK'}")
                    break
        
        if depth == 0:
            break
    
    if depth != 0:
        print(f"\n⚠️  Sekcja 'podsumowanie' nie została zamknięta! Głębokość: {depth}")
