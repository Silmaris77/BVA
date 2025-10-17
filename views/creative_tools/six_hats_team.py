"""
Wirtualny Zespół Kreatywny - 6 Kapeluszy de Bono
Interaktywne narzędzie do kreatywnego rozwiązywania problemów
"""

import streamlit as st
from typing import Dict, List, Optional
import json
from datetime import datetime

from data.six_hats_templates import (
    PROBLEM_TEMPLATES, 
    HATS_DEFINITIONS, 
    HATS_ORDER
)
from utils.six_hats_engine import SixHatsEngine

# ===============================================
# INICJALIZACJA SESSION STATE
# ===============================================

def init_six_hats_state():
    """Inicjalizuje stan narzędzia"""
    if 'sht_problem_type' not in st.session_state:
        st.session_state.sht_problem_type = None
    
    if 'sht_problem' not in st.session_state:
        st.session_state.sht_problem = ""
    
    if 'sht_context' not in st.session_state:
        st.session_state.sht_context = ""
    
    if 'sht_mode' not in st.session_state:
        st.session_state.sht_mode = "auto"  # auto / interactive
    
    if 'sht_started' not in st.session_state:
        st.session_state.sht_started = False
    
    if 'sht_messages' not in st.session_state:
        st.session_state.sht_messages = []
    
    if 'sht_current_hat_index' not in st.session_state:
        st.session_state.sht_current_hat_index = 0
    
    if 'sht_completed' not in st.session_state:
        st.session_state.sht_completed = False
    
    if 'sht_awaiting_user' not in st.session_state:
        st.session_state.sht_awaiting_user = False
    
    # Engine inicjalizowany lazy - tylko gdy potrzebny (oszczędza czas przy pierwszym renderze)
    if 'sht_engine' not in st.session_state:
        st.session_state.sht_engine = None
    
    if 'sht_saved_sessions' not in st.session_state:
        st.session_state.sht_saved_sessions = []

def get_engine():
    """Lazy initialization engine - tworzy tylko gdy potrzebny"""
    if st.session_state.sht_engine is None:
        st.session_state.sht_engine = SixHatsEngine()
    return st.session_state.sht_engine

def reset_six_hats():
    """Resetuje sesję"""
    st.session_state.sht_started = False
    st.session_state.sht_messages = []
    st.session_state.sht_current_hat_index = 0
    st.session_state.sht_completed = False
    st.session_state.sht_awaiting_user = False

# ===============================================
# KROK 1: WYBÓR PROBLEMU
# ===============================================

