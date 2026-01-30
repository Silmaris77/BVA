import json

# Porównaj struktury tabs między v1.0 i v2.0
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    v2 = json.load(f)

print("=== PORÓWNANIE STRUKTURY TABS ===\n")

v1_tabs = v1['sections']['learning']['tabs']
v2_tabs = v2['nauka']['tabs']

print(f"v1.0 tabs: {len(v1_tabs)}")
print(f"v2.0 tabs: {len(v2_tabs)}\n")

print("--- v1.0 pierwszy tab ---")
print(json.dumps(v1_tabs[0], indent=2, ensure_ascii=False)[:500])

print("\n--- v2.0 pierwszy tab ---")
print(json.dumps(v2_tabs[0], indent=2, ensure_ascii=False)[:500])

# Sprawdź czy v2.0 ma wszystkie potrzebne pola
print("\n=== ANALIZA POLA SECTIONS ===")
print(f"\nv1.0 - typ sections: {type(v1_tabs[0].get('sections'))}")
print(f"v2.0 - typ sections: {type(v2_tabs[0].get('sections'))}")

if isinstance(v1_tabs[0].get('sections'), list):
    print(f"v1.0 - liczba sections: {len(v1_tabs[0]['sections'])}")
    print(f"v1.0 - przykładowa section:")
    if v1_tabs[0]['sections']:
        first_section = v1_tabs[0]['sections'][0]
        print(f"  title: {first_section.get('title', 'BRAK')[:80]}")
        print(f"  content: {first_section.get('content', 'BRAK')[:80]}")

if isinstance(v2_tabs[0].get('sections'), list):
    print(f"\nv2.0 - liczba sections: {len(v2_tabs[0]['sections'])}")
    print(f"v2.0 - przykładowa section:")
    if v2_tabs[0]['sections']:
        first_section = v2_tabs[0]['sections'][0]
        print(f"  title: {first_section.get('title', 'BRAK')[:80]}")
        print(f"  content: {first_section.get('content', 'BRAK')[:80]}")
