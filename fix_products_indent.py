"""Fix indentation inside sales_tab_products block"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find sales_tab_products block (line 4748)
# All content from line 4749 to 5574 (before HR tab) needs +4 spaces

products_start = None
products_end = None

for i, line in enumerate(lines):
    if i == 4747 and "with sales_tab_products:" in line:
        products_start = i + 1  # Start after "with sales_tab_products:"
        print(f"Found sales_tab_products at line {i + 1}")
    
    # Find where HR tab starts (end of sales section)
    if products_start and i > products_start and "with tab_hr:" in line:
        products_end = i
        print(f"Found HR tab at line {i + 1}")
        break

if products_start and products_end:
    print(f"\nFixing indentation from line {products_start + 1} to {products_end}")
    
    fixed = 0
    for i in range(products_start, products_end):
        # Skip completely empty lines
        if lines[i].strip() == "":
            continue
        
        # Add 4 spaces to all content lines
        if lines[i].startswith("        "):  # Currently 8 spaces
            lines[i] = "    " + lines[i]  # Make it 12 spaces
            fixed += 1
    
    print(f"✅ Fixed {fixed} lines")
    
    with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
else:
    print("❌ Could not find products block boundaries")
