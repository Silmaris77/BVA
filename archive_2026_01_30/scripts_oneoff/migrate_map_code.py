"""
Migrate client map/list code from disabled tab_clients to active sales_tab_map
"""

# Read the file
with open('views/business_games_refactored/industries/fmcg_playable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find insertion point (in sales_tab_map, after "# TODO: Przenieść kod z tab_clients")
insert_idx = None
for i, line in enumerate(lines):
    if 'TODO: Przenieść kod z tab_clients' in line and i > 1390 and i < 1410:
        insert_idx = i + 1  # After the TODO comment
        print(f"Found insertion point at line {i+1}: {line.strip()}")
        break

# Find source code start (tab_clients disabled block)
source_start = None
for i, line in enumerate(lines):
    if 'if False:  # Original tab_clients code - disabled' in line and i > 3700:
        source_start = i + 1  # Start after the "if False:"
        print(f"Found source start at line {i+1}")
        break

# Find source code end (before tab_products)
source_end = None
for i, line in enumerate(lines):
    if 'if False:  # Original tab_products code - disabled' in line and i > 4400:
        # Go back to find the previous section end
        for j in range(i-1, max(0, i-50), -1):
            if lines[j].strip() and not lines[j].strip().startswith('#'):
                source_end = j + 1
                print(f"Found source end at line {j+1}: {lines[j].strip()[:60]}")
                break
        break

if insert_idx and source_start and source_end:
    print(f"\n✅ Migration plan:")
    print(f"   - Insert at line: {insert_idx}")
    print(f"   - Copy from line: {source_start} to {source_end}")
    print(f"   - Total lines to copy: {source_end - source_start}")
    
    # Extract source code
    source_code = lines[source_start:source_end]
    
    # Remove one level of indentation (was in if False: block - 4 spaces)
    migrated_code = []
    for line in source_code:
        if line.strip():  # Non-empty line
            # Remove 4 spaces of indentation
            if line.startswith('        '):
                migrated_code.append(line[4:])
            else:
                migrated_code.append(line)
        else:
            migrated_code.append(line)
    
    # Build new file
    new_lines = (
        lines[:insert_idx] +  # Everything before insertion point
        migrated_code +  # Migrated client map code
        lines[insert_idx:]  # Everything after
    )
    
    # Remove the TODO placeholder line
    new_lines = [l for l in new_lines if 'TODO: Przenieść kod z tab_clients' not in l]
    
    # Write back
    with open('views/business_games_refactored/industries/fmcg_playable.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ Migration complete!")
    print(f"   - Added {len(migrated_code)} lines to sales_tab_map")
    print(f"   - File updated successfully")
else:
    print(f"\n❌ Could not find migration points:")
    print(f"   - Insert index: {insert_idx}")
    print(f"   - Source start: {source_start}")
    print(f"   - Source end: {source_end}")
