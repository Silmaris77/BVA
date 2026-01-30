"""
Naprawa uszkodzonego pliku users_data.json
"""

import json
import shutil
from datetime import datetime

print("="*60)
print("   NAPRAWA PLIKU users_data.json")
print("="*60)
print()

file_path = "users_data.json"

# 1. Kopia zapasowa
backup_path = f"users_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
print(f"1️⃣ Tworzę kopię zapasową: {backup_path}")
try:
    shutil.copy(file_path, backup_path)
    print(f"   ✅ Kopia zapisana")
except Exception as e:
    print(f"   ⚠️ Błąd kopii: {e}")

print()

# 2. Próba wczytania z diagnostyką
print("2️⃣ Diagnoza błędu...")
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Spróbuj załadować
    json.loads(content)
    print("   ✅ JSON jest poprawny!")
    
except json.JSONDecodeError as e:
    print(f"   ❌ Błąd JSON:")
    print(f"      Linia: {e.lineno}")
    print(f"      Kolumna: {e.colno}")
    print(f"      Znak: {e.pos}")
    print(f"      Wiadomość: {e.msg}")
    print()
    
    # Pokaż kontekst błędu
    print("3️⃣ Kontekst błędu:")
    lines = content.split('\n')
    if e.lineno > 0 and e.lineno <= len(lines):
        start = max(0, e.lineno - 3)
        end = min(len(lines), e.lineno + 2)
        
        for i in range(start, end):
            marker = " ► " if i == e.lineno - 1 else "   "
            print(f"{marker}{i+1:4d} | {lines[i][:100]}")
            if i == e.lineno - 1 and e.colno:
                print(f"       {' ' * (e.colno-1)}^ TUTAJ")
    print()
    
    # 4. Automatyczna naprawa
    print("4️⃣ Próba automatycznej naprawy...")
    
    # Najczęstsze problemy:
    # - Brak przecinka między obiektami
    # - Dodatkowy przecinek na końcu
    # - Znaki niedozwolone
    
    fixed = False
    
    # Spróbuj naprawić brakujący przecinek
    if "Expecting ',' delimiter" in e.msg:
        print("   🔧 Wykryto brak przecinka")
        # Znajdź miejsce błędu
        pos = e.pos
        before = content[:pos]
        after = content[pos:]
        
        # Sprawdź czy to problem z przecinkiem między obiektami
        if before.rstrip().endswith('}') and after.lstrip().startswith('"'):
            print("   🔧 Dodaję brakujący przecinek...")
            fixed_content = before.rstrip() + ',\n' + after.lstrip()
            
            # Testuj poprawkę
            try:
                json.loads(fixed_content)
                print("   ✅ Naprawa udana!")
                
                # Zapisz naprawiony plik
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"   💾 Zapisano naprawiony plik")
                fixed = True
                
            except json.JSONDecodeError as e2:
                print(f"   ❌ Naprawa nie zadziałała: {e2.msg}")
    
    if not fixed:
        print()
        print("="*60)
        print("⚠️ RĘCZNA NAPRAWA WYMAGANA")
        print("="*60)
        print(f"1. Otwórz plik: {file_path}")
        print(f"2. Przejdź do linii: {e.lineno}")
        print(f"3. Sprawdź kolumnę: {e.colno}")
        print(f"4. Popraw błąd: {e.msg}")
        print(f"5. Zapisz plik")
        print()
        print("Lub przywróć kopię zapasową:")
        print(f"   copy {backup_path} {file_path}")

except Exception as e:
    print(f"❌ Nieoczekiwany błąd: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*60)