def show_problem_selection():
    """Wyświetla ekran wyboru problemu"""
    st.markdown("### 🎯 Krok 1: Wybierz rodzaj problemu")
    
    st.info("""
    **Metoda 6 Kapeluszy de Bono** to technika kreatywnego myślenia, która pozwala spojrzeć 
    na problem z różnych perspektyw. Wirtualny zespół pomoże Ci przeanalizować Twoje wyzwanie 
    z 6 różnych punktów widzenia.
    """)
    
    # Wybór szablonu
    template_cols = st.columns(2)
    
    for idx, (key, template) in enumerate(PROBLEM_TEMPLATES.items()):
        col = template_cols[idx % 2]
        
        with col:
            if st.button(
                template["name"],
                key=f"template_{key}",
                help=template["description"],
                use_container_width=True
            ):
                st.session_state.sht_problem_type = key
                st.rerun()
    
    st.markdown("---")
    
    # Jeśli wybrano szablon
    if st.session_state.sht_problem_type:
        template = PROBLEM_TEMPLATES[st.session_state.sht_problem_type]
        
        st.markdown(f"### {template['name']}")
        st.caption(template['description'])
        
        if template['example']:
            st.markdown(f"**Przykład:** {template['example']}")
        
        # Prompt suggestions
        if template['prompts']:
            st.markdown("**Przykładowe pytania:**")
            for prompt in template['prompts']:
                if st.button(f"💡 {prompt}", key=f"prompt_{prompt}", use_container_width=True):
                    st.session_state.sht_problem = prompt
        
        st.markdown("---")
        
        # Własny opis problemu
        st.markdown("### ✍️ Opisz swój problem")
        
        problem_input = st.text_area(
            "Opisz szczegółowo problem lub wyzwanie, które chcesz rozwiązać:",
            value=st.session_state.sht_problem,
            height=100,
            placeholder="Np. Jak zwiększyć zaangażowanie pracowników w projekty innowacyjne?",
            key="problem_textarea"
        )
        
        context_input = st.text_area(
            "Dodatkowy kontekst (opcjonalnie):",
            value=st.session_state.sht_context,
            height=80,
            placeholder="Np. Firma 50 osób, branża IT, budżet 50k PLN rocznie na innowacje",
            key="context_textarea"
        )
        
        # Wybór trybu
        st.markdown("### ⚙️ Tryb sesji")
        
        mode_col1, mode_col2 = st.columns(2)
        
        with mode_col1:
            if st.button(
                "🤖 Automatyczny",
                help="AI przeprowadzi całą sesję automatycznie - obserwuj dyskusję",
                use_container_width=True,
                type="primary" if st.session_state.sht_mode == "auto" else "secondary"
            ):
                st.session_state.sht_mode = "auto"
        
        with mode_col2:
            if st.button(
                "💬 Interaktywny",
                help="Możesz zadawać pytania i prosić o wyjaśnienia",
                use_container_width=True,
                type="primary" if st.session_state.sht_mode == "interactive" else "secondary"
            ):
                st.session_state.sht_mode = "interactive"
        
        mode_desc = {
            "auto": "🤖 **Tryb automatyczny:** Zespół przeprowadzi pełną dyskusję, a Ty obserwuj. Pod koniec otrzymasz syntezę.",
            "interactive": "💬 **Tryb interaktywny:** Zespół wypowiada się po kolei, ale Ty możesz zadawać pytania dowolnemu kapeluszowi."
        }
        
        st.info(mode_desc[st.session_state.sht_mode])
        
        st.markdown("---")
        
        # Start sesji
        if problem_input and problem_input.strip():
            if st.button("🚀 Rozpocznij sesję kreatywną", type="primary", use_container_width=True):
                st.session_state.sht_problem = problem_input.strip()
                st.session_state.sht_context = context_input.strip() if context_input else ""
                st.session_state.sht_started = True
                st.session_state.sht_current_hat_index = 0
                
                # Przyznaj XP za start
                if 'experience_points' in st.session_state:
                    st.session_state.experience_points += 1
                
                st.rerun()
        else:
            st.warning("⚠️ Najpierw opisz problem, który chcesz rozwiązać.")

# ===============================================
# KROK 2: SESJA KREATYWNA
# ===============================================

