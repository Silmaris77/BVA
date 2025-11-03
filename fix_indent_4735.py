"""
Fix indentation error at line 4734-4735 in fmcg_playable.py
The problem: line 4734 has extra indent, causing line 4735 to have wrong indent
"""

# Read the file
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Check current state
print(f"Line 4733 (index 4732): {repr(lines[4732])}")
print(f"Line 4734 (index 4733): {repr(lines[4733])}")
print(f"Line 4735 (index 4734): {repr(lines[4734])}")
print(f"Line 4736 (index 4735): {repr(lines[4735])}")

# Fix: Remove extra indentation from line 4734 onwards
# Line 4734 should be empty with just \n
# Line 4735 should start with "            # Dynamic header" (12 spaces, same as line 4732)

# Count leading spaces
def count_leading_spaces(line):
    return len(line) - len(line.lstrip(' '))

line_4732_indent = count_leading_spaces(lines[4732])  # "# Check if Heinz scenario"
print(f"\nLine 4732 has {line_4732_indent} leading spaces")

# Line 4733 (empty line) should have no content
lines[4733] = "\n"

# Lines 4734+ currently have too much indent - need to reduce by 4 spaces
# But only if they currently have more indent than line 4732
for i in range(4734, min(4800, len(lines))):  # Check next ~65 lines
    if lines[i].strip():  # Non-empty line
        current_indent = count_leading_spaces(lines[i])
        if current_indent > line_4732_indent:
            # Remove 4 extra spaces
            lines[i] = lines[i][4:]

# Write back
with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Fixed indentation around line 4735")
