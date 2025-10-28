"""
Skrypt migracji: ai_conversation → conversation
Aktualizuje wszystkie zapisane dane użytkowników
"""

import json
import os
from datetime import datetime

def migrate_user_data(user_data):
    """Migruje dane pojedynczego użytkownika"""
    changes_made = []
    
    # Sprawdź czy user ma business_games
    if "business_games" not in user_data:
        return changes_made
    
    for industry_id, bg_data in user_data["business_games"].items():
        # Migruj aktywne kontrakty
        if "contracts" in bg_data and "active" in bg_data["contracts"]:
            for contract in bg_data["contracts"]["active"]:
                if contract.get("contract_type") == "ai_conversation":
                    contract["contract_type"] = "conversation"
                    changes_made.append(f"Active contract {contract.get('id', 'unknown')}: ai_conversation → conversation")
        
        # Migruj ukończone kontrakty
        if "contracts" in bg_data and "completed" in bg_data["contracts"]:
            for contract in bg_data["contracts"]["completed"]:
                if contract.get("contract_type") == "ai_conversation":
                    contract["contract_type"] = "conversation"
                    changes_made.append(f"Completed contract {contract.get('id', 'unknown')}: ai_conversation → conversation")
    
    return changes_made

def main():
    """Główna funkcja migracji"""
    users_file = "users_data.json"
    backup_file = f"users_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Sprawdź czy plik istnieje
    if not os.path.exists(users_file):
        print(f"❌ Plik {users_file} nie istnieje!")
        return
    
    print(f"📂 Wczytuję {users_file}...")
    with open(users_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    # Backup
    print(f"💾 Tworzę backup: {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    # Migracja
    print(f"🔄 Migruję dane dla {len(users_data)} użytkowników...")
    total_changes = 0
    
    for username, user_data in users_data.items():
        changes = migrate_user_data(user_data)
        if changes:
            print(f"\n👤 {username}:")
            for change in changes:
                print(f"   ✅ {change}")
            total_changes += len(changes)
    
    if total_changes > 0:
        # Zapisz zmigrowane dane
        print(f"\n💾 Zapisuję zmigrowane dane do {users_file}...")
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Migracja zakończona! Zmieniono {total_changes} kontraktów.")
        print(f"📋 Backup zapisany jako: {backup_file}")
    else:
        print(f"\n✅ Brak zmian - wszystkie kontrakty już używają nowej nomenklatury!")
        # Usuń backup jeśli nie było zmian
        os.remove(backup_file)
        print(f"🗑️ Usunięto niepotrzebny backup.")

if __name__ == "__main__":
    main()
