"""Fix empty line with wrong indentation at line 4744"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Line 4743: {repr(lines[4742])}")
print(f"Line 4744: {repr(lines[4743])}")
print(f"Line 4745: {repr(lines[4744])}")
print(f"Line 4746: {repr(lines[4745])}")

# Line 4744 is "        \n" (8 spaces) - should be just "\n" or have 12 spaces
# This line ends the `with sales_tab_prep:` block prematurely!

# Replace it with proper empty line (no spaces)
lines[4743] = "\n"

print("\n✅ Fixed line 4744 - removed extra spaces from empty line")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
