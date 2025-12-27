import json

file_path = r"c:\Users\pksia\Dropbox\BVA\data\lessons\11_Conversational_Intelligence_V2_FULL.json"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        json.loads(content)
    print("✅ JSON is valid!")
except json.JSONDecodeError as e:
    print(f"❌ JSON Error at line {e.lineno}, column {e.colno}")
    print(f"Error: {e.msg}")
    print(f"\nContext around error:")
    
    # Show lines around the error
    lines = content.split('\n')
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)
    
    for i in range(start, end):
        marker = " >>> " if i == e.lineno - 1 else "     "
        print(f"{marker}{i+1:4d}: {lines[i]}")
