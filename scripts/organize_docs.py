#!/usr/bin/env python3
"""
Skrypt do organizacji plików markdown w folderze docs/
"""

import os
import shutil
from typing import Dict, List

def organize_markdown_files():
    """Organizuje pliki markdown w odpowiednie foldery"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "docs")
    
    # Mapowanie plików na foldery
    file_mapping = {
        # Planning & Strategy
        "planning": [
            "REFAKTORING_STRATEGICZNY_PLAN.md",
            "GAMIFICATION_ENHANCEMENT_PLAN.md",
            "PODCAST_INTEGRATION_RECOMMENDATION.md",
            "MIND_MAP_IMPLEMENTATION.md",
            "MIND_MAP_QUICK_START.md",
            "MIND_MAP_USER_GUIDE.md",
            "INTERACTIVE_MAP_USER_GUIDE.md",
            "COURSE_MAP_USER_GUIDE.md",
        ],
        
        # Implementation & Features
        "implementation": [
            "BADGE_SYSTEM_STEP3_IMPLEMENTATION.md",
            "MIND_MAP_IMPLEMENTATION_FINAL.md",
            "PRACTICAL_EXERCISES_FINAL_READY.md",
            "SELF_REFLECTION_IMPLEMENTATION_FINAL_STATUS.md",
            "PROMPT_IMPLEMENTACJA_NEUROPRZYWODZTWO.md",
            "PROMPT_NEUROCOIN_SYSTEM_IMPLEMENTATION.md",
            "INTEGRACJA_UMIEJĘTNOŚCI_KOMPLETNA.md",
            "PRZEBUDOWA_APLIKACJI_KOMPLETNA.md",
        ],
        
        # Fixes & Bug Reports
        "fixes": [
            "APPLICATION_IMPORT_ERRORS_FIXED.md",
            "CIRCULAR_IMPORT_FIX_COMPLETE.md",
            "COURSE_MAP_BUGS_FIXED.md",
            "COURSE_MAP_RESPONSIVE_COLORS_FIXED.md",
            "DEGEN_FIX_FINAL_VERIFICATION.md",
            "DOUBLE_CLICK_PROBLEM_SOLVED_FINAL.md",
            "EKSPLORATOR_USUNIETY_RAPORT.md",
            "HTML_MARKDOWN_FIX_FINAL_STATUS.md",
            "LESSON_COMPLETION_FIX_SUMMARY.md",
            "LESSON_IMPORT_ERROR_FIXED.md",
            "MAIN_NEW_FIXED_FINAL_STATUS.md",
            "MERGE_CONFLICTS_FIXED.md",
            "MISSION_MANAGER_IMPORT_ERROR_FIXED.md",
            "NAUKA_SECTION_FIX_COMPLETE.md",
            "NAVIGATION_REFACTOR_COMPLETE.md",
            "PROGRESS_BAR_UPDATE_SUMMARY.md",
            "SHOP_BOOSTER_ERROR_FIX_COMPLETE.md",
            "SHOP_FIX_AND_CLEANUP_COMPLETE.md",
            "STREAMLIT_AGRAPH_PROBLEM_SOLVED.md",
            "TIMESTAMP_FIX_FINAL_STATUS.md",
            "XP_FIXES_COMPLETION_SUMMARY.md",
            "RESTORE_COMMIT_37f5584.md",
        ],
        
        # Status & Summaries
        "status": [
            "BADGE_SYSTEM_VERIFICATION_FINAL.md",
            "CLEANUP_ANALYSIS.md",
            "CLEANUP_FINAL_STATUS.md",
            "CLEANUP_SUMMARY.md",
            "FINAL_COMPLETION_SUMMARY.md",
            "REFACTORING_SUMMARY.md",
            "TABS_TESTING_INSTRUCTIONS.md",
            "TRANSFORMATION_COMPLETE_STATUS.md",
            "TRANSFORMATION_FINAL_STATUS.md",
        ]
    }
    
    moved_files = []
    errors = []
    
    print("📁 Organizowanie plików markdown...")
    print("=" * 50)
    
    for folder_name, file_list in file_mapping.items():
        folder_path = os.path.join(docs_dir, folder_name)
        
        for filename in file_list:
            source_path = os.path.join(base_dir, filename)
            dest_path = os.path.join(folder_path, filename)
            
            if os.path.exists(source_path):
                try:
                    shutil.move(source_path, dest_path)
                    moved_files.append(f"{filename} → docs/{folder_name}/")
                    print(f"✅ Przeniesiono: {filename} → docs/{folder_name}/")
                except Exception as e:
                    errors.append(f"Błąd przy {filename}: {e}")
                    print(f"❌ Błąd: {filename} - {e}")
            else:
                print(f"⚠️  Nie znaleziono: {filename}")
    
    # Znajdź pozostałe pliki MD w katalogu głównym
    remaining_md_files = []
    for file in os.listdir(base_dir):
        if file.endswith('.md') and os.path.isfile(os.path.join(base_dir, file)):
            remaining_md_files.append(file)
    
    if remaining_md_files:
        print("\n📋 Pozostałe pliki MD do ręcznego sprawdzenia:")
        for file in remaining_md_files:
            print(f"   - {file}")
    
    print("\n" + "=" * 50)
    print("📊 PODSUMOWANIE ORGANIZACJI")
    print("=" * 50)
    print(f"✅ Przeniesiono plików: {len(moved_files)}")
    print(f"❌ Błędów: {len(errors)}")
    print(f"📝 Pozostałych plików MD: {len(remaining_md_files)}")
    
    # Stwórz README.md w folderze docs
    create_docs_readme(docs_dir)
    
    return moved_files, errors, remaining_md_files

def create_docs_readme(docs_dir):
    """Tworzy README.md w folderze docs z opisem struktury"""
    
    readme_content = """# Dokumentacja ZenDegenAcademy

