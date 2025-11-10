"""
Business Conversation Simulator v2.0
Interaktywny symulator rozmów biznesowych z:
- Wyborem poziomu trudności
- AI-generowanym kontekstem
- Możliwością poprawiania odpowiedzi
"""

import streamlit as st
from typing import Dict, Optional, List
import json
import re

# ===============================================
# SCENARIUSZE ROZMÓW - BAZOWE SZABLONY
# ===============================================

SCENARIOS = {
    "salary_raise": {
        "name": "💰 Rozmowa o podwyżkę",
        "description": "Prosisz szefa o podwyżkę",
        "ai_role": "Szef",
        "user_role": "Pracownik",
        "initiator": "user",
        "category": "wynagrodzenia",
        "optimal_ciq": {
            "opening": [2, 3],  # Pozycyjny (argumenty) lub Transformacyjny (wizja rozwoju)
            "middle": [3],  # Transformacyjny (budowanie wartości)
            "crisis": [1, 2],  # Transakcyjny (konkretne liczby) lub Pozycyjny (uzasadnienie)
            "closing": [3]  # Transformacyjny (długoterminowa współpraca)
        },
        "context_notes": "C-IQ I akceptowalny przy przedstawianiu konkretnych oczekiwań finansowych. C-IQ II dobry przy argumentacji osiągnięciami. C-IQ III optymalny przy budowaniu wizji wspólnego rozwoju."
    },
    "difficult_feedback": {
        "name": "📢 Trudny feedback",
        "description": "Przekazujesz trudny feedback pracownikowi",
        "ai_role": "Pracownik",
        "user_role": "Menedżer",
        "initiator": "user",
        "category": "zarządzanie",
        "optimal_ciq": {
            "opening": [2, 3],  # Pozycyjny (jasne standardy) lub Transformacyjny (rozwój)
            "middle": [3],  # Transformacyjny (wsparcie i rozwój)
            "crisis": [2],  # Pozycyjny (jasne granice)
            "closing": [3]  # Transformacyjny (plan rozwoju)
        },
        "context_notes": "C-IQ II optymalny przy określaniu granic i standardów. C-IQ III najlepszy przy budowaniu planu naprawczego i wspieraniu rozwoju."
    },
    "team_conflict": {
        "name": "⚡ Konflikt w zespole",
        "description": "Rozwiązujesz konflikt między członkami zespołu",
        "ai_role": "Członek zespołu",
        "user_role": "Mediator",
        "initiator": "user",
        "category": "konflikty",
        "optimal_ciq": {
            "opening": [2, 3],  # Pozycyjny (zasady) lub Transformacyjny (mediacja)
            "middle": [3],  # Transformacyjny (zrozumienie perspektyw)
            "crisis": [2],  # Pozycyjny (przywrócenie porządku)
            "closing": [3]  # Transformacyjny (budowanie wspólnej wizji)
        },
        "context_notes": "C-IQ II skuteczny przy ustalaniu zasad dyskusji. C-IQ III kluczowy przy budowaniu porozumienia i wspólnych rozwiązań."
    },
    "delegation": {
        "name": "📋 Delegowanie zadania",
        "description": "Delegujesz zadanie przeciążonemu pracownikowi",
        "ai_role": "Pracownik",
        "user_role": "Menedżer",
        "initiator": "user",
        "category": "zarządzanie",
        "optimal_ciq": {
            "opening": [1, 2],  # Transakcyjny (pilne) lub Pozycyjny (wyjaśnienie)
            "middle": [3],  # Transformacyjny (zrozumienie sytuacji)
            "crisis": [1],  # Transakcyjny (szybka decyzja)
            "closing": [3]  # Transformacyjny (wsparcie)
        },
        "context_notes": "C-IQ I optymalny w sytuacjach pilnych - jasne, szybkie komunikaty. C-IQ II dobry przy wyjaśnianiu priorytetów. C-IQ III najlepszy przy wspólnym szukaniu rozwiązań."
    },
    "motivation": {
        "name": "🔥 Motywowanie pracownika",
        "description": "Motywujesz zdemotywowanego pracownika",
        "ai_role": "Pracownik",
        "user_role": "Menedżer",
        "initiator": "user",
        "category": "motywacja",
        "optimal_ciq": {
            "opening": [3],  # Transformacyjny (empatia)
            "middle": [3],  # Transformacyjny (zrozumienie przyczyn)
            "crisis": [2],  # Pozycyjny (przypomnienie celów)
            "closing": [3]  # Transformacyjny (plan działania)
        },
        "context_notes": "C-IQ III dominuje - motywacja wymaga głębokiego zrozumienia i budowania zaangażowania. C-IQ II pomocny przy przypominaniu o celach i standardach."
    },
    "change_resistance": {
        "name": "🔄 Opór wobec zmian",
        "description": "Przekonujesz zespół do zmian organizacyjnych",
        "ai_role": "Członek zespołu",
        "user_role": "Lider zmiany",
        "initiator": "user",
        "category": "zmiany",
        "optimal_ciq": {
            "opening": [2, 3],  # Pozycyjny (powody zmian) lub Transformacyjny (wizja)
            "middle": [3],  # Transformacyjny (adresowanie obaw)
            "crisis": [2],  # Pozycyjny (konieczność zmian)
            "closing": [3]  # Transformacyjny (wspólna realizacja)
        },
        "context_notes": "C-IQ II skuteczny przy wyjaśnianiu biznesowej konieczności zmian. C-IQ III kluczowy przy budowaniu zaangażowania i współtworzeniu rozwiązań."
    },
    "difficult_client": {
        "name": "😤 Trudny klient",
        "description": "Uspokajasz niezadowolonego klienta",
        "ai_role": "Klient",
        "user_role": "Account Manager",
        "initiator": "ai",
        "category": "klienci",
        "optimal_ciq": {
            "opening": [1],  # Transakcyjny (natychmiastowa reakcja)
            "middle": [2, 3],  # Pozycyjny (procedury) lub Transformacyjny (odbudowa relacji)
            "crisis": [1],  # Transakcyjny (szybkie działanie)
            "closing": [3]  # Transformacyjny (długoterminowa relacja)
        },
        "context_notes": "C-IQ I optymalny na starcie - klient potrzebuje szybkiej, konkretnej reakcji. C-IQ II dobry przy wyjaśnianiu procedur. C-IQ III najlepszy przy odbudowie zaufania."
    },
    "negotiation": {
        "name": "💼 Negocjacje",
        "description": "Negocjujesz warunki współpracy",
        "ai_role": "Partner biznesowy",
        "user_role": "Negocjator",
        "initiator": "user",
        "category": "negocjacje",
        "optimal_ciq": {
            "opening": [2, 3],  # Pozycyjny (pozycja) lub Transformacyjny (partnerstwo)
            "middle": [2, 3],  # Mix - zależnie od stylu negocjacji
            "crisis": [2],  # Pozycyjny (stanowczość)
            "closing": [3]  # Transformacyjny (win-win)
        },
        "context_notes": "C-IQ I akceptowalny przy wymianie konkretów. C-IQ II skuteczny przy obronie swojej pozycji. C-IQ III optymalny przy budowaniu partnerstwa win-win."
    }
}

