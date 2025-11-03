"""Change tabs from 3 to 4"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the tab definition
old = 'sales_tab_map, sales_tab_visit, sales_tab_products = st.tabs(['
new = 'sales_tab_map, sales_tab_prep, sales_tab_visit, sales_tab_products = st.tabs(['

if old in content:
    content = content.replace(old, new, 1)
    print("✅ Changed tab variables")
else:
    print("ERROR: Could not find tab definition")
    exit(1)

# Also update tab names
content = content.replace('"🗺️ Mapa & Klienci",', '"🗺️ Klienci & Trasa",\n            "💼 Przygotowanie",', 1)
content = content.replace('"💬 Wizyta u klienta",', '"💬 Wizyta",', 1)

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Updated to 4 tabs")
