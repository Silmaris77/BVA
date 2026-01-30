"""
Temporary script to migrate visit code from disabled block to active sales_tab_visit
"""

# Read the file
with open('views/business_games_refactored/industries/fmcg_playable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where to insert (after the placeholder in sales_tab_visit)
insert_idx = None
for i, line in enumerate(lines):
    if 'trwa migracja kodu' in line.lower() and i > 1400 and i < 1500:
        insert_idx = i + 1  # After the placeholder
        print(f"Found insertion point at line {i+1}: {line.strip()}")
        break

# Find source code in disabled block (starts with "# ROUTE PLANNING")  
source_start = None
for i, line in enumerate(lines):
    if i > 2900 and '# ROUTE PLANNING - Multi-select clients' in line:
        # Go back to find the "else:" that wraps this
        for j in range(i, max(0, i-20), -1):
            if lines[j].strip() == 'else:':
                source_start = j + 1  # Start after "else:"
                print(f"Found source start at line {j+1}: else: block")
                break
        break

# Find where disabled block ends (before "# DAY ADVANCEMENT" or HR section)
source_end = None
for i in range(len(lines)-1, 0, -1):
    if i > 4600 and ('# DAY ADVANCEMENT' in lines[i] or 'TAB: HR & TEAM' in lines[i]):
        source_end = i - 1
        print(f"Found source end at line {i}: {lines[i].strip()[:50]}")
        break

if insert_idx and source_start and source_end:
    print(f"\n✅ Migration plan:")
    print(f"   - Insert at line: {insert_idx}")
    print(f"   - Copy from line: {source_start} to {source_end}")
    print(f"   - Total lines to copy: {source_end - source_start}")
    
    # Extract source code
    source_code = lines[source_start:source_end]
    
    # Remove one level of indentation (was in if False: block)
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
        migrated_code +  # Migrated visit code
        lines[insert_idx:]  # Everything after (will remove placeholder later)
    )
    
    # Remove the placeholder line
    new_lines = [l for l in new_lines if 'trwa migracja kodu' not in l.lower()]
    
    # Write back
    with open('views/business_games_refactored/industries/fmcg_playable.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ Migration complete!")
    print(f"   - Added {len(migrated_code)} lines to sales_tab_visit")
    print(f"   - File updated successfully")
else:
    print(f"\n❌ Could not find migration points:")
    print(f"   - Insert index: {insert_idx}")
    print(f"   - Source start: {source_start}")
    print(f"   - Source end: {source_end}")
