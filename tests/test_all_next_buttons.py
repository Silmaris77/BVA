#!/usr/bin/env python3
"""
Test sprawdzający czy wszystkie przyciski "Dalej" używają układu kolumnowego
Data: 26 czerwca 2025
"""

import re
import os

def test_all_next_buttons():
    """Sprawdz czy wszystkie przyciski Dalej w lesson.py używają kolumn"""
    
    lesson_file = r"c:\Users\Paweł\Dropbox (Osobiste)\ZenDegenAcademy\views\lesson.py"
    
    if not os.path.exists(lesson_file):
        print("❌ Plik lesson.py nie istnieje")
        return False
    
    with open(lesson_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Znajdź wszystkie wystąpienia zen_button z tekstem "Dalej"
    patterns = [
        r'zen_button\(\s*f"Dalej:',  # Aktywne przyciski Dalej
        r'zen_button\(\s*f"🔒 Dalej:',  # Zablokowane przyciski Dalej
    ]
    
    button_locations = []
    for pattern in patterns:
        matches = list(re.finditer(pattern, content))
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            button_locations.append(line_num)
    
    print(f"🔍 Znaleziono {len(button_locations)} przycisków 'Dalej' w liniach: {button_locations}")
    
    # Sprawdź każdy przycisk czy jest poprzedzony kolumnami
    issues = []
    
    for line_num in button_locations:
        lines = content.split('\n')
        
        # Sprawdź 10 linii przed przyciskiem dla kolumn
        found_columns = False
        found_with_col2 = False
        
        for i in range(max(0, line_num-10), line_num):
            line = lines[i-1] if i > 0 else ""
            if 'st.columns([1, 1, 1])' in line:
                found_columns = True
            if 'with col2:' in line:
                found_with_col2 = True
        
        if not (found_columns and found_with_col2):
            # Sprawdź czy może to jest ten już naprawiony (ma use_container_width=True)
            button_line = lines[line_num-1]
            if 'use_container_width=True' in button_line:
                print(f"✅ Linia {line_num}: Przycisk ma kolumny (use_container_width=True)")
            else:
                issues.append(f"❌ Linia {line_num}: Przycisk bez układu kolumnowego")
                print(f"❌ Linia {line_num}: {button_line.strip()}")
        else:
            print(f"✅ Linia {line_num}: Przycisk ma kolumny")
    
    # Sprawdź czy wszystkie przyciski używają use_container_width=True
    container_width_issues = []
    for line_num in button_locations:
        lines = content.split('\n')
        button_line = lines[line_num-1]
        
        if 'use_container_width=False' in button_line:
            container_width_issues.append(f"⚠️  Linia {line_num}: use_container_width=False (powinno być True)")
    
    print("\n📊 WYNIKI TESTU:")
    print(f"✅ Przycisków z kolumnami: {len(button_locations) - len(issues)}")
    print(f"❌ Przycisków bez kolumn: {len(issues)}")
    
    if issues:
        print("\n🔧 PROBLEMY DO NAPRAWIENIA:")
        for issue in issues:
            print(issue)
    
    if container_width_issues:
        print("\n⚠️  OSTRZEŻENIA:")
        for warning in container_width_issues:
            print(warning)
    
    success = len(issues) == 0
    print(f"\n🎯 WYNIK: {'✅ WSZYSTKIE PRZYCISKI POPRAWNE' if success else '❌ WYMAGANE POPRAWKI'}")
    
    return success

if __name__ == "__main__":
    test_all_next_buttons()