DIFFICULTY_LEVELS = {
    "easy": {
        "name": "🟢 Łatwy",
        "description": "Rozmówca jest otwarty na dialog, łagodny, chętny do współpracy",
        "ai_behavior": "Bądź bardzo otwarty, przyjaźnie nastawiony, łatwo przychodzi Ci kompromis i zrozumienie"
    },
    "medium": {
        "name": "🟡 Średni",
        "description": "Rozmówca jest sceptyczny, ale możliwy do przekonania",
        "ai_behavior": "Bądź umiarkowanie sceptyczny, wymagaj dobrej argumentacji, ale bądź otwarty na dobrze przedstawione argumenty"
    },
    "hard": {
        "name": "🔴 Trudny",
        "description": "Rozmówca jest defensywny, niechętny, wymaga najwyższych umiejętności",
        "ai_behavior": "Bądź bardzo defensywny, wymagający, sceptyczny. Tylko najwyższy poziom C-IQ (Transformacyjny) i perfekcyjna argumentacja mogą Cię przekonać"
    }
}

# ===============================================
# INICJALIZACJA SESSION STATE
# ===============================================

def init_simulator_state():
    """Inicjalizuje stan symulatora"""
    if 'sim_scenario' not in st.session_state:
        st.session_state.sim_scenario = None
    if 'sim_difficulty' not in st.session_state:
        st.session_state.sim_difficulty = None
    if 'sim_context' not in st.session_state:
        st.session_state.sim_context = None
    if 'sim_ai_persona' not in st.session_state:
        st.session_state.sim_ai_persona = None
    if 'sim_messages' not in st.session_state:
        st.session_state.sim_messages = []
    if 'sim_started' not in st.session_state:
        st.session_state.sim_started = False
    if 'sim_context_generated' not in st.session_state:
        st.session_state.sim_context_generated = False
    if 'sim_turn_count' not in st.session_state:
        st.session_state.sim_turn_count = 0
    if 'sim_max_turns' not in st.session_state:
        st.session_state.sim_max_turns = 10
    if 'sim_completed' not in st.session_state:
        st.session_state.sim_completed = False
    if 'sim_awaiting_user_response' not in st.session_state:
        st.session_state.sim_awaiting_user_response = False
    if 'sim_current_user_message' not in st.session_state:
        st.session_state.sim_current_user_message = None

def reset_simulator():
    """Resetuje symulator"""
    st.session_state.sim_scenario = None
    st.session_state.sim_difficulty = None
    st.session_state.sim_context = None
    st.session_state.sim_ai_persona = None
    st.session_state.sim_messages = []
    st.session_state.sim_started = False
    st.session_state.sim_context_generated = False
    st.session_state.sim_turn_count = 0
    st.session_state.sim_completed = False
    st.session_state.sim_awaiting_user_response = False
    st.session_state.sim_current_user_message = None

# ===============================================
# GENEROWANIE KONTEKSTU PRZEZ AI
# ===============================================

def generate_scenario_context(scenario_id: str, difficulty: str) -> Dict:
    """Generuje szczegółowy kontekst scenariusza używając AI"""
    try:
        from utils.ai_exercises import AIExerciseEvaluator
        evaluator = AIExerciseEvaluator()
        
        scenario = SCENARIOS[scenario_id]
        diff_settings = DIFFICULTY_LEVELS[difficulty]
        
        prompt = f"""Jesteś ekspertem w tworzeniu realistycznych scenariuszy rozmów biznesowych do treningów C-IQ.

SCENARIUSZ: {scenario['name']} - {scenario['description']}
POZIOM TRUDNOŚCI: {diff_settings['name']} - {diff_settings['description']}

ROLE:
- Użytkownik gra: {scenario['user_role']}
- AI gra: {scenario['ai_role']}

Wygeneruj szczegółowy, realistyczny kontekst tej sytuacji. Uwzględnij:

1. **KONTEKST DLA UŻYTKOWNIKA** (2-3 zdania):
   - Konkretna sytuacja z nazwami, liczbami, faktami
   - Dlaczego ta rozmowa jest teraz?
   - Co użytkownik chce osiągnąć?

2. **PERSONA AI** (2-3 zdania):
   - Kim dokładnie jest rozmówca? (imię, stanowisko, charakterystyka)
   - Jakie ma obawy/frustracje w tej sytuacji?
   - Jak powinien reagować na różne poziomy C-IQ zgodnie z poziomem trudności

3. **POCZĄTKOWA SYTUACJA** (1 zdanie):
   - Jak rozpoczyna się rozmowa?
   - Kto zaczyna i w jakich okolicznościach?

Odpowiedz TYLKO w formacie JSON (bez ```json):
{{
    "user_context": "Szczegółowy kontekst dla użytkownika...",
    "ai_persona": "Szczegółowa persona AI rozmówcy...",
    "situation_start": "Jak rozpoczyna się rozmowa...",
    "ai_name": "Imię AI rozmówcy",
    "key_challenge": "Główne wyzwanie w tej rozmowie"
}}"""

        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                content = response.text.strip()
                
                # Usuń markdown
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                elif content.startswith("```"):
                    content = content.replace("```", "").strip()
                
                # Wydobądź JSON
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
    
    except Exception as e:
        st.warning(f"⚠️ Nie udało się wygenerować kontekstu AI: {str(e)}")
    
    # Fallback - prosty kontekst
    scenario = SCENARIOS.get(scenario_id, {})
    diff_settings = DIFFICULTY_LEVELS.get(difficulty, DIFFICULTY_LEVELS['medium'])
    
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return {
        "user_context": f"Jesteś {scenario.get('user_role', 'uczestnik')} w sytuacji: {scenario.get('description', 'rozmowa biznesowa')}",
        "ai_persona": f"Rozmówca to {scenario.get('ai_role', 'rozmówca')} z poziomem trudności {diff_settings['name']}",
        "situation_start": "Rozmowa rozpoczyna się teraz",
        "ai_name": "Rozmówca",
        "key_challenge": f"Przekonanie {scenario.get('ai_role', 'rozmówcy')} do współpracy",
        "date": current_date
    }

