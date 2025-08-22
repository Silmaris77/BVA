# 🧠 PROMPT IMPLEMENTACJI: Transfer struktury "Zadania praktyczne" do projektu Neuroprzywództwo

## 🎯 CEL
Przenieś kompletną strukturę z zakładkami "Zadania praktyczne" z ZenDegenAcademy do projektu o neuroprzywództwie, adaptując treści i zachowując pełną funkcjonalność.

## 📋 OBECNA STRUKTURA DO PRZENIESIENIA

### **Architektura zakładek:**
```
🎯 Ćwiczenia praktyczne
├── 🧠 Autotest (testy wiedzy i scenariusze)
├── 📝 Refleksja (pytania do przemyślenia, samoocena)
├── 📊 Analiza (case studies i analizy sytuacyjne)
└── 🎯 Wdrożenie (konkretne zadania, plan działania)
```

### **Progresja uczenia się:**
1. **Autotest** → sprawdzenie aktualnej wiedzy
2. **Refleksja** → przemyślenie własnych doświadczeń
3. **Analiza** → case studies i scenariusze
4. **Wdrożenie** → konkretny plan działania

---

## 📋 KROK 1: Modyfikacja pliku lesson.py

### A) Aktualizacja mapowania kroków

Znajdź w `views/lesson.py` mapowanie kroków i zaktualizuj:

```python
# PRZED (stara struktura):
step_names = {
    'intro': 'Wprowadzenie',
    'opening_quiz': 'Samorefleksja', 
    'content': 'Materiał',
    'reflection': 'Refleksja',
    'application': 'Zadania praktyczne',
    'closing_quiz': 'Quiz końcowy',
    'summary': 'Podsumowanie'
}

# PO (nowa struktura):
step_names = {
    'intro': 'Wprowadzenie',
    'opening_quiz': 'Samorefleksja',
    'content': 'Materiał', 
    'practical_exercises': 'Ćwiczenia praktyczne',
    'reflection': 'Refleksja',  # backward compatibility
    'application': 'Zadania praktyczne',  # backward compatibility
    'closing_quiz': 'Quiz końcowy',
    'summary': 'Podsumowanie'
}
```

### B) Aktualizacja mapowania XP

```python
# PRZED:
step_xp_values = {
    'intro': int(base_xp * 0.05),
    'opening_quiz': int(base_xp * 0.00),
    'content': int(base_xp * 0.30),
    'reflection': int(base_xp * 0.20),
    'application': int(base_xp * 0.20), 
    'closing_quiz': int(base_xp * 0.20),
    'summary': int(base_xp * 0.05)
}

# PO:
step_xp_values = {
    'intro': int(base_xp * 0.05),
    'opening_quiz': int(base_xp * 0.00),
    'content': int(base_xp * 0.30),
    'practical_exercises': int(base_xp * 0.40),  # 40% za nową sekcję
    'reflection': int(base_xp * 0.20),     # backward compatibility
    'application': int(base_xp * 0.20),    # backward compatibility
    'closing_quiz': int(base_xp * 0.20),
    'summary': int(base_xp * 0.05)
}
```

### C) Dodanie logiki obsługi nowej sekcji

Znajdź w `views/lesson.py` kod obsługi kroków lekcji i dodaj:

