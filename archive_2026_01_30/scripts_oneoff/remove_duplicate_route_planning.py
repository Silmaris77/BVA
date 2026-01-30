"""Remove duplicate route planning code (lines 2770-4728) that appears outside tab blocks"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Original file: {len(lines)} lines")

# Find the duplicate block boundaries
# Should start around line 2770 (after sales_tab_visit ends)
# Should end around line 4728 (before sales_tab_prep starts)

duplicate_start = None
duplicate_end = None

for i, line in enumerate(lines):
    # Look for the start of duplicate route planning (after sales_tab_visit block ends)
    if i > 2760 and i < 2780 and "# =========" in line and i + 1 < len(lines):
        next_line = lines[i + 1]
        if "Planowanie trasy" in next_line or "PLANOWANIE TRASY" in next_line:
            duplicate_start = i
            print(f"Found duplicate route planning start at line {i + 1}: {line.strip()}")
            break

if not duplicate_start:
    # Alternative: look for specific marker
    for i, line in enumerate(lines):
        if i > 2760 and i < 2780 and "Planowanie trasy" in line:
            # Go back to find the header
            for j in range(i - 1, max(0, i - 10), -1):
                if "# =========" in lines[j]:
                    duplicate_start = j
                    print(f"Found duplicate route planning start at line {j + 1}")
                    break
            if duplicate_start:
                break

# Find where sales_tab_prep starts
for i, line in enumerate(lines):
    if i > 4720 and "with sales_tab_prep:" in line:
        duplicate_end = i
        print(f"Found sales_tab_prep at line {i + 1}")
        break

if duplicate_start and duplicate_end:
    print(f"\n🗑️ Removing lines {duplicate_start + 1} to {duplicate_end}")
    print(f"   Total lines to remove: {duplicate_end - duplicate_start}")
    
    # Remove the duplicate block
    new_lines = lines[:duplicate_start] + lines[duplicate_end:]
    
    print(f"New file: {len(new_lines)} lines")
    print(f"Removed: {len(lines) - len(new_lines)} lines")
    
    with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print("✅ Duplicate route planning code removed")
else:
    print(f"❌ Could not find boundaries: start={duplicate_start}, end={duplicate_end}")
    if not duplicate_start:
        print("\nSearching for any line with 'Planowanie trasy' around line 2770:")
        for i in range(2760, 2790):
            if i < len(lines) and "Planowanie" in lines[i]:
                print(f"  Line {i + 1}: {lines[i].strip()}")
