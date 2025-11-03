"""Fix st.tabs() to return 4 tabs instead of 3"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the st.tabs( line (around 1461)
for i, line in enumerate(lines):
    if i >= 1460 and i <= 1465 and "st.tabs([" in line:
        print(f"Found st.tabs at line {i + 1}")
        print(f"Current: {repr(lines[i])}")
        
        # Replace the entire st.tabs block (lines 1461-1464)
        # Line 1461: sales_tab_map, sales_tab_prep, sales_tab_visit, sales_tab_products = st.tabs([
        # Line 1462: "... Mapa & Klienci",
        # Line 1463: "... Wizyta",
        # Line 1464: "... Katalog produktów"
        # Line 1465: ])
        
        # Find the closing ])
        end_idx = i
        for j in range(i, min(i + 10, len(lines))):
            if "])" in lines[j]:
                end_idx = j
                break
        
        print(f"Block ends at line {end_idx + 1}")
        
        # Replace the block
        new_block = [
            '        sales_tab_map, sales_tab_prep, sales_tab_visit, sales_tab_products = st.tabs([\n',
            '            "🗺️ Klienci & Trasa",\n',
            '            "💼 Przygotowanie",\n',
            '            "🤝 Wizyta",\n',
            '            "📦 Produkty"\n',
            '        ])\n'
        ]
        
        # Remove old lines and insert new
        lines = lines[:i] + new_block + lines[end_idx + 1:]
        
        print("✅ Fixed st.tabs() definition")
        break

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ File saved")
