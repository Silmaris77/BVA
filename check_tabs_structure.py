import json

# Wczytaj plik v2.0
with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== STRUKTURA NAUKA ===\n")
print(f"Klucz 'nauka' istnieje: {'nauka' in data}")
print(f"Klucz 'tabs' istnieje: {'tabs' in data.get('nauka', {})}")
print(f"\nLiczba tabs: {len(data.get('nauka', {}).get('tabs', []))}")

if 'tabs' in data.get('nauka', {}):
    for i, tab in enumerate(data['nauka']['tabs']):
        print(f"\n--- TAB {i} ---")
        print(f"ID: {tab.get('id', 'BRAK')}")
        print(f"Title: {tab.get('title', 'BRAK')}")
        print(f"Sections: {len(tab.get('sections', []))}")
        
        # Sprawdź czy są inne pola
        all_keys = list(tab.keys())
        print(f"Wszystkie klucze: {all_keys}")

print("\n=== PORÓWNANIE Z v1.0 ===")
# Sprawdź starą strukturę
try:
    with open(r'data\lessons\11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    old_tabs = old_data.get('sections', {}).get('learning', {}).get('tabs', [])
    print(f"\nv1.0 - liczba tabs: {len(old_tabs)}")
    
    if old_tabs:
        print("\nPrzykład taba v1.0:")
        first_tab = old_tabs[0]
        for key in first_tab.keys():
            if key != 'sections':
                print(f"{key}: {first_tab[key]}")
    
except Exception as e:
    print(f"Błąd odczytu v1.0: {e}")
