"""
Moduł narzędzi AI dla BrainVenture Academy
Zawiera zaawansowane narzędzia do rozwoju umiejętności komunikacyjnych i przywództwa
"""

import streamlit as st
from utils.ai_exercises import AIExerciseEvaluator
from utils.components import zen_header, zen_button, stat_card
import json
from typing import Dict, List, Optional

def show_tools_page():
    """Główna strona narzędzi AI"""
    
    # Header strony
    zen_header(
        "🛠️ Narzędzia AI", 
        "Zaawansowane narzędzia do rozwoju umiejętności komunikacyjnych i przywództwa"
    )
    
    # Główne kategorie w tabach
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 C-IQ Tools", 
        "🎭 Symulatory", 
        "📊 Analityki", 
        "🤖 AI Asystent"
    ])
    
    with tab1:
        show_ciq_tools()
    
    with tab2:
        show_simulators()
    
    with tab3:
        show_analytics()
        
    with tab4:
        show_ai_assistant()

def show_ciq_tools():
    """Narzędzia Conversational Intelligence"""
    st.markdown("### 🧠 Narzędzia Conversational Intelligence")
    st.markdown("Wykorzystaj moc AI do analizy i doskonalenia komunikacji na poziomach C-IQ")
    
    # Siatka narzędzi
    col1, col2 = st.columns(2)
    
    with col1:
        # C-IQ Scanner
        with st.container():
            st.markdown("""
            <div style='padding: 20px; border: 2px solid #4CAF50; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);'>
                <h4>🎯 C-IQ Scanner</h4>
                <p><strong>Zeskanuj poziom komunikacji I otrzymaj wersje na wyższych poziomach C-IQ</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>📡 Szybkie skanowanie poziomów komunikacji (I, II, III)</li>
                    <li>⚡ Błyskawiczna konwersja na wyższe poziomy</li>
                    <li>🧠 Analiza wpływu neurobiologicznego</li>
                    <li>🎯 Gotowe alternatywne wersje do użycia</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if zen_button("🎯 Uruchom C-IQ Scanner", key="level_detector", width='stretch'):
                st.session_state.active_tool = "level_detector"
        
    with col2:
        # Detektor Emocji
        with st.container():
            st.markdown("""
            <div style='padding: 20px; border: 2px solid #E91E63; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #ffeef8 0%, #f8bbd9 100%);'>
                <h4>😊 Detektor Emocji</h4>
                <p><strong>Identyfikuj emocje i ich wpływ neurobiologiczny</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>💭 Analiza emocji w tekście</li>
                    <li>🧬 Wpływ na kortyzol/oksytocynę</li>
                    <li>🎯 Strategie regulacji emocji</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if zen_button("😊 Uruchom Detektor Emocji", key="emotion_detector", width='stretch'):
                st.session_state.active_tool = "emotion_detector"
        
        # Analizator Komunikacji
        with st.container():
            st.markdown("""
            <div style='padding: 20px; border: 2px solid #2196F3; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #e3f2fd 0%, #90caf9 100%);'>
                <h4>📝 Analizator Komunikacji</h4>
                <p><strong>Kompleksowa analiza stylu komunikacyjnego</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>📊 Wielowymiarowa analiza</li>
                    <li>🎭 Styl komunikacyjny</li>
                    <li>🔍 Szczegółowy raport</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if zen_button("📝 Uruchom Analizator", key="communication_analyzer", width='stretch'):
                st.session_state.active_tool = "communication_analyzer"
    
    # Wyświetl aktywne narzędzie
    active_tool = st.session_state.get('active_tool')
    if active_tool:
        st.markdown("---")
        
        # Przycisk resetowania
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if zen_button("❌ Zamknij narzędzie", key="close_tool", width='stretch'):
                del st.session_state.active_tool
                st.rerun()
        
        st.markdown("---")
        
        if active_tool == 'level_detector':
            show_level_detector()
        elif active_tool == 'emotion_detector':
            show_emotion_detector()
        elif active_tool == 'communication_analyzer':
            show_communication_analyzer()

def show_level_detector():
    """C-IQ Scanner - główna funkcjonalność"""
    st.markdown("## 🎯 C-IQ Scanner")
    st.markdown("**Zeskanuj poziom komunikacji** i **zobacz alternatywne wersje** na wyższych poziomach Conversational Intelligence")
    
    # Tabs z różnymi trybami
    tab1, tab2, tab3 = st.tabs([
        "📝 Analiza tekstu", 
        "💬 Przykłady poziomów", 
        "📧 Szablony emaili"
    ])
    
    with tab1:
        st.markdown("#### Wklej dowolny tekst do analizy C-IQ")
        
        # Przykłady do szybkiego testowania
        with st.expander("💡 Przykłady do przetestowania", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Poziom I (Transakcyjny):**")
                example_1 = "Wyślij raport do końca dnia. Brak dyskusji."
                if st.button("📋 Użyj przykładu", key="example_1"):
                    st.session_state.level_detector_input = example_1
                
                st.markdown("**Poziom II (Pozycyjny):**") 
                example_2 = "Uważam, że ten pomysł nie ma sensu. Moja propozycja jest lepsza bo..."
                if st.button("📋 Użyj przykładu", key="example_2"):
                    st.session_state.level_detector_input = example_2
            
            with col2:
                st.markdown("**Poziom III (Transformacyjny):**")
                example_3 = "Jakie widzisz możliwości w tej sytuacji? Jak możemy razem wypracować rozwiązanie, które będzie działać dla wszystkich?"
                if st.button("📋 Użyj przykładu", key="example_3"):
                    st.session_state.level_detector_input = example_3
        
        text_input = st.text_area(
            "Tekst do analizy:",
            value=st.session_state.get('level_detector_input', ''),
            placeholder="Wklej tutaj email, transkrypcję rozmowy, lub planowaną wypowiedź...",
            height=200,
            key="level_detector_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if zen_button("📡 Skanuj poziom C-IQ", key="analyze_level", width='stretch'):
                if text_input.strip():
                    with st.spinner("🤖 Scanner analizuje poziom rozmowy..."):
                        result = analyze_conversation_level(text_input)
                        if result:
                            st.session_state.last_analysis_result = result
                            # Usunięto duplikację - wynik pojawi się poniżej
                        else:
                            st.error("Nie udało się przeanalizować tekstu. Spróbuj ponownie.")
                else:
                    st.warning("⚠️ Wpisz tekst do analizy")
        
        with col2:
            if text_input:
                word_count = len(text_input.split())
                st.metric("Słowa", word_count)
        
        # Wyświetl wynik analizy jeśli istnieje
        if 'last_analysis_result' in st.session_state and text_input.strip():
            st.markdown("---")
            
            if st.session_state.last_analysis_result.get('analyzed_text') != text_input:
                st.warning("⚠️ Pokazuję wynik dla poprzedniego tekstu. Kliknij 'Analizuj' ponownie.")
                
            display_level_analysis(st.session_state.last_analysis_result)
    
    with tab2:
        show_ciq_examples()
    
    with tab3:
        show_email_templates()

def analyze_conversation_level(text: str) -> Optional[Dict]:
    """Analizuje poziom C-IQ w tekście"""
    
    evaluator = AIExerciseEvaluator()
    
    # Sprawdź czy evaluator jest w demo mode
    if hasattr(evaluator, 'demo_mode') and evaluator.demo_mode:
        st.info("ℹ️ C-IQ Scanner w trybie demo - używam analizy heurystycznej")
        return create_fallback_analysis(text)
    
    prompt = f"""
Jesteś ekspertem w Conversational Intelligence. Przeanalizuj następujący tekst i określ jego poziom C-IQ.

TEKST DO ANALIZY:
"{text}"

POZIOMY C-IQ:
- **Poziom I (Transakcyjny)**: Wymiana informacji, fokus na zadania, język dyrektywny, brak emocji, jednokierunkowa komunikacja
- **Poziom II (Pozycyjny)**: Obrona stanowisk, argumentowanie, "my vs oni", konfrontacja, przekonywanie, walka o rację  
- **Poziom III (Transformacyjny)**: Współtworzenie, pytania otwarte, "wspólny cel", budowanie zaufania, język partnerski

WAŻNE: 
1. Odpowiedz TYLKO w poprawnym formacie JSON, bez dodatkowych komentarzy.
2. MUSISZ wybrać JEDEN dominujący poziom - nie można wykrywać wielu poziomów jednocześnie:
   - "detected_level" może być tylko: "Poziom I" lub "Poziom II" lub "Poziom III"
   - Wybierz poziom który najlepiej charakteryzuje CAŁOŚĆ tekstu
   - Jeśli tekst zawiera elementy różnych poziomów, wybierz ten który DOMINUJE
3. W sekcji "alternative_versions" podaj alternatywy TYLKO dla poziomów wyższych niż wykryty:
   - Jeśli wykryjesz Poziom I: podaj wersje dla II i III
   - Jeśli wykryjesz Poziom II: podaj wersję tylko dla III  
   - Jeśli wykryjesz Poziom III: pozostaw alternative_versions puste {{}}

{{
    "detected_level": "Poziom I/II/III",
    "confidence": [1-10],
    "explanation": "Szczegółowe wyjaśnienie dlaczego to ten poziom - cytuj konkretne fragmenty",
    "key_indicators": ["konkretny wskaźnik językowy 1", "konkretny wskaźnik językowy 2"],
    "neurobiological_impact": "Przewidywany wpływ na hormony - czy wzbudza kortyzol (stres) czy oksytocynę (zaufanie)",
    "improvement_suggestions": ["jak podnieść na wyższy poziom - konkretne zmiany"],
    "alternative_versions": {{
        "level_ii": "Jak brzmiałby ten tekst przepisany na poziom II (tylko jeśli wykryty poziom to I)",
        "level_iii": "Jak brzmiałby ten tekst przepisany na poziom III (jeśli wykryty poziom to I lub II)"
    }},
    "practical_tips": ["konkretna wskazówka komunikacyjna 1", "konkretna wskazówka 2"],
    "emotional_tone": "neutralny/pozytywny/negatywny/agresywny/partnerski",
    "trust_building_score": [1-10],
    "language_patterns": ["wzorzec językowy 1", "wzorzec językowy 2"]
}}
"""
    
    try:
        # Użyj bezpośrednio funkcji z AIExerciseEvaluator
        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            
            if response and response.text:
                content = response.text.strip()
                
                # Usuń markdown formatowanie jeśli jest
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                # Spróbuj sparsować JSON
                import json
                import re
                
                # Znajdź JSON w odpowiedzi
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    
                    try:
                        result = json.loads(json_str)
                        
                        # Sprawdź czy mamy wymagane pola dla detektora C-IQ
                        if 'detected_level' in result and 'confidence' in result:
                            st.success("✅ Skanowanie C-IQ ukończone!")
                            # Dodaj analizowany tekst do wyniku
                            result['analyzed_text'] = text
                            return result
                        else:
                            st.warning("⚠️ AI zwróciło niepełną analizę")
                            st.json(result)  # Pokaż co zwróciło
                            return create_fallback_analysis(text)
                            
                    except json.JSONDecodeError as json_err:
                        st.error(f"❌ Błąd parsowania JSON: {str(json_err)}")
                        st.warning("Używam analizy backup zamiast niepoprawnego JSON")
                        return create_fallback_analysis(text)
                else:
                    st.warning("⚠️ Nie udało się znaleźć JSON w odpowiedzi AI")
                    return create_fallback_analysis(text)
            else:
                st.warning("⚠️ AI nie zwróciło odpowiedzi")
                return create_fallback_analysis(text)
        else:
            st.warning("⚠️ Model AI niedostępny")
            return create_fallback_analysis(text)
            
    except Exception as e:
        st.error(f"❌ Błąd podczas analizy: {str(e)}")
        return create_fallback_analysis(text)

def create_fallback_analysis(text: str) -> Dict:
    """Tworzy fallback analizę gdy AI nie działa"""
    
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Prosta heurystyka do określenia poziomu
    level_iii_keywords = ['jak', 'możemy', 'razem', 'wspólnie', 'jakie', 'czy moglibyśmy', 'co myślisz', 'jak widzisz']
    level_ii_keywords = ['uważam', 'myślę że', 'nie zgadzam się', 'moja propozycja', 'lepiej by było']
    level_i_keywords = ['wyślij', 'zrób', 'musisz', 'wykonaj', 'deadline', 'koniec']
    
    level_iii_score = sum(1 for keyword in level_iii_keywords if keyword in text_lower)
    level_ii_score = sum(1 for keyword in level_ii_keywords if keyword in text_lower)
    level_i_score = sum(1 for keyword in level_i_keywords if keyword in text_lower)
    
    if level_iii_score > max(level_ii_score, level_i_score):
        detected_level = "Poziom III"
        confidence = min(9, 6 + level_iii_score)
        trust_score = min(9, 7 + level_iii_score)
        explanation = "Tekst zawiera elementy współtworzenia i pytania otwarte charakterystyczne dla Poziomu III."
    elif level_ii_score > level_i_score:
        detected_level = "Poziom II" 
        confidence = min(8, 5 + level_ii_score)
        trust_score = max(3, 6 - level_ii_score)
        explanation = "Tekst zawiera elementy argumentacji i obrony stanowisk charakterystyczne dla Poziomu II."
    else:
        detected_level = "Poziom I"
        confidence = min(8, 5 + level_i_score) 
        trust_score = max(2, 5 - level_i_score)
        explanation = "Tekst ma charakter transakcyjny i dyrektywny charakterystyczny dla Poziomu I."
    
    # Twórz alternatywne wersje zależnie od wykrytego poziomu
    alternative_versions = {}
    
    if detected_level == "Poziom I":
        alternative_versions = {
            "level_ii": f"Uważam, że ta sytuacja wymaga analizy. Moja perspektywa jest taka, że...",
            "level_iii": f"Jakie widzimy możliwości w tej sytuacji? Jak możemy razem wypracować najlepsze rozwiązanie?"
        }
    elif detected_level == "Poziom II":
        alternative_versions = {
            "level_iii": f"Jakie widzimy możliwości w tej sytuacji? Jak możemy razem wypracować rozwiązanie, które będzie działać dla wszystkich?"
        }
    # Poziom III nie ma alternatyw - to już najwyższy poziom
    
    return {
        "analyzed_text": text,
        "detected_level": detected_level,
        "confidence": confidence,
        "explanation": explanation,
        "key_indicators": [f"Długość tekstu: {word_count} słów", "Analiza heurystyczna słów kluczowych"],
        "neurobiological_impact": f"Przewidywany wpływ odpowiada charakterystyce {detected_level}",
        "improvement_suggestions": ["Dodaj więcej pytań otwartych", "Użyj języka współtworzenia"] if detected_level != "Poziom III" else ["Kontynuuj używanie transformacyjnego stylu komunikacji"],
        "alternative_versions": alternative_versions,
        "practical_tips": ["Zadawaj więcej pytań otwartych", "Używaj języka 'my' zamiast 'ty'"] if detected_level != "Poziom III" else ["Wykorzystuj moc współtworzenia", "Buduj na osiągniętym wysokim poziomie"],
        "emotional_tone": "neutralny",
        "trust_building_score": trust_score,
        "language_patterns": ["Wykryte wzorce na podstawie analizy słów kluczowych"]
    }

def display_level_analysis(result: Dict):
    """Wyświetla wyniki analizy poziom C-IQ"""
    
    if not result:
        st.error("Brak wyników analizy")
        return
    
    # Główny wynik w metrykach
    level = result.get('detected_level', 'Nie określono')
    confidence = result.get('confidence', 0)
    trust_score = result.get('trust_building_score', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Wykryty poziom", level)
    with col2:
        st.metric("🎲 Pewność analizy", f"{confidence}/10")
    with col3:
        st.metric("🤝 Budowanie zaufania", f"{trust_score}/10")
    
    # Wizualizacja poziomów z kolorami - poprawiona logika wykrywania
    st.markdown("### 📊 Analiza poziomów C-IQ")
    
    level_info = {
        "Poziom I": {"color": "🔴", "desc": "Transakcyjny - wymiana informacji", "bg": "#ffebee"},
        "Poziom II": {"color": "🟡", "desc": "Pozycyjny - obrona stanowisk", "bg": "#fff8e1"}, 
        "Poziom III": {"color": "🟢", "desc": "Transformacyjny - współtworzenie", "bg": "#e8f5e8"}
    }
    
    # Lepsze wykrywanie dominującego poziomu  
    detected_level = result.get('detected_level', '').strip()
    
    for lvl, info in level_info.items():
        # Precyzyjne wykrywanie - tylko jeden poziom może być aktywny
        is_detected = False
        
        if "III" in detected_level and lvl == "Poziom III":
            is_detected = True
        elif "II" in detected_level and "III" not in detected_level and lvl == "Poziom II":
            is_detected = True  
        elif "I" in detected_level and "II" not in detected_level and "III" not in detected_level and lvl == "Poziom I":
            is_detected = True
            
        border_style = "border: 2px solid #4CAF50;" if is_detected else "border: 1px solid #ddd;"
        selected_indicator = "<strong>🎯 WYKRYTO</strong>" if is_detected else ""
        
        st.markdown(f"""
        <div style='padding: 15px; margin: 5px 0; border-radius: 10px; background-color: {info['bg']}; {border_style}'>
            {info['color']} <strong>{lvl}</strong> {selected_indicator}<br>
            <span style='color: #666;'>{info['desc']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Szczegółowe wyjaśnienie
    if 'explanation' in result:
        st.markdown("### 💡 Szczegółowa analiza")
        st.info(result['explanation'])
    
    # Wskaźniki w dwóch kolumnach
    col1, col2 = st.columns(2)
    
    with col1:
        # Wskaźniki kluczowe
        if 'key_indicators' in result:
            st.markdown("### 🔍 Kluczowe wskaźniki językowe")
            for indicator in result['key_indicators']:
                st.markdown(f"• {indicator}")
        
        # Wzorce językowe
        if 'language_patterns' in result:
            st.markdown("### 📝 Wzorce językowe")
            for pattern in result['language_patterns']:
                st.markdown(f"• {pattern}")
    
    with col2:
        # Ton emocjonalny
        if 'emotional_tone' in result:
            st.markdown("### 🎭 Ton emocjonalny")
            tone = result['emotional_tone']
            tone_colors = {
                'pozytywny': '🟢', 'neutralny': '🟡', 'negatywny': '🔴',
                'agresywny': '🔴', 'partnerski': '🟢'
            }
            color = tone_colors.get(tone.lower(), '⚪')
            st.markdown(f"{color} **{tone.title()}**")
        
        # Wpływ neurobiologiczny
        if 'neurobiological_impact' in result:
            st.markdown("### 🧠 Wpływ neurobiologiczny")
            st.warning(result['neurobiological_impact'])
    
    # Sugestie poprawy
    if 'improvement_suggestions' in result:
        st.markdown("### 🎯 Jak podnieść poziom komunikacji")
        for suggestion in result['improvement_suggestions']:
            st.markdown(f"• {suggestion}")
    
    # Alternatywne wersje w expanderach - pokazuj tylko wyższe poziomy
    if 'alternative_versions' in result:
        alt_versions = result['alternative_versions']
        detected_level = result.get('detected_level', '')
        
        # Logika: WAŻNE - sprawdzaj od najdłuższego do najkrótszego ciągu!
        if 'Poziom III' in detected_level:
            # Dla poziomu III: BRAK nagłówka, tylko gratulacje
            st.success("🎉 **Gratulacje!** To już najwyższy poziom C-IQ - Transformacyjny!")
            st.info("💡 **Twoja komunikacja wykorzystuje:**\n"
                   "• Język współtworzenia\n"
                   "• Pytania otwarte\n" 
                   "• Budowanie wspólnych celów\n"
                   "• Stymulację oksytocyny (zaufanie)")
                   
        elif 'Poziom II' in detected_level:
            # Dla poziomu II: pokaż nagłówek i alternatywę III
            st.markdown("### 🔄 Jak brzmiałoby na wyższym poziomie C-IQ")
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("🚀 Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
            else:
                st.info("🎉 To już wysoki poziom komunikacji! Poziom III to najwyższy dostępny poziom.")
                
        elif 'Poziom I' in detected_level:
            # Dla poziomu I: pokaż nagłówek i alternatywy II + III
            st.markdown("### 🔄 Jak brzmiałoby na wyższych poziomach C-IQ")
            
            if 'level_ii' in alt_versions and alt_versions['level_ii']:
                with st.expander("📈 Poziom II - Pozycyjny", expanded=False):
                    st.success(alt_versions['level_ii'])
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("🚀 Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
        else:
            # Fallback dla nieokreślonych poziomów - pokaż nagłówek
            st.markdown("### 🔄 Jak brzmiałoby na wyższych poziomach C-IQ")
            
            if 'level_ii' in alt_versions and alt_versions['level_ii']:
                with st.expander("📈 Poziom II - Pozycyjny", expanded=False):
                    st.success(alt_versions['level_ii'])
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("🚀 Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
    
    # Praktyczne wskazówki
    if 'practical_tips' in result:
        st.markdown("### 💡 Praktyczne wskazówki do zastosowania")
        for i, tip in enumerate(result['practical_tips'], 1):
            st.markdown(f"**{i}.** {tip}")

def show_ciq_examples():
    """Pokazuje przykłady różnych poziomów C-IQ"""
    st.markdown("#### 📚 Przykłady poziomów C-IQ w praktyce")
    
    examples = [
        {
            "scenario": "Informowanie o problemie w projekcie",
            "level_1": "Projekt się opóźnia. Deadline za tydzień. Pracujcie dłużej.",
            "level_2": "Uważam, że zespół nie wywiązuje się z zobowiązań. To wina słabego planowania z waszej strony.",
            "level_3": "Widzę, że projekt może się opóźnić. Jakie widzicie przyczyny tej sytuacji? Jak możemy razem znaleźć rozwiązanie?"
        },
        {
            "scenario": "Feedback dla pracownika",
            "level_1": "Twój raport ma błędy. Popraw i wyślij ponownie.",
            "level_2": "Nie zgadzam się z Twoim podejściem. Moja metoda jest lepsza, ponieważ...",
            "level_3": "Zauważyłem kilka obszarów w raporcie, które możemy razem ulepszyć. Co myślisz o tych aspektach?"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        st.markdown(f"### Przykład {i}: {example['scenario']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🔴 Poziom I - Transakcyjny**")
            st.text_area(
                "Poziom I",
                value=example['level_1'],
                height=100,
                key=f"example_{i}_1",
                label_visibility="collapsed"
            )
            
        with col2:
            st.markdown("**🟡 Poziom II - Pozycyjny**")
            st.text_area(
                "Poziom II",
                value=example['level_2'],
                height=100,
                key=f"example_{i}_2",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("**🟢 Poziom III - Transformacyjny**")
            st.text_area(
                "Poziom III",
                value=example['level_3'],
                height=100,
                key=f"example_{i}_3",
                label_visibility="collapsed"
            )

def show_email_templates():
    """Pokazuje szablony emaili na różnych poziomach C-IQ"""
    st.markdown("#### 📧 Szablony emaili biznesowych")
    st.info("🚧 Funkcja w przygotowaniu - biblioteka szablonów emaili na różnych poziomach C-IQ")

def show_emotion_detector():
    """Detektor Emocji w komunikacji"""
    st.markdown("## 😊 Detektor Emocji")
    st.markdown("Identyfikuj emocje w komunikacji i poznaj ich wpływ neurobiologiczny")
    
    st.info("🚧 **W przygotowaniu** - wkrótce będziesz mógł analizować emocje w tekstach i ich wpływ na kortyzol/oksytocynę")
    
    # Placeholder dla przyszłej funkcjonalności
    text_input = st.text_area(
        "Tekst do analizy emocji:",
        placeholder="Wklej tekst aby zanalizować obecne w nim emocje...",
        height=150,
        disabled=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔍 Planowane funkcje:**")
        st.markdown("• Identyfikacja emocji w tekście")
        st.markdown("• Analiza intensywności emocji") 
        st.markdown("• Wpływ na kortyzol/oksytocynę")
        st.markdown("• Sugestie regulacji emocji")
    
    with col2:
        st.markdown("**🎯 Rodzaje emocji do wykrywania:**")
        st.markdown("• Stres i napięcie")
        st.markdown("• Frustracja i złość")
        st.markdown("• Radość i entuzjazm") 
        st.markdown("• Lęk i niepewność")


def show_communication_analyzer():
    """Kompleksowy analizator komunikacji"""
    st.markdown("## 📝 Analizator Komunikacji")
    st.markdown("Kompleksowa wielowymiarowa analiza stylu komunikacyjnego")
    
    st.info("🚧 **W przygotowaniu** - zaawansowana analiza wszystkich aspektów komunikacji")
    
    # Placeholder dla różnych rodzajów analiz
    analysis_types = st.multiselect(
        "Wybierz rodzaje analiz:",
        [
            "🎯 Poziomy C-IQ",
            "😊 Analiza emocji", 
            "🧠 Wpływ neurobiologiczny",
            "🤝 Budowanie zaufania",
            "📊 Styl komunikacyjny",
            "🎭 Ton i postawa",
            "📈 Skuteczność przekazu"
        ],
        disabled=True
    )
    
    st.text_area(
        "Tekst do kompleksowej analizy:",
        placeholder="Wklej długszy tekst do szczegółowej analizy...",
        height=200,
        disabled=True
    )
    
    st.markdown("**📊 Przykładowy raport będzie zawierał:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🎯 Poziomy C-IQ**")
        st.markdown("• Dominujący poziom")
        st.markdown("• Rozkład procentowy")
        st.markdown("• Rekomendacje")
    
    with col2:
        st.markdown("**🧠 Neurobiologia**") 
        st.markdown("• Wpływ na kortyzol")
        st.markdown("• Stymulacja oksytocyny")
        st.markdown("• Bezpieczeństwo psychologiczne")
    
    with col3:
        st.markdown("**📈 Skuteczność**")
        st.markdown("• Clarność przekazu")
        st.markdown("• Potencjał zaufania")
        st.markdown("• Ryzyko konfliktu")

def show_simulators():
    """Symulatory komunikacyjne"""
    st.markdown("### 🎭 Symulatory Komunikacyjne")
    st.markdown("Interaktywne symulacje różnych scenariuszy komunikacyjnych")
    
    # Siatka symulatorów
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 20px; border: 2px solid #9C27B0; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #f3e5f5 0%, #ce93d8 100%);'>
            <h4>💼 Symulator Rozmów Biznesowych</h4>
            <p><strong>Ćwicz trudne rozmowy z AI partnerem</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>🎯 Różne scenariusze biznesowe</li>
                <li>🤖 AI odgrywa różne role</li>
                <li>📊 Ocena w czasie rzeczywistym</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("💼 Uruchom Symulator", key="business_simulator", width='stretch'):
            st.info("🚧 W przygotowaniu - interaktywne symulacje rozmów biznesowych")
    
    with col2:
        st.markdown("""
        <div style='padding: 20px; border: 2px solid #795548; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #efebe9 0%, #bcaaa4 100%);'>
            <h4>🤝 Trener Negocjacji</h4>
            <p><strong>Doskonał umiejętności negocjacyjne</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>⚖️ Scenariusze negocjacyjne</li>
                <li>🎯 Techniki C-IQ w negocjacjach</li>
                <li>📈 Analiza skuteczności</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("🤝 Uruchom Trenera", key="negotiation_trainer", width='stretch'):
            st.info("🚧 W przygotowaniu - trening umiejętności negocjacyjnych")

def show_analytics():
    """Analityki i tracking postępów"""
    st.markdown("### 📊 Analityki i Tracking")
    st.markdown("Zaawansowane analityki postępów w rozwoju umiejętności komunikacyjnych")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='padding: 15px; border: 1px solid #4CAF50; border-radius: 10px; background: #f8fff8;'>
            <h4>📈 Tracker Postępów</h4>
            <p>Monitoruj rozwój umiejętności C-IQ w czasie</p>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("📈 Zobacz Postępy", key="progress_tracker", width='stretch'):
            st.info("🚧 W przygotowaniu - szczegółowy tracking postępów w nauce")
    
    with col2:
        st.markdown("""
        <div style='padding: 15px; border: 1px solid #FF9800; border-radius: 10px; background: #fffbf0;'>
            <h4>🎯 Cele Rozwoju</h4>
            <p>Ustaw i śledź osobiste cele komunikacyjne</p>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("🎯 Ustaw Cele", key="development_goals", width='stretch'):
            st.info("🚧 W przygotowaniu - system celów rozwojowych")
    
    with col3:
        st.markdown("""
        <div style='padding: 15px; border: 1px solid #2196F3; border-radius: 10px; background: #f0f8ff;'>
            <h4>📋 Raport Umiejętności</h4>
            <p>Kompleksowy raport Twoich kompetencji</p>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("📋 Zobacz Raport", key="skills_report", width='stretch'):
            st.info("🚧 W przygotowaniu - szczegółowy raport umiejętności")

def show_ai_assistant():
    """AI Asystent personalny"""
    st.markdown("### 🤖 AI Asystent Personalny")
    st.markdown("Twój osobisty coach AI do rozwoju umiejętności komunikacyjnych")
    
    # Placeholder dla chatbota
    st.info("🚧 **W przygotowaniu** - inteligentny asystent AI dostępny 24/7")
    
    # Demo interfejsu chatbota
    st.markdown("#### 💬 Przykład rozmowy z AI Asystenem:")
    
    # Przykładowe wiadomości
    with st.chat_message("assistant"):
        st.markdown("Cześć! Jestem Twoim AI Asystenem do rozwoju komunikacji. W czym mogę Ci pomóc?")
    
    with st.chat_message("user"):
        st.markdown("Jak przygotować się do trudnej rozmowy z szefem?")
    
    with st.chat_message("assistant"):
        st.markdown("""
        Świetne pytanie! Oto moja strategia oparta na C-IQ:
        
        **🎯 Przygotowanie:**
        1. Zidentyfikuj cel rozmowy (co chcesz osiągnąć)
        2. Przygotuj pytania otwarte zamiast oskarżeń
        3. Zastanów się nad wspólnymi celami
        
        **💭 Podczas rozmowy:**
        - Zacznij od poziomu III: "Chciałbym porozmawiać o..."
        - Unikaj języka "ty" na rzecz "my", "nas"
        - Zadawaj pytania: "Jak widzisz tę sytuację?"
        
        Chcesz przećwiczyć konkretny scenariusz?
        """)
    
    # Wyłączony input
    chat_input = st.chat_input("Napisz wiadomość do AI Asystenta...", disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔮 Planowane funkcje:**")
        st.markdown("• Rozmowy w czasie rzeczywistym")
        st.markdown("• Personalizowane porady")
        st.markdown("• Analiza postępów")
        st.markdown("• Przypomnienia o ćwiczeniach")
    
    with col2:
        st.markdown("**🎯 Obszary wsparcia:**")
        st.markdown("• Przygotowanie do trudnych rozmów")
        st.markdown("• Analiza komunikacji")
        st.markdown("• Strategie C-IQ")
        st.markdown("• Budowanie pewności siebie")

if __name__ == "__main__":
    show_tools_page()