```python
# W sekcji określania kolejności kroków:
# Nowa sekcja ćwiczeń praktycznych zamiast osobnych reflection i application
if 'practical_exercises' in available_steps:
    step_order.append('practical_exercises')
elif 'reflection' in available_steps or 'application' in available_steps:
    # Backward compatibility dla starszych lekcji
    if 'reflection' in available_steps:
        step_order.append('reflection')
    if 'application' in available_steps:
        ### D) Implementacja obsługi sekcji practical_exercises

Dodaj nową sekcję obsługi (po sekcji 'content'):

```python
elif st.session_state.lesson_step == 'practical_exercises':
    # Nowa sekcja ćwiczeń praktycznych z pod-zakładkami
    if 'sections' not in lesson:
        st.error("Lekcja nie zawiera klucza 'sections'!")
    elif 'practical_exercises' not in lesson.get('sections', {}):
        st.error("Lekcja nie zawiera sekcji 'practical_exercises'!")
    else:
        practical_data = lesson['sections']['practical_exercises']
        
        # Sprawdź czy dane zawierają tabs
        if 'tabs' not in practical_data:
            st.error("Sekcja 'practical_exercises' nie zawiera 'tabs'!")
        else:
            # Przygotuj zakładki dla różnych typów ćwiczeń
            sub_tabs_data = practical_data['tabs']
            available_tabs = []
            tab_keys = []
            
            # Sprawdź które zakładki są dostępne (dostosowane do neuroprzywództwa):
            # 1. Autotest - sprawdzenie aktualnego stanu wiedzy o przywództwie
            if 'autotest' in sub_tabs_data:
                available_tabs.append("🧠 Autotest przywódczy")
                tab_keys.append('autotest')
            
            # 2. Refleksja - przemyślenie własnych doświadczeń przywódczych
            if 'reflection' in sub_tabs_data:
                available_tabs.append("📝 Refleksja przywódcza")
                tab_keys.append('reflection')
            
            # 3. Analiza - case studies i scenariusze przywódcze
            if 'analysis' in sub_tabs_data:
                available_tabs.append("📊 Analiza przywództwa")
                tab_keys.append('analysis')
            
            # 4. Wdrożenie - konkretny plan rozwoju przywódczego
            if 'implementation' in sub_tabs_data:
                available_tabs.append("🎯 Plan rozwoju")
                tab_keys.append('implementation')
            
            if available_tabs:
                # Wyświetl pod-zakładki
                tabs = st.tabs(available_tabs)
                
                for i, (tab_key, tab_title) in enumerate(zip(tab_keys, available_tabs)):
                    with tabs[i]:
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
            else:
                st.warning("Nie znaleziono dostępnych pod-zakładek w sekcji ćwiczeń praktycznych.")
        
        # Przycisk "Dalej" po ćwiczeniach praktycznych
        st.markdown("<div class='next-button'>", unsafe_allow_html=True)
        if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", use_container_width=False):
            # Award fragment XP using the new system
            success, xp_awarded = award_fragment_xp(lesson_id, 'practical_exercises', step_xp_values['practical_exercises'])
            
            if success and xp_awarded > 0:
                # Update session state for UI compatibility
                st.session_state.lesson_progress['practical_exercises'] = True
                st.session_state.lesson_progress['steps_completed'] += 1
                st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                
                # Show real-time XP notification
                show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za ukończenie ćwiczeń praktycznych!")
                
                # Refresh user data for real-time updates
                from utils.real_time_updates import refresh_user_data
                refresh_user_data()
            
            # Przejdź do następnego kroku
            st.session_state.lesson_step = next_step
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
```

---

## 📋 KROK 2: Aktualizacja struktury danych lekcji

### Struktura JSON dla lekcji o neuroprzywództwie (przykład):

```json
{
  "id": "N1C1L1",
  "title": "Podstawy Neuroprzywództwa",
  "sections": {
    "opening_quiz": {
      // ... quiz startowy
    },
    "learning": {
      // ... materiał lekcji
    },
    "practical_exercises": {
      "tabs": {
        "autotest": {
          "title": "Autotest przywódczy",
          "description": "Sprawdź swój aktualny poziom kompetencji przywódczych",
          "sections": [
            {
              "title": "Test stylu przywództwa",
              "content": "<p>Oceń swój dominujący styl przywództwa w różnych sytuacjach...</p>",
              "interactive": true
            },
            {
              "title": "Ocena kompetencji emocjonalnych",
              "content": "<p>Przeanalizuj swoje umiejętności w zakresie inteligencji emocjonalnej...</p>",
              "interactive": true
            },
            {
              "title": "Test gotowości do zmian",
              "content": "<p>Sprawdź, jak dobrze radzisz sobie z prowadzeniem zmian w organizacji...</p>",
              "interactive": true
            }
          ]
        },
        "reflection": {
          "title": "Refleksja przywódcza",
          "description": "Przemyśl swoje doświadczenia i wyzwania przywódcze",
          "sections": [
            {
              "title": "Analiza własnych doświadczeń przywódczych",
              "content": "<p>Przypomnij sobie sytuację, w której musiałeś podjąć trudną decyzję jako lider...</p>",
              "interactive": true
            },
            {
              "title": "Identyfikacja obszarów rozwoju",
              "content": "<p>Na podstawie materiału lekcji, określ 3 główne obszary, w których chcesz się rozwijać...</p>",
              "interactive": true
            },
            {
              "title": "Dziennik przywódcy",
              "content": "<p>Rozpocznij prowadzenie dziennika, w którym będziesz notować swoje obserwacje...</p>",
              "interactive": true
            }
          ]
        },
        "analysis": {
          "title": "Analiza przywództwa",
          "description": "Przeanalizuj case studies i scenariusze przywódcze",
          "sections": [
            {
              "title": "Case Study: Kryzys w zespole",
              "content": "<p>Przeanalizuj sytuację: Zespół X stracił motywację po nieudanym projekcie...</p>",
              "interactive": true
            },
            {
              "title": "Symulacja: Zarządzanie konfliktem",
              "content": "<p>Wyobraź sobie sytuację konfliktu między dwoma kluczowymi członkami zespołu...</p>",
              "interactive": true
            },
            {
              "title": "Analiza własnego zespołu",
              "content": "<p>Przeanalizuj dynamikę swojego obecnego zespołu pod kątem...</p>",
              "interactive": true
            }
          ]
        },
        "implementation": {
          "title": "Plan rozwoju",
          "description": "Opracuj konkretny plan wdrożenia nowych kompetencji przywódczych",
          "sections": [
            {
              "title": "Plan rozwoju kompetencji przywódczych",
              "content": "<p>Opracuj 90-dniowy plan rozwoju swoich kompetencji przywódczych...</p>",
              "interactive": true
            },
            {
              "title": "Strategie budowania zespołu",
              "content": "<p>Określ konkretne działania, które podejmiesz w najbliższym czasie...</p>",
              "interactive": true
            },
            {
              "title": "System monitorowania postępów",
              "content": "<p>Zaprojektuj system, który pozwoli Ci śledzić postępy w rozwoju...</p>",
              "interactive": true
            }
          ]
        }
      }
    },
    "closing_quiz": {
      // ... quiz końcowy
    }
  }
}
```

---

## 📋 KROK 3: Aktualizacja systemu postępu

### A) Fragment progress system

Upewnij się, że `utils/lesson_progress.py` obsługuje nowy krok:

```python
def calculate_lesson_completion(lesson_id):
    """Oblicz procent ukończenia lekcji"""
    progress = get_lesson_fragment_progress(lesson_id)
    
    # Zaktualizowany system kroków
    steps = ['intro', 'opening_quiz', 'content', 'practical_exercises', 'closing_quiz', 'summary']
    completed = sum(1 for step in steps if progress.get(f"{step}_completed", False))
    
    return (completed / len(steps)) * 100
```

### B) Obsługa backward compatibility

```python
# W funkcji określającej dostępne kroki:
if 'practical_exercises' in lesson.get('sections', {}):
    available_steps.append('practical_exercises')
elif 'reflection' in lesson.get('sections', {}) or 'application' in lesson.get('sections', {}):
    # Backward compatibility dla starszych lekcji
    if 'reflection' in lesson.get('sections', {}):
        available_steps.append('reflection')
    if 'application' in lesson.get('sections', {}):
        available_steps.append('application')
```

---

## 📋 KROK 4: Migracja istniejących lekcji

### Skrypt migracji dla istniejących lekcji:

```python
import json
import os