# ===============================================
# ANALIZA C-IQ
# ===============================================

def analyze_message_ciq(message: str, scenario: Dict, context: Dict, turn_number: int = 1) -> Dict:
    """Analizuje poziom C-IQ wypowiedzi z uwzględnieniem kontekstowej adekwatności"""
    try:
        from utils.ai_exercises import AIExerciseEvaluator
        evaluator = AIExerciseEvaluator()
        
        # Określ fazę rozmowy
        if turn_number <= 2:
            phase = "opening"
        elif turn_number >= 8:
            phase = "closing"
        else:
            phase = "middle"
        
        optimal_levels = scenario.get('optimal_ciq', {}).get(phase, [3])
        context_notes = scenario.get('context_notes', '')
        
        prompt = f"""Jesteś ekspertem w Conversational Intelligence. Oceń wypowiedź w kontekście rozmowy biznesowej.

KONTEKST: {context['user_context']}
ROLA UŻYTKOWNIKA: {scenario['user_role']}
WYZWANIE: {context['key_challenge']}
FAZA ROZMOWY: {phase} (runda {turn_number}/10)

WAŻNE - KONTEKSTOWA ADEKWATNOŚĆ C-IQ:
{context_notes}

Optymalne poziomy C-IQ w tej fazie: {', '.join(['I (Transakcyjny)' if x==1 else 'II (Pozycyjny)' if x==2 else 'III (Transformacyjny)' for x in optimal_levels])}

WYPOWIEDŹ: "{message}"

Oceń poziom C-IQ (1-3):
- I (Transakcyjny): rozkazy, "ty musisz", konkretne działania, szybka reakcja
- II (Pozycyjny): argumenty, "ja vs ty", obrona pozycji, wyjaśnienia
- III (Transformacyjny): "my", empatia, pytania otwarte, współtworzenie

KLUCZOWE: Oceń czy użyty poziom był ADEKWATNY do sytuacji i fazy rozmowy.
Czasem C-IQ I lub II to OPTYMALNA decyzja (np. pilna sprawa, ustalanie granic, konkretne liczby).

Odpowiedź JSON (bez ```json):
{{
    "level": "Transakcyjny/Pozycyjny/Transformacyjny",
    "level_number": 1/2/3,
    "score": 1-10,
    "reasoning": "Dlaczego ten poziom? (2-3 zdania)",
    "tip": "Konkretna wskazówka jak ulepszyć (1 zdanie)",
    "contextual_fit": "optimal/good/suboptimal",
    "contextual_comment": "Dlaczego ten poziom był/nie był adekwatny w tym kontekście? (1-2 zdania)"
}}"""

        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                elif content.startswith("```"):
                    content = content.replace("```", "").strip()
                
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    
                    level_num = result.get("level_number", 2)
                    contextual_fit = result.get("contextual_fit", "good")
                    
                    # Określ kolor bazując na kontekstowej adekwatności
                    if contextual_fit == "optimal":
                        if level_num == 3:
                            color = "green"  # 🟢 Transformacyjny optymalny
                        else:
                            color = "blue"   # 🔵 Transakcyjny/Pozycyjny optymalny w kontekście!
                    elif contextual_fit == "good":
                        color = "orange"  # 🟡 Akceptowalny
                    else:
                        color = "red"  # 🔴 Nieadekwatny do sytuacji
                    
                    result["color"] = color
                    result["optimal_levels"] = optimal_levels
                    result["phase"] = phase
                    return result
    
    except Exception as e:
        st.warning(f"⚠️ Błąd analizy C-IQ: {str(e)}")
    
    # Fallback
    return {
        "level": "Pozycyjny",
        "level_number": 2,
        "score": 5,
        "reasoning": "Standardowa odpowiedź biznesowa",
        "tip": "Spróbuj użyć pytań otwartych i języka 'my razem'",
        "color": "orange",
        "contextual_fit": "good",
        "contextual_comment": "Poziom akceptowalny w tej sytuacji",
        "optimal_levels": [3],
        "phase": "middle"
    }

# ===============================================
# GENEROWANIE ODPOWIEDZI AI
# ===============================================

