#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analiza struktury wszystkich lekcji - gdzie jest practical_exercises
"""

import json
import glob
import os

def analyze_lessons():
    """Przeanalizuj strukturę wszystkich lekcji"""
    
    lesson_files = sorted(glob.glob('data/lessons/*.json'))
    
    print(f"\n{'='*100}")
    print(f"ANALIZA STRUKTURY LEKCJI - practical_exercises")
    print(f"{'='*100}\n")
    print(f"{'Plik':<60} | {'Top-level':<10} | {'In sections':<12} | {'In learning':<12}")
    print(f"{'-'*60}|{'-'*11}|{'-'*13}|{'-'*12}")
    
    stats = {
        'total': 0,
        'top_level': 0,
        'in_sections': 0,
        'in_learning': 0,
        'missing': 0
    }
    
    for filepath in lesson_files:
        stats['total'] += 1
        filename = os.path.basename(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lesson = json.load(f)
            
            has_top = 'practical_exercises' in lesson
            has_sections = 'practical_exercises' in lesson.get('sections', {})
            has_learning = False
            if 'sections' in lesson and 'learning' in lesson['sections']:
                has_learning = 'practical_exercises' in lesson['sections']['learning']
            
            # Stats
            if has_top:
                stats['top_level'] += 1
            if has_sections:
                stats['in_sections'] += 1
            if has_learning:
                stats['in_learning'] += 1
            if not (has_top or has_sections or has_learning):
                stats['missing'] += 1
            
            # Display
            top_mark = '✅' if has_top else '❌'
            sec_mark = '✅' if has_sections else '❌'
            learn_mark = '✅' if has_learning else '❌'
            
            print(f"{filename:<60} | {top_mark:<10} | {sec_mark:<12} | {learn_mark:<12}")
            
        except Exception as e:
            print(f"{filename:<60} | ERROR: {str(e)}")
    
    print(f"\n{'='*100}")
    print(f"PODSUMOWANIE:")
    print(f"{'='*100}")
    print(f"Łącznie lekcji: {stats['total']}")
    print(f"✅ practical_exercises na TOP-LEVEL: {stats['top_level']}")
    print(f"⚠️  practical_exercises w SECTIONS: {stats['in_sections']}")
    print(f"⚠️  practical_exercises w SECTIONS.LEARNING: {stats['in_learning']}")
    print(f"❌ BRAK practical_exercises: {stats['missing']}")
    print(f"{'='*100}\n")
    
    return stats

if __name__ == "__main__":
    stats = analyze_lessons()
    
    print("\n💡 REKOMENDACJA:")
    print("="*100)
    print("STANDARD: practical_exercises powinno być na TOP-LEVEL (obok intro, sections, summary)")
    print("ACTION: Lekcje z practical_exercises w sections/learning należy przenieść na top-level")
    print("="*100)