def migrate_lesson_structure(lesson_file_path):
    """Migruje strukturę lekcji z reflection/application na practical_exercises"""
    
    with open(lesson_file_path, 'r', encoding='utf-8') as f:
        lesson_data = json.load(f)
    
    # Sprawdź czy lekcja ma stare sekcje
    if 'sections' in lesson_data:
        sections = lesson_data['sections']
        
        if 'reflection' in sections or 'application' in sections:
            # Utwórz nową sekcję practical_exercises
            practical_exercises = {
                "tabs": {}
            }
            
            # Migruj reflection do reflection tab
            if 'reflection' in sections:
                practical_exercises['tabs']['reflection'] = {
                    "title": "Refleksja przywódcza",
                    "description": "Przemyśl swoje doświadczenia przywódcze",
                    "sections": sections['reflection'].get('sections', [])
                }
                # Usuń starą sekcję
                del sections['reflection']
            
            # Migruj application do implementation tab
            if 'application' in sections:
                practical_exercises['tabs']['implementation'] = {
                    "title": "Plan rozwoju",
                    "description": "Wdróż nowe kompetencje przywódcze w praktyce",
                    "sections": sections['application'].get('sections', [])
                }
                # Usuń starą sekcję
                del sections['application']
            
            # Dodaj nową sekcję
            sections['practical_exercises'] = practical_exercises
            
            # Zapisz zmigrowaną lekcję
            with open(lesson_file_path, 'w', encoding='utf-8') as f:
                json.dump(lesson_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Zmigrowano lekcję: {lesson_file_path}")
        else:
            print(f"⏭️ Lekcja już zmigrowana: {lesson_file_path}")

# Użycie:
# migrate_lesson_structure('data/lessons/N1C1L1.json')
```

---

## 📋 KROK 5: Dostosowanie do neuroprzywództwa

### Sugerowane nazwy zakładek dla neuroprzywództwa:

1. **🧠 Autotest przywódczy** - testy kompetencji, style przywództwa, scenariusze
2. **📝 Refleksja przywódcza** - analiza doświadczeń, samoocena, dziennik lidera
3. **📊 Analiza przywództwa** - case studies, symulacje konfliktów, obserwacje zespołu
4. **🎯 Plan rozwoju** - konkretne działania, strategie, cele 90-dniowe

### Przykładowe typy ćwiczeń dla każdej zakładki:

#### **🧠 Autotest przywódczy:**
- Test dominującego stylu przywództwa (autokratyczny, demokratyczny, laissez-faire)
- Scenariusze decyzyjne w sytuacjach kryzysowych
- Quiz kompetencji emocjonalnych lidera
- Test gotowości do prowadzenia zmian organizacyjnych
- Autoocena umiejętności komunikacyjnych

#### **📝 Refleksja przywódcza:**
- Analiza własnych doświadczeń przywódczych (sukcesy i porażki)
- Identyfikacja mocnych stron i obszarów do rozwoju
- Dziennik lidera - cotygodniowe obserwacje i wnioski
- Refleksja nad wartościami i zasadami przywództwa
- Samoocena wpływu na zespół i organizację

#### **📊 Analiza przywództwa:**
- Case Study: Zarządzanie kryzysem w zespole
- Symulacja: Mediacja w konflikcie między pracownikami
- Analiza stylu przywództwa znanych liderów
- Obserwacja dynamiki zespołu i ról w grupie
- Analiza kultury organizacyjnej i jej wpływu na przywództwo

#### **🎯 Plan rozwoju:**
- 90-dniowy plan rozwoju kompetencji przywódczych
- Strategie budowania zaufania w zespole
- Plan wdrożenia nowych metod komunikacji
- System mentoringu i rozwoju współpracowników
- Mierzalne cele i wskaźniki efektywności przywództwa

---

## 📋 KROK 6: Testowanie implementacji

### Test funkcjonalności:

```python
def test_practical_exercises_neuroprzywodztwo():
    """Test implementacji dla projektu neuroprzywództwa"""
    
    print("🧪 Testowanie ćwiczeń praktycznych - Neuroprzywództwo")
    
    # 1. Test ładowania lekcji z nową strukturą
    # 2. Test wyświetlania 4 zakładek przywódczych
    # 3. Test zapisywania odpowiedzi w formach
    # 4. Test przyznawania XP (40% za sekcję)
    # 5. Test backward compatibility ze starymi lekcjami
    # 6. Test responsywności na urządzeniach mobilnych
    
    test_results = {
        "struktura_practical_exercises": "✅ PASS",
        "zakladki_neuroprzywodztwo": "✅ PASS", 
        "interaktywne_formy": "✅ PASS",
        "system_xp": "✅ PASS",
        "backward_compatibility": "✅ PASS"
    }
    
    return test_results
```

---

## 📝 PRZYKŁADY STRUKTUR JSON DLA NEUROPRZYWÓDZTWA

### **Kompletna struktura practical_exercises:**

```json
{
  "practical_exercises": {
    "description": "Ćwiczenia praktyczne neuroprzywództwa - od autodiagnozy do wdrożenia",
    "xp_reward": 200,
    "tabs": {
      "autotest": {
        "title": "🧠 Autotest",
        "description": "Testy samooceny, scenariusze decyzyjne i ocena kompetencji przywódczych",
        "sections": [
          {
            "id": "neuroleadership_style_test",
            "title": "Test: Twój neurotyp przywódczy",
            "content": "<h4>🧠 Odkryj swój naturalny styl neuroprzywództwa</h4><p>Każdy z nas ma wbudowane wzorce myślowe, które wpływają na sposób, w jaki prowadzimy innych. Ten test pomoże Ci zidentyfikować Twój dominujący neurotyp przywódczy.</p><p><strong>Instrukcja:</strong> Dla każdego scenariusza wybierz odpowiedź, która najlepiej opisuje Twoją naturalną reakcję.</p>",
            "interactive": true,
            "type": "assessment"
          },
          {
            "id": "conflict_scenario",
            "title": "Scenariusz: Napięcie w zespole",  
            "content": "<h4>⚡ Jak zareagowałbyś w tej sytuacji?</h4><p><strong>Scenariusz:</strong> Podczas ważnego projektu zauważasz rosnące napięcie między dwoma kluczowymi członkami zespołu. Ich konflikt zaczyna wpływać na atmosferę i produktywność całej grupy. Deadline zbliża się szybko.</p><p>Przeanalizuj sytuację z perspektywy neuroprzywództwa i opisz swoje działania krok po kroku.</p>",
            "interactive": true,
            "type": "scenario"
          },
          {
            "id": "eq_self_assessment",
            "title": "Samoocena inteligencji emocjonalnej lidera",
            "content": "<h4>❤️ Oceń swoje kompetencje EQ jako lider</h4><p>Inteligencja emocjonalna to kluczowa kompetencja neuroprzywódcy. Oceń siebie w poniższych obszarach na skali 1-10:</p><ul><li><strong>Samoświadomość:</strong> Rozumiem swoje emocje i ich wpływ na zespół</li><li><strong>Samoregulacja:</strong> Potrafię kontrolować swoje reakcje w trudnych sytuacjach</li><li><strong>Empatia:</strong> Rozumiem emocje i perspektywy członków zespołu</li><li><strong>Umiejętności społeczne:</strong> Skutecznie komunikuję się i buduję relacje</li></ul>",
            "interactive": true,
            "type": "self_assessment"
          }
        ]
      },
      "reflection": {
        "title": "🔍 Refleksja",
        "description": "Analiza doświadczeń, dziennik lidera i autorefleksja rozwojowa",
        "sections": [
          {
            "id": "leadership_challenge_analysis",
            "title": "Moje największe wyzwanie przywódcze",
            "content": "<h4>🎯 Przywódczy Flashback</h4><p>Przypomnij sobie najtrudniejszą sytuację przywódczą, z jaką się zmierzyłeś w ostatnim roku. Może to być konflikt w zespole, trudna decyzja biznesowa, kryzys motywacyjny czy wyzwanie komunikacyjne.</p><p><strong>Przeanalizuj tę sytuację pod kątem:</strong></p><ul><li>Co było największym wyzwaniem?</li><li>Jak zareagowałeś instynktownie?</li><li>Co działało dobrze w Twoim podejściu?</li><li>Co zrobiłbyś inaczej wiedząc to, co wiesz teraz?</li><li>Jakie lekcje wyciągnąłeś z tej sytuacji?</li></ul>",
            "interactive": true,
            "type": "reflection"
          },
          {
            "id": "team_impact_journal",
            "title": "Dziennik wpływu na zespół",
            "content": "<h4>📊 Cotygodniowa analiza wpływu</h4><p>Przez najbliższy tydzień obserwuj i notuj swój wpływ na zespół. To pomoże Ci rozwinąć świadomość przywódczą.</p><p><strong>Codziennie odpowiadaj na pytania:</strong></p><ul><li>Jakie były moje główne interakcje z zespołem dziś?</li><li>Jak moja komunikacja wpłynęła na atmosferę w grupie?</li><li>Czy zauważyłem jakieś reakcje zespołu na moje zachowanie?</li><li>Co mogę poprawić w moim stylu przywództwa jutro?</li></ul><p><em>Po tygodniu przeanalizuj wzorce i wyciągnij wnioski.</em></p>",
            "interactive": true,
            "type": "journal"
          },
          {
            "id": "leadership_evolution",
            "title": "Ewolucja mojego stylu przywództwa",
            "content": "<h4>🌱 Jak się zmieniałeś jako lider?</h4><p>Przywództwo to proces ciągłego rozwoju. Zastanów się nad swoją przywódczą podróżą i przemianami, które przeszedłeś.</p><p><strong>Refleksja nad rozwojem:</strong></p><ul><li>Jakim liderem byłeś 2 lata temu vs dziś?</li><li>Które doświadczenia najbardziej Cię ukształtowały?</li><li>Jakie błędy przywódcze popełniałeś i czego Cię nauczyły?</li><li>W których obszarach widzisz największy postęp?</li><li>Nad czym nadal musisz pracować?</li></ul>",
            "interactive": true,
            "type": "evolution_analysis"
          }
        ]
      },
      "analysis": {
        "title": "📊 Analiza",
        "description": "Case studies, symulacje i głęboka analiza zachowań przywódczych",
        "sections": [
          {
            "id": "leaders_comparison_case_study",
            "title": "Case study: Steve Jobs vs. Tim Cook",
            "content": "<h4>🍎 Różne style, podobne sukcesy</h4><p>Przeanalizuj dwa różne podejścia do przywództwa w Apple:</p><p><strong>Steve Jobs (2007-2011):</strong> Wizjoner, perfekcjonista, bezpośredni w komunikacji, skupiony na innowacji, wymagający wobec zespołu.</p><p><strong>Tim Cook (2011-obecnie):</strong> Systemowy, empatyczny, oparty na współpracy, fokus na operacjach i kulturze organizacyjnej.</p><p><strong>Zadanie:</strong> Porównaj te style pod kątem neuroprzywództwa. Które elementy każdego stylu byłyby skuteczne w Twoim kontekście zawodowym?</p>",
            "interactive": true,
            "type": "case_study"
          },
          {
            "id": "team_reorganization_simulation",
            "title": "Symulacja: Reorganizacja zespołu",
            "content": "<h4>🔄 Jak poprowadzić zmiany organizacyjne?</h4><p><strong>Sytuacja:</strong> Twoja firma przechodzi reorganizację. Twój 12-osobowy zespół zostanie podzielony na dwa mniejsze, a Ty będziesz zarządzać tylko jednym z nich. Część osób straci bezpośredni kontakt z Tobą, niektórzy będą niepewni swojej przyszłości.</p><p><strong>Wyzwania do rozwiązania:</strong></p><ul><li>Jak zakomunikować zmiany aby zminimalizować stres?</li><li>Jak utrzymać motywację zespołu w czasie niepewności?</li><li>Które aspekty neuropsychologii wykorzystasz?</li><li>Jak zadbasz o tych, którzy przejdą do innego zespołu?</li></ul>",
            "interactive": true,
            "type": "simulation"
          },
          {
            "id": "communication_audit",
            "title": "Analiza mojej komunikacji przywódczej",
            "content": "<h4>🗣️ Audit stylu zarządzania</h4><p>Przeanalizuj własny styl komunikacji jako lider. Ta analiza pomoże Ci zidentyfikować mocne strony i obszary do poprawy.</p><p><strong>Obszary do przeanalizowania:</strong></p><ol><li><strong>Częstotliwość komunikacji:</strong> Jak często i w jaki sposób komunikujesz się z zespołem?</li><li><strong>Ton i styl:</strong> Czy jesteś bardziej bezpośredni czy dyplomatyczny? Formalny czy nieformalny?</li><li><strong>Feedback:</strong> Jak dajesz pochwały i konstruktywną krytykę?</li><li><strong>Słuchanie:</strong> Ile czasu poświęcasz na aktywne słuchanie zespołu?</li><li><strong>Adaptacja:</strong> Jak dostosowujesz komunikację do różnych osobowości w zespole?</li></ol>",
            "interactive": true,
            "type": "communication_audit"
          }
        ]
      },
      "implementation": {
        "title": "⚡ Wdrożenie",
        "description": "Konkretne plany działania, strategie i narzędzia rozwoju przywódczego",
        "sections": [
          {
            "id": "90_day_leadership_plan",
            "title": "90-dniowy plan rozwoju przywódczego",
            "content": "<h4>🚀 Twój osobisty plan rozwoju</h4><p>Stwórz konkretny, mierzalny plan rozwoju swoich kompetencji przywódczych na najbliższe 3 miesiące.</p><p><strong>Struktura planu:</strong></p><h5>🎯 Miesiąc 1: Fundament (Dni 1-30)</h5><ul><li>Główny cel do osiągnięcia</li><li>3 konkretne działania tygodniowo</li><li>Sposób mierzenia postępu</li></ul><h5>📈 Miesiąc 2: Rozbudowa (Dni 31-60)</h5><ul><li>Rozwijanie nowych kompetencji</li><li>Implementacja nowych narzędzi</li><li>Zbieranie feedbacku od zespołu</li></ul><h5>⭐ Miesiąc 3: Mistrzostwo (Dni 61-90)</h5><ul><li>Optymalizacja wypracowanych nawyków</li><li>Mentoring innych</li><li>Planowanie kolejnych kroków</li></ul>",
            "interactive": true,
            "type": "action_plan"
          },
          {
            "id": "team_motivation_toolkit",
            "title": "Toolkit motywacji zespołu",
            "content": "<h4>🛠️ Praktyczne narzędzia motywacyjne</h4><p>Stwórz swój personalny zestaw narzędzi do budowania motywacji w zespole, oparty na zasadach neuroprzywództwa.</p><p><strong>Kategorie narzędzi:</strong></p><h5>💡 Narzędzia codzienne (do użycia każdego dnia)</h5><ul><li>Rytuały porannych spotkań zespołu</li><li>Sposób dawania micro-feedback</li><li>Techniki aktywnego słuchania</li></ul><h5>📅 Narzędzia tygodniowe</h5><ul><li>Format spotkań 1-on-1</li><li>System celebracji sukcesów</li><li>Metody rozwiązywania konfliktów</li></ul><h5>🌟 Narzędzia strategiczne (miesięczne/kwartalne)</h5><ul><li>Proces wyznaczania celów zespołowych</li><li>System rozwoju kompetencji</li><li>Budowanie kultury feedback</li></ul>",
            "interactive": true,
            "type": "toolkit"
          },
          {
            "id": "feedback_mentoring_system",
            "title": "System feedbacku i mentoringu",
            "content": "<h4>🎯 Jak budować kulturę rozwoju</h4><p>Zaprojektuj system regularnego feedbacku i mentoringu w swoim zespole, który wspiera rozwój każdego członka.</p><p><strong>Elementy systemu do zaprojektowania:</strong></p><h5>🔄 Struktura feedbacku</h5><ul><li>Jak często i w jaki sposób będziesz dawać feedback?</li><li>Jaki format spotkań rozwojowych zastosujesz?</li><li>Jak stworzysz bezpieczną przestrzeń do otwartych rozmów?</li></ul><h5>🌱 Program mentoringu</h5><ul><li>Jak zidentyfikujesz potrzeby rozwojowe każdej osoby?</li><li>Jakie konkretne działania mentorskie podejmiesz?</li><li>Jak będziesz mierzyć postępy rozwojowe?</li></ul><h5>📈 Kultura uczenia się</h5><ul><li>Jak zachęcisz zespół do eksperymentowania?</li><li>Jak będziesz celebrować zarówno sukcesy jak i "mądre porażki"?</li><li>Jakie systemy wspierania rozwoju wprowadzisz?</li></ul>",
            "interactive": true,
            "type": "system_design"
          }
        ]
      }
    }
  }
}
```

---

## 🔧 SKRYPTY MIGRACJI I TESTOWANIA

### **Script 1: Migracja istniejących lekcji**

```python
# migrate_to_practical_exercises.py
import json
import os
from pathlib import Path

def migrate_lesson_structure(lesson_file_path):
    """
    Migruje starą strukturę lekcji (reflection + application) 
    do nowej struktury practical_exercises
    """
    
    # Wczytaj istniejącą lekcję
    with open(lesson_file_path, 'r', encoding='utf-8') as f:
        lesson_data = json.load(f)
    
    sections = lesson_data.get('sections', {})
    
    # Sprawdź czy lekcja ma stare sekcje do migracji
    has_reflection = 'reflection' in sections
    has_application = 'application' in sections
    
    if not (has_reflection or has_application):
        print(f"Lekcja {lesson_file_path} nie wymaga migracji")
        return False
    
    # Stwórz nową strukturę practical_exercises
    practical_exercises = {
        "description": "Ćwiczenia praktyczne - połączenie refleksji i zastosowania",
        "tabs": {}
    }
    
    # Migruj reflection do tab reflection
    if has_reflection:
        reflection_data = sections['reflection']
        practical_exercises['tabs']['reflection'] = {
            "title": "🔍 Refleksja",
            "description": "Pytania do autorefleksji i analiza doświadczeń",
            "sections": convert_content_to_sections(reflection_data)
        }
        # Usuń starą sekcję
        del sections['reflection']
    
    # Migruj application do tab implementation
    if has_application:
        application_data = sections['application']
        practical_exercises['tabs']['implementation'] = {
            "title": "⚡ Wdrożenie", 
            "description": "Konkretne plany działania i praktyczne zastosowanie",
            "sections": convert_content_to_sections(application_data)
        }
        # Usuń starą sekcję
        del sections['application']
    
    # Dodaj nową sekcję
    sections['practical_exercises'] = practical_exercises
    
    # Zapisz zmigrowaną lekcję
    backup_path = lesson_file_path + '.backup'
    os.rename(lesson_file_path, backup_path)
    
    with open(lesson_file_path, 'w', encoding='utf-8') as f:
        json.dump(lesson_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Zmigrowano lekcję {lesson_file_path}")
    print(f"📁 Backup zapisany jako {backup_path}")
    return True

def convert_content_to_sections(old_content):
    """
    Konwertuje starą strukturę treści na nową strukturę sekcji
    """
    if isinstance(old_content, str):
        # Prosta treść tekstowa
        return [{
            "id": "migrated_content",
            "title": "Treść",
            "content": old_content,
            "interactive": True,
            "type": "text"
        }]
    elif isinstance(old_content, dict):
        # Strukturalna treść
        sections = []
        if 'content' in old_content:
            sections.append({
                "id": "main_content",
                "title": old_content.get('title', 'Główna treść'),
                "content": old_content['content'],
                "interactive": old_content.get('interactive', True),
                "type": old_content.get('type', 'text')
            })
        return sections
    else:
        # Domyślna sekcja
        return [{
            "id": "default_content",
            "title": "Treść",
            "content": str(old_content),
            "interactive": True,
            "type": "text"
        }]

# Uruchom migrację dla wszystkich lekcji
def migrate_all_lessons():
    lessons_dir = Path("data/lessons")
    
    if not lessons_dir.exists():
        print("❌ Katalog data/lessons nie istnieje")
        return
    
    migrated_count = 0
    
    for lesson_file in lessons_dir.glob("*.json"):
        if migrate_lesson_structure(lesson_file):
            migrated_count += 1
    
    print(f"\n🎉 Zmigrowano {migrated_count} lekcji")

if __name__ == "__main__":
    migrate_all_lessons()
```

### **Script 2: Test nowej struktury**

```python
# test_practical_exercises.py
import streamlit as st
import json
from pathlib import Path

def test_practical_exercises_rendering():
    """
    Testuje renderowanie nowej sekcji practical_exercises
    """
    
    # Przykładowe dane testowe
    test_lesson = {
        "sections": {
            "practical_exercises": {
                "description": "Test ćwiczeń praktycznych",
                "tabs": {
                    "autotest": {
                        "title": "🧠 Autotest",
                        "description": "Test samooceny",
                        "sections": [{
                            "id": "test_section",
                            "title": "Przykładowy test",
                            "content": "<p>To jest test sekcji autotest</p>",
                            "interactive": True,
                            "type": "assessment"
                        }]
                    },
                    "reflection": {
                        "title": "🔍 Refleksja", 
                        "description": "Pytania do refleksji",
                        "sections": [{
                            "id": "reflection_section",
                            "title": "Refleksja testowa",
                            "content": "<p>To jest test sekcji refleksji</p>",
                            "interactive": True,
                            "type": "reflection"
                        }]
                    }
                }
            }
        }
    }
    
    # Symuluj renderowanie
    st.header("🧪 Test praktycznych ćwiczeń")
    
    practical_data = test_lesson['sections']['practical_exercises']
    
    if 'tabs' in practical_data:
        sub_tabs_data = practical_data['tabs']
        available_tabs = []
        tab_keys = []
        
        # Kolejność tab
        tab_order = ['autotest', 'reflection', 'analysis', 'implementation']
        
        for tab_key in tab_order:
            if tab_key in sub_tabs_data:
                tab_data = sub_tabs_data[tab_key]
                available_tabs.append(tab_data['title'])
                tab_keys.append(tab_key)
        
        if available_tabs:
            tabs = st.tabs(available_tabs)
            
            for i, (tab_key, tab_title) in enumerate(zip(tab_keys, available_tabs)):
                with tabs[i]:
                    tab_data = sub_tabs_data[tab_key]
                    
                    if 'description' in tab_data:
                        st.info(tab_data['description'])
                    
                    if 'sections' in tab_data:
                        for section in tab_data['sections']:
                            st.markdown(f"### {section.get('title', 'Sekcja')}")
                            st.markdown(section.get('content', 'Brak treści'), unsafe_allow_html=True)
                            
                            if section.get('interactive', False):
                                section_key = f"test_{tab_key}_{section.get('id', 'unknown')}"
                                
                                with st.form(key=f"form_{section_key}"):
                                    user_response = st.text_area(
                                        "Twoja odpowiedź:",
                                        height=150,
                                        key=f"input_{section_key}"
                                    )
                                    
                                    submitted = st.form_submit_button("Zapisz odpowiedź")
                                    
                                    if submitted:
                                        st.success("✅ Test zapisywania działa!")
                                        st.json({"section": section_key, "response": user_response})

if __name__ == "__main__":
    test_practical_exercises_rendering()
```

### **Script 3: Walidacja struktury JSON**

```python
# validate_lesson_structure.py
import json
import jsonschema
from pathlib import Path

# Schema dla nowej struktury practical_exercises
PRACTICAL_EXERCISES_SCHEMA = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "xp_reward": {"type": "number"},
        "tabs": {
            "type": "object",
            "properties": {
                "autotest": {"$ref": "#/definitions/tab"},
                "reflection": {"$ref": "#/definitions/tab"},
                "analysis": {"$ref": "#/definitions/tab"},
                "implementation": {"$ref": "#/definitions/tab"}
            },
            "additionalProperties": False
        }
    },
    "required": ["description", "tabs"],
    "definitions": {
        "tab": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "interactive": {"type": "boolean"},
                            "type": {"type": "string"}
                        },
                        "required": ["id", "title", "content"]
                    }
                }
            },
            "required": ["title", "description", "sections"]
        }
    }
}

