import json

try:
    with open(r'c:\Users\pksia\Dropbox\BVA\data\lessons\MILWAUKEE_Application_First_Canvas.json', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ JSON poprawny!")
    print(f"   - Kluczy: {len(data)}")
    print(f"   - Sekcji: {len(data.get('sections', []))}")
    print(f"   - Tytuł: {data.get('title', 'BRAK')}")
    
except json.JSONDecodeError as e:
    print(f"❌ Błąd JSON: {e}")
except Exception as e:
    print(f"❌ Błąd: {e}")
