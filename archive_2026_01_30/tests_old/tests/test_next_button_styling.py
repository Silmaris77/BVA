#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test sprawdzający czy przyciski "Dalej: Podsumowanie" mają jednolity styl z przyciskami nawigacji poziomej.
"""

import re

def test_next_button_styling():
    """Sprawdź czy CSS dla przycisków 'Dalej' jest spójny z nawigacją poziomą."""
    
    # Wczytaj plik lesson.py
    with open('views/lesson.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 Sprawdzanie stylowania przycisków 'Dalej'...")
    
    # 1. Sprawdź czy istnieje CSS dla .next-button .stButton > button
    next_button_css_pattern = r'\.next-button\s+\.stButton\s*>\s*button\s*\{'
    has_next_button_css = bool(re.search(next_button_css_pattern, content))
    
    print(f"✅ CSS dla przycisków 'Dalej': {'ZNALEZIONO' if has_next_button_css else '❌ BRAK'}")
    
    # 2. Sprawdź czy używany jest zen_button zamiast st.button dla zablokowanych przycisków
    disabled_button_pattern = r'zen_button\(\s*f"🔒 Dalej:'
    has_zen_button_disabled = bool(re.search(disabled_button_pattern, content))
    
    print(f"✅ Użycie zen_button dla zablokowanych przycisków: {'TAK' if has_zen_button_disabled else '❌ NIE'}")
    
    # 3. Sprawdź czy nie ma już starych st.button dla zablokowanych przycisków
    old_disabled_pattern = r'st\.button\(\s*f"🔒 Dalej:'
    has_old_disabled = bool(re.search(old_disabled_pattern, content))
    
    print(f"✅ Brak starych st.button dla zablokowanych przycisków: {'TAK' if not has_old_disabled else '❌ NIE, WCIĄŻ SĄ'}")
    
    # 4. Sprawdź czy CSS dla next-button ma podobną szerokość do przycisków nawigacji
    width_pattern = r'\.next-button\s+\.stButton\s*>\s*button[^}]*width:\s*200px'
    has_consistent_width = bool(re.search(width_pattern, content))
    
    print(f"✅ Jednolita szerokość przycisków (200px): {'TAK' if has_consistent_width else '❌ NIE'}")
    
    # 5. Sprawdź czy CSS dla next-button ma wysokość 48px (jak przyciski nawigacji)
    height_pattern = r'\.next-button\s+\.stButton\s*>\s*button[^}]*height:\s*48px'
    has_consistent_height = bool(re.search(height_pattern, content))
    
    print(f"✅ Jednolita wysokość przycisków (48px): {'TAK' if has_consistent_height else '❌ NIE'}")
    
    # Podsumowanie
    all_checks = [
        has_next_button_css,
        has_zen_button_disabled,
        not has_old_disabled,
        has_consistent_width,
        has_consistent_height
    ]
    
    passed = sum(all_checks)
    total = len(all_checks)
    
    print(f"\n📊 Wynik: {passed}/{total} sprawdzeń przeszło pomyślnie")
    
    if passed == total:
        print("🎉 Wszystkie sprawdzenia przeszły! Przyciski 'Dalej' powinny mieć spójny styl z nawigacją poziomą.")
        return True
    else:
        print("⚠️ Niektóre sprawdzenia nie przeszły. Sprawdź powyższe szczegóły.")
        return False

if __name__ == "__main__":
    test_next_button_styling()
