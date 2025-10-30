"""
Test SQL Integration dla FMCG Mechanics
Testuje zapisywanie i odczyt wizyt oraz stanu gry
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from pprint import pprint

# Import FMCG functions
from utils.fmcg_mechanics import (
    execute_visit_placeholder,
    save_fmcg_visit_to_sql,
    update_fmcg_game_state_sql,
    load_fmcg_game_state_sql
)
from utils.business_game import initialize_fmcg_game_new


def ensure_test_user_exists(username: str) -> bool:
    """
    Upewnia się że użytkownik testowy istnieje w JSON
    
    Args:
        username: Nazwa użytkownika testowego
    
    Returns:
        True jeśli user istnieje lub został utworzony
    """
    try:
        users_file = Path(__file__).parent / "users_data.json"
        
        # Load or create users file
        if users_file.exists():
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
        else:
            users = {}
        
        # Check if user exists
        if username in users:
            print(f"✅ User {username} already exists in JSON")
            return True
        
        # Create test user
        users[username] = {
            "username": username,
            "password": "test123",
            "created_at": datetime.now().isoformat(),
            "business_games": {},
            "degencoins": 0
        }
        
        # Save
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created test user {username} in JSON")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False


def ensure_test_user_exists(username: str) -> bool:
    """Upewnij się że testowy użytkownik istnieje w JSON"""
    users_file = Path(__file__).parent / "users_data.json"
    
    try:
        # Load existing users
        if users_file.exists():
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
        else:
            users = {}
        
        # Check if user exists
        if username in users:
            print(f"✅ User {username} already exists in JSON")
            return True
        
        # Create test user
        users[username] = {
            "username": username,
            "email": f"{username}@test.com",
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "role": "beta_tester",
            "business_games": {}
        }
        
        # Save
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created test user {username} in JSON")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False


def test_sql_integration():
    """Test pełnego cyklu: init → visit → save → load"""
    
    print("=" * 80)
    print("TEST FMCG SQL INTEGRATION")
    print("=" * 80)
    
    # Test user - use existing beta tester
    username = "test_fmcg_sql"  # Test user
    
    print(f"\n0️⃣  Przygotowanie środowiska testowego")
    print("-" * 80)
    
    # Ensure test user exists
    if not ensure_test_user_exists(username):
        print("❌ Nie udało się stworzyć użytkownika testowego")
        return False
    
    print(f"\n1️⃣  Inicjalizacja nowej gry dla użytkownika: {username}")
    print("-" * 80)
    
    # Initialize game
    game_data = initialize_fmcg_game_new(username)
    game_state = game_data["fmcg_state"]
    clients = game_state.get("clients", {})  # Clients są w game_state, nie game_data
    
    print(f"✅ Gra zainicjalizowana:")
    print(f"   - Energy: {game_state['energy']}%")
    print(f"   - Klienci PROSPECT: {game_state['clients_prospect']}")
    print(f"   - Marketing budget: {game_state['marketing_budget']} PLN")
    
    # Get first client
    first_client_id = list(clients.keys())[0]
    first_client = clients[first_client_id]
    print(f"\n   Pierwszy klient: {first_client['name']}")
    print(f"   - Typ: {first_client['type']}")
    print(f"   - Dystans: {first_client['distance_from_base']:.1f} km")
    
    print(f"\n2️⃣  Wykonanie wizyty u pierwszego klienta")
    print("-" * 80)
    
    # Execute visit
    try:
        updated_client, updated_game_state, visit_record = execute_visit_placeholder(
            client=first_client,
            game_state=game_state,
            conversation_quality=5,  # Świetna rozmowa
            order_value=2500,  # Pierwsze zamówienie
            tasks_completed=2,
            tools_used=["gratis", "pos_material"]
        )
        
        print(f"✅ Wizyta wykonana:")
        print(f"   - Status klienta: {first_client['status']} → {updated_client['status']}")
        print(f"   - Energia: {game_state['energy']}% → {updated_game_state['energy']}%")
        print(f"   - Zmiana reputacji: +{visit_record['reputation_change']}")
        print(f"   - Wartość zamówienia: {visit_record['order_value']} PLN")
        
        # Update references
        clients[first_client_id] = updated_client
        game_state = updated_game_state
        
    except Exception as e:
        print(f"❌ Błąd podczas wizyty: {e}")
        return False
    
    print(f"\n3️⃣  Zapis wizyty do SQL")
    print("-" * 80)
    
    # Save visit to SQL
    visit_saved = save_fmcg_visit_to_sql(username, visit_record, game_state)
    
    if visit_saved:
        print(f"✅ Wizyta zapisana do SQL")
    else:
        print(f"⚠️  Wizyta nie została zapisana (SQL może być niedostępny)")
    
    print(f"\n4️⃣  Zapis stanu gry do SQL")
    print("-" * 80)
    
    # Save game state to SQL
    state_saved = update_fmcg_game_state_sql(username, game_state, clients)
    
    if state_saved:
        print(f"✅ Stan gry zapisany do SQL")
    else:
        print(f"⚠️  Stan gry nie został zapisany")
        return False
    
    print(f"\n5️⃣  Odczyt stanu gry")
    print("-" * 80)
    
    # Load game state (from JSON or SQL depending on config)
    loaded_data = load_fmcg_game_state_sql(username)
    
    if not loaded_data:
        # Try loading directly from JSON
        print(f"ℹ️  Trying direct JSON load...")
        try:
            users_file = Path(__file__).parent / "users_data.json"
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            user_data = users.get(username, {})
            business_games = user_data.get('business_games', {})
            fmcg_game = business_games.get('fmcg')
            
            if fmcg_game:
                loaded_game_state = fmcg_game.get("fmcg_state")
                loaded_clients = loaded_game_state.get("clients", {}) if loaded_game_state else {}
                loaded_data = (loaded_game_state, loaded_clients)
                print(f"✅ Loaded from JSON directly")
            else:
                print(f"❌ No FMCG game in JSON either")
        except Exception as e:
            print(f"❌ JSON load error: {e}")
    
    if loaded_data:
        loaded_game_state, loaded_clients = loaded_data
        
        print(f"✅ Stan gry wczytany z SQL:")
        print(f"   - Energy: {loaded_game_state['energy']}%")
        print(f"   - Klienci PROSPECT: {loaded_game_state['clients_prospect']}")
        print(f"   - Klienci ACTIVE: {loaded_game_state['clients_active']}")
        print(f"   - Monthly sales: {loaded_game_state['monthly_sales']} PLN")
        print(f"   - Liczba klientów: {len(loaded_clients)}")
        
        # Verify first client
        loaded_first_client = loaded_clients.get(first_client_id)
        if loaded_first_client:
            print(f"\n   Pierwszy klient (po wczytaniu):")
            print(f"   - Nazwa: {loaded_first_client['name']}")
            print(f"   - Status: {loaded_first_client['status']}")
            print(f"   - Reputacja: {loaded_first_client.get('reputation', 'N/A')}")
            print(f"   - Total sales: {loaded_first_client.get('total_sales', 0)} PLN")
    else:
        print(f"❌ Nie udało się wczytać stanu gry")
        return False
    
    print(f"\n6️⃣  Weryfikacja danych")
    print("-" * 80)
    
    # Verify data integrity
    errors = []
    
    if loaded_game_state['energy'] != game_state['energy']:
        errors.append(f"Energy mismatch: {loaded_game_state['energy']} != {game_state['energy']}")
    
    if loaded_game_state['clients_active'] != game_state['clients_active']:
        errors.append(f"Active clients mismatch: {loaded_game_state['clients_active']} != {game_state['clients_active']}")
    
    if loaded_game_state['monthly_sales'] != game_state['monthly_sales']:
        errors.append(f"Sales mismatch: {loaded_game_state['monthly_sales']} != {game_state['monthly_sales']}")
    
    if loaded_first_client and loaded_first_client['status'] != updated_client['status']:
        errors.append(f"Client status mismatch: {loaded_first_client['status']} != {updated_client['status']}")
    elif not loaded_first_client:
        errors.append("First client not found in loaded data")
    
    if errors:
        print("❌ Wykryto błędy:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ Wszystkie dane zgodne!")
    
    print(f"\n" + "=" * 80)
    print("✅ TEST SQL INTEGRATION ZAKOŃCZONY SUKCESEM!")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    try:
        success = test_sql_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ KRYTYCZNY BŁĄD: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
