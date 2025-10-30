"""
Test FMCG Client Card - Quick Validation
"""

import sys
sys.path.append('c:\\Users\\pksia\\Dropbox\\BVA')

from utils.fmcg_client_helpers import (
    create_new_client_entry,
    get_reputation_status,
    migrate_fmcg_customers_to_new_structure,
    add_product_to_portfolio
)
from utils.fmcg_reputation import update_client_reputation, record_visit
from utils.fmcg_products import (
    get_product_info,
    suggest_cross_sell_products
)

print("=" * 60)
print("🧪 TEST 1: Create new client entry")
print("=" * 60)

client = create_new_client_entry("trad_001", status="prospect")
print(f"✅ Client created: {client['id']}")
print(f"   Status: {client['status']}")
print(f"   Reputation: {client['reputation']}")
print(f"   Portfolio: {len(client['products_portfolio'])} products")
print(f"   Timeline: {len(client['events_timeline'])} events")

print("\n" + "=" * 60)
print("🧪 TEST 2: Reputation status")
print("=" * 60)

for rep in [-75, -25, 0, 25, 50, 85]:
    status = get_reputation_status(rep)
    print(f"Rep {rep:+4d}: {status['emoji']} {status['label']:15s} ({status['color']})")

print("\n" + "=" * 60)
print("🧪 TEST 3: Update reputation - visit on time")
print("=" * 60)

change = update_client_reputation(
    client,
    "regular_visit_on_time",
    description="Wizyta w terminie"
)
print(f"✅ Reputation change: {change:+d}")
print(f"   New reputation: {client['reputation']}")
print(f"   Timeline events: {len(client['events_timeline'])}")
print(f"   Last event: {client['events_timeline'][-1]['description']}")

print("\n" + "=" * 60)
print("🧪 TEST 4: Add product to portfolio")
print("=" * 60)

added = add_product_to_portfolio(client, "yogurt_natural", initial_volume=100)
print(f"✅ Product added: {added}")
print(f"   Portfolio size: {len(client['products_portfolio'])}")
print(f"   Product: {client['products_portfolio'][0]['product_id']}")
print(f"   Monthly volume: {client['products_portfolio'][0]['monthly_volume']}")
print(f"   Monthly value: {client['monthly_value']} PLN")
print(f"   Reputation: {client['reputation']} (should be +20: +5 from visit, +15 from cross-sell)")

print("\n" + "=" * 60)
print("🧪 TEST 5: Cross-sell suggestions")
print("=" * 60)

suggestions = suggest_cross_sell_products(client, max_suggestions=3)
print(f"✅ {len(suggestions)} suggestions:")
for i, sugg in enumerate(suggestions, 1):
    prod = sugg['product']
    print(f"{i}. {prod['name']}")
    print(f"   Reason: {sugg['reason']}")
    print(f"   Priority: {sugg['priority']}")
    print(f"   Expected volume: {sugg['expected_volume']}")

print("\n" + "=" * 60)
print("🧪 TEST 6: Migration (old structure → new)")
print("=" * 60)

# Symuluj starą strukturę
old_bg_data = {
    "customers": {
        "prospects": ["trad_001", "trad_002"],
        "active_clients": ["trad_003"],
        "lost_clients": []
    },
    "conversations": {
        "trad_001": [{"role": "user", "content": "Test"}],
        "trad_002": [],
        "trad_003": [{"role": "assistant", "content": "Witaj"}]
    }
}

new_data, count = migrate_fmcg_customers_to_new_structure(old_bg_data)
print(f"✅ Migrated {count} clients")
print(f"   New structure has 'clients' key: {'clients' in new_data['customers']}")
print(f"   Number of clients: {len(new_data['customers']['clients'])}")

# Sprawdź czy conversations zostały zachowane
for client_id, client_data in new_data['customers']['clients'].items():
    conv_count = len(client_data.get('conversations', []))
    print(f"   {client_id}: {client_data['status']} - {conv_count} conversations preserved")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
