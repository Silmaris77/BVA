"""
Migrate product catalog code from disabled tab_products to active sales_tab_products
"""

# Read the file
with open('views/business_games_refactored/industries/fmcg_playable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find insertion point (in sales_tab_products, after subheader)
insert_idx = None
for i, line in enumerate(lines):
    if 'with sales_tab_products:' in line:
        # Find next line after subheader
        for j in range(i+1, min(i+10, len(lines))):
            if 'st.subheader' in lines[j]:
                insert_idx = j + 1  # After subheader
                print(f"Found insertion point at line {j+1}")
                break
        break

# Find source code start (tab_products disabled block)
source_start = None
for i, line in enumerate(lines):
    if 'if False:  # Original tab_products code - disabled' in line and i > 5000:
        source_start = i + 1  # Start after the "if False:"
        print(f"Found source start at line {i+1}")
        break

# Find source code end (before tab_conversation or next section)
source_end = None
for i, line in enumerate(lines):
    if i > source_start and i < 6500:
        if ('if False:  # Original tab_conversation' in line or 
            'if False:  # DISABLED CODE - TO BE MIGRATED' in line):
            # Go back to find the previous content end
            for j in range(i-1, max(0, i-20), -1):
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
        migrated_code +  # Migrated product catalog code
        lines[insert_idx:]  # Everything after
    )
    
    # Remove placeholder if exists
    new_lines = [l for l in new_lines if not ('trwa migracja kodu z zakładki Produkty' in l.lower())]
    
    # Write back
    with open('views/business_games_refactored/industries/fmcg_playable.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ Migration complete!")
    print(f"   - Added {len(migrated_code)} lines to sales_tab_products")
    print(f"   - File updated successfully")
else:
    print(f"\n❌ Could not find migration points:")
    print(f"   - Insert index: {insert_idx}")
    print(f"   - Source start: {source_start}")
    print(f"   - Source end: {source_end}")
