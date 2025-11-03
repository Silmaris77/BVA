"""
Fix the placement of route planning - it should be INSIDE sales_tab_map, not outside.
Currently it's at line ~2700 with 12 spaces indent but AFTER sales_tab_map ends.
Need to move it to BEFORE line 2684 (inside sales_tab_map).
"""

# Read the file
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where route planning currently is (after the move)
route_planning_marker = "            # Route planning section moved here from after sales_tab_visit\n"
route_planning_start_idx = None

for i, line in enumerate(lines):
    if line == route_planning_marker:
        route_planning_start_idx = i
        break

if route_planning_start_idx is None:
    print("ERROR: Could not find route planning section!")
    exit(1)

print(f"Found route planning at line {route_planning_start_idx + 1}")

# Find where it ends (before sales_tab_visit)
route_planning_end_idx = None
for i in range(route_planning_start_idx + 1, len(lines)):
    if "        with sales_tab_visit:" in lines[i]:
        route_planning_end_idx = i
        break

if route_planning_end_idx is None:
    print("ERROR: Could not find end of route planning section!")
    exit(1)

print(f"Route planning ends at line {route_planning_end_idx}")
print(f"Extracting {route_planning_end_idx - route_planning_start_idx} lines")

# Extract the route planning code
route_planning_code = lines[route_planning_start_idx:route_planning_end_idx]

# Find where sales_tab_map ends (looking for line with 8 spaces after route planning was removed)
# It should be around line 2693: "        # ======== OLD TAB: ROZMOWA"
sales_tab_map_end_idx = None
for i in range(1500, route_planning_start_idx):
    if "            # ======================================" in lines[i] and i > 2600:
        # Check if next few lines are comments about OLD TAB
        if i + 5 < len(lines) and "OLD TAB:" in lines[i + 1]:
            sales_tab_map_end_idx = i
            break

if sales_tab_map_end_idx is None:
    # Try alternative: find "if False:  # DISABLED CODE"
    for i in range(2600, route_planning_start_idx):
        if "            if False:  # DISABLED CODE" in lines[i]:
            sales_tab_map_end_idx = i - 3  # 3 lines before (before the comment block)
            break

if sales_tab_map_end_idx is None:
    print("ERROR: Could not find where to insert route planning!")
    print("Trying to find it manually...")
    for i in range(2680, 2695):
        print(f"Line {i+1}: {repr(lines[i][:80])}")
    exit(1)

print(f"Will insert route planning before line {sales_tab_map_end_idx + 1}")

# Rebuild file:
# 1. Lines 0 to sales_tab_map_end_idx - KEEP
# 2. Insert route planning HERE
# 3. Lines sales_tab_map_end_idx to route_planning_start_idx - KEEP  
# 4. SKIP lines route_planning_start_idx to route_planning_end_idx (old location)
# 5. Lines route_planning_end_idx onwards - KEEP

new_lines = []
new_lines.extend(lines[0:sales_tab_map_end_idx])
new_lines.append("\n")
new_lines.extend(route_planning_code)
new_lines.extend(lines[sales_tab_map_end_idx:route_planning_start_idx])
# SKIP route_planning_start_idx:route_planning_end_idx
new_lines.extend(lines[route_planning_end_idx:])

print(f"New file: {len(new_lines)} lines (was {len(lines)})")

# Write
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ Route planning moved inside sales_tab_map!")
