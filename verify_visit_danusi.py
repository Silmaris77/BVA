"""
Weryfikacja wizyty u Danusi - Detailed Check
"""

import sys
sys.path.append('c:\\Users\\pksia\\Dropbox\\BVA')

from utils.fmcg_mechanics import load_fmcg_game_state_sql
import json

username = "Basia"

print("=" * 80)
print("WERYFIKACJA WIZYTY - Sklep 'U Danusi' (pias_001)")
print("=" * 80)

loaded_data = load_fmcg_game_state_sql(username)

if loaded_data:
    game_state, clients = loaded_data
    
    client_id = "pias_001"
    client = clients.get(client_id)
    
    if client:
        print(f"\n📋 KLIENT: {client.get('name', 'N/A')}")
        print(f"   Właściciel: {client.get('owner', 'N/A')}")
        print(f"   Lokalizacja: {client.get('location', 'N/A')}")
        
        print(f"\n📊 STATUS:")
        print(f"   Status: {client.get('status', 'N/A').upper()}")
        print(f"   Reputacja: {client.get('reputation', 0)}")
        print(f"   Ostatnia wizyta: {client.get('last_visit_date', 'Brak')}")
        print(f"   Następna wizyta: {client.get('next_visit_due', 'Brak')}")
        
        print(f"\n📝 HISTORIA WIZYT:")
        visits = client.get('visits_history', [])
        print(f"   Liczba wizyt: {len(visits)}")
        if visits:
            for idx, visit in enumerate(visits, 1):
                print(f"\n   Wizyta #{idx}:")
                print(f"      Data: {visit.get('date', 'N/A')}")
                print(f"      Jakość: {visit.get('quality', 0)}/5")
                print(f"      Zmiana reputacji: {visit.get('reputation_change', 0):+d}")
                print(f"      Reputacja po: {visit.get('reputation_after', 0)}")
                print(f"      Notatki: {visit.get('notes', 'Brak')[:100]}...")
        
        print(f"\n📅 TIMELINE WYDARZEŃ:")
        events = client.get('events_timeline', [])
        print(f"   Liczba wydarzeń: {len(events)}")
        if events:
            for idx, event in enumerate(events, 1):
                print(f"\n   Wydarzenie #{idx}:")
                print(f"      Data: {event.get('date', 'N/A')}")
                print(f"      Typ: {event.get('type', 'N/A')}")
                print(f"      Opis: {event.get('description', 'N/A')[:80]}...")
                print(f"      Zmiana reputacji: {event.get('reputation_change', 0):+d}")
                print(f"      Reputacja po: {event.get('reputation_after', 0)}")
        
        print(f"\n📦 PORTFOLIO PRODUKTÓW:")
        portfolio = client.get('products_portfolio', [])
        print(f"   Liczba produktów: {len(portfolio)}")
        if portfolio:
            for prod in portfolio:
                print(f"      - {prod.get('product_id', 'N/A')}: {prod.get('volume_monthly', 0)} szt/mies")
        else:
            print(f"      (brak produktów - PROSPECT)")
        
        print(f"\n📈 STATYSTYKI GRY:")
        print(f"   Energia: {game_state.get('energy', 0)}%")
        print(f"   Wizyty w tym tygodniu: {game_state.get('visits_this_week', 0)}")
        print(f"   Sprzedaż miesięczna: {game_state.get('monthly_sales', 0):,} PLN")
        print(f"   Klienci PROSPECT: {game_state.get('clients_prospect', 0)}")
        print(f"   Klienci ACTIVE: {game_state.get('clients_active', 0)}")
        
        print(f"\n🔍 POTENCJALNE PROBLEMY:")
        issues = []
        
        # Check 1: Reputacja spadła zamiast wzrosnąć
        if visits and visits[-1].get('reputation_change', 0) < 0:
            issues.append(f"⚠️  Reputacja SPADŁA o {visits[-1]['reputation_change']} (jakość wizyty: {visits[-1]['quality']}/5)")
        
        # Check 2: Wizyta była zapisana ale nie ma w timeline odpowiedniego eventu
        if len(visits) != len([e for e in events if 'visit' in e.get('type', '')]):
            issues.append(f"⚠️  Niezgodność: {len(visits)} wizyt vs {len(events)} wydarzeń")
        
        # Check 3: Status nadal PROSPECT mimo wizyty
        if client.get('status') == 'prospect' and len(visits) > 0:
            issues.append(f"ℹ️  Klient nadal PROSPECT (to OK - kontrakt dopiero po quality >= 4)")
        
        # Check 4: Portfolio puste mimo wizyty
        if len(portfolio) == 0 and len(visits) > 0:
            issues.append(f"ℹ️  Brak produktów w portfolio (to OK - kontrakt nie został podpisany)")
        
        # Check 5: Quality wizyty
        if visits:
            quality = visits[-1].get('quality', 0)
            if quality < 4:
                issues.append(f"ℹ️  Jakość wizyty ({quality}/5) za niska do podpisania kontraktu (potrzeba >= 4)")
        
        if issues:
            for issue in issues:
                print(f"   {issue}")
        else:
            print(f"   ✅ Wszystko wygląda OK!")
        
        print(f"\n{'=' * 80}")
        print(f"ANALIZA ZAKOŃCZONA")
        print(f"{'=' * 80}\n")
        
    else:
        print(f"❌ Nie znaleziono klienta {client_id}")
else:
    print("❌ Nie udało się załadować danych gry")
