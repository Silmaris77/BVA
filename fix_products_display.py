"""
Fix indentation in products display code.
The display code (lines 4878+) should be at same level as the if/else blocks,
not inside the else block.
"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the line with "# Display count"
display_count_idx = None
for i in range(4870, 4890):
    if "# Display count" in lines[i]:
        display_count_idx = i
        break

if display_count_idx is None:
    print("ERROR: Could not find '# Display count'")
    exit(1)

print(f"Found '# Display count' at line {display_count_idx + 1}")
print(f"Current indentation: {len(lines[display_count_idx]) - len(lines[display_count_idx].lstrip())}")

# This section and everything after should have 12 spaces (same as "if is_heinz_scenario")
# Currently it has 16 spaces (inside the else block)

# Find where this section ends (before HR tab at ~5580)
section_end = None
for i in range(5550, 5600):
    if "# TAB: HR" in lines[i]:
        section_end = i
        break

if section_end is None:
    print("ERROR: Could not find HR tab")
    exit(1)

print(f"Section ends at line {section_end + 1}")

# Reduce indentation by 4 spaces for all lines from display_count_idx to section_end
fixed = 0
for i in range(display_count_idx, section_end):
    line = lines[i]
    if line.startswith("                "):  # 16+ spaces
        # Remove 4 spaces
        lines[i] = line[4:]
        fixed += 1

print(f"Fixed {fixed} lines")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Fixed product display indentation")
