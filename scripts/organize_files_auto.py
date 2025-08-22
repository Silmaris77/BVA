#!/usr/bin/env python3
"""
Automatyczna organizacja plików w projekcie ZenDegenAcademy
Przenosi pliki do odpowiednich folderów zgodnie z analizą
"""

import os
import shutil
from pathlib import Path
import glob

def create_folders():
    """Tworzy potrzebne foldery jeśli nie istnieją"""
    folders_to_create = [
        'tests',
        'scripts', 
        'docs/fixes',
        'docs/status',
        'docs/analysis',
        'prototypes/archived-main-versions'
    ]
    
    for folder in folders_to_create:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"📁 Folder: {folder}")

def move_documentation_files():
    """Przenosi pliki dokumentacji do docs/"""
    
    # Pliki z fiksami i kompletami
    fix_patterns = [
        '*_COMPLETE.md',
        '*_FIX*.md', 
        'CIRCULAR_IMPORT_*.md',
        'HTML_PANEL_*.md',
        'INSPIRATIONS_*.md',
        'INTEGRACJA_*.md',
        'LESSON_*.md',
        'NAVIGATION_*.md',
        'NEXT_BUTTON_*.md',
        'PANEL_XP_*.md',
        'QUIZ_*.md',
        'READ_STATUS_*.md',
        'REPEAT_*.md',
        'SHOP_*.md',
        'KEYERROR_*.md'
    ]
    
    # Pliki ze statusami i analizami
    status_patterns = [
        '*_STATUS.md',
        '*_ANALYSIS.md',
        'CLEANUP_*.md',
        'MAIN_NEW_*.md',
        'MERGE_*.md',
        'MISSION_*.md',
        'PRZEBUDOWA_*.md',
        'REFAKTORING_*.md',
        'RESTORE_*.md',
        'TRANSFORMATION_*.md'
    ]
    
    moved_count = 0
    
    # Przenieś pliki fix
    for pattern in fix_patterns:
        for file in glob.glob(pattern):
            if os.path.isfile(file):
                try:
                    shutil.move(file, f'docs/fixes/{file}')
                    print(f"📄 {file} → docs/fixes/")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Błąd przenoszenia {file}: {e}")
    
    # Przenieś pliki status
    for pattern in status_patterns:
        for file in glob.glob(pattern):
            if os.path.isfile(file):
                try:
                    shutil.move(file, f'docs/status/{file}')
                    print(f"📄 {file} → docs/status/")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Błąd przenoszenia {file}: {e}")
    
    return moved_count

def move_test_files():
    """Przenosi pliki testowe do tests/"""
    moved_count = 0
    
    for file in glob.glob('test_*.py'):
        if os.path.isfile(file):
            try:
                shutil.move(file, f'tests/{file}')
                print(f"🧪 {file} → tests/")
                moved_count += 1
            except Exception as e:
                print(f"❌ Błąd przenoszenia {file}: {e}")
    
    return moved_count

def move_prototype_files():
    """Przenosi pliki prototypowe do prototypes/"""
    moved_count = 0
    
    # HTML prototypes
    html_patterns = [
        '*prototype*.html',
        '*proposal*.html', 
        '*layout*.html',
        'mobile_*.html'
    ]
    
    for pattern in html_patterns:
        for file in glob.glob(pattern):
            if os.path.isfile(file):
                try:
                    shutil.move(file, f'prototypes/{file}')
                    print(f"🛠️ {file} → prototypes/")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Błąd przenoszenia {file}: {e}")
    
    # Alternatywne pliki main (jeśli nie są używane)
    main_alternatives = [
        'main_new.py',
        'main_new_fixed.py', 
        'main_new_clean.py',
        'launch_app.py',
        'launch_new_app.py'
    ]
    
    for file in main_alternatives:
        if os.path.isfile(file):
            # Sprawdź czy plik jest pusty lub nieużywany
            if os.path.getsize(file) == 0:
                print(f"🗑️ Usuwam pusty plik: {file}")
                os.remove(file)
            else:
                try:
                    shutil.move(file, f'prototypes/archived-main-versions/{file}')
                    print(f"🛠️ {file} → prototypes/archived-main-versions/")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Błąd przenoszenia {file}: {e}")
    
    return moved_count

def move_script_files():
    """Przenosi skrypty pomocnicze do scripts/"""
    moved_count = 0
    
    script_patterns = [
        '*cleanup*.py',
        '*organize*.py',
        'analyze_*.py',
        'execute_*.py',
        'validate_*.py',
        'verify_*.py',
        'quick_*.py',
        'simple_*.py',
        'remove_*.py',
        '*.ps1'
    ]
    
    # Wyjątki - pliki które zostają w root
    exceptions = [
        'analyze_files_organization.py',  # ten skrypt
        'main.py'  # główny plik aplikacji
    ]
    
    for pattern in script_patterns:
        for file in glob.glob(pattern):
            if os.path.isfile(file) and file not in exceptions:
                try:
                    shutil.move(file, f'scripts/{file}')
                    print(f"⚙️ {file} → scripts/")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Błąd przenoszenia {file}: {e}")
    
    return moved_count

