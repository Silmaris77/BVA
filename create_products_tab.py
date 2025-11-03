"""
Move products code from sales_tab_prep to new sales_tab_products
"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find sales_tab_prep start (around line 4776)
prep_start = None
for i in range(4770, 4780):
    if "with sales_tab_prep:" in lines[i]:
        prep_start = i
        break

if prep_start is None:
    print("ERROR: Could not find sales_tab_prep")
    exit(1)

print(f"Found sales_tab_prep at line {prep_start + 1}")

# Find where HR tab starts (line ~5561) - this is where products code ends
hr_start = None
for i in range(5550, 5570):
    if "# TAB: HR & TEAM" in lines[i]:
        hr_start = i
        break

if hr_start is None:
    print("ERROR: Could not find HR tab")
    exit(1)

print(f"Found HR tab at line {hr_start + 1}")

# Extract products code (from prep_start+1 to hr_start)
products_code = lines[prep_start+1:hr_start]
print(f"Extracted {len(products_code)} lines of products code")

# Create new simple prep tab content
new_prep_content = '''            st.subheader("💼 Przygotowanie do Wizyt")
            
            st.info("""
            🚧 **Sekcja w budowie**
            
            Tutaj będą dostępne narzędzia Trade-Marketing:
            - 🎁 Planowanie promocji
            - 📊 Analiza konkurencji
            - 💰 Kalkulator marży
            - 📋 Materiały POS
            """)
            
            st.markdown("---")
            st.markdown("💡 **Wskazówka**: Katalog produktów znajdziesz w zakładce **'📦 Produkty'**")
        
'''

# Create new products tab content
new_products_content = '''        
        # =========================================================================
        # SUB-TAB: PRODUKTY (Katalog produktów)
        # =========================================================================
        
        with sales_tab_products:
'''

# Rebuild file:
# 1. Lines up to prep_start - KEEP
# 2. Line with "with sales_tab_prep:" - KEEP
# 3. Replace old prep content with new simple content
# 4. Add new products tab with products code
# 5. Lines from hr_start onwards - KEEP

new_lines = []
new_lines.extend(lines[0:prep_start+1])  # Up to and including "with sales_tab_prep:"
new_lines.append(new_prep_content)  # New simple prep content
new_lines.append(new_products_content)  # Products tab header
new_lines.extend(products_code)  # All the products code
new_lines.extend(lines[hr_start:])  # HR tab onwards

print(f"New file will have {len(new_lines)} lines (was {len(lines)})")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ Created separate Products tab!")