def generate_ai_response(scenario: Dict, context: Dict, difficulty: str, messages: List[Dict], user_ciq_level: str) -> str:
    """Generuje odpowiedź AI rozmówcy"""
    try:
        from utils.ai_exercises import AIExerciseEvaluator
        evaluator = AIExerciseEvaluator()
        
        recent_messages = messages[-6:] if len(messages) > 6 else messages
        conversation_history = "\n".join([
            f"{'AI (' + context.get('ai_name', scenario['ai_role']) + ')' if m['role'] == 'ai' else 'Użytkownik'}: {m['content']}"
            for m in recent_messages
        ])
        
        diff_behavior = DIFFICULTY_LEVELS[difficulty]['ai_behavior']
        
        prompt = f"""Jesteś ekspertem w symulacji realistycznych rozmów biznesowych.

TWOJA ROLA: {scenario['ai_role']} (imię: {context.get('ai_name', 'Rozmówca')})
TWOJA PERSONA: {context['ai_persona']}
POZIOM TRUDNOŚCI: {DIFFICULTY_LEVELS[difficulty]['name']}
JAK MASZ SIĘ ZACHOWYWAĆ: {diff_behavior}

KONTEKST SYTUACJI: {context['user_context']}
GŁÓWNE WYZWANIE: {context['key_challenge']}

HISTORIA ROZMOWY:
{conversation_history}

POZIOM C-IQ UŻYTKOWNIKA W OSTATNIEJ WYPOWIEDZI: {user_ciq_level}

ZASADY ODPOWIEDZI:
1. Reaguj na poziom C-IQ użytkownika:
   - Transformacyjny → bądź bardziej otwarty, obniż defensywność
   - Pozycyjny → bądź umiarkowanie defensywny
   - Transakcyjny → bądź bardzo defensywny, zamknięty

2. Zachowaj poziom trudności ({DIFFICULTY_LEVELS[difficulty]['name']}):
   {diff_behavior}

3. Odpowiedz naturalnie, 2-4 zdania, jako {context.get('ai_name', scenario['ai_role'])}
4. NIE dodawaj meta-komentarzy

Odpowiedź:"""

        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
    
    except Exception as e:
        st.warning(f"⚠️ Błąd generowania odpowiedzi: {str(e)}")
    
    # Fallback
    if user_ciq_level == "Transformacyjny":
        return f"Dziękuję za zrozumienie. Faktycznie, to jest dobry punkt. Jak możemy to wspólnie rozwiązać?"
    elif user_ciq_level == "Pozycyjny":
        return f"Rozumiem Twój punkt widzenia, ale widzę to nieco inaczej. Może porozmawiajmy dalej?"
    else:
        return f"Okej, rozumiem. Co jeszcze?"

def generate_initial_ai_message(scenario: Dict, context: Dict) -> str:
    """Generuje początkową wiadomość AI"""
    try:
        from utils.ai_exercises import AIExerciseEvaluator
        evaluator = AIExerciseEvaluator()
        
        prompt = f"""ROLA: {scenario['ai_role']} ({context.get('ai_name')})
PERSONA: {context['ai_persona']}
SYTUACJA: {context['situation_start']}

Rozpocznij rozmowę jako {context.get('ai_name')}. 2-3 zdania, naturalnie, wyraź problem/frustrację zgodnie z kontekstem.

Odpowiedź:"""

        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
    
    except Exception:
        pass
    
    return f"Dzień dobry. Musimy porozmawiać o ważnej sprawie."

# ===============================================
# GŁÓWNY INTERFEJS
# ===============================================

