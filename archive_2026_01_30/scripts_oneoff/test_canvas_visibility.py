"""Test canvas lesson visibility"""
import sys
import json
sys.path.insert(0, '.')

from data.lessons import load_lessons

# Load lessons
lessons = load_lessons()
print(f"Total lessons loaded: {len(lessons)}")

# Check Milwaukee lessons
mil_lessons = [k for k in lessons.keys() if 'MILWAUKEE' in k.upper()]
print(f"\nMilwaukee lessons in load_lessons(): {mil_lessons}")

# Check specific lesson
canvas_id = "MILWAUKEE_Application_First_Canvas"
if canvas_id in lessons:
    canvas = lessons[canvas_id]
    print(f"\n✅ Canvas lesson FOUND in lessons dict")
    print(f"   Title: {canvas.get('lesson', {}).get('title', 'NO_TITLE')}")
    print(f"   Category: {canvas.get('metadata', {}).get('category', 'NO_CATEGORY')}")
else:
    print(f"\n❌ Canvas lesson NOT FOUND in lessons dict")

# Check tags manually
print(f"\n--- Resource Tags Check ---")
with open('config/resource_tags.json', encoding='utf-8') as f:
    resource_tags = json.load(f)
    
tags = resource_tags.get('lessons', {}).get(canvas_id, [])
print(f"Tags for {canvas_id}: {tags}")

# Check access logic
print(f"\n--- Access Check for mil2 ---")
user_company = 'Milwaukee'

print(f"Filter logic:")
print(f"  user_company: {user_company}")
print(f"  lesson tags: {tags}")
print(f"  'Milwaukee' in tags: {'Milwaukee' in tags}")
print(f"  'General' in tags: {'General' in tags}")
print(f"  Should be visible: {user_company in tags or 'General' in tags}")

