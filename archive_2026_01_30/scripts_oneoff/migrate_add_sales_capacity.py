"""
🔄 Migration Script: Add sales_capacity to existing FMCG clients

Dodaje parametry sales_capacity do wszystkich klientów którzy ich nie mają.
"""

import json
import os
from utils.fmcg_order_realism import generate_sales_capacity


def migrate_clients_add_sales_capacity():
    """
    Dodaje sales_capacity do wszystkich klientów FMCG którzy go nie mają
    """
    users_file = "users_data.json"
    
    if not os.path.exists(users_file):
        print(f"❌ Plik {users_file} nie istnieje")
        return
    
    print(f"📂 Wczytuję {users_file}...")
    
    # Load users data
    with open(users_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    print(f"✅ Znaleziono {len(users_data)} użytkowników")
    
    total_clients_updated = 0
    total_users_updated = 0
    
    for username, user_data in users_data.items():
        fmcg_clients = user_data.get('fmcg_clients')
        
        if not fmcg_clients:
            continue  # Skip users without FMCG game
        
        print(f"\n📊 Użytkownik: {username}")
        print(f"  Klienci: {len(fmcg_clients)}")
        
        # Update each client
        clients_updated_for_user = 0
        
        for client_id, client_data in fmcg_clients.items():
            # Check if already has sales_capacity
            if client_data.get('sales_capacity'):
                continue  # Skip - already has it
            
            # Generate sales_capacity
            size_sqm = client_data.get('size_sqm', 80)
            client_type = client_data.get('type', 'Sklep osiedlowy')
            
            sales_capacity = generate_sales_capacity(size_sqm, client_type)
            client_data['sales_capacity'] = sales_capacity
            
            clients_updated_for_user += 1
            print(f"    ✅ {client_data.get('name', client_id)}: dodano sales_capacity ({size_sqm} m²)")
        
        if clients_updated_for_user > 0:
            total_clients_updated += clients_updated_for_user
            total_users_updated += 1
            print(f"  💾 Zaktualizowano {clients_updated_for_user} klientów")
        else:
            print(f"  ℹ️ Wszyscy klienci już mają sales_capacity")
    
    # Save back to file
    if total_clients_updated > 0:
        # Create backup first
        backup_file = f"users_data_backup_sales_capacity_{os.path.getmtime(users_file):.0f}.json"
        print(f"\n💾 Tworzę backup: {backup_file}")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        
        # Save updated data
        print(f"💾 Zapisuję zaktualizowane dane do {users_file}...")
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ MIGRACJA ZAKOŃCZONA")
    print(f"{'='*60}")
    print(f"Zaktualizowano użytkowników: {total_users_updated}")
    print(f"Zaktualizowano klientów: {total_clients_updated}")


if __name__ == "__main__":
    print("="*60)
    print("🚀 MIGRACJA: Dodawanie sales_capacity do klientów FMCG")
    print("="*60)
    
    response = input("\n⚠️ Czy chcesz kontynuować migrację? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        migrate_clients_add_sales_capacity()
    else:
        print("❌ Migracja anulowana")
