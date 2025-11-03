"""
Remove duplicate congratulations message (lines 4720-4727) 
and ensure sales_tab_visit block continues properly
"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Lines 4720-4728 are duplicate:
# Line 4720: "        # Show congratulations..."  
# Line 4721-4727: Duplicate congratulations code
# Line 4728: empty
# Line 4729: "        # ======== SUB-TAB: PRZYGOTOWANIE"

# Remove lines 4719-4728 (indices 4718-4727)
# Line 4719 is "                # Rest of visit code continues..."

print("Before removal:")
for i in range(4718, 4730):
    print(f"{i+1}: {repr(lines[i][:60])}")

# Remove duplicate lines
del lines[4718:4728]  # Remove 10 lines

print(f"\nRemoved 10 lines")
print(f"New total: {len(lines)} lines")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Removed duplicate congratulations code")
