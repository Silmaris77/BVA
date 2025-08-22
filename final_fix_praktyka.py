#!/usr/bin/env python3
"""
Ostateczna naprawa - zastąp uszkodzone linie bezpośrednio
"""

import os

def fix_broken_emoji_lines():
    """Naprawia konkretne linie z uszkodzonymi emoji"""
    
    file_path = "views/lesson.py"
    
    # Wczytaj wszystkie linie
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Znajdź i zastąp uszkodzone linie
    for i, line in enumerate(lines):
        # Linia 619 (około)
        if 'available_tabs.append("' in line and 'Quiz końcowy"' in line and '�' in line:
            lines[i] = line.replace('available_tabs.append("� Quiz końcowy")', 'available_tabs.append("🎓 Quiz końcowy")')
            print(f"✅ Naprawiono linię {i+1}: Quiz końcowy")
        
        # Linia 630 (około)
        if 'available_tabs.append("' in line and 'Zadania Praktyczne"' in line and '�' in line:
            lines[i] = line.replace('available_tabs.append("� Zadania Praktyczne")', 'available_tabs.append("🚀 Zadania Praktyczne")')
            print(f"✅ Naprawiono linię {i+1}: Zadania Praktyczne")
    
    # Zapisz naprawiony plik
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Plik został zapisany")

def add_missing_rendering_logic():
    """Dodaje brakującą logikę renderowania"""
    
    file_path = "views/lesson.py"
    
    # Wczytaj plik
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Znajdź punkt gdzie ma być dodany kod (przed komentarzem o starej strukturze)
    target = "                # Stara struktura z 'tabs' (backward compatibility)"
    
    if target not in content:
        print("❌ Nie znaleziono punktu wstawienia")
        return False
    
    # Kod do wstawienia
    new_logic = '''
                # Renderuj zakładki dla nowej struktury (exercises, closing_quiz)  
                if available_tabs and 'tabs' not in practical_data:
                    # Wyświetl pod-zakładki dla nowej struktury
                    tabs = tabs_with_fallback(available_tabs)
                    
                    for i, (tab_key, tab_title) in enumerate(zip(tab_keys, available_tabs)):
                        with tabs[i]:
                            if tab_key == 'closing_quiz':
                                # Specjalna obsługa dla quizu końcowego
                                st.info("🎓 **Quiz końcowy** - Sprawdź swoją wiedzę z tej lekcji. Musisz uzyskać minimum 75% poprawnych odpowiedzi, aby przejść dalej.")
                                
                                quiz_data = sub_tabs_data['closing_quiz']
                                quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=75)
                                
                                # Oznacz quiz jako ukończony po wypełnieniu
                                if quiz_completed:
                                    # Zapisz stan zaliczenia quizu do sprawdzania w nawigacji
                                    closing_quiz_key = f"closing_quiz_{lesson_id}"
                                    if closing_quiz_key not in st.session_state:
                                        st.session_state[closing_quiz_key] = {}
                                    
                                    st.session_state[closing_quiz_key]["quiz_completed"] = True
                                    st.session_state[closing_quiz_key]["quiz_passed"] = quiz_passed
                                    
                                    closing_quiz_xp_key = f"closing_quiz_xp_{lesson_id}"
                                    if not st.session_state.get(closing_quiz_xp_key, False):
                                        # Award fragment XP for quiz completion
                                        fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                        # Quiz końcowy dostaje 1/3 z XP practical_exercises 
                                        success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                        st.session_state[closing_quiz_xp_key] = True
                                        if success and earned_xp > 0:
                                            show_xp_notification(earned_xp, f"Zdobyłeś {earned_xp} XP za ukończenie quizu końcowego!")
                                    
                                    if quiz_passed:
                                        st.success("✅ Gratulacje! Zaliczyłeś quiz końcowy! Możesz teraz przejść do podsumowania.")
                                    else:
                                        st.error("❌ Aby przejść do podsumowania, musisz uzyskać przynajmniej 75% poprawnych odpowiedzi. Spróbuj ponownie!")
                            else:
                                # Standardowa obsługa dla innych zakładek (exercises)
                                tab_data = sub_tabs_data[tab_key]
                                
                                # Wyświetl opis zakładki jeśli istnieje
                                if 'description' in tab_data:
                                    st.info(tab_data['description'])
                                
                                # Wyświetl sekcje w zakładce
                                if 'sections' in tab_data:
                                    for section in tab_data['sections']:
                                        st.markdown(f"### {section.get('title', 'Sekcja')}")
                                        st.markdown(section.get('content', 'Brak treści'), unsafe_allow_html=True)
                                else:
                                    st.warning(f"Zakładka '{tab_title}' nie zawiera sekcji do wyświetlenia.")

'''
    
    # Wstaw nowy kod
    content = content.replace(target, new_logic + target)
    
    # Zapisz plik
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Dodano logikę renderowania dla nowej struktury")
    return True

def main():
    print("🔧 OSTATECZNA NAPRAWA SEKCJI PRAKTYKA")
    print("=" * 50)
    
    # Krok 1: Napraw uszkodzone emoji
    fix_broken_emoji_lines()
    
    # Krok 2: Dodaj brakującą logikę renderowania
    add_missing_rendering_logic()
    
    print("\n✅ WSZYSTKIE NAPRAWY ZAKOŃCZONE")
    print("🚀 Sekcja Praktyka powinna teraz działać poprawnie")

if __name__ == "__main__":
    main()