Ten folder zawiera całą dokumentację projektu ZenDegenAcademy, zorganizowaną w logiczne kategorie.

## 📁 Struktura dokumentacji

### `/planning/` - Planowanie i strategia
- Plany strategiczne refaktoringu
- Plany implementacji nowych funkcji
- Przewodniki użytkownika
- Dokumentacja architektury

### `/implementation/` - Implementacja i funkcje
- Dokumentacja implementacji nowych systemów
- Opisy zaimplementowanych funkcji
- Integracje systemów
- Transformacje aplikacji

### `/fixes/` - Naprawy i poprawki
- Raporty napraw błędów
- Dokumentacja rozwiązanych problemów
- Refaktoringi kodu
- Import fixes i aktualizacje

### `/status/` - Status i podsumowania
- Statusy projektów
- Podsumowania prac
- Analizy i weryfikacje
- Instrukcje testowania

## 📋 Jak korzystać z dokumentacji

1. **Dla deweloperów**: Sprawdź `/planning/` dla architektury i `/implementation/` dla szczegółów technicznych
2. **Dla QA**: Zobacz `/fixes/` dla historii błędów i `/status/` dla statusów projektów
3. **Dla PM**: Przejrzyj `/status/` dla podsumowań i `/planning/` dla roadmap

## 🔍 Wyszukiwanie dokumentacji

Używaj funkcji wyszukiwania w IDE lub:
```bash
grep -r "szukany_tekst" docs/
```

---
*Dokumentacja automatycznie zorganizowana - 2025-06-22*
"""
    
    readme_path = os.path.join(docs_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📄 Utworzono: docs/README.md")

if __name__ == "__main__":
    print("🗂️  ZenDegenAcademy - Organizacja dokumentacji")
    print("=" * 50)
    
    moved, errors, remaining = organize_markdown_files()
    
    if remaining:
        print("\n💡 Sugestie dla pozostałych plików:")
        for file in remaining:
            if "CLEANUP" in file.upper():
                print(f"   {file} → docs/status/")
            elif "PLAN" in file.upper() or "STRATEGY" in file.upper():
                print(f"   {file} → docs/planning/")
            elif "FIX" in file.upper() or "ERROR" in file.upper():
                print(f"   {file} → docs/fixes/")
            else:
                print(f"   {file} → docs/status/ (default)")
    
    print("\n✨ Organizacja dokumentacji zakończona!")
    print(f"📁 Sprawdź folder docs/ dla uporządkowanej dokumentacji")
