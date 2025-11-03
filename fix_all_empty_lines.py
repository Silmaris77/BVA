"""Fix all empty lines with 8 spaces in sales_tab_prep section"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find and fix all lines that are "        \n" (8 spaces + newline)
# in the sales_tab_prep section (lines 4770-5000)

fixed_count = 0
for i in range(4770, min(5000, len(lines))):
    if lines[i] == "        \n":
        lines[i] = "\n"
        fixed_count += 1
        print(f"Fixed line {i+1}")

print(f"\n✅ Fixed {fixed_count} empty lines with wrong indentation")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
