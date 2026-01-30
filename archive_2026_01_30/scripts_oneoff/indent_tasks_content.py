"""Add indentation to tasks section content (inside expander)"""

file_path = r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py"

# Read file
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the tasks expander content (after 'with st.expander', before '# TAB: SPRZEDAŻ')
expander_start_marker = 'with st.expander(f"📋 Zadania onboardingowe {tasks_badge}"'
sales_marker = '# TAB: SPRZEDAŻ'

expander_idx = None
sales_idx = None

for i, line in enumerate(lines):
    if expander_start_marker in line and expander_idx is None:
        expander_idx = i + 1  # Start AFTER the expander line
    if sales_marker in line and sales_idx is None:
        sales_idx = i
        break

if expander_idx and sales_idx:
    print(f"Found tasks expander content: lines {expander_idx + 1} to {sales_idx}")
    print(f"Adding indentation to {sales_idx - expander_idx} lines")
    
    # Add 4 spaces to these lines
    for i in range(expander_idx, sales_idx):
        # Skip completely empty lines
        if lines[i].strip():
            lines[i] = "    " + lines[i]
    
    # Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("OK Indented tasks section content inside expander")
else:
    print(f"ERROR: Could not find markers. expander={expander_idx}, sales={sales_idx}")
