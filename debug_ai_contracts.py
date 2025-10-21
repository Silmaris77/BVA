"""
Debug script - sprawdza dlaczego AI contracts nie pojawiają się
"""

from data.business_data import CONTRACTS_POOL, FIRM_LEVELS, GAME_CONFIG

# 1. Sprawdź kontrakty AI
ai_contracts = [c for c in CONTRACTS_POOL if c.get("contract_type") == "ai_conversation"]

print("=" * 80)
print("AI CONVERSATION CONTRACTS")
print("=" * 80)
for c in ai_contracts:
    print(f"\n{c['id']}: {c['tytul']}")
    print(f"  Wymagany poziom: {c['wymagany_poziom']}")
    print(f"  Trudność: {c['trudnosc']}")
    print(f"  Nagroda: {c['nagroda_base']}-{c['nagroda_5star']}")

# 2. Sprawdź poziomy firmy
print("\n" + "=" * 80)
print("FIRM LEVELS")
print("=" * 80)
for level, data in FIRM_LEVELS.items():
    print(f"\nPoziom {level}: {data['nazwa']}")
    print(f"  Wymagania: {data.get('wymagania', 'N/A')}")

# 3. Sprawdź starting values
print("\n" + "=" * 80)
print("STARTING VALUES")
print("=" * 80)
print(f"Starting level: {GAME_CONFIG['starting_level']}")
print(f"Starting reputation: {GAME_CONFIG['starting_reputation']}")
print(f"Starting coins: {GAME_CONFIG.get('starting_coins', 'N/A')}")

# 4. Symuluj nową grę
print("\n" + "=" * 80)
print("SYMULACJA: Nowa gra - jakie kontrakty dostępne?")
print("=" * 80)
firm_level = GAME_CONFIG["starting_level"]
available_for_level_1 = [c for c in CONTRACTS_POOL if c["wymagany_poziom"] <= firm_level]

print(f"\nPoziom firmy: {firm_level}")
print(f"Dostępnych kontraktów: {len(available_for_level_1)}/{len(CONTRACTS_POOL)}")

# Grupuj po typie
by_type = {}
for c in available_for_level_1:
    ctype = c.get("contract_type", "standard")
    if ctype not in by_type:
        by_type[ctype] = []
    by_type[ctype].append(c)

for ctype, contracts in by_type.items():
    print(f"\n  {ctype}: {len(contracts)} kontraktów")
    for c in contracts:
        print(f"    - {c['id']}: {c['tytul']} (req_level={c['wymagany_poziom']})")

# 5. Sprawdź czy AI contracts są dostępne
print("\n" + "=" * 80)
print("DOSTĘPNOŚĆ AI CONTRACTS")
print("=" * 80)
for c in ai_contracts:
    is_available = c["wymagany_poziom"] <= firm_level
    status = "✅ DOSTĘPNY" if is_available else f"❌ NIEDOSTĘPNY (wymaga poziomu {c['wymagany_poziom']})"
    print(f"{c['id']}: {status}")
