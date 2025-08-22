#!/usr/bin/env python3
"""
Skrypt do naprawy uszkodzonych emoji w views/lesson.py
"""

import os
import re

def fix_emoji_in_lesson_view():
    """Naprawia uszkodzone emoji w pliku views/lesson.py"""
    
    file_path = "views/lesson.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Błąd: Nie znaleziono pliku {file_path}")
        return False
    
    # Wczytaj plik
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Lista zamian emoji
    emoji_replacements = [
        ('available_tabs.append("� Quiz końcowy")', 'available_tabs.append("🎓 Quiz końcowy")'),
        ('available_tabs.append("� Zadania Praktyczne")', 'available_tabs.append("🚀 Zadania Praktyczne")'),
        # Dodatkowe wzorce jeśli potrzebne
    ]
    
    # Wykonaj zamiany
    modified = False
    for old_pattern, new_pattern in emoji_replacements:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            modified = True
            print(f"✅ Naprawiono: {old_pattern} → {new_pattern}")
    
    if modified:
        # Zapisz naprawiony plik
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Zapisano naprawiony plik: {file_path}")
        return True
    else:
        print("ℹ️ Nie znaleziono uszkodzonych emoji do naprawy")
        return False

def main():
    """Główna funkcja"""
    print("🔧 NAPRAWA USZKODZONYCH EMOJI W VIEWS/LESSON.PY")
    print("=" * 50)
    
    success = fix_emoji_in_lesson_view()
    
    if success:
        print("\n✅ NAPRAWA ZAKOŃCZONA POMYŚLNIE")
        print("🚀 Emoji zostały naprawione - sekcja Praktyka powinna teraz działać poprawnie")
    else:
        print("\n❌ NAPRAWA NIE BYŁA POTRZEBNA LUB SIĘ NIE POWIODŁA")
    
    return success

if __name__ == "__main__":
    main()
