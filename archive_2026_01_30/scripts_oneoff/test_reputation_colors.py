"""
Quick Test - Zmień reputację klientów żeby zobaczyć kolory gauge'a
"""

import sys
sys.path.append('c:\\Users\\pksia\\Dropbox\\BVA')

from utils.fmcg_mechanics import load_fmcg_game_state_sql, update_fmcg_game_state_sql

username = "Basia"

print("🔄 Ładuję dane gry...")
loaded_data = load_fmcg_game_state_sql(username)

if loaded_data:
    game_state, clients = loaded_data
    
    print(f"✅ Załadowano {len(clients)} klientów")
    
    # Ustaw różne reputacje żeby zobaczyć kolory
    client_ids = list(clients.keys())
    
    if len(client_ids) >= 5:
        # -75 (LOST - czerwony)
        clients[client_ids[0]]["reputation"] = -75
        print(f"   {client_ids[0]}: reputation = -75 (💀 LOST - czerwony)")
        
        # -25 (AT RISK - pomarańczowy)
        clients[client_ids[1]]["reputation"] = -25
        print(f"   {client_ids[1]}: reputation = -25 (⚠️ AT RISK - pomarańczowy)")
        
        # 0 (NEUTRAL - żółty)
        clients[client_ids[2]]["reputation"] = 0
        print(f"   {client_ids[2]}: reputation = 0 (😐 NEUTRAL - żółty)")
        
        # +50 (GOOD - żółty)
        clients[client_ids[3]]["reputation"] = 50
        print(f"   {client_ids[3]}: reputation = +50 (😊 GOOD - żółty)")
        
        # +85 (CHAMPION - niebieski)
        clients[client_ids[4]]["reputation"] = 85
        print(f"   {client_ids[4]}: reputation = +85 (🏆 CHAMPION - niebieski)")
        
        # Zapisz
        print("\n💾 Zapisuję zmiany...")
        if update_fmcg_game_state_sql(username, game_state, clients):
            print("✅ GOTOWE! Przeładuj stronę i kliknij 'Szczegóły' na różnych klientach!")
            print("\n📊 Zobaczysz:")
            print("   • Sklep 1: 💀 LOST (czerwony pasek)")
            print("   • Sklep 2: ⚠️ AT RISK (pomarańczowy pasek)")  
            print("   • Sklep 3: 😐 NEUTRAL (żółty pasek)")
            print("   • Sklep 4: 😊 GOOD (żółty pasek, dłuższy)")
            print("   • Sklep 5: 🏆 CHAMPION (niebieski pasek)")
        else:
            print("❌ Błąd zapisu!")
    else:
        print("❌ Za mało klientów (potrzeba 5)")
else:
    print("❌ Nie znaleziono danych gry!")
