"""
Business Conversation Simulator
Interaktywny symulator rozmów biznesowych z analizą C-IQ w czasie rzeczywistym
"""

import streamlit as st
from typing import Dict, Optional, List
import json
import re

# ===============================================
# SCENARIUSZE ROZMÓW - SZABLON
# ===============================================

SCENARIOS = {
    "salary_raise": {
        "name": "💰 Rozmowa o podwyżkę",
        "description": "Prosisz szefa o podwyżkę",
        "ai_role": "Szef",
        "user_role": "Pracownik",
        "initiator": "user",
    },
    "difficult_feedback": {
        "name": "📢 Feedback dla pracownika",
        "description": "Musisz przekazać trudny feedback pracownikowi",
        "ai_role": "Pracownik",
        "user_role": "Menedżer",
        "initiator": "user",
    },
    "team_conflict": {
        "name": "⚡ Rozwiązanie konfliktu",
        "description": "Dwóch członków zespołu ma konflikt",
        "ai_role": "Członek zespołu",
        "user_role": "Mediator",
        "initiator": "user",
    },
    "delegation": {
        "name": "📋 Delegowanie zadania",
        "description": "Delegujesz ważne zadanie pracownikowi",
        "ai_role": "Pracownik",
        "user_role": "Menedżer",
        "initiator": "user",
    },
    "motivation": {
        "name": "🔥 Motywowanie zdemotywowanego",
        "description": "Pracownik stracił motywację i rozważa zmianę pracy. Musisz go zmotywować.",
        "ai_persona": "Jesteś Pawłem, zdemotywowanym Senior Developerem (5 lat w firmie), który czuje się wypalony i niedoceniany. Praca przestała Cię inspirować - rutynowe zadania, brak rozwoju, ostatni projekt zakończył się porażką. Dostałeś ofertę z konkurencji (+40% wypłaty). Jesteś otwarty na rozmowę, ale potrzebujesz szczerości, zrozumienia i konkretnych zmian, nie pustych obietnic.",
        "ai_role": "Pracownik",
        "user_role": "Menedżer",
        "initiator": "user",
        "context": "Jesteś menedżerem. Paweł to Twój najlepszy specjalista, ale od 3 miesięcy widzisz spadek zaangażowania - przychodzi o 10, wychodzi o 16, minimalna komunikacja. HR wspomniało że dostał ofertę z konkurencji. Nie możesz stracić takiego eksperta."
    },
    "change_resistance": {
        "name": "🔄 Opór wobec zmian",
        "description": "Przekonujesz zespół do dużej zmiany organizacyjnej, na którą są opory.",
        "ai_persona": "Jesteś Piotrem, sceptycznym Senior Developerem (8 lat w firmie), który obawia się zmian. Widziałeś jak 2 lata temu wprowadzono nowy system który okazał się porażką i wszyscy stracili 6 miesięcy. Teraz znowu firma chce 'rewolucji' - nowy CRM, nowe procesy. Jesteś ostrożny, defensywny i potrzebujesz przekonujących argumentów oraz poczucia bezpieczeństwa.",
        "ai_role": "Członek zespołu",
        "user_role": "Lider zmiany",
        "initiator": "user",
        "context": "Jesteś liderem projektu zmiany. Firma wprowadza nowy system CRM który zastąpi stary Excel i 5 różnych narzędzi. To będzie 6 miesięcy migracji. Zespół pamięta poprzednią porażkę i jest sceptyczny. Piotr jako senior dev ma duży wpływ na innych - jeśli on się nie przekona, cały zespół będzie przeciw."
    },
    "difficult_client": {
        "name": "😤 Rozmowa z trudnym klientem",
        "description": "Klient jest niezadowolony z realizacji projektu i grozi rezygnacją.",
        "ai_persona": "Jesteś Janem Kowalskim, CEO firmy TechCorp (kontrakt 500k PLN/rok), sfrustrowanym klientem który czuje że jego projekt jest zaniedbywany. Projekt się opóźnia o 2 miesiące, ostatni release miał krytyczne błędy, a komunikacja kuleje - nikt nie odpowiada na emaile. Jesteś niezadowolony, oschły i poważnie rozważasz zmianę dostawcy. Możesz być wymagający, ale jeśli zobaczysz autentyczną chęć rozwiązania problemu i konkretny plan działania, stajesz się bardziej otwarty.",
        "ai_role": "Klient",
        "user_role": "Account Manager",
        "initiator": "ai",  # Klient dzwoni zdenerwowany
        "context": "Jesteś Account Managerem. Klient TechCorp (największy kontrakt - 500k/rok) jest niezadowolony. Projekt opóźnia się bo zespół dev ma problemy z integracją, a Ty zapomniałeś wysłać 2 weekly reporty. Klient właśnie do Ciebie dzwoni - jest wściekły i wspomina o rozwiązaniu umowy."
    },
    "negotiation": {
        "name": "💼 Negocjacje warunków",
        "description": "Negocjujesz warunki współpracy z wymagającym partnerem biznesowym.",
        "ai_persona": "Jesteś Anną Nowak, CEO firmy konsultingowej Premium Consulting (50 pracowników, 10 lat na rynku), twardym negocjatorem który zna swoją wartość. Twoja stawka to 250 PLN/h, nie zejdziesz poniżej 220 PLN/h. Chcesz przedpłaty 50%, płatności w 14 dni i pełnej kontroli nad metodologią. Masz 3 inne oferty czekające. Nie boisz się odejść, jeśli oferta nie jest satysfakcjonująca. Szanujesz profesjonalizm i konkretne argumenty biznesowe, ale nie akceptujesz presji ani manipulacji.",
        "ai_role": "Partner biznesowy",
        "user_role": "Negocjator",
        "initiator": "user",
        "context": "Jesteś negocjatorem ze startupu (budżet ograniczony). Potrzebujesz konsultingu Premium Consulting do projektu transformacji (3 miesiące, ~200h). Twój budżet to max 180 PLN/h, płatność po 30 dniach. Premium Consulting ma świetną reputację ale jest drogi. Musisz wynegocjować dobre warunki ale nie stracić tej firmy."
    }
}