def show_business_simulator():
    """Główny interfejs symulatora v2.0"""
    init_simulator_state()
    
    st.markdown("### 💼 Symulator Rozmów Biznesowych")
    st.markdown("Interaktywne symulacje z AI-generowanym kontekstem i możliwością poprawiania odpowiedzi")
    st.markdown("---")
    
    # ===== KROK 1: WYBÓR SCENARIUSZA I TRUDNOŚCI =====
    if not st.session_state.sim_context_generated:
        st.markdown("#### 🎯 Krok 1: Wybierz scenariusz i poziom trudności")
        
        # Wybór scenariusza
        scenario_options = {s['name']: sid for sid, s in SCENARIOS.items()}
        selected_name = st.selectbox(
            "📋 Scenariusz:",
            options=list(scenario_options.keys()),
            key="sim_scenario_select"
        )
        selected_id = scenario_options[selected_name]
        scenario = SCENARIOS[selected_id]
        
        st.info(f"**{scenario['description']}**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"👤 **Ty:** {scenario['user_role']}")
        with col2:
            st.markdown(f"🤖 **AI:** {scenario['ai_role']}")
        
        st.markdown("---")
        
        # Wybór poziomu trudności
        st.markdown("**⚙️ Poziom trudności:**")
        
        diff_cols = st.columns(3)
        
        for idx, (diff_id, diff_info) in enumerate(DIFFICULTY_LEVELS.items()):
            with diff_cols[idx]:
                if st.button(
                    diff_info['name'],
                    help=diff_info['description'],
                    use_container_width=True,
                    type="primary" if idx == 1 else "secondary"
                ):
                    st.session_state.sim_difficulty = diff_id
                    st.rerun()
        
        # Wyświetl wybrany poziom
        if st.session_state.sim_difficulty:
            selected_diff = DIFFICULTY_LEVELS[st.session_state.sim_difficulty]
            st.success(f"✅ Wybrany poziom: **{selected_diff['name']}**")
            st.caption(selected_diff['description'])
            
            st.markdown("---")
            st.markdown("#### 🎬 Krok 2: Wygeneruj szczegółowy kontekst")
            
            if st.button("🤖 Generuj kontekst scenariusza przez AI", type="primary", use_container_width=True):
                with st.spinner("🔄 AI tworzy realistyczny kontekst sytuacji..."):
                    context = generate_scenario_context(selected_id, st.session_state.sim_difficulty)
                    
                    st.session_state.sim_scenario = selected_id
                    st.session_state.sim_context = context
                    st.session_state.sim_context_generated = True
                    st.rerun()
        
        return
    
    # ===== KROK 3: POKAŻ WYGENEROWANY KONTEKST =====
    if not st.session_state.sim_started:
        scenario = SCENARIOS[st.session_state.sim_scenario]
        context = st.session_state.sim_context
        diff = DIFFICULTY_LEVELS[st.session_state.sim_difficulty]
        
        st.success(f"✅ Kontekst wygenerowany!")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"#### {scenario['name']}")
        with col2:
            st.metric("Poziom", diff['name'])
        
        st.markdown("---")
        
        # Wyświetl szczegóły
        st.markdown("**📋 Twój kontekst:**")
        st.info(context['user_context'])
        
        st.markdown(f"**🤖 Rozmówca: {context.get('ai_name', scenario['ai_role'])}**")
        with st.expander("🎭 Persona rozmówcy", expanded=False):
            st.markdown(context['ai_persona'])
        
        st.markdown(f"**🎬 Początek rozmowy:**")
        st.caption(context['situation_start'])
        
        st.markdown(f"**🎯 Główne wyzwanie:**")
        st.warning(context['key_challenge'])
        
        st.markdown("---")
        
        # Przyciski
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Rozpocznij symulację", type="primary", use_container_width=True):
                st.session_state.sim_started = True
                st.session_state.sim_messages = []
                st.session_state.sim_awaiting_user_response = True  # Zawsze czekamy na użytkownika
                
                # Jeśli AI rozpoczyna - dodaj pierwszą wiadomość
                if scenario['initiator'] == 'ai':
                    initial_msg = generate_initial_ai_message(scenario, context)
                    st.session_state.sim_messages.append({
                        'role': 'ai',
                        'content': initial_msg
                    })
                
                # XP za start
                try:
                    from data.users import award_xp_for_activity
                    award_xp_for_activity(
                        st.session_state.username,
                        'tool_used',
                        1,
                        {'tool_name': 'Business Simulator v2', 'scenario': st.session_state.sim_scenario}
                    )
                except:
                    pass
                
                st.rerun()
        
        with col2:
            if st.button("🔄 Wygeneruj inny kontekst", use_container_width=True):
                st.session_state.sim_context_generated = False
                st.session_state.sim_context = None
                st.rerun()
        
        return
    
    # ===== AKTYWNA SYMULACJA =====
    scenario = SCENARIOS[st.session_state.sim_scenario]
    context = st.session_state.sim_context
    diff = DIFFICULTY_LEVELS[st.session_state.sim_difficulty]
    
    # Sprawdź czy zakończono
    if st.session_state.sim_completed:
        show_summary(scenario, context, diff)
        return
    
    # Nagłówek
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"#### {scenario['name']}")
        st.caption(f"Rozmówca: {context.get('ai_name', scenario['ai_role'])}")
    with col2:
        st.metric("Poziom", diff['name'])
    with col3:
        turns = st.session_state.sim_turn_count
        max_turns = st.session_state.sim_max_turns
        st.metric("Runda", f"{turns}/{max_turns}")
    
    # Przycisk zakończ
    if st.button("🏁 Zakończ rozmowę", help="Zakończ i zobacz podsumowanie"):
        st.session_state.sim_completed = True
        st.rerun()
    
    st.markdown("---")
    
    # Panel kontekstu - zawsze widoczny
    st.markdown("### 📋 Kontekst sytuacji")
    
    col_ctx1, col_ctx2 = st.columns([1, 1])
    
    with col_ctx1:
        st.markdown("**📝 Twój kontekst:**")
        st.info(context['user_context'])
        
        st.markdown(f"**🎯 Główne wyzwanie:**")
        st.warning(context['key_challenge'])
    
    with col_ctx2:
        st.markdown(f"**🤖 Rozmówca: {context.get('ai_name', scenario['ai_role'])}**")
        st.info(context['ai_persona'])
        
        st.markdown(f"**🎬 Początek rozmowy:**")
        st.caption(context['situation_start'])
    
    st.markdown("---")
    
    # Historia rozmowy
    user_message_count = 0  # Licznik wiadomości użytkownika
    
    for idx, msg in enumerate(st.session_state.sim_messages):
        if msg['role'] == 'ai':
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg['content'])
        else:
            user_message_count += 1
            remaining = st.session_state.sim_max_turns - user_message_count + 1
            
            with st.chat_message("user", avatar="👤"):
                # Nagłówek z numerem rundy
                st.caption(f"💬 Runda {user_message_count}/{st.session_state.sim_max_turns} (pozostało: {remaining})")
                st.markdown(msg['content'])
                
                # Analiza C-IQ
                if 'ciq_analysis' in msg:
                    analysis = msg['ciq_analysis']
                    color = analysis.get('color', 'blue')
                    contextual_fit = analysis.get('contextual_fit', 'good')
                    contextual_comment = analysis.get('contextual_comment', '')
                    
                    # Buduj feedback z uwzględnieniem kontekstowej adekwatności
                    feedback_text = f"""**📊 C-IQ: {analysis['level']}** (ocena: {analysis['score']}/10)

{analysis['reasoning']}"""
                    
                    # Dodaj komentarz o kontekstowej adekwatności dla C-IQ I i II gdy są optymalne
                    if contextual_fit == "optimal" and analysis.get('level_number', 3) in [1, 2]:
                        feedback_text += f"\n\n✨ **Świetny wybór!** {contextual_comment}"
                    elif contextual_comment:
                        feedback_text += f"\n\n� {contextual_comment}"
                    
                    feedback_text += f"\n\n�💡 **Wskazówka:** {analysis['tip']}"
                    
                    if color == 'green':
                        st.success(feedback_text)
                    elif color == 'blue':
                        st.info(feedback_text)  # Niebieskie tło dla optymalnego C-IQ I/II
                    elif color == 'orange':
                        st.warning(feedback_text)
                    else:
                        st.error(feedback_text)
                    
                    # Przyciski POWTÓRZ / DALEJ / ZAKOŃCZ (tylko dla ostatniej wiadomości użytkownika)
                    if idx == len(st.session_state.sim_messages) - 1 and not st.session_state.sim_awaiting_user_response:
                        # Wyśrodkuj przyciski używając pustych kolumn po bokach
                        col_space1, col_btn1, col_btn2, col_btn3, col_space2 = st.columns([1, 2, 2, 2, 1])
                        
                        with col_btn1:
                            if st.button("🔄 Powtórz", key=f"retry_{idx}", use_container_width=True, help="Usuń swoją odpowiedź i spróbuj ponownie"):
                                # Usuń ostatnią wiadomość użytkownika
                                st.session_state.sim_messages.pop()
                                # Ustaw flagę aby pokazać pole czatu
                                st.session_state.sim_awaiting_user_response = True
                                st.rerun()
                        
                        with col_btn2:
                            if st.button("✅ Dalej", key=f"continue_{idx}", type="primary", use_container_width=True, help="Kontynuuj rozmowę"):
                                # Generuj odpowiedź AI
                                with st.spinner(f"💭 {context.get('ai_name')} myśli..."):
                                    user_ciq = analysis.get('level', 'nieznany')
                                    ai_response = generate_ai_response(
                                        scenario, 
                                        context, 
                                        st.session_state.sim_difficulty,
                                        st.session_state.sim_messages,
                                        user_ciq
                                    )
                                    
                                    st.session_state.sim_messages.append({
                                        'role': 'ai',
                                        'content': ai_response
                                    })
                                    
                                    st.session_state.sim_turn_count += 1
                                    st.session_state.sim_awaiting_user_response = True
                                    st.rerun()
                        
                        with col_btn3:
                            if st.button("🏁 Zakończ", key=f"finish_{idx}", use_container_width=True, help="Zakończ rozmowę i zobacz podsumowanie"):
                                st.session_state.sim_completed = True
                                st.rerun()
    
    # Input użytkownika - pokazuj tylko gdy czekamy na odpowiedź
    if st.session_state.sim_turn_count < st.session_state.sim_max_turns:
        if st.session_state.sim_awaiting_user_response:
            user_input = st.chat_input("Twoja odpowiedź...")
            
            if user_input and user_input.strip():
                # Dodaj wiadomość użytkownika
                st.session_state.sim_messages.append({
                    'role': 'user',
                    'content': user_input
                })
                
                # Analizuj C-IQ z numerem rundy
                with st.spinner("🔍 Analizuję poziom C-IQ..."):
                    turn_number = st.session_state.sim_turn_count
                    ciq_analysis = analyze_message_ciq(user_input, scenario, context, turn_number)
                    st.session_state.sim_messages[-1]['ciq_analysis'] = ciq_analysis
                
                st.session_state.sim_awaiting_user_response = False
                st.rerun()
    else:
        st.info("🏁 Osiągnąłeś maksymalną liczbę rund. Kliknij 'Zakończ rozmowę' aby zobaczyć podsumowanie.")

