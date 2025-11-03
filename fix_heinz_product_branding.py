"""Fix product details to recognize Heinz products as own brand, not competitor"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Step 1: Update function signature to accept scenario_name parameter
for i, line in enumerate(lines):
    if "def _render_product_details(product: Dict):" in line:
        lines[i] = "def _render_product_details(product: Dict, scenario_name: str = 'lifetime'):\n"
        print(f"✅ Updated function signature at line {i + 1}")
        break

# Step 2: Update is_freshlife logic to handle Heinz scenario
for i, line in enumerate(lines):
    if i > 190 and i < 200 and 'is_freshlife = product.get("brand") == "FreshLife"' in line:
        # Replace with scenario-aware logic
        new_logic = '''    # Determine if product is "own brand" based on scenario
    if scenario_name == "heinz_foodservice":
        # In Heinz scenario, Heinz and Pudliszki are own brands
        is_own_brand = product.get("brand") in ["Heinz", "Pudliszki"]
    else:
        # In FreshLife scenarios (lifetime, quickstart), FreshLife is own brand
        is_own_brand = product.get("brand") == "FreshLife"
    
    # Keep is_freshlife for backward compatibility in some code sections
    is_freshlife = is_own_brand
'''
        lines[i] = new_logic
        print(f"✅ Updated is_freshlife logic at line {i + 1}")
        break

# Step 3: Update function call to pass scenario_name
for i, line in enumerate(lines):
    if "_render_product_details(product)" in line and i > 2990:
        # Need to find scenario_name in context
        # It should be available in the parent scope
        lines[i] = line.replace("_render_product_details(product)", "_render_product_details(product, scenario_name)")
        print(f"✅ Updated function call at line {i + 1}")
        break

# Step 4: Update competitor message to be scenario-aware
for i, line in enumerate(lines):
    if 'st.info("ℹ️ To produkt konkurencji. FreshLife nie sprzedaje tego produktu.")' in line:
        new_message = '''        if scenario_name == "heinz_foodservice":
            st.info("ℹ️ To produkt konkurencji (nie należy do portfolio Heinz).")
        else:
            st.info("ℹ️ To produkt konkurencji. FreshLife nie sprzedaje tego produktu.")'''
        lines[i] = new_message + "\n"
        print(f"✅ Updated competitor message at line {i + 1}")
        break

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Product details function updated for Heinz scenario")