# ===============================================
# INICJALIZACJA SESSION STATE
# ===============================================

def init_simulator_state():
    """Inicjalizuje stan symulatora w session state"""
    if 'sim_scenario' not in st.session_state:
        st.session_state.sim_scenario = None
    if 'sim_messages' not in st.session_state:
        st.session_state.sim_messages = []
    if 'sim_started' not in st.session_state:
        st.session_state.sim_started = False
    if 'sim_turn_count' not in st.session_state:
        st.session_state.sim_turn_count = 0
    if 'sim_max_turns' not in st.session_state:
        st.session_state.sim_max_turns = 10
    if 'sim_completed' not in st.session_state:
        st.session_state.sim_completed = False
    if 'sim_errors' not in st.session_state:
        st.session_state.sim_errors = []

def reset_simulator():
    """Resetuje symulator do stanu początkowego"""
    st.session_state.sim_scenario = None
    st.session_state.sim_messages = []
    st.session_state.sim_started = False
    st.session_state.sim_turn_count = 0
    st.session_state.sim_completed = False

# ===============================================
# FUNKCJE AI - ANALIZA C-IQ
# ===============================================

def analyze_message_ciq(message: str, scenario: Dict) -> Dict:
    """Analizuje poziom C-IQ wypowiedzi używając AI"""
    try:
        # Import AI evaluatora
        from utils.ai_exercises import AIExerciseEvaluator
        evaluator = AIExerciseEvaluator()
        
        prompt = f"""Jesteś ekspertem w Conversational Intelligence. Oceń następującą wypowiedź w kontekście rozmowy biznesowej.

KONTEKST ROZMOWY: {scenario['description']}
ROLA UŻYTKOWNIKA: {scenario['user_role']}
ROLA ROZMÓWCY: {scenario['ai_role']}

WYPOWIEDŹ DO OCENY: "{message}"

Oceń poziom C-IQ według skali 1-3:
- Poziom I (Transakcyjny): Wymiana informacji, rozkazy, brak dialogu, język "ty musisz"
- Poziom II (Pozycyjny): Obrona swojej pozycji, argumentowanie, walka o rację, "ja vs ty"
- Poziom III (Transformacyjny): Współtworzenie, empatia, pytania otwarte, język "my", zrozumienie

Odpowiedz TYLKO w formacie JSON (bez ```json):
{{
    "level": "Transakcyjny" lub "Pozycyjny" lub "Transformacyjny",
    "score": 1-10,
    "reasoning": "Krótkie wyjaśnienie dlaczego ten poziom (1-2 zdania)",
    "tip": "Konkretna wskazówka jak podnieść poziom (1 zdanie)",
    "is_appropriate": true lub false
}}"""

        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                content = response.text.strip()
                # Usuń markdown formatowanie jeśli jest
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                elif content.startswith("```"):
                    content = content.replace("```", "").strip()
                
                # Znajdź JSON
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    
                    # Określ kolor dla UI
                    level = result.get("level", "Pozycyjny")
                    is_appropriate = result.get("is_appropriate", False)
                    
                    if level == "Transformacyjny":
                        color = "green"
                    elif is_appropriate:
                        color = "blue"
                    else:
                        color = "red" if level == "Transakcyjny" else "orange"
                    
                    result["color"] = color
                    return result
    except Exception as e:
        # Zapisz błąd do session state aby przetrwał reload
        if 'sim_errors' not in st.session_state:
            st.session_state.sim_errors = []
        error_msg = f"⚠️ AI C-IQ Analysis Error: {type(e).__name__}: {str(e)}"
        st.session_state.sim_errors.append(error_msg)
        st.warning(error_msg)
    
    # Fallback - prosta heurystyka
    return analyze_message_ciq_fallback(message)

