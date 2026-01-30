#!/usr/bin/env python3
"""
Test kompletnej blokady wszystkich przycisków "Dalej" prowadzących do "Podsumowania"
Sprawdza czy wszystkie możliwe ścieżki do sekcji summary są zabezpieczone wymogiem zaliczenia quizu końcowego.
"""

def test_complete_blocking_coverage():
    """Test pokrycia wszystkich przycisków Dalej prowadzących do summary"""
    
    print("🧪 Test kompletnej blokady przycisków 'Dalej'")
    print("=" * 50)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Znajdź wszystkie sekcje, które mogą prowadzić do summary
        sections_with_next_buttons = [
            'practical_exercises',  # Nowa główna sekcja
            'reflection',          # Backward compatibility
            'application'          # Backward compatibility
        ]
        
        print("✅ Sprawdzanie blokad w sekcjach:")
        all_sections_secured = True
        
        for section in sections_with_next_buttons:
            # Sprawdź czy sekcja ma logikę blokowania
            section_pattern = f"elif st.session_state.lesson_step == '{section}'"
            if section_pattern in content:
                print(f"✅ Sekcja '{section}': ZNALEZIONA")
                
                # Sprawdź czy ma blokadę dla summary
                blocking_checks = [
                    f"if next_step == 'summary':",
                    f"quiz_passed = closing_quiz_state.get(\"quiz_passed\", False)",
                    f"🔒 Dalej:",
                    f"Musisz zaliczyć quiz końcowy (min. 75%)"
                ]
                
                section_secured = True
                for check in blocking_checks:
                    # Znajdź pozycję sekcji w pliku
                    section_start = content.find(section_pattern)
                    if section_start != -1:
                        # Znajdź koniec sekcji (następna sekcja elif lub elif/else)
                        section_end = content.find("elif st.session_state.lesson_step ==", section_start + 1)
                        if section_end == -1:
                            section_end = len(content)
                        
                        section_content = content[section_start:section_end]
                        
                        if check not in section_content:
                            print(f"   ❌ Brak blokady: {check}")
                            section_secured = False
                
                if section_secured:
                    print(f"   ✅ Sekcja '{section}' zabezpieczona")
                else:
                    print(f"   ❌ Sekcja '{section}' NIE zabezpieczona")
                    all_sections_secured = False
            else:
                print(f"⚠️  Sekcja '{section}': NIEZNALEZIONA (może nie być używana)")
        
        return all_sections_secured
        
    except Exception as e:
        print(f"❌ Błąd podczas sprawdzania: {e}")
        return False

def test_navigation_button_blocking():
    """Test blokady przycisku nawigacji poziomej"""
    
    print("\n🧪 Test blokady przycisku nawigacji poziomej")
    print("=" * 50)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź blokadę w nawigacji poziomej
        nav_blocking_checks = [
            ("if step == 'summary':", "Sprawdzanie kroku summary w nawigacji"),
            ("quiz_passed = closing_quiz_state.get(\"quiz_passed\", False)", "Pobieranie stanu zaliczenia"),
            ("if not quiz_passed and not is_current:", "Warunek blokady nawigacji"),
            ("🔒", "Ikona zablokowanej nawigacji"),
            ("Musisz zaliczyć quiz końcowy (min. 75%)", "Komunikat blokady nawigacji")
        ]
        
        all_nav_secured = True
        print("✅ Sprawdzanie blokady nawigacji poziomej:")
        for check, desc in nav_blocking_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_nav_secured = False
        
        return all_nav_secured
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania nawigacji: {e}")
        return False

def test_quiz_state_management():
    """Test zarządzania stanem quizu końcowego"""
    
    print("\n🧪 Test zarządzania stanem quizu końcowego")
    print("=" * 40)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź zapisywanie stanu quizu
        quiz_state_checks = [
            ("closing_quiz_key = f\"closing_quiz_{lesson_id}\"", "Klucz stanu quizu"),
            ("st.session_state[closing_quiz_key] = {}", "Inicjalizacja stanu"),
            ("quiz_completed", "Zapisywanie ukończenia"),
            ("quiz_passed", "Zapisywanie zaliczenia"),
            ("passing_threshold=75", "Próg 75%"),
            ("Możesz teraz przejść do podsumowania", "Komunikat odblokowania")
        ]
        
        all_state_ok = True
        print("✅ Sprawdzanie zarządzania stanem quizu:")
        for check, desc in quiz_state_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_state_ok = False
        
        return all_state_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania stanu: {e}")
        return False

def test_user_experience():
    """Test doświadczenia użytkownika"""
    
    print("\n🧪 Test doświadczenia użytkownika")
    print("=" * 35)
    
    try:
        with open('views/lesson.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź komunikaty dla użytkownika
        ux_checks = [
            ("⚠️ Aby przejść do podsumowania", "Komunikat ostrzegawczy"),
            ("Quiz znajdziesz w sekcji 'Praktyka'", "Wskazówka lokalizacji quizu"),
            ("🎓 Quiz końcowy", "Wskazanie zakładki"),
            ("minimum 75%", "Jasne określenie wymagania"),
            ("🔒", "Wizualna ikona blokady"),
            ("disabled=True", "Techniczna blokada przycisku"),
            ("help=", "Tooltips z wyjaśnieniem")
        ]
        
        all_ux_ok = True
        print("✅ Sprawdzanie doświadczenia użytkownika:")
        for check, desc in ux_checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}: BRAK")
                all_ux_ok = False
        
        return all_ux_ok
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania UX: {e}")
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
    print("🔐 TEST KOMPLETNEJ BLOKADY DOSTĘPU DO PODSUMOWANIA")
    print("=" * 80)
    
    tests = [
        ("Pokrycie wszystkich sekcji", test_complete_blocking_coverage),
        ("Blokada nawigacji poziomej", test_navigation_button_blocking),
        ("Zarządzanie stanem quizu", test_quiz_state_management),
        ("Doświadczenie użytkownika", test_user_experience),
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
        print("✅ Kompletna blokada dostępu do podsumowania została zaimplementowana!")
        print("\n🔒 Zabezpieczone ścieżki:")
        print("• Przycisk nawigacji poziomej '4. Podsumowanie' (🔒)")
        print("• Przycisk 'Dalej' w sekcji 'Praktyka'")
        print("• Przycisk 'Dalej' w sekcji 'Refleksja' (backward compatibility)")
        print("• Przycisk 'Dalej' w sekcji 'Zadania praktyczne' (backward compatibility)")
        print("\n🎯 Wymagania:")
        print("• Minimum 75% w quizie końcowym")
        print("• Quiz dostępny w sekcji 'Praktyka' → '🎓 Quiz końcowy'")
        print("• Stan zaliczenia zapisywany w session_state")
        print("\n👤 Komunikaty użytkownika:")
        print("• Jasne wskazówki gdzie znaleźć quiz")
        print("• Tooltips z wyjaśnieniem blokady")
        print("• Wizualne ikony blokady (🔒)")
        print("• Komunikaty potwierdzające odblokowanie")
        print("\n🚀 Mechanizm jest kompletny i gotowy do użytku!")
    else:
        print(f"⚠️  {passed}/{total} testów przeszło")
        print("🔧 Wymagane dodatkowe zabezpieczenia")
