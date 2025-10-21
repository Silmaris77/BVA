import data.business_data as bd

ai_contracts = [c for c in bd.CONTRACTS_POOL if c.get('contract_type') == 'ai_conversation']

print(f"✅ Import successful!")
print(f"📋 Total contracts: {len(bd.CONTRACTS_POOL)}")
print(f"💬 AI Conversation contracts: {len(ai_contracts)}")
print("\nAI Conversation contracts:")
for c in ai_contracts:
    print(f"  - {c['id']}: {c['tytul']}")
    print(f"    NPC: {c.get('npc_config', {}).get('name', 'Unknown')}")
    print(f"    Category: {c['kategoria']}")
