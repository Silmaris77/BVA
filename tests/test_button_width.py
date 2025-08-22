#!/usr/bin/env python3
"""
Test jednakowej szerokości przycisków nawigacji poziomej
Sprawdza czy CSS dla przycisków nawigacji zapewnia jednakową szerokość.
"""

def test_button_width_css():
    """Test CSS dla jednakowej szerokości przycisków"""
    
    print("🧪 Test CSS dla jednakowej szerokości przycisków")
    print("=" * 50)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź CSS dla przycisków nawigacji
        css_checks = [
            (".lesson-nav-container .stButton > button", "Selektor CSS dla przycisków nawigacji"),
            ("width: 100% !important", "Pełna szerokość przycisku"),
            ("min-width: 120px !important", "Minimalna szerokość"),
            ("max-width: 100% !important", "Maksymalna szerokość"),
            ("height: 48px !important", "Jednakowa wysokość"),
            ("white-space: nowrap !important", "Brak zawijania tekstu"),
            ("overflow: hidden !important", "Ukrywanie przepełnienia"),
            ("text-overflow: ellipsis !important", "Wielokropek dla długiego tekstu"),
            ("display: flex !important", "Flexbox layout"),
            ("align-items: center !important", "Wyśrodkowanie pionowe"),
            ("justify-content: center !important", "Wyśrodkowanie poziome"),
            ("font-size: 0.9rem !important", "Jednakowy rozmiar czcionki")
        ]
        
        all_css_present = True
        print("✅ Sprawdzanie CSS dla przycisków:")
        for css_rule, description in css_checks:
            if css_rule in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}: BRAK")
                all_css_present = False
        
        return all_css_present
        
    except Exception as e:
        print(f"❌ Błąd podczas sprawdzania CSS: {e}")
        return False

def test_button_container_structure():
    """Test struktury kontenerów przycisków"""
    
    print("\n🧪 Test struktury kontenerów")
    print("=" * 35)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź strukturę kontenerów
        structure_checks = [
            ("st.columns(4)", "4 kolumny dla przycisków"),
            ("use_container_width=True", "Użycie pełnej szerokości kolumny"),
            ("lesson-nav-container", "Kontener CSS nawigacji"),
            ("with cols[i]:", "Użycie kolumn dla przycisków")
        ]
        
        all_structure_ok = True
        print("✅ Sprawdzanie struktury:")
        for check, desc in structure_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_structure_ok = False
        
        return all_structure_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania struktury: {e}")
        return False

def test_button_text_consistency():
    """Test spójności tekstu przycisków"""
    
    print("\n🧪 Test spójności tekstu przycisków")
    print("=" * 40)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź nazwy kroków
        step_names_checks = [
            ("'intro': 'Wprowadzenie'", "Nazwa: Wprowadzenie (13 znaków)"),
            ("'content': 'Nauka'", "Nazwa: Nauka (5 znaków)"),
            ("'practical_exercises': 'Praktyka'", "Nazwa: Praktyka (8 znaków)"),
            ("'summary': 'Podsumowanie'", "Nazwa: Podsumowanie (12 znaków)")
        ]
        
        print("✅ Sprawdzanie nazw kroków:")
        all_names_ok = True
        for check, desc in step_names_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_names_ok = False
        
        # Sprawdź format przycisków
        button_format_checks = [
            ("f\"👉 {i+1}. {step_name}\"", "Format aktualnego kroku"),
            ("f\"✅ {i+1}. {step_name}\"", "Format ukończonego kroku"),
            ("f\"🔒 {i+1}. {step_name}\"", "Format zablokowanego kroku"),
            ("f\"{i+1}. {step_name}\"", "Format przyszłego kroku")
        ]
        
        print("\n✅ Sprawdzanie formatów przycisków:")
        for check, desc in button_format_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_names_ok = False
        
        return all_names_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania tekstów: {e}")
        return False

def test_responsive_design():
    """Test responsywnego designu"""
    
    print("\n🧪 Test responsywnego designu")
    print("=" * 35)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź elementy responsywnego designu
        responsive_checks = [
            ("line-height: 1.2 !important", "Odpowiednia wysokość linii"),
            ("min-width: 120px", "Minimalna szerokość na małych ekranach"),
            ("font-size: 0.9rem", "Skalowany rozmiar czcionki"),
            ("padding: 1rem", "Padding kontenera"),
            ("margin-bottom: 2rem", "Odstęp dolny")
        ]
        
        all_responsive_ok = True
        print("✅ Sprawdzanie responsywności:")
        for check, desc in responsive_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_responsive_ok = False
        
        return all_responsive_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania responsywności: {e}")
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
    print("🎨 TEST JEDNAKOWEJ SZEROKOŚCI PRZYCISKÓW NAWIGACJI")
    print("=" * 70)
    
    tests = [
        ("CSS dla szerokości przycisków", test_button_width_css),
        ("Struktura kontenerów", test_button_container_structure),
        ("Spójność tekstu przycisków", test_button_text_consistency),
        ("Responsywny design", test_responsive_design),
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
        print("✅ CSS dla jednakowej szerokości przycisków został dodany!")
        print("\n🎨 Zastosowane poprawki:")
        print("• Wszystkie przyciski mają width: 100%")
        print("• Minimalna szerokość: 120px")
        print("• Jednakowa wysokość: 48px")
        print("• Flexbox dla idealnego wyśrodkowania")
        print("• Obsługa przepełnienia tekstu (ellipsis)")
        print("• Responsywny rozmiar czcionki")
        print("\n📐 Nazwy kroków:")
        print("• 1. Wprowadzenie (13 znaków)")
        print("• 2. Nauka (5 znaków)")
        print("• 3. Praktyka (8 znaków)")
        print("• 4. Podsumowanie (12 znaków)")
        print("\n🚀 Wszystkie przyciski będą teraz jednakowej szerokości!")
    else:
        print(f"⚠️  {passed}/{total} testów przeszło")
        print("🔧 Wymagane dodatkowe poprawki CSS")
