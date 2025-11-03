"""
Fix indentation for sales_tab_products code block
"""

with open('views/business_games_refactored/industries/fmcg_playable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the sales_tab_products block
products_start = None
products_end = None

for i, line in enumerate(lines):
    if 'with sales_tab_products:' in line and i > 4060:
        products_start = i + 2  # After subheader line
        print(f"Found sales_tab_products start at line {i+1}")
        break

# Find where it ends (before next main section - likely "OLD TAB" or "TAB: HR")
for i in range(products_start, len(lines)):
    if i > products_start and ('# TAB: HR' in lines[i] or 
                                '# OLD TAB:' in lines[i] or
                                'with tab_hr:' in lines[i]):
        products_end = i
        print(f"Found sales_tab_products end at line {i+1}")
        break

if products_start and products_end:
    print(f"\nFixing indentation for lines {products_start+1} to {products_end}")
    print(f"Total lines to fix: {products_end - products_start}")
    
    # Add 4 spaces to each line in the block
    new_lines = lines.copy()
    for i in range(products_start, products_end):
        # Skip empty lines
        if lines[i].strip():
            # Add 4 spaces of indentation
            new_lines[i] = '    ' + lines[i]
    
    # Write back
    with open('views/business_games_refactored/industries/fmcg_playable.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n[OK] Fixed indentation for sales_tab_products block!")
    print(f"     Lines {products_start+1}-{products_end} now properly indented")
else:
    print(f"\n[ERROR] Could not find block boundaries:")
    print(f"  Start: {products_start}")
    print(f"  End: {products_end}")
