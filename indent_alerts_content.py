"""Add indentation to alerts and tasks sections"""

file_path = r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py"

# Read file
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the alerts content section (after st.subheader, before with dash_tasks:)
alerts_start_marker = 'st.subheader("⚠️ Alerty Reputacji")'
tasks_start_marker = 'with dash_tasks:'

alerts_start_idx = None
tasks_start_idx = None

for i, line in enumerate(lines):
    if alerts_start_marker in line and alerts_start_idx is None:
        alerts_start_idx = i + 1  # Start AFTER the subheader line
    if tasks_start_marker in line and tasks_start_idx is None:
        tasks_start_idx = i
        break

if alerts_start_idx and tasks_start_idx:
    print(f"Found alerts content: lines {alerts_start_idx + 1} to {tasks_start_idx}")
    print(f"Adding indentation to {tasks_start_idx - alerts_start_idx} lines")
    
    # Add 4 spaces to these lines (skip empty comment lines)
    for i in range(alerts_start_idx, tasks_start_idx):
        # Skip completely empty lines, but indent others
        if lines[i].strip():  # If line has content
            lines[i] = "    " + lines[i]
    
    # Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("OK Indented alerts section inside dash_alerts")
else:
    print(f"ERROR: Could not find markers. alerts_start={alerts_start_idx}, tasks_start={tasks_start_idx}")
