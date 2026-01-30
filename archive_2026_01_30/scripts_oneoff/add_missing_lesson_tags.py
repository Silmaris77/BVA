#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dodanie tagów dla brakujących lekcji
"""

import json
from pathlib import Path

tags_path = Path(r'c:\Users\pksia\Dropbox\BVA\config\resource_tags.json')

# Wczytaj tagi
with open(tags_path, 'r', encoding='utf-8') as f:
    tags = json.load(f)

# Dodaj brakujące lekcje
new_tags = {
    # Lekcje v2.0
    "11. Od słów do zaufania - Conversational Intelligence V2": ["General", "Warta", "Heinz", "Milwaukee"],
    "DEMO_Lesson_V2_Full_Example": ["General"],
    
    # Backupy i szablony - tylko General (do testów)
    "1. Mózg emocjonalny copy": ["General"],
    "11. Od słów do zaufania - Conversational Intelligence_NEW": ["General"],
    "MILWAUKEE_Application_First_Canvas_original": ["Milwaukee"],
    "MILWAUKEE_Application_First_Canvas_v1_backup": ["Milwaukee"],
    "lesson_template": ["General"],
    "lesson_template_v2": ["General"]
}

# Dodaj do istniejących tagów
for lesson_name, lesson_tags in new_tags.items():
    if lesson_name not in tags['lessons']:
        tags['lessons'][lesson_name] = lesson_tags
        print(f"✅ Dodano: {lesson_name} → {lesson_tags}")
    else:
        print(f"⚠️  Już istnieje: {lesson_name}")

# Zapisz
with open(tags_path, 'w', encoding='utf-8') as f:
    json.dump(tags, f, indent=2, ensure_ascii=False)

print(f"\n✅ Zapisano {len(new_tags)} nowych tagów do resource_tags.json")
print(f"📊 Łącznie lekcji z tagami: {len(tags['lessons'])}")