def analyze_message_ciq_fallback(message: str) -> Dict:
    """Prosta heurystyczna analiza C-IQ gdy AI nie działa"""
    message_lower = message.lower()
    
    # Słowa kluczowe dla poziomu III
    level_3_keywords = [
        'razem', 'wspólnie', 'jak możemy', 'zrozumiem', 'pomóż mi zrozumieć',
        'jakie masz', 'co myślisz', 'współpraca', 'nasz cel', 'nasza',
        'słucham', 'doceniam', 'cenię', 'co dla ciebie', 'twoja perspektywa'
    ]
    
    # Słowa kluczowe dla poziomu I
    level_1_keywords = [
        'musisz', 'powinieneś', 'zrób', 'wymaga', 'oczekuję',
        'nie możesz', 'zakazuję', 'natychmiast', 'rozkaz'
    ]
    
    # Pytania otwarte (poziom III)
    open_questions = ['jak', 'dlaczego', 'co', 'w jaki sposób', 'jakie']
    
    level_3_count = sum(1 for word in level_3_keywords if word in message_lower)
    level_1_count = sum(1 for word in level_1_keywords if word in message_lower)
    open_q_count = sum(1 for word in open_questions if word in message_lower and '?' in message)
    
    # Określ poziom
    if level_3_count >= 2 or open_q_count >= 1:
        return {
            "level": "Transformacyjny",
            "score": 8,
            "reasoning": "Używasz języka współpracy i pytań otwartych",
            "tip": "Kontynuuj takie podejście - buduje zaufanie",
            "color": "green",
            "is_appropriate": True
        }
    elif level_1_count >= 2:
        return {
            "level": "Transakcyjny",
            "score": 3,
            "reasoning": "Używasz języka dyrektywnego i rozkazów",
            "tip": "Spróbuj zadać pytanie otwarte zamiast dawać polecenie",
            "color": "red",
            "is_appropriate": False
        }
    else:
        return {
            "level": "Pozycyjny",
            "score": 5,
            "reasoning": "Prezentujesz swoją pozycję",
            "tip": "Użyj języka 'my' zamiast 'ty' i zadaj pytanie otwarte",
            "color": "orange",
            "is_appropriate": False
        }

# ===============================================
# FUNKCJE AI - GENEROWANIE ODPOWIEDZI
# ===============================================