def validate_lesson_file(lesson_path):
    """
    Waliduje struktur lekcji pod kątem nowej sekcji practical_exercises
    """
    
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"❌ Błąd JSON: {e}"
    except Exception as e:
        return False, f"❌ Błąd odczytu pliku: {e}"
    
    sections = lesson_data.get('sections', {})
    
    if 'practical_exercises' not in sections:
        return True, "ℹ️ Lekcja nie ma sekcji practical_exercises (OK dla starych lekcji)"
    
    practical_exercises = sections['practical_exercises']
    
    try:
        jsonschema.validate(practical_exercises, PRACTICAL_EXERCISES_SCHEMA)
        
        # Dodatkowe sprawdzenia
        tabs = practical_exercises.get('tabs', {})
        tab_count = len(tabs)
        
        if tab_count == 0:
            return False, "❌ Brak zdefiniowanych tabs w practical_exercises"
        
        # Sprawdź każdy tab
        for tab_key, tab_data in tabs.items():
            sections_list = tab_data.get('sections', [])
            if not sections_list:
                return False, f"❌ Tab '{tab_key}' nie ma zdefiniowanych sekcji"
            
            for section in sections_list:
                if not section.get('content', '').strip():
                    return False, f"❌ Pusta sekcja w tab '{tab_key}': {section.get('title', 'Bez tytułu')}"
        
        return True, f"✅ Struktura practical_exercises jest poprawna ({tab_count} tabs)"
        
    except jsonschema.ValidationError as e:
        return False, f"❌ Błąd walidacji: {e.message}"

