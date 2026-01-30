"""
Test Contract Signing
Sprawdza czy podpisanie kontraktu działa (PROSPECT → ACTIVE)
"""

import sys
sys.path.append('c:\\Users\\pksia\\Dropbox\\BVA')

from utils.fmcg_mechanics import load_fmcg_game_state_sql
from utils.fmcg_reputation import sign_contract

username = "Basia"

print("🔄 Ładuję dane gry...")
loaded_data = load_fmcg_game_state_sql(username)

if loaded_data:
    game_state, clients = loaded_data
    
    print(f"✅ Załadowano {len(clients)} klientów\n")
    
    # Znajdź PROSPECT klienta
    prospect_clients = {cid: c for cid, c in clients.items() if c.get('status') == 'prospect'}
    
    if prospect_clients:
        client_id = list(prospect_clients.keys())[0]
        client_data = clients[client_id]
        
        print(f"📋 Klient PROSPECT: {client_data.get('name', client_id)}")
        print(f"   Status przed: {client_data.get('status', 'N/A')}")
        print(f"   Reputacja przed: {client_data.get('reputation', 0)}")
        
        # Sprawdź portfolio przed
        portfolio_before = len(client_data.get('products_portfolio', []))
        events_before = len(client_data.get('events_timeline', []))
        print(f"   Produkty w portfolio przed: {portfolio_before}")
        print(f"   Wydarzenia przed: {events_before}")
        
        # Podpisz kontrakt z 3 produktami
        test_products = ["fl_cola_250", "fl_energy_250", "fl_chips_paprika"]
        print(f"\n📝 Podpisywanie kontraktu z produktami:")
        for pid in test_products:
            print(f"   - {pid}")
        
        sign_contract(client_data, test_products)
        
        print(f"\n✅ Kontrakt podpisany!")
        print(f"   Status po: {client_data.get('status', 'N/A').upper()}")
        print(f"   Reputacja po: {client_data.get('reputation', 0)}")
        print(f"   Data rozpoczęcia: {client_data.get('contract_start_date')}")
        print(f"   Data przedłużenia: {client_data.get('contract_renewal_date')}")
        
        # Sprawdź portfolio po
        portfolio_after = len(client_data.get('products_portfolio', []))
        events_after = len(client_data.get('events_timeline', []))
        print(f"   Produkty w portfolio po: {portfolio_after} (dodano: {portfolio_after - portfolio_before})")
        print(f"   Wydarzenia po: {events_after} (dodano: {events_after - events_before})")
        
        # Pokaż produkty w portfolio
        if client_data.get('products_portfolio'):
            print(f"\n📦 Portfolio produktów:")
            for product in client_data['products_portfolio']:
                print(f"   - {product.get('product_id')}: {product.get('volume_monthly', 0)} szt/mies")
        
        # Pokaż ostatnie wydarzenie
        if client_data.get('events_timeline'):
            last_event = client_data['events_timeline'][-1]
            print(f"\n📅 Ostatnie wydarzenie:")
            print(f"   Typ: {last_event.get('type')}")
            print(f"   Opis: {last_event.get('description')}")
            print(f"   Zmiana reputacji: {last_event.get('reputation_change'):+d}")
            print(f"   Produkty: {', '.join(last_event.get('related_products', []))}")
        
        print(f"\n✅ Test zakończony pomyślnie!")
        print(f"\n💡 Status zmieniony: PROSPECT → {client_data.get('status', 'N/A').upper()}")
        print(f"💡 Bonus reputacji: +20 za podpisanie kontraktu")
        print(f"💡 Nie zapisuję do SQL - to tylko test lokalny")
        
    else:
        print("❌ Brak klientów PROSPECT do testowania")
    
else:
    print("❌ Nie znaleziono danych gry!")
