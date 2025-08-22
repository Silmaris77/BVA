#!/usr/bin/env python3
"""
Naprawia główny problem z renderowaniem sekcji Praktyka w views/lesson.py
"""

import os
import re

def find_and_fix_practical_section():
    """Znajduje i naprawia sekcję practical_exercises"""
    
    file_path = "views/lesson.py"
    
    # Wczytaj cały plik
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Znajdź punkt wstawienia - przed komentarzem o starej strukturze
    insertion_point = "# Stara struktura z 'tabs' (backward compatibility)"
    
    if insertion_point not in content:
        print("❌ Nie znaleziono punktu wstawienia")
        return False
    
    # Kod do wstawienia
    new_code = '''
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
                                # Standardowa obsługa dla innych zakładek (exercises, reflection, application)
                                tab_data = sub_tabs_data[tab_key]
                                
                                # Wyświetl opis zakładki jeśli istnieje
                                if 'description' in tab_data:
                                    st.info(tab_data['description'])
                                
                                # Wyświetl sekcje w zakładce
                                if 'sections' in tab_data:
                                    for section in tab_data['sections']:
                                        st.markdown(f"### {section.get('title', 'Sekcja')}")
                                        st.markdown(section.get('content', 'Brak treści'), unsafe_allow_html=True)
                                        
                                        # Jeśli sekcja wymaga odpowiedzi użytkownika
                                        if section.get('interactive', False):
                                            # Generuj klucz dla przechowywania odpowiedzi
                                            section_key = f"practical_{tab_key}_{section.get('title', '').replace(' ', '_').lower()}"
                                            
                                            # Użyj formularza dla lepszego UX
                                            with st.form(key=f"form_{section_key}"):
                                                # Pobierz istniejącą odpowiedź (jeśli jest)
                                                existing_response = st.session_state.get(section_key, "")
                                                
                                                # Wyświetl pole tekstowe z istniejącą odpowiedzią
                                                user_response = st.text_area(
                                                    "Twoja odpowiedź:",
                                                    value=existing_response,
                                                    height=200,
                                                    key=f"input_{section_key}"
                                                )
                                                
                                                # Przycisk do zapisywania odpowiedzi w formularzu
                                                submitted = st.form_submit_button("Zapisz odpowiedź")
                                                
                                                if submitted:
                                                    # Zapisz odpowiedź w stanie sesji
                                                    st.session_state[section_key] = user_response
                                                    st.success("Twoja odpowiedź została zapisana!")
                                else:
                                    st.warning(f"Zakładka '{tab_title}' nie zawiera sekcji do wyświetlenia.")
                
                '''
    
    # Dodaj nowy kod przed starą strukturą
    content = content.replace(
        f"                {insertion_point}",
        f"{new_code}                {insertion_point}"
    )
    
    # Napraw uszkodzone emoji
    content = content.replace('"� Quiz końcowy"', '"🎓 Quiz końcowy"')
    content = content.replace('"� Zadania Praktyczne"', '"🚀 Zadania Praktyczne"')
    
    # Zapisz naprawiony plik
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Naprawiono sekcję practical_exercises")
    print("✅ Naprawiono uszkodzone emoji")
    return True

def main():
    print("🔧 NAPRAWA SEKCJI PRAKTYKA")
    print("=" * 40)
    
    success = find_and_fix_practical_section()
    
    if success:
        print("\n✅ NAPRAWA ZAKOŃCZONA POMYŚLNIE")
        print("🚀 Sekcja Praktyka powinna teraz wyświetlać zakładki Ćwiczenia i Quiz końcowy")
    else:
        print("\n❌ NAPRAWA SIĘ NIE POWIODŁA")
    
    return success

if __name__ == "__main__":
    main()