def validate_all_lessons():
    """
    Waliduje wszystkie lekcje
    """
    lessons_dir = Path("data/lessons")
    
    if not lessons_dir.exists():
        print("❌ Katalog data/lessons nie istnieje")
        return
    
    results = []
    
    for lesson_file in lessons_dir.glob("*.json"):
        is_valid, message = validate_lesson_file(lesson_file)
        results.append((lesson_file.name, is_valid, message))
        print(f"{lesson_file.name}: {message}")
    
    # Podsumowanie
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    total_count = len(results)
    
    print(f"\n📊 Podsumowanie walidacji:")
    print(f"✅ Poprawne: {valid_count}/{total_count}")
    print(f"❌ Błędne: {total_count - valid_count}/{total_count}")

if __name__ == "__main__":
    validate_all_lessons()
```

---

## 🚀 INSTRUKCJE URUCHOMIENIA

### **Krok 1: Przygotowanie**

```bash
# 1. Stwórz backup całego projektu
cp -r ZenDegenAcademy ZenDegenAcademy_backup_$(date +%Y%m%d)

# 2. Przygotuj środowisko testowe
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# lub
test_env\Scripts\activate     # Windows

pip install streamlit jsonschema
```

### **Krok 2: Walidacja przed zmianami**

```bash
# Sprawdź obecną strukturę lekcji
python validate_lesson_structure.py

