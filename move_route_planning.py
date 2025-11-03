"""
Move ROUTE PLANNING section from outside tabs to inside sales_tab_map
The code from line 2771 to line ~4720 needs to be moved inside sales_tab_map block
which starts at line 1471.

Strategy:
1. Find where sales_tab_map ends (before sales_tab_visit starts at 2698)
2. Move the ROUTE PLANNING section (lines 2771-4720) to just before line 2698
3. Add proper indentation (12 spaces instead of 8)
"""

# Read the file
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print(f"\nLine 2697 (before sales_tab_visit): {repr(lines[2696][:80])}")
print(f"Line 2698 (sales_tab_visit): {repr(lines[2697][:80])}")
print(f"Line 2771 (ROUTE PLANNING start): {repr(lines[2770][:80])}")
print(f"Line 4724 (before sales_tab_prep): {repr(lines[4723][:80])}")
print(f"Line 4728 (sales_tab_prep): {repr(lines[4727][:80])}")

# Extract the ROUTE PLANNING section (lines 2771-4723, indices 2770-4722)
route_planning_start = 2770  # Line 2771 (0-indexed)
route_planning_end = 4723    # Line 4724 (0-indexed, exclusive)

route_planning_code = lines[route_planning_start:route_planning_end]

print(f"\nExtracting {len(route_planning_code)} lines of ROUTE PLANNING code")

# This section needs to be moved to BEFORE line 2698 (sales_tab_visit)
# And needs to have indentation increased by 4 spaces (from 8 to 12)

# Increase indentation for route planning code
indented_route_planning = []
for line in route_planning_code:
    if line.strip():  # Non-empty line
        indented_route_planning.append("    " + line)
    else:
        indented_route_planning.append(line)

# Now rebuild the file:
# 1. Lines 0 to 2697 (everything before sales_tab_visit) - KEEP
# 2. Insert indented route planning code HERE
# 3. Lines 2697 to 2770 (sales_tab_visit start + its initial content) - KEEP
# 4. SKIP lines 2770-4722 (original route planning - already moved)
# 5. Lines 4723+ (sales_tab_prep onwards) - KEEP

new_lines = []
new_lines.extend(lines[0:2697])  # Before sales_tab_visit
new_lines.append("\n")
new_lines.append("            # Route planning section moved here from after sales_tab_visit\n")
new_lines.extend(indented_route_planning)  # Route planning with proper indent
new_lines.append("\n")
new_lines.extend(lines[2697:2770])  # sales_tab_visit block start
# SKIP lines[2770:4723] - this is the old route planning location
new_lines.extend(lines[4723:])  # Rest of file (sales_tab_prep onwards)

print(f"\nNew file will have {len(new_lines)} lines (was {len(lines)})")

# Write the new file
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ Route planning section moved to sales_tab_map!")
