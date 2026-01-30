lines = open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11_Conversational_Intelligence_V2_FULL.json', 'r', encoding='utf-8').readlines()

# Find all keys in podsumowanie section  
in_podsumowanie = False
brace_count = 0

for i, line in enumerate(lines, 1):
    if '"podsumowanie":' in line:
        in_podsumowanie = True
        print(f"Line {i}: START podsumowanie")
        brace_count = 1
        continue
    
    if in_podsumowanie:
        # Count braces
        brace_count += line.count('{') - line.count('}')
        
        # Print keys at level 1 (direct children of podsumowanie)
        stripped = line.strip()
        if stripped.startswith('"') and ':' in stripped:
            # Count indent to determine level
            indent = len(line) - len(line.lstrip())
            if indent == 4:  # Level 1 (direct child of podsumowanie)
                key = stripped.split(':')[0].strip().strip('"')
                print(f"Line {i}: KEY '{key}'")
        
        # Exit when podsumowanie closes
        if brace_count == 0:
            print(f"Line {i}: END podsumowanie")
            break