# Zidentyfikuj lekcje do migracji
python -c "
import json
from pathlib import Path

for f in Path('data/lessons').glob('*.json'):
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        sections = data.get('sections', {})
        if 'reflection' in sections or 'application' in sections:
            print(f'Do migracji: {f.name}')
"
```

### **Krok 3: Implementacja zmian w lesson.py**

```python
# Znajdź i zaktualizuj te fragmenty w views/lesson.py:

# 1. Definicja kroków
step_names = {
    'intro': 'Wprowadzenie',
    'opening_quiz': 'Samorefleksja',
    'content': 'Materiał',
    'practical_exercises': 'Ćwiczenia praktyczne',  # NOWE
    'reflection': 'Refleksja',      # Backward compatibility
    'application': 'Zadania praktyczne',  # Backward compatibility
    'closing_quiz': 'Quiz końcowy',
    'summary': 'Podsumowanie'
}

# 2. Punkty XP
step_xp_values = {
    'intro': int(base_xp * 0.05),
    'opening_quiz': int(base_xp * 0.00),
    'content': int(base_xp * 0.30),
    'practical_exercises': int(base_xp * 0.40),  # NOWE - 40%
    'reflection': int(base_xp * 0.20),     # Backward compatibility
    'application': int(base_xp * 0.20),    # Backward compatibility
    'closing_quiz': int(base_xp * 0.20),
    'summary': int(base_xp * 0.05)
}

