"""Add new sales_tab_products block with products code"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where prep tab ends (should be around line 4742 after our changes)
# Insert new sales_tab_products right after

insert_idx = 4742  # After the prep tab content

new_tab_code = '''        
        # =========================================================================
        # SUB-TAB: PRODUKTY  
        # =========================================================================
        
        with sales_tab_products:
'''

lines.insert(insert_idx, new_tab_code)

print(f"✅ Inserted sales_tab_products header at line {insert_idx + 1}")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Now products code will be in sales_tab_products")