# ===============================================
# PODSUMOWANIE
# ===============================================

def generate_ai_feedback(scenario: Dict, context: Dict, diff: Dict, messages: List[Dict]) -> Dict:
    """Generuje szczegółowy feedback AI na podstawie całej rozmowy z uwzględnieniem kontekstowej adekwatności C-IQ"""
    try:
        from utils.ai_exercises import AIExerciseEvaluator
        evaluator = AIExerciseEvaluator()
        
        # Przygotuj transkrypcję
        conversation = []
        for msg in messages:
            role_name = context.get('ai_name', scenario['ai_role']) if msg['role'] == 'ai' else scenario['user_role']
            conversation.append(f"{role_name}: {msg['content']}")
        
        transcript = "\n\n".join(conversation)
        
        # Zbierz analizy C-IQ z informacją o kontekstowej adekwatności
        user_messages = [m for m in messages if m['role'] == 'user']
        ciq_summary = []
        contextual_wins = []  # Przypadki gdy C-IQ I/II był optymalny
        
        for idx, msg in enumerate(user_messages, 1):
            if 'ciq_analysis' in msg:
                analysis = msg['ciq_analysis']
                level = analysis.get('level', 'Nieznany')
                level_num = analysis.get('level_number', 0)
                contextual_fit = analysis.get('contextual_fit', 'good')
                
                ciq_summary.append(f"- Runda {idx}: {level} (adekwatność: {contextual_fit})")
                
                # Zaznacz optymalne użycie C-IQ I/II
                if contextual_fit == "optimal" and level_num in [1, 2]:
                    contextual_wins.append(f"Runda {idx}: {analysis.get('contextual_comment', '')}")
        
        ciq_text = "\n".join(ciq_summary) if ciq_summary else "Brak analizy"
        contextual_wins_text = "\n".join(contextual_wins) if contextual_wins else "Brak"
        
        prompt = f"""Jesteś ekspertem w Conversational Intelligence i coachingu komunikacji biznesowej.

Przeanalizuj poniższą symulowaną rozmowę biznesową i przygotuj konstruktywny feedback.

WAŻNE - KONTEKSTOWA ADEKWATNOŚĆ C-IQ:
{scenario.get('context_notes', 'Poziom transformacyjny jest zazwyczaj optymalny, ale nie zawsze.')}

Pamiętaj: C-IQ I (Transakcyjny) i II (Pozycyjny) mogą być OPTYMALNYM wyborem w określonych sytuacjach!
- C-IQ I: pilne sprawy, konkretne działania, szybka reakcja
- C-IQ II: ustalanie granic, obrona standardów, jasna argumentacja
- C-IQ III: budowanie relacji, rozwój, współtworzenie

KONTEKST:
- Scenariusz: {scenario['name']}
- Rola użytkownika: {scenario['user_role']}
- Rozmówca: {context.get('ai_name', scenario['ai_role'])}
- Poziom trudności: {diff['name']}
- Wyzwanie: {context['key_challenge']}

TRANSKRYPCJA ROZMOWY:
{transcript}

POZIOMY C-IQ UŻYTKOWNIKA:
{ciq_text}

PRZYPADKI OPTYMALNEGO UŻYCIA C-IQ I/II (do pochwały!):
{contextual_wins_text}

Przygotuj feedback w formacie JSON (bez ```json):
{{
    "strengths": [
        "Mocna strona 1 (konkretny przykład z rozmowy - doceniaj także dobre użycie C-IQ I/II!)",
        "Mocna strona 2 (konkretny przykład z rozmowy)",
        "Mocna strona 3 (konkretny przykład z rozmowy)"
    ],
    "areas_to_improve": [
        "Obszar do rozwoju 1 (co dokładnie poprawić - ale NIE krytykuj C-IQ I/II jeśli był adekwatny!)",
        "Obszar do rozwoju 2 (co dokładnie poprawić)",
        "Obszar do rozwoju 3 (co dokładnie poprawić)"
    ],
    "key_tip": "Jedna najważniejsza wskazówka do zastosowania w następnej rozmowie (1-2 zdania)",
    "overall_rating": 1-10,
    "summary": "Krótkie podsumowanie rozmowy (2-3 zdania)"
}}"""

        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                content = response.text.strip()
                
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                elif content.startswith("```"):
                    content = content.replace("```", "").strip()
                
                import json
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
    
    except Exception as e:
        st.warning(f"⚠️ Nie udało się wygenerować feedback AI: {str(e)}")
    
    # Fallback
    return {
        "strengths": [
            "Ukończyłeś symulację rozmowy",
            "Ćwiczyłeś umiejętności komunikacyjne",
            "Próbowałeś różnych podejść"
        ],
        "areas_to_improve": [
            "Spróbuj używać więcej pytań otwartych",
            "Stosuj język 'my' zamiast 'ty'",
            "Praktykuj empatyczne słuchanie"
        ],
        "key_tip": "W następnej rozmowie zacznij od pytania otwartego, aby lepiej zrozumieć perspektywę rozmówcy.",
        "overall_rating": 6,
        "summary": "Dobra próba komunikacji. Z kolejnymi ćwiczeniami będziesz coraz lepszy!"
    }

