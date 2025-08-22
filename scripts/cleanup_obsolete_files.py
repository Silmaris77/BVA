#!/usr/bin/env python3
"""
Skrypt do usuwania nieużywanych/przestarzałych plików w ZenDegenAcademy
"""

import os
import shutil
from typing import List

def cleanup_obsolete_files():
    """Usuwa pliki oznaczone jako przestarzałe, testy i pomocnicze skrypty"""
    
    # Lista plików do usunięcia
    files_to_remove = [
        # Pliki deprecated
        "views/degen_explorer_deprecated.py",
        
        # Pliki backup  
        "data/users_backup.py",
        
        # Pliki fix_*
        "views/fix_polish_chars.py",
        "fix_streamlit_agraph.py", 
        "fix_recent_activities.py",
        "fix_files.py",
        
        # Pliki test_*
        "test_shop_view.py",
        "test_shop_fix.py", 
        "test_navigation_fix.py",
        "test_main_new_fixed.py",
        "test_eksplorator_removal.py",
        
        # Inne pliki testowe
        "simple_test.py",
        "simple_import_test.py",
        "quick_booster_test.py",
        "live_self_reflection_test.py",
        "keyerror_fix_test.py",
        "final_test.py",
        "final_streamlit_agraph_test.py",
        "end_to_end_test.py",
        "comprehensive_test.py",
        "comprehensive_practical_exercises_test.py",
        "avatar_test.py",
        "alternative_tabs_test.py",
        "admin_test.py",
        
        # Pliki cleanup (po wykonaniu tego skryptu nie będą już potrzebne)
        "execute_cleanup.py",
        "cleanup_files.py",
        "analyze_cleanup.py",
        
        # Skrypty PowerShell
        "fix_merge_conflicts.ps1",
        "cleanup_files.ps1",
        
        # Pliki diagnostyczne
        "diagnostyka_eksplorator.py",
        
        # Pliki weryfikacji (po zakończeniu refaktoringu)
        "manual_verification.py",
        "final_verification_summary.py",
        "final_color_verification.py",
        "final_fix_verification.py",
        "final_mind_map_verification.py",
        "final_practical_verification.py",
        "final_self_reflection_verification.py",
        "IMPLEMENTATION_VERIFICATION.py",
        
        # Pliki launch alternatywne (zostawiamy tylko main.py)
        "launch_app.py",
        "launch_new_app.py",
        "main_new.py",
        "main_new_fixed.py",
        
        # Inne pomocnicze
        "initialize_degencoins.py",
        "award_missing_badges.py",
    ]
    
    # Pliki które mogą zawierać użyteczne dane (sprawdzimy przed usunięciem)
    files_to_check = [
        "views/degen_test.py",  # może być używane w main.py
    ]
    
    # Katalog główny aplikacji
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    removed_files = []
    kept_files = []
    missing_files = []
    
    print("🧹 Rozpoczynam czyszczenie przestarzałych plików...")
    print("=" * 60)
    
    for file_path in files_to_remove:
        full_path = os.path.join(base_dir, file_path)
        
        if os.path.exists(full_path):
            try:
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    removed_files.append(file_path)
                    print(f"✅ Usunięto: {file_path}")
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    removed_files.append(file_path)
                    print(f"✅ Usunięto katalog: {file_path}")
            except Exception as e:
                print(f"❌ Błąd podczas usuwania {file_path}: {e}")
        else:
            missing_files.append(file_path)
            print(f"⚠️  Plik nie istnieje: {file_path}")
    
    print("\n" + "=" * 60)
    print("📊 PODSUMOWANIE CZYSZCZENIA")
    print("=" * 60)
    print(f"✅ Usunięto plików: {len(removed_files)}")
    print(f"⚠️  Plików nie znaleziono: {len(missing_files)}")
    
    if removed_files:
        print(f"\n📁 Usunięte pliki:")
        for file_path in removed_files:
            print(f"   - {file_path}")
    
    if missing_files:
        print(f"\n🔍 Pliki nie znalezione:")
        for file_path in missing_files:
            print(f"   - {file_path}")
    
    print("\n" + "=" * 60)
    print("🔍 SPRAWDZANIE PLIKÓW DO ROZWAŻENIA")
    print("=" * 60)
    
    for file_path in files_to_check:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"📋 Plik do ręcznego sprawdzenia: {file_path}")
            print(f"   Ścieżka: {full_path}")
        else:
            print(f"⚠️  Plik nie istnieje: {file_path}")
    
    return removed_files, missing_files

def check_remaining_structure():
    """Sprawdza strukturę po czyszczeniu"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    important_files = [
        "main.py",
        "views/dashboard.py",
        "views/profile.py",
        "views/lesson.py", 
        "views/skills.py",
        "views/shop.py",
        "utils/components.py",
        "utils/session.py",
        "utils/new_navigation.py",
        "data/users.py",
        "data/test_questions.py",
        "config/settings.py"
    ]
    
    print("\n" + "=" * 60)
    print("🔍 SPRAWDZANIE KLUCZOWYCH PLIKÓW")
    print("=" * 60)
    
    all_good = True
    for file_path in important_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ BRAKUJE: {file_path}")
            all_good = False
    
    if all_good:
        print("\n🎉 Wszystkie kluczowe pliki są na miejscu!")
    else:
        print("\n⚠️  Uwaga: Brakuje niektórych kluczowych plików!")
    
    return all_good

if __name__ == "__main__":
    print("🚀 ZenDegenAcademy - Czyszczenie przestarzałych plików")
    print("=" * 60)
    
    # Wykonaj czyszczenie
    removed, missing = cleanup_obsolete_files()
    
    # Sprawdź strukturę
    structure_ok = check_remaining_structure()
    
    print("\n" + "=" * 60)
    print("✨ CZYSZCZENIE ZAKOŃCZONE")
    print("=" * 60)
    
    if structure_ok:
        print("🎯 Projekt jest gotowy do dalszego refaktoringu!")
        print("📋 Następne kroki:")
        print("   1. Sprawdź czy aplikacja uruchamia się poprawnie")
        print("   2. Usuń referencje do degen_test z main.py i session.py")
        print("   3. Rozpocznij modularyzację zgodnie z planem strategicznym")
    else:
        print("⚠️  Sprawdź brakujące pliki przed kontynuowaniem!")
