#!/usr/bin/env python3
"""
Weryfikacja stanu organizacji plików w ZenDegenAcademy
Sprawdza czy wszystkie pliki są w odpowiednich miejscach
"""

import os
from pathlib import Path

def verify_organization():
    """Sprawdza stan organizacji plików"""
    
    print("🔍 WERYFIKACJA ORGANIZACJI PLIKÓW")
    print("=" * 50)
    
    # Sprawdź obecność kluczowych plików produkcyjnych
    required_files = [
        'main.py',
        'requirements.txt', 
        'start.bat',
        '.gitignore'
    ]
    
    print("\n✅ PLIKI PRODUKCYJNE:")
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - BRAK!")
            all_present = False
    
    # Sprawdź strukturę folderów
    required_folders = [
        'config', 'data', 'utils', 'views', 'pages', 'static', 'assets',
        'docs', 'tests', 'prototypes', 'scripts'
    ]
    
    print("\n📁 STRUKTURA FOLDERÓW:")
    for folder in required_folders:
        if os.path.exists(folder):
            count = len(os.listdir(folder)) if os.path.isdir(folder) else 0
            print(f"✅ {folder}/ ({count} elementów)")
        else:
            print(f"❌ {folder}/ - BRAK!")
            all_present = False
    
    # Statystyki folderów
    folder_stats = {}
    for folder in ['docs', 'tests', 'prototypes', 'scripts']:
        if os.path.exists(folder):
            # Policz pliki w folderze i podfolderach
            count = 0
            for root, dirs, files in os.walk(folder):
                count += len(files)
            folder_stats[folder] = count
    
    print("\n📊 STATYSTYKI ORGANIZACJI:")
    for folder, count in folder_stats.items():
        print(f"📁 {folder}: {count} plików")
    
    # Sprawdź czy nie ma niepotrzebnych plików w root
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    unwanted_patterns = ['test_', 'main_new', 'cleanup_', 'analyze_', 'quick_']
    
    unwanted_in_root = []
    for file in root_files:
        for pattern in unwanted_patterns:
            if file.startswith(pattern):
                unwanted_in_root.append(file)
                break
    
    print("\n🧹 CZYSTOŚĆ ROOT:")
    if unwanted_in_root:
        print("⚠️ Znaleziono pliki które powinny być w podfolderach:")
        for file in unwanted_in_root:
            print(f"  • {file}")
    else:
        print("✅ Katalog główny jest czysty")
    
    # Test funkcjonalności
    print("\n🔧 TEST FUNKCJONALNOŚCI:")
    try:
        import main
        print("✅ main.py - import pomyślny")
    except Exception as e:
        print(f"❌ main.py - błąd importu: {e}")
        all_present = False
    
    # Test przycisków jeśli test istnieje
    if os.path.exists('tests/test_all_next_buttons.py'):
        print("✅ tests/test_all_next_buttons.py - dostępny")
    else:
        print("❌ tests/test_all_next_buttons.py - brak testu przycisków")
    
    # Podsumowanie
    print("\n" + "=" * 50)
    if all_present and not unwanted_in_root:
        print("🎉 ORGANIZACJA KOMPLETNA I POPRAWNA!")
        print("✅ Wszystkie pliki w odpowiednich miejscach")
        print("✅ Aplikacja gotowa do użycia")
    else:
        print("⚠️ WYKRYTO PROBLEMY - WYMAGA UWAGI")
        if not all_present:
            print("❌ Brakuje wymaganych plików/folderów")
        if unwanted_in_root:
            print("❌ Katalog główny zawiera pliki do przeniesienia")
    
    # Instrukcje
    print("\n📋 DOSTĘPNE KOMENDY:")
    print("• streamlit run main.py - uruchom aplikację")
    print("• python tests/test_all_next_buttons.py - test przycisków")
    print("• python scripts/organize_files_auto.py - reorganizuj ponownie")
    
    return all_present and not unwanted_in_root

if __name__ == "__main__":
    verify_organization()