def generate_ai_response(scenario: Dict, messages: List[Dict], user_message: str) -> str:
    """Generuje odpowiedź AI w roli rozmówcy"""
    # Wykryj poziom C-IQ ostatniej wypowiedzi użytkownika (przed blokiem try)
    last_user_ciq = "nieznany"
    if messages and messages[-1]['role'] == 'user' and 'ciq_analysis' in messages[-1]:
        last_user_ciq = messages[-1]['ciq_analysis'].get('level', 'nieznany')
    
    try:
        from utils.ai_exercises import AIExerciseEvaluator
        evaluator = AIExerciseEvaluator()
        
        # Ostatnie 3 wymiany dla kontekstu
        recent_messages = messages[-6:] if len(messages) > 6 else messages
        conversation_history = "\n".join([
            f"{'AI (' + scenario['ai_role'] + ')' if m['role'] == 'ai' else 'Użytkownik (' + scenario['user_role'] + ')'}: {m['content']}"
            for m in recent_messages
        ])
        
        # Pobierz kontekst sytuacji (jeśli istnieje)
        context = scenario.get('context', scenario.get('description', 'Brak kontekstu'))
        
        prompt = f"""Jesteś ekspertem w symulacji realistycznych rozmów biznesowych.

TWOJA ROLA: {scenario['ai_role']}
ROLA UŻYTKOWNIKA: {scenario['user_role']}

PERSONA (jak masz się zachowywać):
{scenario.get('ai_persona', 'Zachowuj się naturalnie i profesjonalnie.')}

KONTEKST SYTUACJI:
{context}

HISTORIA ROZMOWY:
{conversation_history}

OSTATNIA WYPOWIEDŹ UŻYTKOWNIKA: "{user_message}"
POZIOM C-IQ UŻYTKOWNIKA: {last_user_ciq}

WAŻNE ZASADY ODPOWIEDZI:
1. Reaguj na poziom C-IQ użytkownika:
   - Jeśli Transformacyjny (empatia, pytania otwarte, "my") → bądź bardziej otwarty, współpracuj, obniż defensywność
   - Jeśli Pozycyjny (argumenty, "ja vs ty") → bądź umiarkowanie defensywny, ale nie zamykaj się całkowicie
   - Jeśli Transakcyjny (rozkazy, "ty musisz") → bądź bardzo defensywny, oschły, niechętny

2. Zachowuj realizm - nie przesadzaj z emocjami ani agresją
3. Odpowiedz TYLKO jako {scenario['ai_role']}, naturalnie, 2-4 zdania
4. NIE pisz "(jako {scenario['ai_role']})" ani innych meta-komentarzy
5. Pamiętaj o kontekście sytuacji i swojej personie

Odpowiedz TYLKO tekstem wypowiedzi, bez dodatkowych oznaczeń:"""

        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
    except Exception as e:
        # Zapisz błąd do session state
        if 'sim_errors' not in st.session_state:
            st.session_state.sim_errors = []
        error_msg = f"⚠️ AI Response Error: {type(e).__name__}: {str(e)}"
        st.session_state.sim_errors.append(error_msg)
        st.warning(error_msg)
    
    # Fallback
    return generate_ai_response_fallback(scenario, last_user_ciq)

def generate_ai_response_fallback(scenario: Dict, user_ciq_level: str) -> str:
    """Prosta odpowiedź AI gdy API nie działa"""
    if user_ciq_level == "Transformacyjny":
        responses = [
            f"Naprawdę doceniam Twoje podejście. Jako {scenario['ai_role']}, widzę że chcesz znaleźć dobre rozwiązanie. Jak możemy to wspólnie przemyśleć?",
            f"Dziękuję za zrozumienie. Faktycznie, to jest skomplikowana sytuacja. Może razem znajdziemy wyjście?",
            f"Cieszę się, że możemy porozmawiać w taki sposób. Co proponujesz, żebyśmy zrobili dalej?"
        ]
    elif user_ciq_level == "Pozycyjny":
        responses = [
            f"Hmm, rozumiem Twój punkt widzenia, ale widzę to trochę inaczej. Może porozmawiajmy o szczegółach?",
            f"Okej, słucham co masz do powiedzenia. Ale mam też swoje zastrzeżenia.",
            f"To ciekawa perspektywa. Chociaż muszę powiedzieć, że ja widzę to nieco inaczej."
        ]
    else:  # Transakcyjny
        responses = [
            f"No dobrze, rozumiem. A co jeszcze chciałeś powiedzieć?",
            f"Jasne. I co dalej?",
            f"Okej, przyjąłem do wiadomości. Co jeszcze?"
        ]
    
    import random
    return random.choice(responses)

