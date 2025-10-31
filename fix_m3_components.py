"""
Quick script to refactor material3_components.py
"""

# Read the original file
with open('utils/material3_components.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where apply_material3_theme starts
apply_theme_line = None
for i, line in enumerate(lines):
    if 'def apply_material3_theme():' in line:
        apply_theme_line = i
        break

print(f"Total lines: {len(lines)}")
print(f"apply_material3_theme at line: {apply_theme_line + 1}")

# Create new content
new_content = []

# Keep first 11 lines (imports + first 2 functions)
new_content.extend(lines[:11])

# Add simplified m3_lesson_card_styles
new_content.append('def m3_lesson_card_styles():\n')
new_content.append('    """Style kart są teraz w static/css/core/components.css"""\n')
new_content.append('    pass\n')
new_content.append('\n')

# Add simplified apply_material3_theme
new_content.append('def apply_material3_theme():\n')
new_content.append('    """Aplikuje wszystkie style Material 3 przez ThemeManager"""\n')
new_content.append('    ThemeManager.apply_all()\n')
new_content.append('\n')
new_content.append('\n')

# Find where helper functions start (m3_card)
helper_start = None
for i, line in enumerate(lines):
    if 'def m3_card(' in line:
        helper_start = i
        break

print(f"Helper functions start at line: {helper_start + 1}")

# Add header before helpers
new_content.append('# ========================================\n')
new_content.append('# FUNKCJE HELPER (zachowane dla kompatybilności)\n')
new_content.append('# ========================================\n')
new_content.append('\n')

# Add all helper functions
if helper_start:
    new_content.extend(lines[helper_start:])

# Write new file
with open('utils/material3_components.py', 'w', encoding='utf-8') as f:
    f.writelines(new_content)

print("File refactored successfully!")
print(f"New file has {len(new_content)} lines")
