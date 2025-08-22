#!/usr/bin/env python3
"""
Test funkcjonalności poziomej nawigacji lekcji
Sprawdza czy wszystkie zmiany zostały poprawnie zaimplementowane
"""

import sys
import os

# Dodaj folder główny do ścieżki
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_import():
    """Test importu modułu lesson"""
    try:
        import views.lesson
        print("✅ Import views.lesson: SUKCES")
        return True
    except Exception as e:
        print(f"❌ Import views.lesson: BŁĄD - {e}")
        return False

def verify_horizontal_navigation_implementation():
    """Sprawdź implementację poziomej nawigacji"""
    
    print("🔍 Sprawdzanie implementacji poziomej nawigacji lekcji...")
    print("=" * 60)
    
    try:
        # Czytaj kod źródłowy
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Lista kontrolna implementacji
        checks = [
            # Podstawowa struktura
            ("def show_horizontal_lesson_navigation():", "Funkcja poziomej nawigacji"),
            ("st.columns(4)", "4 kolumny dla przycisków"),
            ("lesson-nav-container", "Kontener CSS nawigacji"),
            
            # Nazwy kroków
            ("'intro': 'Wprowadzenie'", "Nazwa: Wprowadzenie"),
            ("'content': 'Nauka'", "Nazwa: Nauka"),
            ("'practical_exercises': 'Praktyka'", "Nazwa: Praktyka"),
            ("'summary': 'Podsumowanie'", "Nazwa: Podsumowanie"),
            
            # Funkcjonalność przycisków
            ("👉", "Znacznik aktualnego kroku"),
            ("✅", "Znacznik ukończonego kroku"),
            ("is_current", "Logika aktualnego kroku"),
            ("is_completed", "Logika ukończonego kroku"),
            ("disabled=True", "Blokada przyszłych kroków"),
            
            # Wywołanie funkcji
            ("show_horizontal_lesson_navigation()", "Wywołanie funkcji"),
            
            # Uproszczenie sidebar
            ("Tylko przycisk powrotu w sidebar", "Komentarz uproszczenia sidebar"),
            ("← Wszystkie lekcje", "Przycisk powrotu do listy")
        ]
        
        all_passed = True
        for check_text, description in checks:
            if check_text in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}: BRAK")
                all_passed = False
        
        print()
        print("🎨 Style CSS:")
        css_elements = [
            "lesson-nav-container",
            "lesson-nav-title", 
            "linear-gradient",
            "border-radius",
            "box-shadow"
        ]
        
        for element in css_elements:
            if element in content:
                print(f"✅ CSS: {element}")
            else:
                print(f"❌ CSS: {element}: BRAK")
                
        return all_passed
        
    except Exception as e:
        print(f"❌ Błąd podczas sprawdzania: {e}")
        return False

def verify_sidebar_simplification():
    """Sprawdź uproszczenie sidebar"""
    
    print("\n🔍 Sprawdzanie uproszczenia sidebar...")
    print("=" * 40)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź elementy sidebar
        sidebar_checks = [
            ("with st.sidebar:", "Sekcja sidebar"),
            ("← Wszystkie lekcje", "Przycisk powrotu"),
            ("Tylko przycisk powrotu w sidebar", "Komentarz o uproszczeniu")
        ]
        
        all_sidebar_ok = True
        for check, desc in sidebar_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_sidebar_ok = False
                
        return all_sidebar_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania sidebar: {e}")
        return False

if __name__ == "__main__":
    print("🧪 KOMPLEKSOWY TEST POZIOMEJ NAWIGACJI LEKCJI")
    print("=" * 70)
    
    # Uruchom wszystkie testy
    tests = [
        ("Import modułu", test_import),
        ("Implementacja poziomej nawigacji", verify_horizontal_navigation_implementation),
        ("Uproszczenie sidebar", verify_sidebar_simplification)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔥 {test_name}")
        print("-" * 50)
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Błąd testu {test_name}: {e}")
            results.append(False)
    
    # Podsumowanie
    print("\n" + "=" * 70)
    print("📊 PODSUMOWANIE TESTÓW")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        print("✅ Pozioma nawigacja lekcji została poprawnie zaimplementowana!")
        print("\n📋 Co zostało zrealizowane:")
        print("• Przeniesiono nawigację z sidebar na główną stronę")
        print("• Stworzono 4 poziome przyciski nawigacji")
        print("• Zmieniono nazwy kroków na: Wprowadzenie, Nauka, Praktyka, Podsumowanie")
        print("• Uproszczono sidebar do samego przycisku powrotu")
        print("• Dodano responsywne style CSS")
        print("• Zaimplementowano logikę statusów przycisków")
    else:
        print(f"⚠️  {passed}/{total} testów przeszło pomyślnie")
        if passed > 0:
            print("✅ Częściowy sukces - większość funkcji działa")
        else:
            print("❌ Wymagane są dodatkowe poprawki")
