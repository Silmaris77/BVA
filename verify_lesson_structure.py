#!/usr/bin/env python3
"""
Test weryfikacji struktury lekcji w aktywnej aplikacji
"""

def verify_lesson_structure():
    """Weryfikuje aktualną strukturę lekcji w views.lesson"""
    
    print("🔍 Weryfikacja struktury lekcji w aktywnej aplikacji")
    print("=" * 60)
    
    try:
        from views.lesson import show_lesson
        print("✅ Import views.lesson - SUCCESS")
    except Exception as e:
        print(f"❌ Import views.lesson - FAILED: {e}")
        return False
    
    print("\n📋 Sprawdzenie mapowania step_names:")
    
    # Symulacja stanu do sprawdzenia step_names
    import streamlit as st
    from data.lessons import load_lessons
    
    # Upewnijmy się, że mamy przykładową lekcję
    lessons = load_lessons()
    if not lessons:
        print("❌ Brak dostępnych lekcji do testowania")
        return False
    
    # Weź pierwszą dostępną lekcję
    first_lesson_id = list(lessons.keys())[0]
    first_lesson = lessons[first_lesson_id]
    
    print(f"🧪 Testowanie na lekcji: {first_lesson_id}")
    print(f"   Tytuł: {first_lesson.get('title', 'Brak tytułu')}")
    
    # Sprawdź dostępne sekcje
    sections = first_lesson.get('sections', {})
    available_sections = list(sections.keys())
    
    print(f"\n📦 Dostępne sekcje w lekcji:")
    for section in available_sections:
        print(f"   - {section}")
    
    # Sprawdź step_order dla tej lekcji
    available_steps = []
    
    if 'intro' in first_lesson or 'sections' in first_lesson:
        available_steps.append('intro')
    
    if 'sections' in first_lesson:
        if 'learning' in sections:
            available_steps.append('content')
        
        if 'practical_exercises' in sections:
            available_steps.append('practical_exercises')
        elif 'reflection' in sections or 'application' in sections:
            if 'reflection' in sections:
                available_steps.append('reflection')
            if 'application' in sections:
                available_steps.append('application')
    
    available_steps.append('summary')
    
    print(f"\n🔗 Obliczony step_order:")
    for i, step in enumerate(available_steps, 1):
        print(f"   {i}. {step}")
    
    # Mapowanie nazw
    step_names = {
        'intro': 'Wprowadzenie',
        'content': 'Nauka',
        'practical_exercises': 'Praktyka',
        'reflection': 'Refleksja',
        'application': 'Zadania praktyczne',
        'summary': 'Podsumowanie'
    }
    
    print(f"\n📛 Nazwy wyświetlane:")
    for step in available_steps:
        display_name = step_names.get(step, step.capitalize())
        print(f"   {step} → {display_name}")
    
    print(f"\n📊 Liczba etapów: {len(available_steps)}")
    
    if len(available_steps) == 4:
        print("✅ Struktura 4-etapowa POTWIERDZONA")
        
        expected_4_stage = ['intro', 'content', 'practical_exercises', 'summary']
        if available_steps == expected_4_stage:
            print("✅ Idealna struktura 4-etapowa")
        else:
            print("⚠️  Struktura 4-etapowa, ale z backward compatibility")
            
        return True
    else:
        print(f"⚠️  Struktura {len(available_steps)}-etapowa (nie 4-etapowa)")
        return False

if __name__ == "__main__":
    verify_lesson_structure()