def generate_transcript(scenario: Dict, context: Dict, messages: List[Dict]) -> str:
    """Generuje transkrypcję rozmowy w formacie tekstowym"""
    lines = []
    lines.append("=" * 60)
    lines.append("TRANSKRYPCJA ROZMOWY - SYMULATOR BIZNESOWY")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Scenariusz: {scenario['name']}")
    lines.append(f"Twoja rola: {scenario['user_role']}")
    lines.append(f"Rozmówca: {context.get('ai_name', scenario['ai_role'])}")
    lines.append(f"Data: {context.get('date', 'N/A')}")
    lines.append("")
    lines.append("=" * 60)
    lines.append("")
    
    for idx, msg in enumerate(messages, 1):
        if msg['role'] == 'ai':
            role_name = context.get('ai_name', scenario['ai_role'])
            lines.append(f"[{role_name}]:")
        else:
            role_name = scenario['user_role']
            lines.append(f"[{role_name}]:")
            
        lines.append(msg['content'])
        
        # Dodaj szczegółową analizę C-IQ dla wiadomości użytkownika
        if msg['role'] == 'user' and 'ciq_analysis' in msg:
            analysis = msg['ciq_analysis']
            level = analysis.get('level', 'N/A')
            score = analysis.get('score', 0)
            contextual_fit = analysis.get('contextual_fit', 'unknown')
            
            # Symbol adekwatności
            fit_symbol = "✅" if contextual_fit == "optimal" else "👍" if contextual_fit == "good" else "⚠️"
            fit_text = {
                "optimal": "OPTYMALNY",
                "good": "Dobry",
                "suboptimal": "Do poprawy"
            }.get(contextual_fit, "N/A")
            
            lines.append(f"  → C-IQ: {level} ({score}/10) | Adekwatność: {fit_symbol} {fit_text}")
            
            # Dodaj komentarz kontekstowy jeśli istnieje
            if 'contextual_comment' in analysis and analysis['contextual_comment']:
                lines.append(f"  💡 {analysis['contextual_comment']}")
        
        lines.append("")
    
    lines.append("=" * 60)
    lines.append("KONIEC TRANSKRYPCJI")
    lines.append("=" * 60)
    
    return "\n".join(lines)

