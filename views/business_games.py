"""
Business Games - UI
Widok główny z zakładkami: Dashboard, Rynek Kontraktów, Pracownicy, Rankingi
"""

import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go

from data.business_data import FIRM_LEVELS, EMPLOYEE_TYPES, GAME_CONFIG
from utils.business_game import (
    initialize_business_game, refresh_contract_pool, accept_contract,
    submit_contract_solution, hire_employee, fire_employee,
    calculate_daily_costs, get_firm_summary, get_revenue_chart_data,
    get_category_distribution, calculate_overall_score, can_accept_contract,
    can_hire_employee, update_user_ranking
)
from utils.components import zen_header
from utils.material3_components import apply_material3_theme
from utils.scroll_utils import scroll_to_top

# =============================================================================
# GŁÓWNA FUNKCJA
# =============================================================================

def show_business_games(username, user_data):
    """Główny widok Business Games"""
    
    # Przewiń na górę strony
    scroll_to_top()
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Używamy standardowego nagłówka - tak jak w innych zakładkach
    zen_header("Business Games")
    
    # Inicjalizacja jeśli pierwszy raz
    if "business_game" not in user_data:
        user_data["business_game"] = initialize_business_game(username)
        st.success("🎉 Witaj w Business Games! Twoja firma została założona!")
        save_user_data(username, user_data)
    
    bg_data = user_data["business_game"]
    
    # Odśwież pulę kontraktów
    bg_data = refresh_contract_pool(bg_data)
    user_data["business_game"] = bg_data
    
    # Nagłówek z podsumowaniem firmy
    render_header(user_data)
    
    st.markdown("---")
    
    # Główne zakładki
    tabs = st.tabs(["🏢 Dashboard", "💼 Rynek Kontraktów", "👥 Pracownicy", "📜 Historia", "� Wydarzenia", "�🏆 Rankingi"])
    
    with tabs[0]:
        show_dashboard_tab(username, user_data)
    
    with tabs[1]:
        show_contracts_tab(username, user_data)
    
    with tabs[2]:
        show_employees_tab(username, user_data)
    
    with tabs[3]:
        show_history_tab(username, user_data)
    
    with tabs[4]:
        show_events_tab(username, user_data)
    
    with tabs[5]:
        show_rankings_tab(username, user_data)

# =============================================================================
# NAGŁÓWEK
# =============================================================================

