#!/usr/bin/env python3
"""
Napraw konkretne linie z uszkodzonymi emoji
"""

import os

def fix_specific_lines():
    """Naprawia konkretne linie z uszkodzonymi emoji"""
    
    file_path = "views/lesson.py"
    
    # Wczytaj wszystkie linie
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Znajdź i napraw linie z uszkodzonymi emoji
    modified = False
    for i, line in enumerate(lines):
        if '"� Quiz końcowy"' in line:
            lines[i] = line.replace('"� Quiz końcowy"', '"🎓 Quiz końcowy"')
            modified = True
            print(f"✅ Naprawiono linię {i+1}: Quiz końcowy")
        
        if '"� Zadania Praktyczne"' in line:
            lines[i] = line.replace('"� Zadania Praktyczne"', '"🚀 Zadania Praktyczne"')
            modified = True
            print(f"✅ Naprawiono linię {i+1}: Zadania Praktyczne")
    
    if modified:
        # Zapisz naprawiony plik
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✅ Zapisano naprawiony plik")
        return True
    else:
        print("ℹ️ Nie znaleziono linii do naprawy")
        return False

def main():
    print("🔧 NAPRAWA KONKRETNYCH LINII Z USZKODZONYMI EMOJI")
    print("=" * 50)
    
    success = fix_specific_lines()
    
    if success:
        print("\n✅ NAPRAWA ZAKOŃCZONA")
    
    return success

if __name__ == "__main__":
    main()
