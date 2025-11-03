"""Fix line 4814 - empty line with 8 spaces ends the with sales_tab_prep block"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Line 4813: {repr(lines[4812])}")
print(f"Line 4814: {repr(lines[4813])}")
print(f"Line 4815: {repr(lines[4814])}")

# Line 4814 (index 4813) is "        \n" - should be just "\n"
if lines[4813] == "        \n":
    lines[4813] = "\n"
    print("✅ Fixed line 4814")
else:
    print(f"ERROR: Line 4814 is not what we expected: {repr(lines[4813])}")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
