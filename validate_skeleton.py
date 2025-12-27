import json

file_path = r"c:\Users\pksia\Dropbox\BVA\data\lessons\11_Conversational_Intelligence_V2_SKELETON.json"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("✅ Szkielet JSON jest poprawny!")
    print(f"Tytuł: {data['title']}")
    print(f"Sekcje główne: wprowadzenie, nauka, praktyka, podsumowanie")
    print(f"Status: {data['_template_info']['status']}")
except Exception as e:
    print(f"❌ Błąd: {e}")
