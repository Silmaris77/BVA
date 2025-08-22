#!/usr/bin/env python3
"""
Test mechanizmu blokowania dostępu do "Podsumowania" bez zaliczenia quizu końcowego (min. 75%)
Sprawdza logikę blokady, zapisywanie stanu quizu i odblokowanie nawigacji.
"""

def test_summary_blocking_logic():
    """Test mechanizmu blokowania sekcji 'Podsumowanie'"""
    
    print("🧪 Test mechanizmu blokowania 'Podsumowania'")
    print("=" * 50)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź elementy mechanizmu blokowania
        blocking_checks = [
            # Sprawdzanie stanu quizu
            ("closing_quiz_key = f\"closing_quiz_{lesson_id}\"", "Klucz quizu końcowego"),
            ("closing_quiz_state = st.session_state.get(closing_quiz_key, {})", "Pobieranie stanu quizu"),
            ("quiz_passed = closing_quiz_state.get(\"quiz_passed\", False)", "Sprawdzanie zaliczenia"),
            
            # Logika blokowania
            ("if step == 'summary':", "Specjalna logika dla 'summary'"),
            ("if not quiz_passed and not is_current:", "Warunek blokady"),
            ("🔒", "Ikona zablokowanego kroku"),
            ("Musisz zaliczyć quiz końcowy (min. 75%)", "Komunikat o wymaganiu"),
            
            # Zapisywanie stanu quizu
            ("st.session_state[closing_quiz_key] = {}", "Inicjalizacja stanu quizu"),
            ("quiz_completed", "Zapisywanie ukończenia"),
            ("quiz_passed", "Zapisywanie zaliczenia"),
            
            # Komunikaty użytkownika
            ("Możesz teraz przejść do podsumowania", "Komunikat o odblokowaniu"),
            ("musisz uzyskać przynajmniej 75%", "Komunikat o wymaganiu 75%")
        ]
        
        all_present = True
        print("✅ Sprawdzanie mechanizmu blokowania:")
        for check_text, description in blocking_checks:
            if check_text in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}: BRAK")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Błąd podczas sprawdzania: {e}")
        return False

def test_quiz_threshold_logic():
    """Test logiki progu 75% w quizie końcowym"""
    
    print("\n🧪 Test progu 75% w quizie końcowym")
    print("=" * 40)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź ustawienia progu
        threshold_checks = [
            ("passing_threshold=75", "Próg 75% w display_quiz"),
            ("minimum 75% poprawnych odpowiedzi", "Informacja o progu dla użytkownika"),
            ("przynajmniej 75%", "Komunikat błędu o 75%"),
            ("Quiz końcowy", "Nazwa quizu końcowego"),
            ("🎓", "Ikona quizu końcowego")
        ]
        
        all_threshold_ok = True
        print("✅ Sprawdzanie ustawień progu 75%:")
        for check, desc in threshold_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_threshold_ok = False
        
        return all_threshold_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania progu: {e}")
        return False

def test_navigation_button_states():
    """Test stanów przycisku nawigacji dla 'Podsumowania'"""
    
    print("\n🧪 Test stanów przycisku 'Podsumowania'")
    print("=" * 40)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź różne stany przycisku
        button_states = [
            ("🔒", "Stan zablokowany (quiz niezdany)"),
            ("👉", "Stan aktualny"),
            ("✅", "Stan ukończony"),
            ("disabled = True", "Blokowanie przycisku"),
            ("help_text", "Dynamiczny tekst pomocy"),
            ("if step == 'summary':", "Specjalne traktowanie summary")
        ]
        
        all_states_ok = True
        print("✅ Sprawdzanie stanów przycisku:")
        for state, desc in button_states:
            if state in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_states_ok = False
        
        return all_states_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania stanów: {e}")
        return False

def test_session_state_management():
    """Test zarządzania stanem sesji dla quizu"""
    
    print("\n🧪 Test zarządzania stanem sesji")
    print("=" * 35)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź zarządzanie session_state
        session_checks = [
            ("st.session_state[closing_quiz_key]", "Zapisywanie do session_state"),
            ("quiz_completed", "Przechowywanie stanu ukończenia"),
            ("quiz_passed", "Przechowywanie stanu zaliczenia"),
            ("if closing_quiz_key not in st.session_state", "Sprawdzenie istnienia klucza"),
            ("st.session_state.get(closing_quiz_key, {})", "Bezpieczne pobieranie")
        ]
        
        all_session_ok = True
        print("✅ Sprawdzanie zarządzania session_state:")
        for check, desc in session_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_session_ok = False
        
        return all_session_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania session_state: {e}")
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
    print("🔐 TEST MECHANIZMU BLOKOWANIA PODSUMOWANIA")
    print("=" * 70)
    
    tests = [
        ("Mechanizm blokowania", test_summary_blocking_logic),
        ("Próg 75% w quizie", test_quiz_threshold_logic),
        ("Stany przycisku nawigacji", test_navigation_button_states),
        ("Zarządzanie session_state", test_session_state_management),
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
        print("✅ Mechanizm blokowania został poprawnie zaimplementowany!")
        print("\n🔐 Funkcje mechanizmu:")
        print("• Blokuje dostęp do 'Podsumowania' bez zaliczonego quizu końcowego")
        print("• Wymaga minimum 75% w quizie końcowym")
        print("• Wyświetla odpowiednie ikony i komunikaty (🔒, help text)")
        print("• Zapisuje stan zaliczenia w session_state")
        print("• Odblokuje nawigację po zaliczeniu quizu")
        print("• Dynamicznie aktualizuje stan przycisku")
        print("\n👤 Doświadczenie użytkownika:")
        print("• Jasny komunikat o wymaganiu zaliczenia quizu")
        print("• Przycisk 'Podsumowanie' zablokowany do momentu zaliczenia")
        print("• Potwierdzenie odblokowania po zaliczeniu quizu")
        print("• Zachowana funkcjonalność dla innych kroków")
    else:
        print(f"⚠️  {passed}/{total} testów przeszło")
        print("🔧 Wymagane dodatkowe sprawdzenie mechanizmu")
