import os
import json

lessons_dir = 'data/lessons'
print("Sprawdzanie długości opisów lekcji:")
print("=" * 50)

for filename in sorted(os.listdir(lessons_dir)):
    if filename.endswith('.json') and not filename.startswith('lesson_template'):
        filepath = os.path.join(lessons_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                description = data.get('description', '')
                length = len(description)
                status = "✅ OK" if length <= 150 else "❌ ZA DŁUGI"
                print(f"{filename}")
                print(f"  Długość: {length} znaków {status}")
                print(f"  Opis: {description}")
                print()
        except Exception as e:
            print(f"{filename}: BŁĄD - {e}")
            print()
