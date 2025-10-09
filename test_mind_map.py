#!/usr/bin/env python
"""
Test funkcji mapy myśli dla lekcji 11
"""

import sys
import os

# Dodaj główny katalog do path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

import json
from utils.mind_map import create_lesson_mind_map

def test_mind_map():
    """Test mapy myśli dla lekcji 11"""
    
    print("🧪 Test mapy myśli dla lekcji 'Od słów do zaufania'")
    print("=" * 60)
    
    # Załaduj dane lekcji
    try:
        with open('data/lessons/11. Od słów do zaufania - Conversational Intelligence.json', 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)
        
        print(f"✅ Załadowano lekcję: {lesson_data.get('title', 'Unknown')}")
        
        # Sprawdź obecność mind_map
        has_mind_map_direct = 'mind_map' in lesson_data
        has_mind_map_summary = 'summary' in lesson_data and 'mind_map' in lesson_data.get('summary', {})
        
        print(f"📊 mind_map bezpośrednio: {has_mind_map_direct}")
        print(f"📊 mind_map w summary: {has_mind_map_summary}")
        
        if has_mind_map_summary:
            mind_map_data = lesson_data['summary']['mind_map']
            print(f"🎯 Centralny węzeł: {mind_map_data.get('central_node', {}).get('label', 'Unknown')}")
            print(f"📝 Liczba kategorii: {len(mind_map_data.get('categories', []))}")
            print(f"🔗 Liczba połączeń: {len(mind_map_data.get('relationships', []))}")
        
        # Spróbuj utworzyć mapę myśli
        print(f"\n🛠️ Tworzenie mapy myśli...")
        result = create_lesson_mind_map(lesson_data)
        
        print(f"🔍 Result type: {type(result)}")
        print(f"🔍 Result bool: {bool(result)}")
        print(f"🔍 Result is None: {result is None}")
        
        if result is not None:
            print(f"✅ Mapa myśli została utworzona pomyślnie!")
        else:
            print(f"❌ Nie udało się utworzyć mapy myśli")
            
    except Exception as e:
        print(f"❌ Błąd: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mind_map()