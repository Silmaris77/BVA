content = open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\11_Conversational_Intelligence_V2_FULL.json', 'r', encoding='utf-8').read()

# Count all braces
total_open = content.count('{')
total_close = content.count('}')

print(f"Total opening braces: {total_open}")
print(f"Total closing braces: {total_close}")
print(f"Difference: {total_open - total_close}")

if total_open != total_close:
    print("\n❌ MISMATCHED BRACES!")
    if total_open > total_close:
        print(f"Missing {total_open - total_close} closing brace(s)")
    else:
        print(f"Extra {total_close - total_open} closing brace(s)")
else:
    print("\n✅ Braces are balanced")
