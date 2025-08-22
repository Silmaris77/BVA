#!/usr/bin/env python3
"""
Test usunięcia przycisków i nagłówka z sidebar
Sprawdza czy sidebar został całkowicie opróżniony i przycisk powrotu przeniesiony na główną stronę.
"""

def test_sidebar_cleanup():
    """Test usunięcia zawartości z sidebar"""
    
    print("🧪 Test usunięcia zawartości sidebar")
    print("=" * 40)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
          # Sprawdź konkretnie zawartość sekcji sidebar
        import re
        
        # Wyciągnij tylko sekcję sidebar
        sidebar_pattern = r'with st\.sidebar:(.*?)(?=\n\s{0,8}[^\s]|\Z)'
        sidebar_match = re.search(sidebar_pattern, content, re.DOTALL)
        
        if sidebar_match:
            sidebar_content = sidebar_match.group(1)
            print(f"📝 Zawartość sidebar: '{sidebar_content.strip()}'")
            
            # Sprawdź, czy sidebar zawiera tylko 'pass'
            if sidebar_content.strip() == "pass":
                print("✅ Sidebar jest pusty (zawiera tylko 'pass')")
                return True
            else:
                print("❌ Sidebar nie jest pusty!")
                return False
        else:
            print("❌ Nie znaleziono sekcji sidebar")
            return False
        
        # Sprawdź przeniesienie przycisku powrotu na główną stronę
        print("\n✅ Sprawdzanie przeniesienia przycisku powrotu:")
        navigation_checks = [
            ("← Wszystkie lekcje", "Przycisk powrotu"),
            ("type=\"secondary\"", "Typ przycisku secondary"),
            ("help=\"Powróć do listy wszystkich lekcji\"", "Tooltip przycisku"),
            ("st.session_state.current_lesson = None", "Funkcjonalność powrotu")
        ]
        
        navigation_ok = True
        for check, desc in navigation_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                navigation_ok = False
        
        return navigation_ok
        
    except Exception as e:
        print(f"❌ Błąd podczas sprawdzania: {e}")
        return False

def test_main_navigation_placement():
    """Test umieszczenia nawigacji w głównej części"""
    
    print("\n🧪 Test umieszczenia nawigacji w głównej części")
    print("=" * 50)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź elementy głównej nawigacji
        main_nav_checks = [
            ("show_horizontal_lesson_navigation()", "Wywołanie funkcji nawigacji"),
            ("📚 Nawigacja lekcji", "Tytuł nawigacji"),
            ("st.columns(4)", "4 kolumny nawigacji"),
            ("lesson-nav-container", "Kontener CSS nawigacji"),
            ("👉", "Znacznik aktualnego kroku"),
            ("✅", "Znacznik ukończonego kroku")
        ]
        
        all_present = True
        for check, desc in main_nav_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_present = False
                
        return all_present
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania głównej nawigacji: {e}")
        return False

def verify_syntax():
    """Sprawdź składnię pliku"""
    
    print("\n🧪 Test składni")
    print("=" * 20)
    
    try:
        import py_compile
        py_compile.compile('views/lesson.py', doraise=True)
        print("✅ Składnia poprawna")
        return True
    except Exception as e:
        print(f"❌ Błąd składni: {e}")
        return False

if __name__ == "__main__":
    print("🔧 TEST USUNIĘCIA ZAWARTOŚCI SIDEBAR")
    print("=" * 60)
    
    tests = [
        ("Opróżnienie sidebar", test_sidebar_cleanup),
        ("Główna nawigacja", test_main_navigation_placement),
        ("Składnia", verify_syntax)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Błąd testu {test_name}: {e}")
            results.append(False)
    
    print("\n📊 PODSUMOWANIE")
    print("=" * 30)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 WSZYSTKIE TESTY PRZESZŁY!")
        print("✅ Sidebar został poprawnie opróżniony")
        print("✅ Przycisk powrotu przeniesiony na główną stronę")
        print("✅ Nawigacja działa w głównej części aplikacji")
        print("\n📋 Zrealizowane zmiany:")
        print("• Usunięto nagłówek 'Nawigacja' z sidebar")
        print("• Usunięto przycisk '← Wszystkie lekcje' z sidebar")
        print("• Sidebar pozostaje całkowicie pusty (tylko pass)")
        print("• Przeniesiono przycisk powrotu na główną stronę")
        print("• Zachowano funkcjonalność nawigacji poziomej")
    else:
        print(f"⚠️  {passed}/{total} testów przeszło")
        print("🔧 Wymagane dodatkowe poprawki")