def cleanup_empty_files():
    """Usuwa puste lub niepotrzebne pliki"""
    deleted_count = 0
    
    # Sprawdź i usuń puste pliki
    for file in os.listdir('.'):
        if os.path.isfile(file) and file.endswith('.py'):
            if os.path.getsize(file) == 0:
                print(f"🗑️ Usuwam pusty plik: {file}")
                os.remove(file)
                deleted_count += 1
    
    return deleted_count

def create_readme_files():
    """Tworzy pliki README w nowych folderach"""
    
    readme_content = {
        'tests/README.md': """# 🧪 Testy Automatyczne

Ten folder zawiera testy automatyczne dla aplikacji ZenDegenAcademy.

## Uruchamianie testów

```bash
# Uruchom wszystkie testy
python -m pytest tests/

# Uruchom konkretny test
python tests/test_nazwa.py
```

## Typy testów

- `test_*_navigation.py` - Testy nawigacji
- `test_*_button*.py` - Testy przycisków
- `test_*_quiz*.py` - Testy quizów
- `test_*_shop*.py` - Testy sklepu
""",
        
        'scripts/README.md': """# ⚙️ Skrypty Pomocnicze

Ten folder zawiera skrypty pomocnicze dla rozwoju i utrzymania aplikacji.

## Kategorie skryptów

### Cleanup & Organizacja
- `cleanup_*.py` - Skrypty porządkujące kod
- `organize_*.py` - Skrypty organizujące strukturę

### Analiza & Walidacja  
- `analyze_*.py` - Skrypty analizujące kod
- `validate_*.py` - Skrypty walidacyjne
- `verify_*.py` - Skrypty weryfikacyjne

### Szybkie testy
- `quick_*.py` - Szybkie testy funkcjonalności
- `simple_*.py` - Proste skrypty testowe

### PowerShell
- `*.ps1` - Skrypty PowerShell dla Windows
""",
        
        'prototypes/archived-main-versions/README.md': """# 📦 Zarchiwizowane Wersje Main

Ten folder zawiera alternatywne/historyczne wersje pliku main.py.

⚠️ **Uwaga:** Te pliki nie są używane w produkcji. Główny plik to `main.py` w katalogu root.

## Pliki

- `main_new.py` - Nowa wersja (nieukończona)
- `main_new_fixed.py` - Poprawiona wersja (nieukończona)  
- `main_new_clean.py` - Oczyszczona wersja (nieukończona)
- `launch_*.py` - Alternatywne launchery
"""
    }
    
    for file_path, content in readme_content.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📝 Utworzono: {file_path}")

def main():
    """Główna funkcja organizująca pliki"""
    
    print("🚀 ROZPOCZYNAM ORGANIZACJĘ PLIKÓW")
    print("=" * 50)
    
    # Sprawdź czy jesteśmy w katalogu głównym
    if not os.path.exists('main.py'):
        print("❌ Błąd: Uruchom skrypt z katalogu głównego projektu")
        return
    
    # Krok 1: Utwórz foldery
    print("\n📁 TWORZENIE FOLDERÓW...")
    create_folders()
    
    # Krok 2: Przenieś dokumentację
    print("\n📚 PRZENOSZENIE DOKUMENTACJI...")
    docs_moved = move_documentation_files()
    
    # Krok 3: Przenieś testy
    print("\n🧪 PRZENOSZENIE TESTÓW...")
    tests_moved = move_test_files()
    
    # Krok 4: Przenieś prototypy
    print("\n🛠️ PRZENOSZENIE PROTOTYPÓW...")
    prototypes_moved = move_prototype_files()
    
    # Krok 5: Przenieś skrypty
    print("\n⚙️ PRZENOSZENIE SKRYPTÓW...")
    scripts_moved = move_script_files()
    
    # Krok 6: Wyczyść puste pliki
    print("\n🗑️ USUWANIE PUSTYCH PLIKÓW...")
    deleted_count = cleanup_empty_files()
    
    # Krok 7: Utwórz README
    print("\n📝 TWORZENIE README...")
    create_readme_files()
    
    # Podsumowanie
    print("\n" + "=" * 50)
    print("✅ ORGANIZACJA ZAKOŃCZONA")
    print(f"📚 Dokumentacja przeniesiona: {docs_moved} plików")
    print(f"🧪 Testy przeniesione: {tests_moved} plików")
    print(f"🛠️ Prototypy przeniesione: {prototypes_moved} plików") 
    print(f"⚙️ Skrypty przeniesione: {scripts_moved} plików")
    print(f"🗑️ Usunięte pliki: {deleted_count}")
    
    total_moved = docs_moved + tests_moved + prototypes_moved + scripts_moved + deleted_count
    print(f"📊 Łącznie przetworzono: {total_moved} plików")
    
    print("\n🎯 NASTĘPNE KROKI:")
    print("1. Uruchom aplikację: streamlit run main.py")
    print("2. Sprawdź czy wszystko działa")
    print("3. Zcommituj zmiany do Git")

if __name__ == "__main__":
    main()
