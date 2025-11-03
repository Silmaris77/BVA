"""
Fix indentation for sales_tab_map code block
All code after 'with sales_tab_map:' should be indented by 4 spaces
"""

with open('views/business_games_refactored/industries/fmcg_playable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the sales_tab_map block
map_start = None
map_end = None

for i, line in enumerate(lines):
    if 'with sales_tab_map:' in line and i > 1390:
        map_start = i + 2  # After subheader line
        print(f"Found sales_tab_map start at line {i+1}")
        break

# Find where it ends (before "with sales_tab_visit:" or similar)
for i in range(map_start, len(lines)):
    if i > map_start and ('with sales_tab_visit:' in lines[i] or 
                           'with sales_tab_products:' in lines[i] or
                           '# SUB-TAB: WIZYTA' in lines[i]):
        map_end = i
        print(f"Found sales_tab_map end at line {i+1}")
        break

if map_start and map_end:
    print(f"\nFixing indentation for lines {map_start+1} to {map_end}")
    print(f"Total lines to fix: {map_end - map_start}")
    
    # Add 4 spaces to each line in the block
    new_lines = lines.copy()
    for i in range(map_start, map_end):
        # Skip empty lines
        if lines[i].strip():
            # Add 4 spaces of indentation
            new_lines[i] = '    ' + lines[i]
        # Keep empty lines as-is
    
    # Write back
    with open('views/business_games_refactored/industries/fmcg_playable.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n[OK] Fixed indentation for sales_tab_map block!")
    print(f"     Lines {map_start+1}-{map_end} now properly indented")
else:
    print(f"\n[ERROR] Could not find block boundaries:")
    print(f"  Start: {map_start}")
    print(f"  End: {map_end}")
