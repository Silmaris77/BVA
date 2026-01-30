"""
Test Visit Recording Integration
Sprawdza czy wizyty są zapisywane do visits_history i events_timeline
"""

import sys
sys.path.append('c:\\Users\\pksia\\Dropbox\\BVA')

from utils.fmcg_mechanics import load_fmcg_game_state_sql
from utils.fmcg_reputation import record_visit

username = "Basia"

print("🔄 Ładuję dane gry...")
loaded_data = load_fmcg_game_state_sql(username)

if loaded_data:
    game_state, clients = loaded_data
    
    print(f"✅ Załadowano {len(clients)} klientów\n")
    
    # Wybierz pierwszego klienta
    client_id = list(clients.keys())[0]
    client_data = clients[client_id]
    
    print(f"📋 Klient: {client_data.get('name', client_id)}")
    print(f"   Status: {client_data.get('status', 'N/A')}")
    print(f"   Reputacja przed: {client_data.get('reputation', 0)}")
    
    # Sprawdź historię przed
    visits_before = len(client_data.get('visits_history', []))
    events_before = len(client_data.get('events_timeline', []))
    print(f"   Wizyty przed: {visits_before}")
    print(f"   Wydarzenia przed: {events_before}")
    
    # Symuluj wizytę
    print("\n🎯 Symulacja wizyty (jakość: 4/5)...")
    reputation_change = record_visit(
        client_data=client_data,
        visit_quality=4,
        notes="Test wizyty - omówienie produktów"
    )
    
    print(f"\n✅ Wizyta zapisana!")
    print(f"   Zmiana reputacji: {reputation_change:+d}")
    print(f"   Reputacja po: {client_data.get('reputation', 0)}")
    
    # Sprawdź historię po
    visits_after = len(client_data.get('visits_history', []))
    events_after = len(client_data.get('events_timeline', []))
    print(f"   Wizyty po: {visits_after} (dodano: {visits_after - visits_before})")
    print(f"   Wydarzenia po: {events_after} (dodano: {events_after - events_before})")
    
    # Pokaż ostatnią wizytę
    if client_data.get('visits_history'):
        last_visit = client_data['visits_history'][-1]
        print(f"\n📊 Ostatnia wizyta:")
        print(f"   Data: {last_visit.get('date')}")
        print(f"   Jakość: {last_visit.get('quality')}/5")
        print(f"   Notatki: {last_visit.get('notes')}")
        print(f"   Zmiana reputacji: {last_visit.get('reputation_change'):+d}")
        print(f"   Reputacja po: {last_visit.get('reputation_after')}")
    
    # Pokaż ostatnie wydarzenie
    if client_data.get('events_timeline'):
        last_event = client_data['events_timeline'][-1]
        print(f"\n📅 Ostatnie wydarzenie:")
        print(f"   Data: {last_event.get('date')}")
        print(f"   Typ: {last_event.get('type')}")
        print(f"   Opis: {last_event.get('description')}")
        print(f"   Zmiana reputacji: {last_event.get('reputation_change'):+d}")
    
    print(f"\n✅ Test zakończony pomyślnie!")
    print(f"\n💡 Nie zapisuję do SQL - to tylko test lokalny")
    
else:
    print("❌ Nie znaleziono danych gry!")
