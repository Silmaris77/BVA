"""
Fix indentation in fmcg_playable.py for sales_tab_prep block.
All code from line 4734 to line ~5510 needs to be indented by 4 spaces.
"""

# Read the file
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Fix indentation from line 4734 (index 4733) to line 5510 (index 5509)
# Add 4 spaces to each line in this range
START_LINE = 4733  # 0-indexed
END_LINE = 5509    # 0-indexed (exclusive)

for i in range(START_LINE, min(END_LINE, len(lines))):
    # Only add indentation to non-empty lines
    if lines[i].strip():
        lines[i] = "    " + lines[i]

# Write back
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"✅ Fixed indentation for lines {START_LINE+1} to {min(END_LINE, len(lines))+1}")
