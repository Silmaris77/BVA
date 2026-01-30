# -*- coding: utf-8 -*-
"""
Add indentation to Dashboard sub-tabs content
"""

with open('views/business_games_refactored/industries/fmcg_playable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line: "st.markdown("### 🎯 Cele Tygodniowe")"
# From there until "st.subheader("⚠️ Alerty Reputacji")" needs +4 spaces (inside dash_stats)

goals_start = None
alerts_start = None

for i, line in enumerate(lines):
    if 'st.markdown("### 🎯 Cele Tygodniowe")' in line and i > 850:
        goals_start = i + 1  # Start from next line
    elif 'st.subheader("⚠️ Alerty Reputacji")' in line and i > 950:
        alerts_start = i
        break

if goals_start and alerts_start:
    print(f"Found goals code: lines {goals_start + 1} to {alerts_start}")
    print(f"Adding indentation to {alerts_start - goals_start} lines")
    
    # Add 4 spaces to each line in this range
    for i in range(goals_start, alerts_start):
        if lines[i].strip():  # Non-empty line
            lines[i] = "    " + lines[i]
    
    # Write back
    with open('views/business_games_refactored/industries/fmcg_playable.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("OK Indented goals section inside dash_stats")
else:
    print("ERROR Could not find boundaries")
    if not goals_start:
        print("  - Goals section not found")
    if not alerts_start:
        print("  - Alerts section not found")
