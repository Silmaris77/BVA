"""
Skrypt do aktualizacji importów z data.users na data.users_new
Zastępuje stare importy w plikach produkcyjnych

Author: Migration Script
Date: 2025
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# Pliki do zaktualizowania (produkcyjne)
PRODUCTION_FILES = [
    "main.py",
    "views/business_games.py",
    "views/admin.py", 
    "views/dashboard.py",
    "utils/activity_tracker.py"
]

# Wzorce do zastąpienia
PATTERNS = [
    (r'from data\.users import', 'from data.users_new import'),
    (r'from data import users', 'from data import users_new as users'),
    (r'import data\.users', 'import data.users_new as data.users')
]

def backup_file(filepath):
    """Tworzy kopię zapasową pliku"""
    backup_dir = Path("temp/import_backups")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = Path(filepath).name
    backup_path = backup_dir / f"{filename}.{timestamp}.bak"
    
    shutil.copy2(filepath, backup_path)
    print(f"  ✅ Backup: {backup_path}")
    return backup_path

def update_file(filepath):
    """Aktualizuje importy w pliku"""
    print(f"\n📝 Aktualizuję: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"  ⚠️  Plik nie istnieje!")
        return False
    
    # Backup
    backup_path = backup_file(filepath)
    
    # Wczytaj zawartość
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = 0
    
    # Zastąp wszystkie wzorce
    for old_pattern, new_pattern in PATTERNS:
        matches = re.findall(old_pattern, content)
        if matches:
            content = re.sub(old_pattern, new_pattern, content)
            changes += len(matches)
            print(f"  🔄 Zastąpiono: {old_pattern} -> {new_pattern} ({len(matches)}x)")
    
    if changes == 0:
        print(f"  ℹ️  Brak zmian")
        return True
    
    # Zapisz zaktualizowaną zawartość
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Zapisano {changes} zmian")
    
    # Weryfikacja składni Python
    try:
        compile(content, filepath, 'exec')
        print(f"  ✅ Składnia poprawna")
    except SyntaxError as e:
        print(f"  ❌ BŁĄD SKŁADNI: {e}")
        # Przywróć z backupu
        shutil.copy2(backup_path, filepath)
        print(f"  ↩️  Przywrócono z backupu")
        return False
    
    return True

def main():
    """Główna funkcja"""
    print("🚀 AKTUALIZACJA IMPORTÓW: data.users -> data.users_new")
    print("=" * 60)
    
    base_dir = Path(__file__).parent.parent.parent
    os.chdir(base_dir)
    
    success_count = 0
    fail_count = 0
    
    for filepath in PRODUCTION_FILES:
        if update_file(filepath):
            success_count += 1
        else:
            fail_count += 1
    
    # Podsumowanie
    print("\n" + "=" * 60)
    print("📊 PODSUMOWANIE")
    print("=" * 60)
    print(f"✅ Zaktualizowano: {success_count} plików")
    print(f"❌ Błędy: {fail_count} plików")
    
    if fail_count == 0:
        print("\n🎉 Wszystkie importy zaktualizowane pomyślnie!")
        print("📁 Backupy w: temp/import_backups/")
        print("\n⚠️  NASTĘPNE KROKI:")
        print("1. Uruchom aplikację: streamlit run main.py")
        print("2. Przetestuj podstawowe funkcje (login, dashboard)")
        print("3. Przetestuj business games")
        print("4. Sprawdź czy dual-write działa (sprawdź JSON i SQL)")
    else:
        print("\n⚠️  Wystąpiły błędy - sprawdź logi powyżej")
        print("📁 Pliki przywrócone z backupów")
    
    return fail_count == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