def generate_initial_ai_message(scenario: Dict) -> str:
    """Generuje początkową wiadomość AI gdy AI rozpoczyna rozmowę"""
    try:
        from utils.ai_exercises import AIExerciseEvaluator
        evaluator = AIExerciseEvaluator()
        
        prompt = f"""Jesteś ekspertem w symulacji rozmów biznesowych.

TWOJA ROLA: {scenario['ai_role']}
PERSONA: {scenario['ai_persona']}
KONTEKST: {scenario['context']}

Rozpocznij rozmowę jako {scenario['ai_role']}. Pamiętaj:
- To TY dzwonisz/przychodzisz do użytkownika (on jest {scenario['user_role']})
- Wyraź problem/frustrację zgodnie z kontekstem
- 2-3 zdania, naturalnie, realistycznie
- Nie bądź nadmiernie agresywny, ale pokaż emocje
- NIE pisz "(jako {scenario['ai_role']})" - po prostu zagraj rolę

Odpowiedz TYLKO tekstem wypowiedzi:"""

        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
    except Exception as e:
        # Zapisz błąd do session state
        if 'sim_errors' not in st.session_state:
            st.session_state.sim_errors = []
        error_msg = f"⚠️ AI Initial Message Error: {type(e).__name__}: {str(e)}"
        st.session_state.sim_errors.append(error_msg)
        st.warning(error_msg)
    
    # Fallback
    if scenario['ai_role'] == "Klient":
        return "Dzień dobry. Muszę z Tobą pilnie porozmawiać o naszym projekcie. Jestem bardzo niezadowolony z tego jak to wszystko wygląda. Projekt się opóźnia, a ja nie dostaję żadnych informacji!"
    else:
        return f"Cześć. Musimy porozmawiać. Jest coś, co mnie naprawdę frustruje w tej sytuacji."

# ===============================================
# GŁÓWNA FUNKCJA SYMULATORA
# ===============================================

