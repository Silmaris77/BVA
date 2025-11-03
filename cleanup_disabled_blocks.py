"""
Remove all disabled code blocks (if False: sections) from fmcg_playable.py
"""

# Read the file
with open('views/business_games_refactored/industries/fmcg_playable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Original file: {len(lines)} lines")

# Find all disabled blocks to remove
blocks_to_remove = []

# Find tab_clients disabled block
for i, line in enumerate(lines):
    if 'if False:  # Original tab_clients code - disabled' in line:
        start = i - 3  # Include comments before
        # Find end (next main section or HR tab)
        for j in range(i+1, len(lines)):
            if ('TAB: HR & TEAM' in lines[j] or 
                'if False:  # Original tab_products' in lines[j]):
                end = j
                blocks_to_remove.append((start, end, 'tab_clients'))
                print(f"Found tab_clients block: lines {start+1}-{end} ({end-start} lines)")
                break
        break

# Find tab_products disabled block  
for i, line in enumerate(lines):
    if 'if False:  # Original tab_products code - disabled' in line:
        start = i - 3  # Include comments before
        # Find end
        for j in range(i+1, len(lines)):
            if ('if False:  # DISABLED CODE - TO BE MIGRATED' in lines[j] or
                'if False:  # Original tab_conversation' in lines[j]):
                end = j
                blocks_to_remove.append((start, end, 'tab_products'))
                print(f"Found tab_products block: lines {start+1}-{end} ({end-start} lines)")
                break
        break

# Find tab_conversation disabled block
for i, line in enumerate(lines):
    if 'if False:  # Original tab_conversation code - disabled' in line:
        start = i - 3  # Include comments before
        # Find end (before DAY ADVANCEMENT or HR section)
        for j in range(i+1, len(lines)):
            if ('# DAY ADVANCEMENT' in lines[j] or 'TAB: HR & TEAM' in lines[j]):
                end = j
                blocks_to_remove.append((start, end, 'tab_conversation'))
                print(f"Found tab_conversation block: lines {start+1}-{end} ({end-start} lines)")
                break
        break

# Sort blocks by start line (descending) to remove from bottom to top
blocks_to_remove.sort(key=lambda x: x[0], reverse=True)

# Remove blocks
new_lines = lines.copy()
total_removed = 0

for start, end, name in blocks_to_remove:
    print(f"\nRemoving {name}: lines {start+1}-{end}")
    del new_lines[start:end]
    total_removed += (end - start)

print(f"\n[OK] Cleanup summary:")
print(f"   - Original: {len(lines)} lines")
print(f"   - Removed: {total_removed} lines")
print(f"   - New: {len(new_lines)} lines")
print(f"   - Reduction: {total_removed / len(lines) * 100:.1f}%")

# Write back
with open('views/business_games_refactored/industries/fmcg_playable.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n[OK] File cleaned successfully!")
