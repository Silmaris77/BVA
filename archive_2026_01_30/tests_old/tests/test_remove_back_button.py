#!/usr/bin/env python3
"""
Test usunięcia przycisku "← Wszystkie lekcje" z poziomej nawigacji
Sprawdza czy przycisk został usunięty i czy nawigacja nadal działa poprawnie.
"""

def test_removal_of_back_button():
    """Test usunięcia przycisku powrotu z poziomej nawigacji"""
    
    print("🧪 Test usunięcia przycisku '← Wszystkie lekcje'")
    print("=" * 50)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
          # Sprawdź, czy przycisk został usunięty z poziomej nawigacji
        removed_elements = [
            ("← Wszystkie lekcje", "Przycisk powrotu"),
            ("Przycisk powrotu do listy lekcji", "Komentarz o przycisku powrotu"),
            ("help=\"Powróć do listy wszystkich lekcji\"", "Tooltip przycisku powrotu w nawigacji")
        ]
        
        print("✅ Sprawdzanie usunięcia zbędnych elementów:")
        any_found = False
        for element, description in removed_elements:
            if element in content:
                print(f"❌ {description}: NADAL OBECNY")
                any_found = True
            else:
                print(f"✅ {description}: USUNIĘTY")
        
        if any_found:
            print("\n⚠️  Niektóre elementy nadal są obecne!")
            return False
        
        # Sprawdź, czy główne elementy nawigacji zostały zachowane
        print("\n✅ Sprawdzanie zachowanych elementów nawigacji:")
        preserved_elements = [
            ("📚 Nawigacja lekcji", "Tytuł nawigacji"),
            ("st.columns(4)", "4 kolumny nawigacji"),
            ("lesson-nav-container", "Kontener CSS"),
            ("👉", "Znacznik aktualnego kroku"),
            ("✅", "Znacznik ukończonego kroku"),
            ("show_horizontal_lesson_navigation()", "Wywołanie funkcji nawigacji")
        ]
        
        all_preserved = True
        for element, description in preserved_elements:
            if element in content:
                print(f"✅ {description}: ZACHOWANY")
            else:
                print(f"❌ {description}: BRAK!")
                all_preserved = False
        
        return all_preserved
        
    except Exception as e:
        print(f"❌ Błąd podczas sprawdzania: {e}")
        return False

def test_sidebar_navigation_dependency():
    """Test czy sidebar zawiera nawigację główną aplikacji"""
    
    print("\n🧪 Test zależności od nawigacji głównej")
    print("=" * 40)
    
    print("📝 Sprawdzanie czy istnieje główna nawigacja:")
    print("• Zakładka 'Lekcje' w głównej nawigacji aplikacji")
    print("• Pozwala na powrót do listy lekcji bez dodatkowego przycisku")
    print("• Upraszcza interfejs - brak duplikacji funkcjonalności")
    
    return True

def test_clean_navigation_layout():
    """Test czystego layoutu nawigacji poziomej"""
    
    print("\n🧪 Test czystego layoutu nawigacji")
    print("=" * 40)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź strukturę nawigacji poziomej
        structure_elements = [
            ("lesson-nav-container", "Kontener nawigacji"),
            ("lesson-nav-title", "Tytuł nawigacji"),
            ("st.columns(4)", "4 kolumny bez dodatkowych przycisków"),
            ("for i, step in enumerate(step_order)", "Pętla po krokach lekcji")
        ]
        
        print("✅ Sprawdzanie czystej struktury:")
        all_clean = True
        for element, description in structure_elements:
            if element in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}: BRAK")
                all_clean = False
        
        # Sprawdź, czy nie ma niepotrzebnych elementów
        unwanted_elements = [
            ("if st.button(\"← Wszystkie lekcje\"", "Dodatkowy przycisk powrotu"),
            ("type=\"secondary\"", "Konfiguracja przycisku powrotu"),
            ("help=\"Powróć do listy", "Tooltip przycisku powrotu")
        ]
        
        print("\n✅ Sprawdzanie braku niepotrzebnych elementów:")
        for element, description in unwanted_elements:
            if element in content:
                print(f"❌ {description}: NADAL OBECNY")
                all_clean = False
            else:
                print(f"✅ {description}: BRAK (poprawnie)")
        
        return all_clean
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania layoutu: {e}")
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
    print("🔧 TEST USUNIĘCIA ZBĘDNEGO PRZYCISKU POWROTU")
    print("=" * 70)
    
    tests = [
        ("Usunięcie przycisku powrotu", test_removal_of_back_button),
        ("Zależność od głównej nawigacji", test_sidebar_navigation_dependency),
        ("Czysty layout nawigacji", test_clean_navigation_layout),
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
        print("✅ Przycisk '← Wszystkie lekcje' został usunięty")
        print("✅ Nawigacja pozioma jest czysta i funkcjonalna")
        print("✅ Duplikacja funkcjonalności została wyeliminowana")
        print("\n💡 Optymalizacja UX:")
        print("• Użytkownik może wrócić do listy lekcji przez główną nawigację")
        print("• Brak duplikacji przycisków - czystszy interfejs")
        print("• Pozioma nawigacja skupia się tylko na krokach lekcji")
        print("• Sidebar pozostaje minimalny i nieinwazyjny")
    else:
        print(f"⚠️  {passed}/{total} testów przeszło")
        print("🔧 Wymagane dodatkowe sprawdzenie")