def show_summary(scenario: Dict, context: Dict, diff: Dict):
    """Wyświetla podsumowanie symulacji"""
    st.success("✅ Rozmowa zakończona!")
    st.markdown("### 📊 Podsumowanie")
    
    total_turns = st.session_state.sim_turn_count
    
    # Podstawowe statystyki
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("💬 Liczba rund", total_turns)
        st.metric("⚙️ Poziom trudności", diff['name'])
    with col_stat2:
        st.metric("📝 Scenariusz", scenario['name'])
        st.metric("🤖 Rozmówca", context.get('ai_name', scenario['ai_role']))
    
    st.markdown("---")
    
    # Analiza poziomów C-IQ z kontekstową adekwatnością
    user_messages = [m for m in st.session_state.sim_messages if m['role'] == 'user']
    if user_messages:
        ciq_levels = [m.get('ciq_analysis', {}).get('level', 'Nieznany') for m in user_messages if 'ciq_analysis' in m]
        
        if ciq_levels:
            from collections import Counter
            level_counts = Counter(ciq_levels)
            
            # Policz kontekstową adekwatność
            optimal_count = sum(1 for m in user_messages if m.get('ciq_analysis', {}).get('contextual_fit') == 'optimal')
            good_count = sum(1 for m in user_messages if m.get('ciq_analysis', {}).get('contextual_fit') == 'good')
            suboptimal_count = sum(1 for m in user_messages if m.get('ciq_analysis', {}).get('contextual_fit') == 'suboptimal')
            
            # Policz optymalne użycie C-IQ I/II
            optimal_low_ciq = sum(1 for m in user_messages 
                                 if m.get('ciq_analysis', {}).get('contextual_fit') == 'optimal' 
                                 and m.get('ciq_analysis', {}).get('level_number', 3) in [1, 2])
            
            st.markdown("#### 📊 Twoje poziomy C-IQ:")
            
            col_ciq1, col_ciq2, col_ciq3 = st.columns(3)
            
            transformacyjny = level_counts.get("Transformacyjny", 0)
            pozycyjny = level_counts.get("Pozycyjny", 0)
            transakcyjny = level_counts.get("Transakcyjny", 0)
            total = len(ciq_levels)
            
            with col_ciq1:
                st.metric(
                    "🟢 Transformacyjny",
                    f"{transformacyjny} ({(transformacyjny/total*100):.0f}%)",
                    delta="Doskonały poziom" if transformacyjny > pozycyjny + transakcyjny else None
                )
            
            with col_ciq2:
                st.metric(
                    "🟡 Pozycyjny",
                    f"{pozycyjny} ({(pozycyjny/total*100):.0f}%)",
                    delta=None
                )
            
            with col_ciq3:
                st.metric(
                    "� Transakcyjny",
                    f"{transakcyjny} ({(transakcyjny/total*100):.0f}%)",
                    delta=None
                )
            
            # Pokaż adekwatność kontekstową
            st.markdown("#### 🎯 Adekwatność do kontekstu:")
            
            col_fit1, col_fit2, col_fit3 = st.columns(3)
            
            with col_fit1:
                st.metric(
                    "✅ Optymalne",
                    f"{optimal_count} ({(optimal_count/total*100):.0f}%)",
                    delta="Świetnie!" if optimal_count > total/2 else None
                )
            
            with col_fit2:
                st.metric(
                    "👍 Dobre",
                    f"{good_count} ({(good_count/total*100):.0f}%)",
                    delta=None
                )
            
            with col_fit3:
                st.metric(
                    "⚠️ Do poprawy",
                    f"{suboptimal_count} ({(suboptimal_count/total*100):.0f}%)",
                    delta="Uwaga!" if suboptimal_count > 0 else None,
                    delta_color="inverse"
                )
            
            # Pochwała za elastyczność sytuacyjną
            if optimal_low_ciq > 0:
                st.info(f"""🔵 **Świetna elastyczność sytuacyjna!** 
                
Użyłeś C-IQ I (Transakcyjny) lub II (Pozycyjny) w sposób optymalny {optimal_low_ciq} {'raz' if optimal_low_ciq == 1 else 'razy'}. 
To pokazuje, że rozumiesz kiedy niższe poziomy C-IQ są właściwym wyborem!""")
            
            # Ogólna ocena
            dominant = level_counts.most_common(1)[0][0]
            adaptability_score = (optimal_count / total * 100) if total > 0 else 0
            
            if adaptability_score >= 70:
                st.success(f"🎉 **Wysoka adaptacyjność ({adaptability_score:.0f}%)** - Doskonale dopasujesz poziom C-IQ do kontekstu!")
            elif adaptability_score >= 50:
                st.info(f"💡 **Dobra adaptacyjność ({adaptability_score:.0f}%)** - Dobrze dopasujesz C-IQ, ale jest przestrzeń na rozwój.")
            else:
                st.warning(f"⚠️ **Adaptacyjność do rozwinięcia ({adaptability_score:.0f}%)** - Zwracaj większą uwagę na kontekst sytuacyjny.")
    
    st.markdown("---")
    
    # Generuj feedback AI
    with st.spinner("🤖 AI przygotowuje szczegółowy feedback..."):
        feedback = generate_ai_feedback(scenario, context, diff, st.session_state.sim_messages)
    
    # Wyświetl feedback AI
    st.markdown("### 🎯 Szczegółowy feedback")
    
    # Ogólna ocena
    rating = feedback.get('overall_rating', 5)
    st.markdown(f"**Ogólna ocena:** {'⭐' * rating} ({rating}/10)")
    
    if 'summary' in feedback:
        st.info(feedback['summary'])
    
    col_feed1, col_feed2 = st.columns(2)
    
    with col_feed1:
        st.markdown("#### 💪 Mocne strony:")
        for strength in feedback.get('strengths', []):
            st.success(f"✅ {strength}")
    
    with col_feed2:
        st.markdown("#### 📈 Obszary do rozwoju:")
        for area in feedback.get('areas_to_improve', []):
            st.warning(f"🔸 {area}")
    
    # Kluczowa wskazówka
    if 'key_tip' in feedback:
        st.markdown("### 💡 Kluczowa wskazówka na przyszłość:")
        st.success(f"**{feedback['key_tip']}**")
    
    st.markdown("---")
    
    # Transkrypcja
    st.markdown("### 📄 Transkrypcja rozmowy")
    
    transcript_text = generate_transcript(scenario, context, st.session_state.sim_messages)
    
    with st.expander("📜 Zobacz pełną transkrypcję", expanded=False):
        st.text(transcript_text)
    
    # Przycisk pobierania
    import datetime
    filename = f"transkrypcja_{scenario.get('name', 'rozmowa').replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    st.download_button(
        label="📥 Pobierz transkrypcję (TXT)",
        data=transcript_text,
        file_name=filename,
        mime="text/plain",
        use_container_width=True
    )
    
    st.markdown("---")
    try:
        from data.users import award_xp_for_activity
        award_xp_for_activity(
            st.session_state.username,
            'ai_exercise',
            15,
            {
                'exercise_name': 'Business Simulator v2',
                'scenario': st.session_state.sim_scenario,
                'difficulty': st.session_state.sim_difficulty,
                'turns': total_turns
            }
        )
        st.success("🎉 **+15 XP** za ukończenie!")
    except:
        pass
    
    # Przyciski
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Nowa symulacja", type="primary", use_container_width=True):
            reset_simulator()
            st.rerun()
    with col2:
        if st.button("❌ Zamknij", use_container_width=True):
            reset_simulator()
            if 'active_simulator' in st.session_state:
                st.session_state.active_simulator = None
            st.rerun()