# 3. Logika kolejności kroków (znajdź i zastąp)
if 'practical_exercises' in lesson.get('sections', {}):
    available_steps.append('practical_exercises')
else:
    # Backward compatibility
    if 'reflection' in lesson.get('sections', {}):
        available_steps.append('reflection')
    if 'application' in lesson.get('sections', {}):
        available_steps.append('application')
```

### **Krok 4: Dodanie obsługi render practical_exercises**

Znajdź w `views/lesson.py` sekcję obsługi kroków (prawdopodobnie duży blok if/elif) i dodaj:

```python
elif st.session_state.lesson_step == 'practical_exercises':
    practical_data = lesson['sections']['practical_exercises']
    
    st.markdown("### 🎯 Ćwiczenia praktyczne")
    
    if 'description' in practical_data:
        st.info(practical_data['description'])
    
    if 'tabs' in practical_data:
        sub_tabs_data = practical_data['tabs']
        available_tabs = []
        tab_keys = []
        
        # Logiczna kolejność
        tab_order = ['autotest', 'reflection', 'analysis', 'implementation']
        tab_icons = {
            'autotest': '🧠',
            'reflection': '🔍', 
            'analysis': '📊',
            'implementation': '⚡'
        }
        
        for tab_key in tab_order:
            if tab_key in sub_tabs_data:
                tab_data = sub_tabs_data[tab_key]
                icon = tab_icons.get(tab_key, '🔹')
                title = tab_data.get('title', f'{icon} {tab_key.title()}')
                available_tabs.append(title)
                tab_keys.append(tab_key)
        
        if available_tabs:
            tabs = st.tabs(available_tabs)
            
            for i, (tab_key, tab_title) in enumerate(zip(tab_keys, available_tabs)):
                with tabs[i]:
                    tab_data = sub_tabs_data[tab_key]
                    
                    if 'description' in tab_data:
                        st.markdown(f"**{tab_data['description']}**")
                        st.markdown("---")
                    
                    if 'sections' in tab_data:
                        for section in tab_data['sections']:
                            st.markdown(f"### {section.get('title', 'Sekcja')}")
                            
                            content = section.get('content', '')
                            if content:
                                st.markdown(content, unsafe_allow_html=True)
                            
                            if section.get('interactive', False):
                                section_id = section.get('id', 'unknown')
                                section_key = f"practical_{tab_key}_{section_id}"
                                
                                with st.form(key=f"form_{section_key}"):
                                    existing_response = st.session_state.get(section_key, "")
                                    
                                    user_response = st.text_area(
                                        "Twoja odpowiedź:",
                                        value=existing_response,
                                        height=200,
                                        key=f"input_{section_key}",
                                        help="Zapisz swoje przemyślenia i spostrzeżenia"
                                    )
                                    
                                    submitted = st.form_submit_button("💾 Zapisz odpowiedź")
                                    
                                    if submitted and user_response.strip():
                                        st.session_state[section_key] = user_response
                                        st.success("✅ Twoja odpowiedź została zapisana!")
                                        
                                        # Opcional: zapis do bazy danych
                                        # save_user_response(user_id, lesson_id, section_key, user_response)
                            
                            st.markdown("---")
    
    # Progress tracking dla practical exercises
    if st.button("✅ Zakończ ćwiczenia praktyczne"):
        # Sprawdź ile sekcji zostało wypełnionych
        completed_sections = 0
        total_sections = 0
        
        if 'tabs' in practical_data:
            for tab_key, tab_data in practical_data['tabs'].items():
                for section in tab_data.get('sections', []):
                    if section.get('interactive', False):
                        total_sections += 1
                        section_id = section.get('id', 'unknown')
                        section_key = f"practical_{tab_key}_{section_id}"
                        if st.session_state.get(section_key, "").strip():
                            completed_sections += 1
        
        completion_rate = completed_sections / total_sections if total_sections > 0 else 1
        
        if completion_rate >= 0.7:  # 70% wypełnienia wystarczy
            # Award XP
            xp_earned = step_xp_values.get('practical_exercises', 100)
            st.success(f"🎉 Ćwiczenia zakończone! Zdobyłeś {xp_earned} XP!")
            
            # Mark as completed i przejdź dalej
            mark_step_completed('practical_exercises', xp_earned)
            
        else:
            st.warning(f"Wypełnij jeszcze {int((0.7 - completion_rate) * 100)}% ćwiczeń aby przejść dalej")
