"""Remove duplicate route planning code that appears outside tab blocks"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the duplicate route planning block
# It starts around line 2770 with "# ROUTE PLANNING - Multi-select clients"
# and ends before "with sales_tab_prep:" at line 4729

start_marker = None
end_marker = None

for i, line in enumerate(lines):
    # Find start: "# ROUTE PLANNING - Multi-select clients + optimization"
    if "# ROUTE PLANNING - Multi-select clients + optimization" in line and i > 2700 and i < 2800:
        # Go back a few lines to include the previous comment/code
        start_marker = i - 5  # Include a few lines before for context
        print(f"Found duplicate route planning start at line {i + 1}")
        print(f"Will delete from line {start_marker + 1}")
    
    # Find end: "with sales_tab_prep:"
    if "with sales_tab_prep:" in line and i > 4700:
        end_marker = i  # Delete up to (but not including) this line
        print(f"Found sales_tab_prep at line {i + 1}")
        break

if start_marker is not None and end_marker is not None:
    # Check what we're about to delete
    deleted_lines = end_marker - start_marker
    print(f"\nWill delete {deleted_lines} lines ({start_marker + 1} to {end_marker})")
    
    # Show first and last line
    print(f"\nFirst line to delete: {repr(lines[start_marker][:60])}")
    print(f"Last line to delete: {repr(lines[end_marker - 1][:60])}")
    print(f"Line after deletion: {repr(lines[end_marker][:60])}")
    
    # Delete the block
    new_lines = lines[:start_marker] + lines[end_marker:]
    
    with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print(f"\n✅ Deleted {deleted_lines} duplicate lines")
    print(f"File now has {len(new_lines)} lines (was {len(lines)})")
else:
    print("❌ Could not find markers")
    if start_marker is None:
        print("  - Start marker not found")
    if end_marker is None:
        print("  - End marker not found")