def render_header(user_data):
    """Renderuje nagłówek z podstawowymi info o firmie"""
    bg_data = user_data["business_game"]
    firm = bg_data["firm"]
    level_info = FIRM_LEVELS[firm["level"]]
    
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; padding: 20px; border-radius: 10px;'>
            <h2 style='margin:0;'>{level_info['ikona']} {firm['name']}</h2>
            <p style='margin:5px 0 0 0; opacity:0.9;'>
                Poziom {firm['level']}: {level_info['nazwa']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("💰 Saldo", f"{user_data.get('degencoins', 0):,} monet", 
                 delta=None)
    
    with col3:
        st.metric("📈 Reputacja", f"{firm['reputation']}", 
                 delta=None)
    
    with col4:
        employees_count = len(bg_data["employees"])
        max_employees = level_info["max_pracownikow"]
        st.metric("👥 Zespół", f"{employees_count}/{max_employees}",
                 delta=None)
    
    with col5:
        st.metric("✅ Kontrakty", f"{bg_data['stats']['contracts_completed']}",
                 delta=None)

# =============================================================================
# TAB 1: DASHBOARD
# =============================================================================

def show_dashboard_tab(username, user_data):
    """Zakładka Dashboard - podsumowanie firmy"""
    bg_data = user_data["business_game"]
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
        user_data["business_game"] = bg_data
        save_user_data(username, user_data)
    
    # =============================================================================
    # SEKCJA LOSOWANIA WYDARZEŃ - NA POCZĄTKU DASHBOARDU
    # =============================================================================
    
    from utils.business_game_events import get_random_event, apply_event_effects
    from datetime import datetime, timedelta
    
    st.markdown("### 🎲 Losowanie Zdarzenia")
    
    # Sprawdź cooldown
    last_roll = bg_data.get("events", {}).get("last_roll")
    can_roll = True
    hours_left = 0
    minutes_left = 0
    
    if last_roll:
        last_dt = datetime.strptime(last_roll, "%Y-%m-%d %H:%M:%S")
        next_roll = last_dt + timedelta(hours=24)
        now = datetime.now()
        
        if now < next_roll:
            can_roll = False
            time_until_next = next_roll - now
            hours_left = int(time_until_next.total_seconds() / 3600)
            minutes_left = int((time_until_next.total_seconds() % 3600) / 60)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if can_roll:
            st.success("✅ **Możesz wylosować zdarzenie!** (Szansa: 20%)")
        else:
            st.warning(f"⏰ **Następne losowanie za: {hours_left}h {minutes_left}min**")
    
    with col2:
        if st.button("🎲 LOSUJ!", disabled=not can_roll, type="primary", key="dashboard_roll_event"):
            # Losuj zdarzenie
            event_result = get_random_event(bg_data, user_data.get("degencoins", 0))
            
            if event_result:
                event_id, event_data = event_result
                
                # Sprawdź czy wymaga wyboru
                if event_data["type"] == "neutral" and "choices" in event_data:
                    # Zapisz zdarzenie tymczasowo w session_state
                    st.session_state["pending_event"] = (event_id, event_data)
                    st.rerun()
                else:
                    # Bezpośrednio aplikuj
                    user_data = apply_event_effects(event_id, event_data, None, user_data)
                    save_user_data(username, user_data)
                    st.success(f"{event_data['emoji']} **{event_data['title']}**")
                    st.balloons() if event_data["type"] == "positive" else None
                    st.rerun()
            else:
                # Brak zdarzenia (80% przypadków)
                bg_data.setdefault("events", {})["last_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_data["business_game"] = bg_data
                save_user_data(username, user_data)
                st.info("😐 Tym razem nic się nie wydarzyło. Spokojny dzień!")
                st.rerun()
    
    # Pending event (jeśli neutralne wymaga wyboru)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data)
    
    st.markdown("---")
    
    # Sprawdź i wyświetl najnowsze zdarzenie (jeśli jest)
    from utils.business_game_events import get_latest_event, get_active_effects
    latest_event = get_latest_event(bg_data)
    if latest_event:
        render_latest_event_card(latest_event)
        st.markdown("---")
    
    # Pokaż aktywne efekty z wydarzeń
    active_effects = get_active_effects(bg_data)
    if active_effects:
        render_active_effects_badge(active_effects)
        st.markdown("---")
    
    st.subheader("📊 Podsumowanie Firmy")
    
    summary = get_firm_summary(user_data)
    
    # Metryki finansowe
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💵 Łączne przychody", f"{summary['total_revenue']:,} 💰")
    
    with col2:
        st.metric("💸 Łączne koszty", f"{summary['total_costs']:,} 💰")
    
    with col3:
        profit_color = "normal" if summary['net_profit'] >= 0 else "inverse"
        st.metric("💎 Zysk netto", f"{summary['net_profit']:,} 💰",
                 delta=None)
    
    with col4:
        st.metric("📉 Koszty dzienne", f"{summary['daily_costs']:.0f} 💰/dzień")
    
    st.markdown("---")
    
    # Sekcja aktywnych kontraktów
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📋 Aktywne Kontrakty")
        
        active_contracts = bg_data["contracts"]["active"]
        
        if len(active_contracts) == 0:
            st.info("Brak aktywnych kontraktów. Przejdź do zakładki 'Rynek Kontraktów' aby przyjąć nowe zlecenie!")
        else:
            for contract in active_contracts:
                render_active_contract_card(contract, username, user_data, bg_data)
    
    with col_right:
        st.subheader("📈 Statystyki")
        
        stats = bg_data["stats"]
        
        st.metric("⭐ Średnia ocena", f"{stats['avg_rating']:.1f}/5.0")
        st.metric("🌟 Kontrakty 5⭐", stats["contracts_5star"])
        st.metric("📊 Pojemność dzienna", f"{summary['daily_capacity']} kontraktów")
        
        st.markdown("---")
        
        st.markdown("### 🎯 Rozkład kontraktów")
        category_dist = get_category_distribution(bg_data)
        
        if category_dist:
            for cat, count in category_dist.items():
                cat_stats = stats["category_stats"][cat]
                st.markdown(f"""
                **{cat}**: {count} kontraktów  
                Średnia: {cat_stats['avg_rating']:.1f}⭐ | Zarobek: {cat_stats['total_earned']:,} 💰
                """)
        else:
            st.info("Brak danych")
    
    st.markdown("---")
    
    # Wykres przychodów (uproszczony)
    st.subheader("💹 Historia przychodów (ostatnie 7 dni)")
    
    revenue_data = get_revenue_chart_data(bg_data, days=7)
    
    if revenue_data["dates"]:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=revenue_data["dates"],
            y=revenue_data["revenue"],
            marker_color='#667eea',
            text=revenue_data["revenue"],
            textposition='auto',
        ))
        fig.update_layout(
            title="Dzienne przychody",
            xaxis_title="Data",
            yaxis_title="Monety",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Brak danych - ukończ pierwszy kontrakt!")
    
    # Edycja nazwy firmy
    st.markdown("---")
    st.subheader("⚙️ Ustawienia")
    
    with st.expander("Zmień nazwę firmy"):
        new_name = st.text_input("Nowa nazwa firmy", value=bg_data["firm"]["name"], key="dashboard_firm_name_input")
        if st.button("💾 Zapisz nazwę", key="dashboard_save_firm_name"):
            bg_data["firm"]["name"] = new_name
            user_data["business_game"] = bg_data
            save_user_data(username, user_data)
            st.success("Nazwa firmy zaktualizowana!")
            st.rerun()

def render_active_contract_card(contract, username, user_data, bg_data):
    """Renderuje kartę aktywnego kontraktu"""
    
    with st.container():
        # Oblicz pozostały czas
        deadline = datetime.strptime(contract["deadline"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        time_left = deadline - now
        hours_left = int(time_left.total_seconds() / 3600)
        
        deadline_color = "🟢" if hours_left > 24 else "🟡" if hours_left > 6 else "🔴"
        
        # Sprawdź czy kontrakt był dotknięty zdarzeniem
        event_affected = contract.get("affected_by_event")
        
        # Ustal kolor ramki na podstawie typu zdarzenia
        if event_affected:
            if event_affected.get("type") == "deadline_reduction":
                border_color = "#ff6b6b"  # Czerwony dla skróconego
            elif event_affected.get("type") == "deadline_extension":
                border_color = "#10b981"  # Zielony dla przedłużonego
            else:
                border_color = "#667eea"  # Domyślny niebieski
        else:
            border_color = "#667eea"  # Domyślny niebieski
        
        # Header (tylko stylowanie ramki)
        st.markdown(f"""
        <div style='border: 2px solid {border_color}; border-radius: 10px; 
                    padding: 15px; margin: 10px 0; background: #f8f9fa;'>
            <h4>{contract['emoji']} {contract['tytul']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # ALERT jeśli dotknięty zdarzeniem
        if event_affected:
            if event_affected.get("type") == "deadline_reduction":
                st.warning(f"⚠️ **Zdarzenie: {event_affected.get('event_title')}** - Deadline skrócony o {event_affected.get('days_reduced')} dzień!")
            elif event_affected.get("type") == "deadline_extension":
                st.success(f"✨ **Zdarzenie: {event_affected.get('event_title')}** - Deadline przedłużony o {event_affected.get('days_added')} dzień!")
        
        # Informacje - natywny Markdown
        st.markdown(f"**Klient:** {contract['klient']} | **Kategoria:** {contract['kategoria']}")
        st.markdown(f"**{deadline_color} Deadline:** {hours_left}h pozostało")
        st.markdown(f"**💰 Nagroda:** {contract['nagroda_base']}-{contract['nagroda_5star']} monet")
        
        with st.expander(f"🔍 Szczegóły i realizacja: {contract['tytul']}"):
            # Renderuj opis i zadanie jako czysty Markdown (bez HTML wrappera)
            st.markdown(f"**Opis sytuacji:**")
            st.markdown(contract['opis'])
            st.markdown("---")
            st.markdown(f"**Zadanie:**")
            st.markdown(contract['zadanie'])
            st.markdown("---")
            
            st.markdown(f"**Wymagana wiedza:** {', '.join(contract['wymagana_wiedza'])}")
            st.markdown(f"**Trudność:** {'🔥' * contract['trudnosc']}")
            st.markdown(f"**Minimalnie:** {contract.get('min_slow', 300)} słów")
            
            st.markdown("---")
            st.subheader("✍️ Twoje rozwiązanie")
            
            # ANTI-CHEAT: Zapisz czas rozpoczęcia pisania
            solution_start_key = f"solution_start_{contract['id']}"
            if solution_start_key not in st.session_state:
                st.session_state[solution_start_key] = datetime.now()
            
            # ANTI-CHEAT: Tracking paste events
            paste_events_key = f"paste_events_{contract['id']}"
            if paste_events_key not in st.session_state:
                st.session_state[paste_events_key] = []
            
            solution_key = f"solution_{contract['id']}"
            solution = st.text_area(
                "Przygotuj kompleksowe rozwiązanie zgodnie z wymaganiami:",
                value=contract.get("solution", ""),
                height=400,
                key=solution_key,
                placeholder="Zacznij pisać swoje rozwiązanie tutaj..."
            )
            
            # ANTI-CHEAT: Dodaj JavaScript do śledzenia wklejania
            st.markdown(f"""
            <script>
            (function() {{
                const textarea = document.querySelector('textarea[aria-label="Przygotuj kompleksowe rozwiązanie zgodnie z wymaganiami:"]');
                if (textarea) {{
                    textarea.addEventListener('paste', function(e) {{
                        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
                        const pasteLength = pastedText.length;
                        const totalLength = textarea.value.length + pasteLength;
                        
                        // Wyślij event do Streamlit (przez hidden input)
                        const event = {{
                            'length': pasteLength,
                            'total_solution_length': totalLength,
                            'timestamp': new Date().toISOString()
                        }};
                        
                        console.log('Paste detected:', event);
                        
                        // Zapisz w localStorage (Streamlit może to odczytać)
                        const existingEvents = JSON.parse(localStorage.getItem('paste_events_{contract['id']}') || '[]');
                        existingEvents.push(event);
                        localStorage.setItem('paste_events_{contract['id']}', JSON.stringify(existingEvents));
                    }});
                }}
            }})();
            </script>
            """, unsafe_allow_html=True)
            
            if solution is None:
                solution = ""
            
            word_count = len(solution.split())
            min_words = contract.get('min_slow', 300)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                progress = min(100, int((word_count / min_words) * 100))
                st.progress(progress / 100)
                st.caption(f"Liczba słów: {word_count}/{min_words} ({progress}%)")
            
            with col2:
                if st.button("✅ Prześlij rozwiązanie", key=f"submit_{contract['id']}", type="primary"):
                    if word_count < min_words:
                        st.error(f"Rozwiązanie zbyt krótkie! Minimum: {min_words} słów")
                    else:
                        # Pobierz dane anti-cheat
                        start_time = st.session_state.get(solution_start_key)
                        paste_events = st.session_state.get(paste_events_key, [])
                        
                        # Prześlij rozwiązanie z danymi anti-cheat
                        updated_user_data, success, message = submit_contract_solution(
                            user_data, contract['id'], solution,
                            start_time=start_time,
                            paste_events=paste_events if paste_events else None
                        )
                        
                        if success:
                            user_data.update(updated_user_data)
                            save_user_data(username, user_data)
                            
                            # Wyczyść tracking anti-cheat
                            if solution_start_key in st.session_state:
                                del st.session_state[solution_start_key]
                            if paste_events_key in st.session_state:
                                del st.session_state[paste_events_key]
                            
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)

# =============================================================================
# TAB 2: RYNEK KONTRAKTÓW
# =============================================================================

def show_contracts_tab(username, user_data):
    """Zakładka Rynek Kontraktów"""
    bg_data = user_data["business_game"]
    
    st.subheader("💼 Dostępne Kontrakty")
    
    # Info o pojemności
    can_accept, reason = can_accept_contract(bg_data)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        active_count = len(bg_data["contracts"]["active"])
        max_active = GAME_CONFIG["max_active_contracts"]
        st.info(f"📋 Aktywne kontrakty: **{active_count}/{max_active}**")
    
    with col2:
        firm_level = bg_data["firm"]["level"]
        employees = bg_data["employees"]
        capacity = FIRM_LEVELS[firm_level]["limit_kontraktow_dzienny"]
        for emp in employees:
            emp_type = EMPLOYEE_TYPES.get(emp["type"])
            if emp_type and emp_type["bonus_type"] == "capacity":
                capacity += emp_type["bonus_value"]
        st.info(f"🎯 Dzienna pojemność: **{int(capacity)} kontraktów**")
    
    with col3:
        # Czas do odświeżenia puli
        last_refresh = datetime.strptime(bg_data["contracts"]["last_refresh"], "%Y-%m-%d %H:%M:%S")
        next_refresh = last_refresh.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        now = datetime.now()
        hours_to_refresh = int((next_refresh - now).total_seconds() / 3600)
        st.info(f"🔄 Nowe kontrakty za: **{hours_to_refresh}h**")
    
    # Przycisk do wymuszenia odświeżenia (dla testów/aktualizacji)
    col_refresh1, col_refresh2 = st.columns([3, 1])
    with col_refresh2:
        if st.button("🔄 Wymuś odświeżenie", help="Pobierz nowe kontrakty teraz (aktualizuje pulę)"):
            bg_data = refresh_contract_pool(bg_data, force=True)
            user_data["business_game"] = bg_data
            save_user_data(username, user_data)
            st.success("✅ Pula kontraktów została odświeżona!")
            st.rerun()
    
    if not can_accept:
        st.warning(f"⚠️ {reason}")
    
    st.markdown("---")
    
    # Filtry
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        category_filter = st.selectbox(
            "Kategoria:",
            ["Wszystkie", "Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership"],
            key="contracts_filter_category"
        )
    
    with col_filter2:
        difficulty_filter = st.selectbox(
            "Trudność:",
            ["Wszystkie", "🔥", "🔥🔥", "🔥🔥🔥", "🔥🔥🔥🔥", "🔥🔥🔥🔥🔥"],
            key="contracts_filter_difficulty"
        )
    
    with col_filter3:
        sort_by = st.selectbox(
            "Sortuj:",
            ["Nagroda: najwyższe", "Nagroda: najniższe", "Trudność: rosnąco", "Czas: najkrótsze"],
            key="contracts_sort_by"
        )
    
    st.markdown("---")
    
    # Lista kontraktów
    available_contracts = bg_data["contracts"]["available_pool"]
    
    # Filtrowanie
    if category_filter != "Wszystkie":
        available_contracts = [c for c in available_contracts if c["kategoria"] == category_filter]
    
    if difficulty_filter != "Wszystkie":
        diff_level = len(difficulty_filter)
        available_contracts = [c for c in available_contracts if c["trudnosc"] == diff_level]
    
    # Sortowanie
    if sort_by == "Nagroda: najwyższe":
        available_contracts = sorted(available_contracts, key=lambda x: x["nagroda_5star"], reverse=True)
    elif sort_by == "Nagroda: najniższe":
        available_contracts = sorted(available_contracts, key=lambda x: x["nagroda_base"])
    elif sort_by == "Trudność: rosnąco":
        available_contracts = sorted(available_contracts, key=lambda x: x["trudnosc"])
    elif sort_by == "Czas: najkrótsze":
        available_contracts = sorted(available_contracts, key=lambda x: x["czas_realizacji_dni"])
    
    if len(available_contracts) == 0:
        st.info("Brak dostępnych kontraktów spełniających kryteria. Zmień filtry lub poczekaj na odświeżenie puli.")
    else:
        for contract in available_contracts:
            render_contract_card(contract, username, user_data, bg_data, can_accept)

def render_contract_card(contract, username, user_data, bg_data, can_accept_new):
    """Renderuje kartę dostępnego kontraktu"""
    
    # Sprawdź czy jest aktywny bonus next_contract
    from utils.business_game_events import get_active_effects
    active_effects = get_active_effects(bg_data)
    has_bonus = any(e.get("type") == "next_contract_bonus" for e in active_effects)
    bonus_multiplier = 1.0
    
    if has_bonus:
        bonus_effect = next((e for e in active_effects if e.get("type") == "next_contract_bonus"), None)
        if bonus_effect:
            bonus_multiplier = bonus_effect.get("multiplier", 1.0)
    
    with st.container():
        # Header z ramką (tylko stylowanie, bez treści kontraktu)
        border_color = "#fbbf24" if has_bonus else "#667eea"  # Złoty dla bonusu
        
        st.markdown(f"""
        <div style='border: 2px solid {border_color}; border-radius: 10px; 
                    padding: 20px; margin: 10px 0; background: white;'>
            <h3>{contract['emoji']} {contract['tytul']}</h3>
            <p><strong>Klient:</strong> {contract['klient']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pokaż bonus jeśli aktywny
        if has_bonus:
            bonus_percent = int((bonus_multiplier - 1) * 100)
            bonus_base = int(contract['nagroda_base'] * bonus_multiplier)
            bonus_5star = int(contract['nagroda_5star'] * bonus_multiplier)
            st.success(f"🌟 **BONUS AKTYWNY: +{bonus_percent}%!** Nagroda: {bonus_base}-{bonus_5star} monet")
        
        # Opis - zwykły Markdown (renderowany przez Streamlit, nie w HTML)
        st.markdown(f"*{contract['opis'][:200]}...*")
        
        # Metryki w kolumnach
        col_reward, col_time, col_diff = st.columns(3)
        with col_reward:
            st.markdown(f"**💰 Nagroda:** {contract['nagroda_base']}-{contract['nagroda_5star']} monet")
        with col_time:
            st.markdown(f"**⏱️ Czas:** {contract['czas_realizacji_dni']} dni")
        with col_diff:
            st.markdown(f"**Trudność:** {'🔥' * contract['trudnosc']}")
        
        st.markdown(f"📚 **Wymagana wiedza:** {', '.join(contract['wymagana_wiedza'][:2])}...")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            with st.expander(f"👁️ Zobacz pełne szczegóły"):
                # Renderuj opis i zadanie jako czysty Markdown (bez HTML wrappera)
                st.markdown(f"**Opis sytuacji:**")
                st.markdown(contract['opis'])
                st.markdown("---")
                st.markdown(f"**Zadanie do wykonania:**")
                st.markdown(contract['zadanie'])
                st.markdown("---")
                st.markdown(f"**Wymagana wiedza z lekcji:**")
                for req in contract['wymagana_wiedza']:
                    st.markdown(f"- {req}")
                st.markdown(f"\n**Wymagany poziom firmy:** {contract['wymagany_poziom']}")
        
        with col2:
            # Sprawdź poziom
            if bg_data["firm"]["level"] < contract["wymagany_poziom"]:
                st.warning(f"🔒 Poziom {contract['wymagany_poziom']}")
            elif not can_accept_new:
                st.error("❌ Brak miejsca")
            else:
                if st.button("✅ Przyjmij", key=f"accept_{contract['id']}", type="primary"):
                    updated_bg, success, message = accept_contract(bg_data, contract['id'])
                    
                    if success:
                        user_data["business_game"] = updated_bg
                        save_user_data(username, user_data)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("---")

# =============================================================================
# TAB 3: PRACOWNICY
# =============================================================================

def show_employees_tab(username, user_data):
    """Zakładka Pracownicy"""
    bg_data = user_data["business_game"]
    
    st.subheader("👥 Zarządzanie Zespołem")
    
    firm_level = bg_data["firm"]["level"]
    max_employees = FIRM_LEVELS[firm_level]["max_pracownikow"]
    current_count = len(bg_data["employees"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Zespół", f"{current_count}/{max_employees}")
    with col2:
        daily_cost = calculate_daily_costs(bg_data)
        st.metric("💸 Koszty dzienne", f"{daily_cost:.0f} 💰")
    with col3:
        monthly_cost = daily_cost * 30
        st.metric("📅 Koszty miesięczne", f"{monthly_cost:.0f} 💰")
    
    st.markdown("---")
    
    # Zatrudnieni pracownicy
    st.subheader("🏢 Obecnie zatrudnieni")
    
    if len(bg_data["employees"]) == 0:
        st.info("Nie masz jeszcze pracowników. Zatrudnij kogoś z listy poniżej!")
    else:
        for employee in bg_data["employees"]:
            render_employee_card(employee, username, user_data, bg_data)
    
    st.markdown("---")
    
    # Dostępni do zatrudnienia
    st.subheader("💼 Dostępni do zatrudnienia")
    
    if current_count >= max_employees:
        st.warning(f"⚠️ Osiągnąłeś limit pracowników na poziomie {firm_level}. Zwiększ poziom firmy aby zatrudnić więcej osób!")
    
    for emp_type, emp_data in EMPLOYEE_TYPES.items():
        render_hire_card(emp_type, emp_data, username, user_data, bg_data)

def render_employee_card(employee, username, user_data, bg_data):
    """Renderuje kartę zatrudnionego pracownika"""
    
    emp_data = EMPLOYEE_TYPES[employee["type"]]
    
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    
    with col1:
        st.markdown(f"### {emp_data['ikona']} {emp_data['nazwa']}")
        st.caption(emp_data['opis'])
    
    with col2:
        st.markdown(f"**Bonus:**  \n{emp_data['bonus']}")
    
    with col3:
        st.markdown(f"**Koszt:**  \n{emp_data['koszt_dzienny']} 💰/dzień")
        st.caption(f"Zatrudniony: {employee['hired_date']}")
    
    with col4:
        if st.button("🗑️", key=f"fire_{employee['id']}", help="Zwolnij"):
            updated_user_data, success, message = fire_employee(user_data, employee['id'])
            if success:
                user_data.update(updated_user_data)
                save_user_data(username, user_data)
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    st.markdown("---")

def render_hire_card(emp_type, emp_data, username, user_data, bg_data):
    """Renderuje kartę dostępnego pracownika"""
    
    # Sprawdź czy już zatrudniony
    already_hired = any(e["type"] == emp_type for e in bg_data["employees"])
    if already_hired:
        return  # Nie pokazuj
    
    can_hire, reason = can_hire_employee(user_data, emp_type)
    
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.markdown(f"### {emp_data['ikona']} {emp_data['nazwa']}")
            st.caption(emp_data['opis'])
        
        with col2:
            st.markdown(f"**Bonus:**  \n{emp_data['bonus']}")
            if emp_data['specjalizacja']:
                st.caption(f"Specjalizacja: {emp_data['specjalizacja']}")
        
        with col3:
            st.markdown(f"**Koszt zatrudnienia:**  \n{emp_data['koszt_zatrudnienia']} 💰")
            st.markdown(f"**Koszt dzienny:**  \n{emp_data['koszt_dzienny']} 💰/dzień")
        
        with col4:
            if not can_hire:
                st.button("🔒", key=f"hire_{emp_type}_locked", disabled=True, help=reason)
            else:
                if st.button("✅ Zatrudnij", key=f"hire_{emp_type}", type="primary"):
                    updated_user_data, success, message = hire_employee(user_data, emp_type)
                    if success:
                        user_data.update(updated_user_data)
                        save_user_data(username, user_data)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("---")

# =============================================================================
# TAB 4: HISTORIA KONTRAKTÓW
# =============================================================================

def show_history_tab(username, user_data):
    """Zakładka Historia - ukończone kontrakty z feedbackiem"""
    bg_data = user_data["business_game"]
    
    st.subheader("📜 Historia Ukończonych Kontraktów")
    
    completed = bg_data["contracts"]["completed"]
    
    if len(completed) == 0:
        st.info("📭 Nie masz jeszcze ukończonych kontraktów. Wykonaj pierwszy kontrakt aby zobaczyć feedback od klienta!")
        return
    
    # Sortuj od najnowszych
    completed_sorted = sorted(completed, key=lambda x: x.get("completed_date", ""), reverse=True)
    
    # Filtry
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox(
            "Kategoria:",
            ["Wszystkie"] + ["Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership"],
            key="history_filter_category"
        )
    with col2:
        filter_rating = st.selectbox(
            "Ocena:",
            ["Wszystkie", "⭐⭐⭐⭐⭐ (5)", "⭐⭐⭐⭐ (4)", "⭐⭐⭐ (3)", "⭐⭐ (2)", "⭐ (1)"],
            key="history_filter_rating"
        )
    with col3:
        show_count = st.selectbox(
            "Pokaż:",
            [10, 25, 50, "Wszystkie"],
            key="history_show_count"
        )
    
    # Filtrowanie
    filtered = completed_sorted
    if filter_category != "Wszystkie":
        filtered = [c for c in filtered if c["kategoria"] == filter_category]
    if filter_rating != "Wszystkie":
        rating_num = int(filter_rating.split("(")[1].split(")")[0])
        filtered = [c for c in filtered if c.get("rating", 0) == rating_num]
    
    # Limit
    if show_count != "Wszystkie":
        filtered = filtered[:show_count]
    
    st.markdown("---")
    st.markdown(f"**Znaleziono:** {len(filtered)} kontraktów")
    st.markdown("---")
    
    # Wyświetl kontrakty
    for contract in filtered:
        render_completed_contract_card(contract)

def render_completed_contract_card(contract):
    """Renderuje kartę ukończonego kontraktu z pełnym feedbackiem"""
    
    rating = contract.get("rating", 0)
    feedback = contract.get("feedback", "Brak feedbacku")
    completed_date = contract.get("completed_date", "Nieznana data")
    reward_coins = contract.get("reward", {}).get("coins", 0)
    
    # Status koloru na podstawie oceny
    if rating >= 4:
        border_color = "#10b981"  # zielony
        bg_color = "#f0fdf4"
    elif rating >= 3:
        border_color = "#f59e0b"  # pomarańczowy
        bg_color = "#fffbeb"
    else:
        border_color = "#ef4444"  # czerwony
        bg_color = "#fef2f2"
    
    with st.container():
        # Header
        st.markdown(f"""
        <div style='border-left: 5px solid {border_color}; 
                    background: {bg_color};
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 8px;'>
            <h4 style='margin: 0 0 10px 0;'>{contract['emoji']} {contract['tytul']}</h4>
            <p style='margin: 0; color: #666;'>
                <strong>Klient:</strong> {contract['klient']} | 
                <strong>Kategoria:</strong> {contract['kategoria']} | 
                <strong>Ukończono:</strong> {completed_date}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metryki w kolumnach
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"### {'⭐' * rating}")
            st.caption(f"Ocena: {rating}/5")
        with col2:
            # Wyświetl 0 monet jeśli kontrakt był odrzucony
            coin_display = f"{reward_coins} monet" if reward_coins > 0 else "0 monet (odrzucono)"
            st.metric("💰 Zarobiono", coin_display)
        with col3:
            rep_change = contract.get("reward", {}).get("reputation", 0)
            # Wyświetl znak + lub - w zależności od wartości
            rep_display = f"+{rep_change}" if rep_change >= 0 else str(rep_change)
            st.metric("📈 Reputacja", rep_display)
        
        st.markdown("---")
        
        # Feedback od klienta - główny element!
        st.markdown("### 💬 Feedback od klienta:")
        
        # Wyświetl feedback jako markdown (renderuje **bold**, listy itp.)
        st.markdown(feedback)
        
        # Expander z pełnymi szczegółami
        with st.expander("📋 Zobacz szczegóły kontraktu i Twoje rozwiązanie"):
            st.markdown("**Opis sytuacji:**")
            st.markdown(contract['opis'])
            st.markdown("---")
            st.markdown("**Zadanie:**")
            st.markdown(contract['zadanie'])
            st.markdown("---")
            st.markdown("**Twoje rozwiązanie:**")
            solution = contract.get("solution", "Brak zapisanego rozwiązania")
            st.markdown(f"""
            <div style='background: #f9fafb; 
                        padding: 15px; 
                        border-left: 3px solid #6366f1;
                        font-family: monospace;'>
                {solution}
            </div>
            """, unsafe_allow_html=True)
            
            # Szczegóły oceny są teraz ukryte - feedback wystarczy
            # Jeśli potrzebujesz debugowania, odkomentuj poniżej:
            # eval_details = contract.get("evaluation_details", {})
            # if eval_details:
            #     st.markdown("---")
            #     st.markdown("**Szczegóły oceny (debug):**")
            #     st.json(eval_details)
        
        st.markdown("---")

# =============================================================================
# TAB 5: WYDARZENIA
# =============================================================================

def show_events_tab(username, user_data):
    """Zakładka Wydarzenia - losowe zdarzenia"""
    bg_data = user_data["business_game"]
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
        user_data["business_game"] = bg_data
        save_user_data(username, user_data)
    
    st.subheader("🎲 Wydarzenia Losowe")
    
    # Info
    st.info("""
    📰 **Jak działają wydarzenia?**
    - Co 24h możesz wylosować nowe zdarzenie (20% szansa)
    - Zdarzenia mogą być **pozytywne** 🎉, **neutralne** ⚖️ lub **negatywne** 💥
    - Niektóre wymagają od Ciebie decyzji!
    - Historia ostatnich wydarzeń poniżej
    """)
    
    st.markdown("---")
    
    # Sekcja losowania
    from utils.business_game_events import should_trigger_event, get_random_event, apply_event_effects
    from datetime import datetime, timedelta
    
    # Sprawdź cooldown
    last_roll = bg_data.get("events", {}).get("last_roll")
    can_roll = True
    hours_left = 0
    minutes_left = 0
    
    if last_roll:
        last_dt = datetime.strptime(last_roll, "%Y-%m-%d %H:%M:%S")
        next_roll = last_dt + timedelta(hours=24)
        now = datetime.now()
        
        if now < next_roll:
            can_roll = False
            time_until_next = next_roll - now
            hours_left = int(time_until_next.total_seconds() / 3600)
            minutes_left = int((time_until_next.total_seconds() % 3600) / 60)
    
    st.markdown("### 🎰 Losowanie Zdarzenia")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if can_roll:
            st.success("✅ **Możesz wylosować zdarzenie!**")
            st.caption("Szansa: 20% na zdarzenie, 80% na brak")
        else:
            st.warning(f"⏰ **Następne losowanie za: {hours_left}h {minutes_left}min**")
            st.caption("Zdarzenia można losować raz na 24 godziny")
    
    with col2:
        if st.button("🎲 LOSUJ!", disabled=not can_roll, type="primary", key="roll_event"):
            # Losuj zdarzenie
            event_result = get_random_event(bg_data, user_data.get("degencoins", 0))
            
            if event_result:
                event_id, event_data = event_result
                
                # Sprawdź czy wymaga wyboru
                if event_data["type"] == "neutral" and "choices" in event_data:
                    # Zapisz zdarzenie tymczasowo w session_state
                    st.session_state["pending_event"] = (event_id, event_data)
                    st.rerun()
                else:
                    # Bezpośrednio aplikuj
                    user_data = apply_event_effects(event_id, event_data, None, user_data)
                    save_user_data(username, user_data)
                    st.success(f"{event_data['emoji']} **{event_data['title']}**")
                    st.balloons() if event_data["type"] == "positive" else None
                    st.rerun()
            else:
                # Brak zdarzenia (80% przypadków)
                bg_data.setdefault("events", {})["last_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_data["business_game"] = bg_data
                save_user_data(username, user_data)
                st.info("😐 Tym razem nic się nie wydarzyło. Spokojny dzień!")
                st.rerun()
    
    # Pending event (jeśli neutralne wymaga wyboru)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data)
    
    st.markdown("---")
    
    # Historia wydarzeń
    st.markdown("### 📜 Historia Wydarzeń")
    
    if "events" not in bg_data or not bg_data["events"].get("history"):
        st.info("Brak wydarzeń w historii. Wylosuj pierwsze zdarzenie powyżej!")
    else:
        history = bg_data["events"]["history"]
        history_sorted = sorted(history, key=lambda x: x["timestamp"], reverse=True)
        
        # Pokazuj tylko ostatnie 10
        for event in history_sorted[:10]:
            render_event_history_card(event)

def render_active_effects_badge(active_effects: list):
    """Renderuje badge z aktywnymi efektami wydarzeń"""
    
    from datetime import datetime
    
    st.markdown("### ✨ Aktywne Efekty Wydarzenia")
    
    for effect in active_effects:
        effect_type = effect.get("type")
        expires = effect.get("expires")
        hours_left = 0
        
        # Oblicz pozostały czas
        if expires:
            expires_dt = datetime.strptime(expires, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_left = expires_dt - now
            hours_left = int(time_left.total_seconds() / 3600)
            
            if hours_left < 0:
                continue  # Pomiń wygasłe
        
        # Ustal emoji i opis w zależności od typu
        if effect_type == "capacity_boost":
            emoji = "🎓"
            title = f"+{effect['value']} pojemności"
            bg_color = "#f0fdf4"
            border_color = "#10b981"
            time_text = f"Wygasa za: {hours_left}h"
        elif effect_type == "capacity_penalty":
            emoji = "🤒"
            title = f"{effect['value']} pojemności"
            bg_color = "#fef2f2"
            border_color = "#ef4444"
            time_text = f"Wygasa za: {hours_left}h"
        elif effect_type == "next_contract_bonus":
            emoji = "🤝"
            title = f"+{int((effect['multiplier'] - 1) * 100)}% nagrody za następny kontrakt"
            bg_color = "#fffbeb"
            border_color = "#f59e0b"
            time_text = "Jednorazowy bonus"
        else:
            continue
        
        st.markdown(f"""
        <div style='border-left: 5px solid {border_color}; 
                    background: {bg_color};
                    padding: 12px; 
                    margin: 8px 0; 
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    gap: 12px;'>
            <span style='font-size: 24px;'>{emoji}</span>
            <div style='flex: 1;'>
                <strong>{title}</strong><br>
                <small style='color: #666;'>{time_text}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_latest_event_card(event: dict):
    """Renderuje małą kartę z najnowszym zdarzeniem na Dashboard"""
    
    # Kolor w zależności od typu
    if event["type"] == "positive":
        border_color = "#10b981"
        bg_color = "#f0fdf4"
    elif event["type"] == "negative":
        border_color = "#ef4444"
        bg_color = "#fef2f2"
    else:  # neutral
        border_color = "#f59e0b"
        bg_color = "#fffbeb"
    
    st.markdown(f"""
    <div style='border-left: 5px solid {border_color}; 
                background: {bg_color};
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 8px;'>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <span style='font-size: 32px;'>{event['emoji']}</span>
            <div>
                <h4 style='margin: 0;'>Ostatnie Zdarzenie: {event['title']}</h4>
                <p style='margin: 5px 0 0 0; color: #666; font-size: 14px;'>{event['timestamp']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"💬 {event['description']}")
    
    # Dodaj informację o dotkniętym kontrakcie
    if event.get("affected_contract"):
        st.caption(f"⚠️ Dotknięty kontrakt: **{event['affected_contract']}**")
    
    # Dodaj informację o przedłużonych kontraktach
    if event.get("affected_contracts_extended"):
        contracts_list = ", ".join(event["affected_contracts_extended"])
        st.caption(f"✨ Przedłużone kontrakty: **{contracts_list}**")

def render_event_choice_modal(event_id: str, event_data: dict, username: str, user_data: dict):
    """Renderuje modal z wyborem dla neutralnego zdarzenia"""
    
    from utils.business_game_events import apply_event_effects
    
    st.markdown("---")
    st.markdown("## ⚖️ Wymagana Decyzja!")
    
    st.markdown(f"""
    <div style='border: 2px solid #f59e0b; 
                background: #fffbeb;
                padding: 20px; 
                border-radius: 10px;
                text-align: center;'>
        <div style='font-size: 48px; margin-bottom: 10px;'>{event_data['emoji']}</div>
        <h2 style='margin: 0;'>{event_data['title']}</h2>
        <p style='margin: 10px 0; color: #666;'>{event_data['description']}</p>
        <p style='margin: 10px 0; font-style: italic; color: #999;'>"{event_data['flavor_text']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🤔 Co robisz?")
    
    # Wyświetl opcje
    cols = st.columns(len(event_data["choices"]))
    
    for idx, (col, choice) in enumerate(zip(cols, event_data["choices"])):
        with col:
            if st.button(choice["text"], key=f"choice_{idx}", type="primary" if idx == 0 else "secondary", use_container_width=True):
                # Aplikuj wybór
                user_data = apply_event_effects(event_id, event_data, idx, user_data)
                save_user_data(username, user_data)
                
                # Usuń pending
                del st.session_state["pending_event"]
                
                st.success(f"✅ Wybrano: {choice['text']}")
                st.rerun()

def render_event_history_card(event: dict):
    """Renderuje kartę zdarzenia w historii"""
    
    # Kolor w zależności od typu
    if event["type"] == "positive":
        border_color = "#10b981"
        icon = "🎉"
    elif event["type"] == "negative":
        border_color = "#ef4444"
        icon = "💥"
    else:
        border_color = "#f59e0b"
        icon = "⚖️"
    
    with st.expander(f"{event['emoji']} {event['title']} - {event['timestamp']}"):
        st.markdown(f"**Opis:** {event['description']}")
        
        if event.get("choice"):
            st.markdown(f"**Twój wybór:** {event['choice']}")
        
        # Informacja o dotkniętym kontrakcie
        if event.get("affected_contract"):
            st.warning(f"⚠️ **Dotknięty kontrakt:** {event['affected_contract']}")
        
        # Informacja o przedłużonych kontraktach
        if event.get("affected_contracts_extended"):
            contracts_list = ", ".join(event["affected_contracts_extended"])
            st.success(f"✨ **Przedłużone kontrakty:** {contracts_list}")
        
        # Efekty
        effects = event.get("effects", {})
        if effects:
            st.markdown("**Efekty:**")
            for key, value in effects.items():
                if key == "coins":
                    st.markdown(f"- 💰 Monety: {value:+d}")
                elif key == "reputation":
                    st.markdown(f"- 📈 Reputacja: {value:+d}")
                elif key == "capacity_boost":
                    st.markdown(f"- 📊 Pojemność: +{value} (na {effects.get('duration_days', 1)} dni)")
                elif key == "capacity_penalty":
                    st.markdown(f"- 📉 Pojemność: {value} (na {effects.get('duration_days', 1)} dni)")
                elif key == "deadline_reduction":
                    st.markdown(f"- ⏰ Deadline: {value} dzień")
                elif key == "deadline_extension":
                    st.markdown(f"- ✨ Deadline: +{value} dzień (dla wszystkich aktywnych)")
                elif key == "next_contract_bonus":
                    bonus_percent = int((value - 1) * 100)
                    st.markdown(f"- 🌟 Bonus: +{bonus_percent}% do następnego kontraktu")

# =============================================================================
# TAB 6: RANKINGI
# =============================================================================

def show_rankings_tab(username, user_data):
    """Zakładka Rankingi"""
    bg_data = user_data["business_game"]
    
    st.subheader("🏆 Rankingi Firm Konsultingowych")
    
    # Aktualizuj overall score
    bg_data = update_user_ranking(bg_data)
    user_data["business_game"] = bg_data
    
    # Selector
    ranking_type = st.selectbox(
        "Wybierz ranking:",
        ["🏆 Ogólny (Overall Score)", "💰 Przychody", "⭐ Jakość (średnia ocena)", "🔥 Produktywność (30 dni)"],
        key="rankings_type_selector"
    )
    
    st.markdown("---")
    
    # Twoja pozycja (highlight)
    render_user_rank_highlight(bg_data, ranking_type)
    
    st.markdown("---")
    
    # Pobierz PRAWDZIWE dane wszystkich użytkowników
    from data.users import load_user_data
    all_users = load_user_data()
    
    # Zbierz firmy z business_game
    all_firms = []
    
    # Określ typ rankingu (label i suffix)
    if ranking_type == "💰 Przychody":
        score_label = "Przychody"
        score_suffix = " 💰"
    elif ranking_type == "⭐ Jakość (średnia ocena)":
        score_label = "Średnia ocena"
        score_suffix = " ⭐"
    elif ranking_type == "🔥 Produktywność (30 dni)":
        score_label = "Kontrakty (30 dni)"
        score_suffix = ""
    else:  # Overall Score (domyślnie)
        score_label = "Overall Score"
        score_suffix = ""
    
    for user, data in all_users.items():
        if data.get("business_game"):
            bg = data["business_game"]
            
            # WAŻNE: Przelicz overall_score dla każdego użytkownika (może być nieaktualny)
            from utils.business_game import calculate_overall_score
            bg["ranking"]["overall_score"] = calculate_overall_score(bg)
            
            # WAŻNE: Przelicz statystyki 30-dniowe na podstawie ukończonych kontraktów
            from datetime import datetime, timedelta
            now = datetime.now()
            thirty_days_ago = now - timedelta(days=30)
            
            contracts_30d = 0
            revenue_30d = 0
            ratings_30d = []
            
            for contract in bg.get("contracts", {}).get("completed", []):
                completed_date_str = contract.get("completed_date")
                if completed_date_str:
                    try:
                        completed_date = datetime.strptime(completed_date_str, "%Y-%m-%d %H:%M:%S")
                        if completed_date >= thirty_days_ago:
                            contracts_30d += 1
                            revenue_30d += contract.get("reward", {}).get("coins", 0)
                            rating = contract.get("rating", 0)
                            if rating > 0:
                                ratings_30d.append(rating)
                    except:
                        pass  # Ignoruj błędy parsowania dat
            
            # Aktualizuj statystyki 30-dniowe
            bg["stats"]["last_30_days"]["contracts"] = contracts_30d
            bg["stats"]["last_30_days"]["revenue"] = revenue_30d
            bg["stats"]["last_30_days"]["avg_rating"] = round(sum(ratings_30d) / len(ratings_30d), 2) if ratings_30d else 0.0
            
            firm = bg.get("firm", {})
            stats = bg.get("stats", {})
            ranking = bg.get("ranking", {})
            
            # Oblicz score w zależności od typu rankingu
            if ranking_type == "💰 Przychody":
                score = stats.get("total_revenue", 0)
            elif ranking_type == "⭐ Jakość (średnia ocena)":
                score = stats.get("avg_rating", 0.0)
            elif ranking_type == "🔥 Produktywność (30 dni)":
                score = stats.get("last_30_days", {}).get("contracts", 0)
            else:  # Overall Score
                score = ranking.get("overall_score", 0)
            
            all_firms.append({
                "name": firm.get("name", f"{user}'s Consulting"),
                "username": user,
                "score": score,
                "is_user": user == username
            })
    
    # Sortuj malejąco
    all_firms.sort(key=lambda x: x["score"], reverse=True)
    
    # Informacja o rankingach
    total_active = len(all_firms)
    user_rank = next((i+1 for i, f in enumerate(all_firms) if f["is_user"]), None)
    
    st.info(f"""
    ℹ️ **Ranking aktywnych firm: {total_active}**
    
    {"🎉 Gratulacje! Jesteś na pozycji #" + str(user_rank) + "!" if user_rank else "Ukończ pierwszy kontrakt, aby pojawić się w rankingu!"}
    
    **Jak działają rankingi:**
    - Aktualizacja na żywo (przy każdym odświeżeniu)
    - Uwzględniamy: przychody, jakość pracy, reputację, poziom firmy
    - Rywalizuj z {total_active-1} innymi firmami!
    """)
    
    # Tytuł rankingu
    st.markdown(f"### 🥇 TOP {min(10, total_active)} - {ranking_type}")
    
    # Pokaż TOP 10 + Twoją firmę (jeśli poza TOP 10)
    top_10 = all_firms[:10]
    
    # Dodaj użytkownika jeśli jest poza TOP 10
    user_firm = next((f for f in all_firms if f["is_user"]), None)
    if user_firm and user_firm not in top_10:
        top_10.append(user_firm)
    
    for idx, firm in enumerate(top_10, 1):
        # Znajdź prawdziwą pozycję w pełnym rankingu
        actual_rank = next((i+1 for i, f in enumerate(all_firms) if f["username"] == firm["username"]), idx)
        medal = "🥇" if actual_rank == 1 else "🥈" if actual_rank == 2 else "🥉" if actual_rank == 3 else f"#{actual_rank}"
        
        # Format score zależnie od typu (liczba całkowita vs z przecinkiem)
        if ranking_type == "⭐ Jakość (średnia ocena)":
            score_display = f"{firm['score']:.1f}"
        else:
            score_display = f"{firm['score']:.0f}"
        
        if firm["is_user"]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <h3 style='margin:0;'>{medal} {firm['name']} (Ty!)</h3>
                <p style='margin:5px 0 0 0;'>{score_label}: {score_display}{score_suffix}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <h4 style='margin:0;'>{medal} {firm['name']}</h4>
                <p style='margin:5px 0 0 0; color: #666;'>{score_label}: {score_display}{score_suffix}</p>
            </div>
            """, unsafe_allow_html=True)

def render_user_rank_highlight(bg_data, ranking_type):
    """Renderuje highlight pozycji użytkownika"""
    
    firm = bg_data["firm"]
    stats = bg_data["stats"]
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 20px; border-radius: 10px;'>
        <h3>🏢 Twoja Firma: {firm['name']}</h3>
        <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 15px;'>
            <div>
                <strong>Overall Score</strong><br>
                {bg_data['ranking']['overall_score']:.0f}
            </div>
            <div>
                <strong>Przychody</strong><br>
                {stats['total_revenue']:,} 💰
            </div>
            <div>
                <strong>Średnia ocena</strong><br>
                {stats['avg_rating']:.1f}⭐
            </div>
            <div>
                <strong>Kontrakty</strong><br>
                {stats['contracts_completed']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def save_user_data(username, user_data):
    """Zapisuje dane użytkownika"""
    from data.users import load_user_data, save_user_data as save_all_users
    all_users = load_user_data()
    all_users[username] = user_data
    save_all_users(all_users)
