import json

with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', encoding='utf-8') as f:
    canvas = json.load(f)

print("✅ JSON VALID!")
print(f"\nPola w root: {list(canvas.keys())}")
print(f"\nTytuł: {canvas['title']}")
print(f"Kategoria: {canvas.get('category')}")
print(f"\nMa intro: {'intro' in canvas}")
print(f"Ma sections: {'sections' in canvas}")
print(f"Ma exercises: {'exercises' in canvas}")
print(f"Ma summary: {'summary' in canvas}")

if 'intro' in canvas:
    print(f"\nIntro pola: {list(canvas['intro'].keys())}")
if 'sections' in canvas:
    print(f"Sections pola: {list(canvas['sections'].keys())}")
    if 'learning' in canvas['sections']:
        print(f"  - learning ma {len(canvas['sections']['learning'])} elementów")
if 'summary' in canvas and 'main' in canvas['summary']:
    print(f"\nSummary.main długość: {len(canvas['summary']['main'])} znaków")
