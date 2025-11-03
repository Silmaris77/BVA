"""
Fix the indentation issue properly.
The with sales_tab_prep: block starts at line 4728
Everything inside it should have 12 spaces indent (8 for with + 4 for content)
"""

# Read the file
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Line 4728 is "        with sales_tab_prep:" (8 spaces)
# Lines inside this block should have 12 spaces (8 + 4)

# Fix lines 4733-4740 to have proper indentation
# Line 4733 should be empty
# Lines 4735+ should have 12 spaces

fixes = [
    (4732, "\n"),  # Empty line (index 4732 = line 4733)
    # Line 4734 (index 4733) - should be comment with 12 spaces
    (4733, "            # Dynamic header based on scenario\n"),
]

for idx, content in fixes:
    if idx < len(lines):
        lines[idx] = content
        print(f"Fixed line {idx+1}: {repr(content[:50])}")

# Write back
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Fixed indentation")
