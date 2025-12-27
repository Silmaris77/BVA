#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sprawdzenie struktury obu lekcji v2.0
"""

import json

demo_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\DEMO_Lesson_V2_Full_Example.json'
lesson11_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json'

# Wczytaj oba pliki
with open(demo_path, 'r', encoding='utf-8') as f:
    demo = json.load(f)

with open(lesson11_path, 'r', encoding='utf-8') as f:
    lesson11 = json.load(f)

print("=== DEMO LESSON ===")
print(f"Template version: {demo.get('_template_info', {}).get('version', 'brak')}")
print(f"Główne klucze: {list(demo.keys())}")
print(f"\nStruktura:")
for key in ['wprowadzenie', 'nauka', 'praktyka', 'podsumowanie']:
    if key in demo:
        if isinstance(demo[key], dict):
            print(f"  ✅ {key}: {list(demo[key].keys())}")
        else:
            print(f"  ✅ {key}: {type(demo[key])}")
    else:
        print(f"  ❌ {key}: BRAK")

print("\n=== LEKCJA 11 ===")
print(f"Template version: {lesson11.get('_template_info', {}).get('version', 'brak')}")
print(f"Główne klucze: {list(lesson11.keys())}")
print(f"\nStruktura:")
for key in ['wprowadzenie', 'nauka', 'praktyka', 'podsumowanie']:
    if key in lesson11:
        if isinstance(lesson11[key], dict):
            print(f"  ✅ {key}: {list(lesson11[key].keys())}")
        else:
            print(f"  ✅ {key}: {type(lesson11[key])}")
    else:
        print(f"  ❌ {key}: BRAK")
