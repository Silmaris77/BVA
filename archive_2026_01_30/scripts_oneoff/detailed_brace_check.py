lines = open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11_Conversational_Intelligence_V2_FULL.json', 'r', encoding='utf-8').readlines()

balance = 0
for i, line in enumerate(lines, 1):
    opens = line.count('{')
    closes = line.count('}')
    
    balance += opens - closes
    
    if i >= 295 and i <= 310:
        print(f"Line {i}: opens={opens}, closes={closes}, balance={balance:+3d} | {line.rstrip()[:80]}")

print(f"\nFinal balance: {balance}")