def show_session():
    """Wyświetla aktywną sesję"""
    
    # Header z informacjami
    st.markdown("### 🎩 Sesja Kreatywna - 6 Kapeluszy")
    
    col_info1, col_info2 = st.columns([3, 1])
    
    with col_info1:
        st.markdown(f"**Problem:** {st.session_state.sht_problem}")
        if st.session_state.sht_context:
            with st.expander("📋 Kontekst"):
                st.write(st.session_state.sht_context)
    
    with col_info2:
        mode_icon = "🤖" if st.session_state.sht_mode == "auto" else "💬"
        mode_name = "Automatyczny" if st.session_state.sht_mode == "auto" else "Interaktywny"
        st.metric("Tryb", f"{mode_icon} {mode_name}")
    
    st.markdown("---")
    
    # Wyświetl legendę kapeluszy
    with st.expander("🎩 Legenda Kapeluszy", expanded=False):
        for hat_key, hat_def in HATS_DEFINITIONS.items():
            st.markdown(f"**{hat_def['name']}** ({hat_def['role']}): {hat_def['description']}")
    
    st.markdown("---")
    
    # Wyświetl dotychczasowe wiadomości
    for idx, msg in enumerate(st.session_state.sht_messages):
        if msg.get("role") == "user":
            # Pytanie użytkownika
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            # Wypowiedź kapeluszy
            hat_def = HATS_DEFINITIONS[msg["hat"]]
            
            with st.chat_message("assistant", avatar=hat_def["name"][0]):
                st.markdown(f"**{hat_def['name']}** ({hat_def['role']})")
                
                # Oznaczenie konfliktu
                if msg.get("is_conflict"):
                    conflict_hat = HATS_DEFINITIONS[msg["conflict_with"]]
                    st.caption(f"⚡ W odpowiedzi na {conflict_hat['name']}")
                
                st.markdown(msg["content"])
    
    # Automatyczne generowanie WSZYSTKICH kapeluszy naraz (bez ciągłych rerun)
    if st.session_state.sht_mode == "auto" and not st.session_state.sht_completed:
        if st.session_state.sht_current_hat_index < len(HATS_ORDER):
            # W trybie auto generuj wszystkie naraz, pokazując progress
            with st.spinner("💭 Zespół prowadzi dyskusję..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                while st.session_state.sht_current_hat_index < len(HATS_ORDER):
                    hat_color = HATS_ORDER[st.session_state.sht_current_hat_index]
                    hat_name = HATS_DEFINITIONS[hat_color]['name']
                    
                    # Aktualizuj status
                    progress = (st.session_state.sht_current_hat_index + 1) / len(HATS_ORDER)
                    progress_bar.progress(progress)
                    status_text.text(f"{hat_name} myśli... ({st.session_state.sht_current_hat_index + 1}/{len(HATS_ORDER)})")
                    
                    # Generuj wypowiedź
                    response = get_engine().generate_hat_response(
                        hat_color=hat_color,
                        problem=st.session_state.sht_problem,
                        context=st.session_state.sht_context,
                        previous_messages=st.session_state.sht_messages,
                        allow_conflict=(st.session_state.sht_current_hat_index > 2)
                    )
                    
                    st.session_state.sht_messages.append(response)
                    st.session_state.sht_current_hat_index += 1
                
                # Wszystkie kapelusze wygenerowane
                progress_bar.progress(1.0)
                status_text.text("✅ Dyskusja zakończona!")
            
            # Zakończ sesję i JEDEN rerun na końcu
            st.session_state.sht_completed = True
            st.rerun()
    
    # Tryb interaktywny - przyciski
    if st.session_state.sht_mode == "interactive" and not st.session_state.sht_completed:
        st.markdown("---")
        
        if st.session_state.sht_current_hat_index < len(HATS_ORDER):
            next_hat = HATS_ORDER[st.session_state.sht_current_hat_index]
            next_hat_def = HATS_DEFINITIONS[next_hat]
            
            col_btn1, col_btn2 = st.columns([3, 1])
            
            with col_btn1:
                if st.button(
                    f"👉 Wysłuchaj {next_hat_def['name']}",
                    type="primary",
                    use_container_width=True,
                    key="next_hat_btn"
                ):
                    response = get_engine().generate_hat_response(
                        hat_color=next_hat,
                        problem=st.session_state.sht_problem,
                        context=st.session_state.sht_context,
                        previous_messages=st.session_state.sht_messages,
                        allow_conflict=(st.session_state.sht_current_hat_index > 2)
                    )
                    
                    st.session_state.sht_messages.append(response)
                    st.session_state.sht_current_hat_index += 1
                    st.rerun()
            
            with col_btn2:
                if st.button("⏭️ Przejdź do syntezy", key="skip_btn", use_container_width=True):
                    st.session_state.sht_current_hat_index = len(HATS_ORDER)
                    st.session_state.sht_completed = True
                    st.rerun()
        
        # Możliwość zadania pytania
        if not st.session_state.sht_awaiting_user:
            with st.expander("💬 Zadaj pytanie konkretnemu kapeluszowi"):
                question_hat = st.selectbox(
                    "Wybierz kapelusz:",
                    options=list(HATS_DEFINITIONS.keys()),
                    format_func=lambda x: HATS_DEFINITIONS[x]["name"],
                    key="question_hat_select"
                )
                
                user_question = st.text_input(
                    "Twoje pytanie:",
                    placeholder="Np. Co jeszcze warto wziąć pod uwagę?",
                    key="user_question_input"
                )
                
                if st.button("📤 Zadaj pytanie", key="ask_question_btn"):
                    if user_question.strip():
                        # Dodaj pytanie użytkownika
                        st.session_state.sht_messages.append({
                            "role": "user",
                            "content": user_question.strip()
                        })
                        
                        # Generuj odpowiedź
                        response = get_engine().generate_hat_response(
                            hat_color=question_hat,
                            problem=st.session_state.sht_problem,
                            context=st.session_state.sht_context,
                            previous_messages=st.session_state.sht_messages,
                            allow_conflict=False  # Nie ma konfliktu przy odpowiedzi na pytanie
                        )
                        
                        st.session_state.sht_messages.append(response)
                        st.rerun()
    
    # Przycisk zakończenia dla trybu interaktywnego
    if st.session_state.sht_mode == "interactive" and st.session_state.sht_current_hat_index >= len(HATS_ORDER) and not st.session_state.sht_completed:
        if st.button("✅ Zakończ sesję i zobacz syntezę", type="primary", use_container_width=True):
            st.session_state.sht_completed = True
            st.rerun()

# ===============================================
# KROK 3: SYNTEZA I PODSUMOWANIE
# ===============================================

def show_synthesis():
    """Wyświetla syntezę sesji"""
    st.success("✅ Sesja kreatywna zakończona!")
    st.markdown("### 📊 Synteza i Wnioski")
    
    # Generuj syntezę
    with st.spinner("🧠 Analizuję dyskusję i przygotowuję syntezę..."):
        synthesis = get_engine().generate_synthesis(
            problem=st.session_state.sht_problem,
            context=st.session_state.sht_context,
            all_messages=st.session_state.sht_messages
        )
    
    # Wyświetl podsumowanie
    st.markdown("#### 📝 Podsumowanie")
    st.info(synthesis["summary"])
    
    st.markdown("---")
    
    # Kluczowe insighty
    st.markdown("#### 💡 Kluczowe Insighty")
    for idx, insight in enumerate(synthesis["key_insights"], 1):
        st.markdown(f"{idx}. {insight}")
    
    st.markdown("---")
    
    # Top 3 pomysły
    st.markdown("#### 🌟 Top 3 Pomysły")
    
    for idx, idea in enumerate(synthesis["top_ideas"], 1):
        with st.expander(f"💡 Pomysł {idx}: {idea['idea']}", expanded=(idx == 1)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ Zalety:**")
                st.write(idea["pros"])
            
            with col2:
                st.markdown("**⚠️ Wyzwania:**")
                st.write(idea["cons"])
            
            st.metric("Realność wdrożenia", f"{idea['feasibility']}/10")
    
    st.markdown("---")
    
    # Następne kroki
    st.markdown("#### 🎯 Rekomendowane Następne Kroki")
    for idx, step in enumerate(synthesis["next_steps"], 1):
        st.markdown(f"{idx}. {step}")
    
    st.markdown("---")
    
    # Główna rekomendacja
    st.markdown("#### 🎯 Główna Rekomendacja Zespołu")
    st.success(synthesis["recommendation"])
    
    st.markdown("---")
    
    # Zapisz sesję
    col_save1, col_save2 = st.columns([2, 1])
    
    with col_save1:
        if st.button("💾 Zapisz sesję do portfolio", use_container_width=True):
            session_data = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "problem_type": st.session_state.sht_problem_type,
                "problem": st.session_state.sht_problem,
                "context": st.session_state.sht_context,
                "mode": st.session_state.sht_mode,
                "messages": st.session_state.sht_messages,
                "synthesis": synthesis
            }
            
            st.session_state.sht_saved_sessions.append(session_data)
            
            # XP za ukończenie
            if 'experience_points' in st.session_state:
                st.session_state.experience_points += 20
            
            st.success("✅ Sesja zapisana w portfolio!")
            st.balloons()
    
    with col_save2:
        # Pobierz raport
        transcript = generate_transcript(synthesis)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"6_kapeluszy_{timestamp}.txt"
        
        st.download_button(
            label="📥 Pobierz raport",
            data=transcript,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Przyciski akcji
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        if st.button("🔄 Nowa sesja", use_container_width=True, type="primary"):
            reset_six_hats()
            st.rerun()
    
    with col_act2:
        if st.button("📚 Zobacz portfolio", use_container_width=True):
            st.session_state.show_sht_portfolio = True
            st.rerun()

def generate_transcript(synthesis: Dict) -> str:
    """Generuje transkrypcję sesji"""
    lines = []
    lines.append("=" * 70)
    lines.append("RAPORT Z SESJI KREATYWNEJ - 6 KAPELUSZY DE BONO")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Problem: {st.session_state.sht_problem}")
    if st.session_state.sht_context:
        lines.append(f"Kontekst: {st.session_state.sht_context}")
    lines.append(f"Tryb: {'Automatyczny' if st.session_state.sht_mode == 'auto' else 'Interaktywny'}")
    lines.append("")
    lines.append("=" * 70)
    lines.append("PRZEBIEG SESJI")
    lines.append("=" * 70)
    lines.append("")
    
    for msg in st.session_state.sht_messages:
        if msg.get("role") == "user":
            lines.append(f"[PYTANIE UŻYTKOWNIKA]:")
            lines.append(msg["content"])
        else:
            hat_def = HATS_DEFINITIONS[msg["hat"]]
            lines.append(f"[{hat_def['name']} - {hat_def['role']}]:")
            lines.append(msg["content"])
        lines.append("")
    
    lines.append("=" * 70)
    lines.append("SYNTEZA")
    lines.append("=" * 70)
    lines.append("")
    lines.append("PODSUMOWANIE:")
    lines.append(synthesis["summary"])
    lines.append("")
    lines.append("KLUCZOWE INSIGHTY:")
    for idx, insight in enumerate(synthesis["key_insights"], 1):
        lines.append(f"{idx}. {insight}")
    lines.append("")
    lines.append("TOP 3 POMYSŁY:")
    for idx, idea in enumerate(synthesis["top_ideas"], 1):
        lines.append(f"\n{idx}. {idea['idea']}")
        lines.append(f"   Zalety: {idea['pros']}")
        lines.append(f"   Wyzwania: {idea['cons']}")
        lines.append(f"   Realność: {idea['feasibility']}/10")
    lines.append("")
    lines.append("NASTĘPNE KROKI:")
    for idx, step in enumerate(synthesis["next_steps"], 1):
        lines.append(f"{idx}. {step}")
    lines.append("")
    lines.append("REKOMENDACJA:")
    lines.append(synthesis["recommendation"])
    lines.append("")
    lines.append("=" * 70)
    
    return "\n".join(lines)

# ===============================================
# MAIN FUNCTION
# ===============================================

def show_six_hats_team():
    """Główna funkcja narzędzia"""
    init_six_hats_state()
    
    # Sprawdź czy pokazać portfolio
    if st.session_state.get('show_sht_portfolio', False):
        show_portfolio()
        return
    
    if not st.session_state.sht_started:
        show_problem_selection()
    elif not st.session_state.sht_completed:
        show_session()
    else:
        show_synthesis()

def show_portfolio():
    """Wyświetla zapisane sesje"""
    st.markdown("### 📚 Portfolio Sesji Kreatywnych")
    
    if not st.session_state.sht_saved_sessions:
        st.info("Nie masz jeszcze żadnych zapisanych sesji. Przeprowadź pierwszą sesję 6 Kapeluszy!")
    else:
        for idx, session in enumerate(reversed(st.session_state.sht_saved_sessions)):
            with st.expander(f"📅 {session['date']} - {session['problem'][:50]}..."):
                st.markdown(f"**Problem:** {session['problem']}")
                if session['context']:
                    st.markdown(f"**Kontekst:** {session['context']}")
                st.markdown(f"**Tryb:** {'Automatyczny' if session['mode'] == 'auto' else 'Interaktywny'}")
                
                st.markdown("**Główna rekomendacja:**")
                st.info(session['synthesis']['recommendation'])
                
                # Pobierz raport
                transcript = generate_transcript(session['synthesis'])
                filename = f"6_kapeluszy_{session['date'].replace(':', '-').replace(' ', '_')}.txt"
                
                st.download_button(
                    label="📥 Pobierz raport",
                    data=transcript,
                    file_name=filename,
                    mime="text/plain",
                    key=f"download_{idx}"
                )
    
    if st.button("⬅️ Powrót", use_container_width=True):
        st.session_state.show_sht_portfolio = False
        st.rerun()
