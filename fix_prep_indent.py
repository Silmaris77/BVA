"""Fix indentation in sales_tab_prep - line 4744 should have 12 spaces, not 8"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Line 4744 (index 4743) should have "            # Filters" (12 spaces)
# Currently has "        # Filters" (8 spaces)

if lines[4743].startswith("        # Filters"):
    lines[4743] = "            # Filters (only show for non-Heinz scenarios)\n"
    print("✅ Fixed line 4744")
else:
    print(f"Line 4744: {repr(lines[4743])}")
    print("ERROR: Line doesn't match expected pattern")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
