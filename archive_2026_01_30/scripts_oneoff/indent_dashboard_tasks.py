"""Add indentation to tasks/onboarding section to place it inside dash_tasks sub-tab"""

file_path = r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py"

# Read file
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find tasks section (starts at onboarding header, ends before "with tab_sales:")
start_marker = 'st.subheader("📋 Zadania i Onboarding")'
end_marker = 'with tab_sales:'

start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if start_marker in line and start_idx is None:
        start_idx = i
    if end_marker in line and start_idx is not None and end_idx is None:
        end_idx = i
        break

if start_idx and end_idx:
    print(f"Found tasks code: lines {start_idx} to {end_idx}")
    print(f"Adding indentation to {end_idx - start_idx} lines")
    
    # Add 4 spaces to these lines
    for i in range(start_idx, end_idx):
        lines[i] = "    " + lines[i]
    
    # Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("OK Indented tasks section inside dash_tasks")
else:
    print(f"ERROR: Could not find markers. start={start_idx}, end={end_idx}")