def show_business_simulator():
    """Główny interfejs symulatora rozmów biznesowych"""
    init_simulator_state()
    
    st.markdown("### 💼 Symulator Rozmów Biznesowych")
    st.markdown("Interaktywne symulacje trudnych rozmów biznesowych z analizą C-IQ w czasie rzeczywistym")
    
    st.markdown("---")
    
    # ===== EKRAN WYBORU SCENARIUSZA =====
    if not st.session_state.sim_started:
        st.markdown("### 🎯 Wybierz scenariusz rozmowy:")
        
        # Przygotuj listę scenariuszy
        scenario_options = {s['name']: sid for sid, s in SCENARIOS.items()}
        
        selected_name = st.selectbox(
            "Scenariusz:",
            options=list(scenario_options.keys()),
            key="sim_scenario_select"
        )
        
        # Pobierz wybrany scenariusz
        selected_id = scenario_options[selected_name]
        scenario = SCENARIOS[selected_id]
        
        # Pokaż szczegóły
        st.markdown("---")
        st.markdown(f"#### {scenario['name']}")
        st.info(f"📋 **Scenariusz:** {scenario['description']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**👤 Ty:** {scenario['user_role']}")
        with col2:
            st.markdown(f"**🤖 AI:** {scenario['ai_role']}")
        
        # Kontekst (jeśli istnieje)
        if 'context' in scenario:
            with st.expander("📄 Szczegółowy kontekst sytuacji", expanded=False):
                st.markdown(scenario['context'])
        
        # Przycisk start
        st.markdown("")
        if st.button("▶️ Rozpocznij symulację", type="primary", use_container_width=True):
            st.session_state.sim_scenario = selected_id
            st.session_state.sim_started = True
            st.session_state.sim_messages = []
            st.session_state.sim_turn_count = 0
            st.session_state.sim_completed = False
            
            # Jeśli AI rozpoczyna, wygeneruj pierwszą wiadomość
            if scenario['initiator'] == 'ai':
                initial_msg = generate_initial_ai_message(scenario)
                st.session_state.sim_messages.append({
                    'role': 'ai',
                    'content': initial_msg
                })
            
            # Award XP za uruchomienie
            try:
                from data.users import award_xp_for_activity
                award_xp_for_activity(
                    st.session_state.username,
                    'tool_used',
                    1,
                    {
                        'tool_name': 'Business Conversation Simulator',
                        'scenario': selected_id,
                        'scenario_name': scenario['name']
                    }
                )
            except Exception:
                pass
            
            st.rerun()
        
        # Legenda poziomów C-IQ
        st.markdown("---")
        st.markdown("#### 📚 Poziomy Conversational Intelligence:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **🔴 Poziom I - Transakcyjny**
            
            - Wymiana informacji
            - Rozkazy, polecenia
            - "Ty mówisz - ja słucham"
            - Brak prawdziwego dialogu
            
            *Przykład:* "Musisz mi dać podwyżkę o 20%"
            """)
        
        with col2:
            st.markdown("""
            **🟡 Poziom II - Pozycyjny**
            
            - Obrona swojej pozycji
            - Argumentowanie, przekonywanie
            - Walka o rację: "ja vs ty"
            
            *Przykład:* "Zasługuję na więcej, bo inni zarabiają więcej"
            """)
        
        with col3:
            st.markdown("""
            **🟢 Poziom III - Transformacyjny**
            
            - Współtworzenie rozwiązań
            - Empatia i zrozumienie
            - Pytania otwarte
            - Język "my razem"
            
            *Przykład:* "Jak możemy wspólnie znaleźć rozwiązanie?"
            """)
        
        return
    
    # ===== AKTYWNA SYMULACJA =====
    scenario_id = st.session_state.sim_scenario
    scenario = SCENARIOS.get(scenario_id)
    
    if not scenario:
        st.error("❌ Błąd: Nieznany scenariusz")
        if st.button("🔄 Restart"):
            reset_simulator()
            st.rerun()
        return
    
    # Sprawdź czy zakończono
    if st.session_state.sim_completed:
        st.success("✅ Rozmowa zakończona!")
        st.markdown("### 📊 Podsumowanie")
        
        # Podstawowe statystyki
        total_turns = st.session_state.sim_turn_count
        st.info(f"""
        **Statystyki rozmowy:**
        - 💬 Liczba wymian: {total_turns}
        - 📝 Scenariusz: {scenario['name']}
        - 🎭 Twoja rola: {scenario['user_role']}
        - 🤖 Rola AI: {scenario['ai_role']}
        """)
        
        # Analiza poziomów C-IQ
        user_messages = [m for m in st.session_state.sim_messages if m['role'] == 'user']
        if user_messages:
            ciq_levels = [m.get('ciq_analysis', {}).get('level', 'Nieznany') for m in user_messages if 'ciq_analysis' in m]
            
            if ciq_levels:
                from collections import Counter
                level_counts = Counter(ciq_levels)
                
                st.markdown("#### 📊 Twoje poziomy C-IQ w rozmowie:")
                for level, count in level_counts.most_common():
                    percentage = (count / len(ciq_levels)) * 100
                    emoji = "🟢" if level == "Transformacyjny" else "🟡" if level == "Pozycyjny" else "🔴"
                    st.markdown(f"{emoji} **{level}:** {count} wypowiedzi ({percentage:.0f}%)")
                
                # Dominujący poziom
                dominant = level_counts.most_common(1)[0][0]
                st.markdown(f"\n**Dominujący poziom:** {dominant}")
                
                if dominant == "Transformacyjny":
                    st.success("🎉 Świetna robota! Używałeś głównie poziomu Transformacyjnego - to buduje najlepsze relacje!")
                elif dominant == "Pozycyjny":
                    st.info("💡 Często używałeś poziomu Pozycyjnego. Spróbuj więcej pytań otwartych i języka 'my' w następnej rozmowie!")
                else:
                    st.warning("⚠️ Dominował poziom Transakcyjny. W następnej rozmowie spróbuj zadawać pytania otwarte zamiast dawać polecenia.")
        
        # Award XP za ukończenie
        try:
            from data.users import award_xp_for_activity
            award_xp_for_activity(
                st.session_state.username,
                'ai_exercise',
                15,
                {
                    'exercise_name': 'Business Conversation Simulator',
                    'scenario': scenario_id,
                    'scenario_name': scenario['name'],
                    'turns': total_turns,
                    'completed': True
                }
            )
            st.success("🎉 **+15 XP** za ukończenie symulacji!")
        except Exception:
            pass
        
        # Przyciski
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Spróbuj innego scenariusza", type="primary", use_container_width=True):
                reset_simulator()
                st.rerun()
        with col2:
            if st.button("❌ Zamknij", use_container_width=True):
                reset_simulator()
                # Jeśli jest active_simulator w session_state, wyczyść
                if 'active_simulator' in st.session_state:
                    st.session_state.active_simulator = None
                st.rerun()
        
        return
    
    # Nagłówek z licznikiem
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"#### {scenario['name']}")
        st.caption(f"👤 Ty: **{scenario['user_role']}** | 🤖 AI: **{scenario['ai_role']}**")
    with col2:
        turns = st.session_state.sim_turn_count
        max_turns = st.session_state.sim_max_turns
        progress = turns / max_turns if max_turns > 0 else 0
        
        if progress < 0.6:
            color_emoji = "🟢"
        elif progress < 0.8:
            color_emoji = "🟡"
        else:
            color_emoji = "🔴"
        
        st.metric("Wymiana", f"{color_emoji} {turns}/{max_turns}")
    
    # Przycisk zakończenia
    if st.button("🏁 Zakończ rozmowę", help="Zakończ i zobacz podsumowanie"):
        st.session_state.sim_completed = True
        st.rerun()
    
    # Kontekst (zwijany)
    with st.expander("📋 Kontekst scenariusza", expanded=False):
        st.info(scenario['context'])
    
    st.markdown("---")
    
    # Wyświetl historię rozmowy
    for msg in st.session_state.sim_messages:
        if msg['role'] == 'ai':
            # Dynamiczne avatar bazując na roli
            avatar_map = {
                "Szef": "💼",
                "Pracownik": "👤",
                "Członek zespołu": "👥",
                "Klient": "😤",
                "Partner biznesowy": "🤝"
            }
            avatar = avatar_map.get(scenario['ai_role'], "🤖")
            
            with st.chat_message("assistant", avatar=avatar):
                st.markdown(msg['content'])
        else:
            # User message
            avatar_map = {
                "Menedżer": "💼",
                "Pracownik": "👤",
                "Mediator": "⚖️",
                "Account Manager": "💼",
                "Negocjator": "🤝",
                "Lider zmiany": "🔄"
            }
            avatar = avatar_map.get(scenario['user_role'], "👤")
            
            with st.chat_message("user", avatar=avatar):
                st.markdown(msg['content'])
                
                # Pokaż analizę C-IQ
                if 'ciq_analysis' in msg:
                    analysis = msg['ciq_analysis']
                    color = analysis.get('color', 'blue')
                    
                    feedback_text = f"""**📊 C-IQ: {analysis['level']}** (ocena: {analysis['score']}/10)
                    
{analysis['reasoning']}

💡 **Wskazówka:** {analysis['tip']}"""
                    
                    if color == 'green':
                        st.success(feedback_text)
                    elif color == 'blue':
                        st.info(feedback_text)
                    elif color == 'orange':
                        st.warning(feedback_text)
                    else:  # red
                        st.error(feedback_text)
    
    # Input użytkownika
    if st.session_state.sim_turn_count < st.session_state.sim_max_turns:
        user_input = st.chat_input("Twoja odpowiedź...")
        
        if user_input and user_input.strip():
            # Dodaj wiadomość użytkownika
            st.session_state.sim_messages.append({
                'role': 'user',
                'content': user_input
            })
            
            # Analizuj C-IQ
            with st.spinner("🔍 Analizuję poziom C-IQ..."):
                ciq_analysis = analyze_message_ciq(user_input, scenario)
                st.session_state.sim_messages[-1]['ciq_analysis'] = ciq_analysis
            
            # Generuj odpowiedź AI
            with st.spinner(f"💭 {scenario['ai_role']} myśli..."):
                ai_response = generate_ai_response(scenario, st.session_state.sim_messages, user_input)
                st.session_state.sim_messages.append({
                    'role': 'ai',
                    'content': ai_response
                })
            
            # Zwiększ licznik
            st.session_state.sim_turn_count += 1
            
            st.rerun()
    else:
        st.info("🏁 Osiągnąłeś maksymalną liczbę wymian (10). Kliknij 'Zakończ rozmowę' aby zobaczyć podsumowanie.")
