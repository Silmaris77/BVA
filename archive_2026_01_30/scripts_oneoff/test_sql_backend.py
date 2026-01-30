"""
Test SQL Backend - sprawdza czy dane czytane są z SQL
"""

from data.repositories import BusinessGameRepository

# Initialize repository (powinien użyć SQL zgodnie z config)
repo = BusinessGameRepository()

print("="*60)
print("🧪 TEST SQL BACKEND")
print("="*60)

# Test 1: Sprawdź konfigurację
print(f"\n1️⃣  Config:")
print(f"   Backend: {repo.backend}")
print(f"   SQL read enabled: {repo.config.get('feature_flags', {}).get('enable_sql_read')}")
print(f"   Default per-user backend: {repo.config.get('per_user_backend', {}).get('*')}")

# Test 2: Sprawdź czy użyje SQL dla Piotra
print(f"\n2️⃣  Decision logic for 'Piotr':")
use_sql_read = repo._should_use_sql_for_read("Piotr")
use_sql_write = repo._should_use_sql_for_write("Piotr")
print(f"   Should use SQL for read: {use_sql_read}")
print(f"   Should use SQL for write: {use_sql_write}")

# Test 3: Pobierz dane Piotra
print(f"\n3️⃣  Loading Piotr's consulting scenario...")
consulting_data = repo.get("Piotr", "consulting")

if consulting_data:
    print(f"   ✅ Data loaded successfully!")
    print(f"   Firm: {consulting_data.get('firm', {}).get('name', 'N/A')}")
    print(f"   Money: {consulting_data.get('money', 0)}")
    print(f"   Level: {consulting_data.get('firm', {}).get('level', 0)}")
    print(f"   Employees: {len(consulting_data.get('employees', []))}")
    active_contracts = len(consulting_data.get('contracts', {}).get('active', []))
    print(f"   Contracts: {active_contracts} active")
else:
    print(f"   ❌ No data found!")

# Test 4: Pobierz dane Pawła
print(f"\n4️⃣  Loading Pawel's consulting scenario...")
pawel_data = repo.get("Pawel", "consulting")

if pawel_data:
    print(f"   ✅ Data loaded successfully!")
    print(f"   Firm: {pawel_data.get('firm', {}).get('name', 'N/A')}")
    print(f"   Money: {pawel_data.get('money', 0)}")
    print(f"   Level: {pawel_data.get('firm', {}).get('level', 0)}")
else:
    print(f"   ❌ No data found!")

print(f"\n{'='*60}")
print(f"✅ TEST COMPLETE")
print(f"{'='*60}")