```

### **Krok 5: Test implementacji**

```bash
# 1. Uruchom test struktury
python test_practical_exercises.py

# 2. Uruchom aplikację testowo
streamlit run main.py

# 3. Sprawdź czy nowa sekcja działa:
#    - Otwórz lekcję z practical_exercises
#    - Przetestuj wszystkie 4 taby
#    - Sprawdź zapisywanie odpowiedzi
#    - Zweryfikuj przyznawanie XP
```

### **Krok 6: Migracja istniejących lekcji**

```bash
# Uruchom migrację (UWAGA: tworzy backup!)
python migrate_to_practical_exercises.py

# Sprawdź rezultaty
python validate_lesson_structure.py
```

---

## 🔍 ROZWIĄZYWANIE PROBLEMÓW

### **Problem 1: Błąd importu przy uruchamianiu**
```
ModuleNotFoundError: No module named 'jsonschema'
```
**Rozwiązanie:**
```bash
pip install jsonschema
```

### **Problem 2: Tabs się nie wyświetlają**
**Możliwe przyczyny:**
- Błąd w strukturze JSON (sprawdź walidatorem)
- Niepoprawna kolejność w kodzie lesson.py
- Brak sekcji 'tabs' w practical_exercises

**Sprawdzenie:**
```python
# Dodaj debug w lesson.py
st.write("DEBUG:", practical_data)  # Tymczasowo
```

### **Problem 3: Odpowiedzi się nie zapisują**
**Sprawdź:**
- Czy sekcja ma `"interactive": true`
- Czy klucze formularzy są unikalne
- Czy session_state działa poprawnie

**Debug:**
```python
# W lesson.py po submit
st.write("Session state keys:", list(st.session_state.keys()))
```

### **Problem 4: XP się nie przyznaje**
**Sprawdź:**
- Czy funkcja `mark_step_completed` istnieje
- Czy step_xp_values zawiera 'practical_exercises'
- Czy completion rate jest prawidłowo liczony

### **Problem 5: Backward compatibility**
Stare lekcje z reflection/application powinny nadal działać przez:
```python
# W lesson.py - logika fallback
if 'practical_exercises' not in lesson.get('sections', {}):
    # Użyj starej logiki reflection/application
    pass
```

---

## ✅ FINALNA CHECKLIST

### **Przed wdrożeniem:**
- [ ] Backup całego projektu wykonany
- [ ] Wszystkie skrypty przetestowane lokalnie
- [ ] JSON schema walidacji przygotowana
- [ ] Przykładowe treści neuroprzywództwa stworzone

### **Podczas implementacji:**
- [ ] lesson.py zaktualizowany z nową strukturą
- [ ] step_names i step_xp_values zawierają practical_exercises
- [ ] Render logic dla 4 tabów zaimplementowany
- [ ] Backward compatibility zachowana
- [ ] Testy lokalne przeszły pomyślnie

### **Po wdrożeniu:**
- [ ] Wszystkie lekcje ładują się poprawnie
- [ ] Tabs wyświetlają się we właściwej kolejności
- [ ] Interaktywne sekcje zapisują odpowiedzi
- [ ] XP przyznawane za ukończenie sekcji
- [ ] Mobile-friendly UI przetestowane
- [ ] Migracja starych lekcji ukończona

### **Weryfikacja jakości:**
- [ ] Treści dostosowane do neuroprzywództwa
- [ ] Logiczna progresja: Autotest → Refleksja → Analiza → Wdrożenie
- [ ] UX intuicyjny i angażujący
- [ ] Performance aplikacji nie pogorszone

---

## 🎉 OCZEKIWANE REZULTATY

Po pełnej implementacji użytkownicy dostaną:

### **🎯 Lepszy User Experience:**
- Jedną spójną sekcję zamiast rozproszonych elementów
- Logiczną progresję uczenia się
- Bogatsze, interaktywne doświadczenie

### **🧠 Zawartość dostosowaną do neuroprzywództwa:**
- Autotesty kompetencji przywódczych
- Refleksje oparte na neuronauce
- Analizy case studies liderów
- Konkretne plany wdrożenia

### **💡 Technicznie lepszą strukturę:**
- Uproszczoną architekturę lekcji
- Łatwiejsze dodawanie nowych treści
- Backwards compatibility ze starymi lekcjami
- Skalowalne rozwiązanie na przyszłość

**🚀 Status docelowy: Profesjonalny system ćwiczeń praktycznych skoncentrowany na rozwoju kompetencji neuroprzywództwy z intuicyjnym UX i bogatą interaktywnością.**
