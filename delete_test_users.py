"""
Skrypt do usuwania testowych użytkowników z users_data.json
Zachowuje tylko realnych użytkowników
"""

import json
from datetime import datetime
import shutil

# Lista realnych użytkowników do zachowania
KEEP_USERS = {
    # Tylko prawdziwi użytkownicy (3 osoby)
    'admin', 'Piotr', 'Pawel'
}

def delete_test_users(dry_run=True):
    """
    Usuwa testowych użytkowników z users_data.json
    
    Args:
        dry_run: Jeśli True, tylko pokazuje co zostanie usunięte (bez zmian)
    """
    
    # 1. Backup
    if not dry_run:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"users_data_backup_before_cleanup_{timestamp}.json"
        shutil.copy("users_data.json", backup_file)
        print(f"✅ Backup utworzony: {backup_file}")
    
    # 2. Wczytaj dane
    with open("users_data.json", "r", encoding="utf-8") as f:
        users_data = json.load(f)
    
    # 3. Identyfikuj użytkowników do usunięcia
    all_users = set(users_data.keys())
    to_delete = all_users - KEEP_USERS
    
    print(f"\n{'='*60}")
    print(f"📊 ANALIZA UŻYTKOWNIKÓW")
    print(f"{'='*60}")
    print(f"Wszyscy użytkownicy: {len(all_users)}")
    print(f"Do zachowania: {len(KEEP_USERS)}")
    print(f"Do usunięcia: {len(to_delete)}")
    
    print(f"\n{'='*60}")
    print(f"✅ ZACHOWANI UŻYTKOWNICY ({len(KEEP_USERS)}):")
    print(f"{'='*60}")
    for user in sorted(KEEP_USERS):
        if user in all_users:
            print(f"  ✓ {user}")
        else:
            print(f"  ⚠️  {user} (nie istnieje w bazie)")
    
    print(f"\n{'='*60}")
    print(f"🗑️  UŻYTKOWNICY DO USUNIĘCIA ({len(to_delete)}):")
    print(f"{'='*60}")
    for user in sorted(to_delete):
        print(f"  ✗ {user}")
    
    # 4. Usuń (jeśli nie dry-run)
    if dry_run:
        print(f"\n{'='*60}")
        print(f"ℹ️  DRY-RUN MODE - Nie wprowadzono zmian")
        print(f"{'='*60}")
        print(f"Aby faktycznie usunąć, uruchom:")
        print(f"  python delete_test_users.py --delete")
        return
    
    # Usuń użytkowników
    for user in to_delete:
        del users_data[user]
    
    # 5. Zapisz
    with open("users_data.json", "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ GOTOWE - Usunięto {len(to_delete)} testowych użytkowników")
    print(f"{'='*60}")
    print(f"Pozostało: {len(users_data)} użytkowników")
    print(f"Backup: {backup_file}")


if __name__ == "__main__":
    import sys
    
    # Sprawdź flagę --delete
    if "--delete" in sys.argv:
        print("⚠️  TRYB USUWANIA - Wprowadzane będą zmiany!")
        confirm = input("Czy na pewno chcesz usunąć testowych użytkowników? (tak/nie): ")
        if confirm.lower() == "tak":
            delete_test_users(dry_run=False)
        else:
            print("❌ Anulowano")
    else:
        # Domyślnie dry-run
        delete_test_users(dry_run=True)
