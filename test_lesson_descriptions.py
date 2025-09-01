#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test sprawdzający, czy zaktualizowane opisy lekcji są prawidłowe.
"""

import json
import os
import sys

# Dodaj główny katalog do ścieżki
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_lesson_descriptions():
    """Test czy opisy lekcji zostały prawidłowo zaktualizowane"""
    
    print("🧪 Test opisów lekcji")
    print("=" * 50)
    
    lesson_files = [
        "data/lessons/8. Kondycja mózgu.json",
        "data/lessons/2. Chemia mózgu.json", 
        "data/lessons/1. Mózg emocjonalny copy.json",
        "data/lessons/5. Stres i odporność psychiczna.json",
        "data/lessons/4. Model SEEDS.json",
        "data/lessons/7. Pamięć i uwaga.json",
        "data/lessons/6. Podejmowanie decyzji i ryzyko.json",
        "data/lessons/3. Model SCARF.json"
    ]
    
    for lesson_file in lesson_files:
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            title = data.get('title', 'Brak tytułu')
            description = data.get('description', 'Brak opisu')
            
            print(f"✅ {os.path.basename(lesson_file)}")
            print(f"   Tytuł: {title}")
            print(f"   Opis: {description[:100]}{'...' if len(description) > 100 else ''}")
            print()
            
        except Exception as e:
            print(f"❌ Błąd w {lesson_file}: {e}")
            
    print("✅ Test zakończony!")

if __name__ == "__main__":
    test_lesson_descriptions()
