"""
Test backward compatibility dla submit_contract_solution
Symuluje przypadek z KeyError: 'business_game'
"""

from utils.business_game import submit_contract_solution, get_current_firm_level, update_firm_level
from datetime import datetime

# Mock user_data z NOWĄ strukturą (business_games zamiast business_game)
user_data_new_structure = {
    "username": "test_user",
    "degencoins": 1000,
    "business_games": {
        "consulting": {
            "firm": {
                "name": "Test Consulting",
                "level": 1,
                "reputation": 50
            },
            "contracts": {
                "active": [
                    {
                        "id": "TEST-001",
                        "tytul": "Test Contract",
                        "kategoria": "Coaching",
                        "nagroda_base": 500,
                        "nagroda_4star": 700,
                        "nagroda_5star": 900,
                        "reputacja": 30,
                        "min_slow": 10  # Niski dla testu
                    }
                ],
                "completed": []
            },
            "stats": {
                "total_revenue": 0,
                "contracts_completed": 0,
                "contracts_5star": 0,
                "contracts_4star": 0,
                "contracts_3star": 0,
                "contracts_2star": 0,
                "contracts_1star": 0,
                "avg_rating": 0.0,
                "category_stats": {
                    "Coaching": {"completed": 0, "total_earned": 0, "avg_rating": 0.0}
                }
            },
            "employees": [],
            "history": {
                "transactions": [],
                "level_ups": []
            }
        }
    }
}

# Mock user_data ze STARĄ strukturą (business_game)
user_data_old_structure = {
    "username": "old_user",
    "degencoins": 1000,
    "business_game": {
        "firm": {
            "name": "Old Consulting",
            "level": 1,
            "reputation": 50
        },
        "contracts": {
            "active": [
                {
                    "id": "TEST-002",
                    "tytul": "Old Contract",
                    "kategoria": "Coaching",
                    "nagroda_base": 500,
                    "nagroda_4star": 700,
                    "nagroda_5star": 900,
                    "reputacja": 30,
                    "min_slow": 10
                }
            ],
            "completed": []
        },
        "stats": {
            "total_revenue": 0,
            "contracts_completed": 0,
            "contracts_5star": 0,
            "contracts_4star": 0,
            "contracts_3star": 0,
            "contracts_2star": 0,
            "contracts_1star": 0,
            "avg_rating": 0.0,
            "category_stats": {
                "Coaching": {"completed": 0, "total_earned": 0, "avg_rating": 0.0}
            }
        },
        "employees": [],
        "history": {
            "transactions": [],
            "level_ups": []
        }
    }
}

print("=" * 80)
print("TEST BACKWARD COMPATIBILITY")
print("=" * 80)

# Test 1: Nowa struktura (business_games)
print("\n✅ Test 1: NOWA STRUKTURA (business_games)")
try:
    updated_data, success, message, _ = submit_contract_solution(
        user_data_new_structure,
        "TEST-001",
        "To jest testowa odpowiedź. Bardzo długa odpowiedź która spełnia minimum słów."
    )
    if success:
        print(f"   ✅ SUCCESS: {message[:50]}...")
        print(f"   Coins: {updated_data['degencoins']}")
        print(f"   Active contracts: {len(updated_data['business_games']['consulting']['contracts']['active'])}")
        print(f"   Completed: {len(updated_data['business_games']['consulting']['contracts']['completed'])}")
    else:
        print(f"   ❌ FAILED: {message}")
except KeyError as e:
    print(f"   ❌ KeyError: {e}")
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

# Test 2: Stara struktura (business_game)
print("\n✅ Test 2: STARA STRUKTURA (business_game)")
try:
    updated_data, success, message, _ = submit_contract_solution(
        user_data_old_structure,
        "TEST-002",
        "To jest testowa odpowiedź dla starej struktury. Długa odpowiedź."
    )
    if success:
        print(f"   ✅ SUCCESS: {message[:50]}...")
        print(f"   Coins: {updated_data['degencoins']}")
        print(f"   Active contracts: {len(updated_data['business_game']['contracts']['active'])}")
        print(f"   Completed: {len(updated_data['business_game']['contracts']['completed'])}")
    else:
        print(f"   ❌ FAILED: {message}")
except KeyError as e:
    print(f"   ❌ KeyError: {e}")
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

# Test 3: get_current_firm_level
print("\n✅ Test 3: get_current_firm_level")
try:
    level_new = get_current_firm_level(user_data_new_structure)
    print(f"   Nowa struktura: level = {level_new}")
    level_old = get_current_firm_level(user_data_old_structure)
    print(f"   Stara struktura: level = {level_old}")
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

# Test 4: update_firm_level
print("\n✅ Test 4: update_firm_level")
try:
    updated_new, leveled_up_new = update_firm_level(user_data_new_structure)
    print(f"   Nowa struktura: leveled_up = {leveled_up_new}")
    updated_old, leveled_up_old = update_firm_level(user_data_old_structure)
    print(f"   Stara struktura: leveled_up = {leveled_up_old}")
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("✅ WSZYSTKIE TESTY ZAKOŃCZONE")
print("=" * 80)
