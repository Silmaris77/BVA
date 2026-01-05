#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sprawdzenie czy wszystkie lekcje mają tagi
"""

import json
from pathlib import Path

# Ścieżki
lessons_dir = Path(r'c:\Users\pksia\Dropbox\BVA\data\lessons')
tags_path = Path(r'c:\Users\pksia\Dropbox\BVA\config\resource_tags.json')

# Wczytaj tagi
with open(tags_path, 'r', encoding='utf-8') as f:
    tags = json.load(f)

lesson_tags = tags['lessons']

# Pobierz wszystkie pliki lekcji
lesson_files = list(lessons_dir.glob('*.json'))

print(f"=== ANALIZA TAGOWANIA LEKCJI ===\n")
print(f"Znalezionych plików lekcji: {len(lesson_files)}")
print(f"Lekcji z tagami w config: {len(lesson_tags)}\n")

# Sprawdź które lekcje nie mają tagów
missing_tags = []
for lesson_file in lesson_files:
    lesson_name = lesson_file.stem  # Nazwa bez rozszerzenia
    if lesson_name not in lesson_tags:
        missing_tags.append(lesson_name)

if missing_tags:
    print(f"❌ LEKCJE BEZ TAGÓW ({len(missing_tags)}):")
    for lesson in sorted(missing_tags):
        print(f"  - {lesson}")
else:
    print("✅ Wszystkie lekcje mają przypisane tagi!")

# Pokaż lekcje v2.0
print("\n=== LEKCJE V2.0 ===")
v2_lessons = [name for name in lesson_tags.keys() if 'V2' in name or 'DEMO' in name]
for lesson in sorted(v2_lessons):
    print(f"  {lesson}: {lesson_tags[lesson]}")
