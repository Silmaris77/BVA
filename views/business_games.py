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
    tabs = st.tabs(["🏢 Dashboard", "💼 Rynek Kontraktów", "👥 Pracownicy", "📜 Historia", "🏆 Rankingi"])
    
    with tabs[0]:
        show_dashboard_tab(username, user_data)
    
    with tabs[1]:
        show_contracts_tab(username, user_data)
    
    with tabs[2]:
        show_employees_tab(username, user_data)
    
    with tabs[3]:
        show_history_tab(username, user_data)
    
    with tabs[4]:
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
        
        # Header (tylko stylowanie ramki)
        st.markdown(f"""
        <div style='border: 2px solid #667eea; border-radius: 10px; 
                    padding: 15px; margin: 10px 0; background: #f8f9fa;'>
            <h4>{contract['emoji']} {contract['tytul']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
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
            st.markdown(f"**Trudność:** {'⭐' * contract['trudnosc']}")
            st.markdown(f"**Minimalnie:** {contract.get('min_slow', 300)} słów")
            
            st.markdown("---")
            st.subheader("✍️ Twoje rozwiązanie")
            
            solution_key = f"solution_{contract['id']}"
            solution = st.text_area(
                "Przygotuj kompleksowe rozwiązanie zgodnie z wymaganiami:",
                value=contract.get("solution", ""),
                height=400,
                key=solution_key,
                placeholder="Zacznij pisać swoje rozwiązanie tutaj..."
            )
            
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
                        # Prześlij rozwiązanie
                        updated_user_data, success, message = submit_contract_solution(
                            user_data, contract['id'], solution
                        )
                        
                        if success:
                            user_data.update(updated_user_data)
                            save_user_data(username, user_data)
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
            ["Wszystkie", "⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
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
    
    with st.container():
        # Header z ramką (tylko stylowanie, bez treści kontraktu)
        st.markdown(f"""
        <div style='border: 2px solid #667eea; border-radius: 10px; 
                    padding: 20px; margin: 10px 0; background: white;'>
            <h3>{contract['emoji']} {contract['tytul']}</h3>
            <p><strong>Klient:</strong> {contract['klient']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Opis - zwykły Markdown (renderowany przez Streamlit, nie w HTML)
        st.markdown(f"*{contract['opis'][:200]}...*")
        
        # Metryki w kolumnach
        col_reward, col_time, col_diff = st.columns(3)
        with col_reward:
            st.markdown(f"**💰 Nagroda:** {contract['nagroda_base']}-{contract['nagroda_5star']} monet")
        with col_time:
            st.markdown(f"**⏱️ Czas:** {contract['czas_realizacji_dni']} dni")
        with col_diff:
            st.markdown(f"**Trudność:** {'⭐' * contract['trudnosc']}")
        
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
# TAB 5: RANKINGI
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
    
    # Informacja o rankingach (mock data dla MVP)
    st.info(f"""
    ℹ️ **Rankingi będą dostępne, gdy więcej użytkowników będzie aktywnych w Business Games.**
    
    Obecnie w systemie jest tylko Twoja firma. Zachęć innych do dołączenia!
    
    **Jak działają rankingi:**
    - Aktualizacja co 1 godzinę
    - Uwzględniamy: przychody, jakość pracy, reputację, poziom firmy
    - Brak barier wejścia - każdy może się ścigać od pierwszego kontraktu!
    """)
    
    # Mock ranking data
    st.markdown("### 🥇 TOP 10 (Demo)")
    
    # Przygotuj dane w zależności od typu rankingu
    if ranking_type == "💰 Przychody":
        user_score = bg_data["stats"]["total_revenue"]
        demo_firms = [
            {"name": bg_data["firm"]["name"], "score": user_score, "is_user": True},
            {"name": "Startup Consulting", "score": 250, "is_user": False},
            {"name": "NewBiz Solutions", "score": 180, "is_user": False},
            {"name": "Fresh Leaders", "score": 120, "is_user": False},
            {"name": "Junior Advisors", "score": 80, "is_user": False},
            {"name": "Beginning Consultants", "score": 40, "is_user": False},
        ]
        score_label = "Przychody"
        score_suffix = " 💰"
    elif ranking_type == "⭐ Jakość (średnia ocena)":
        user_score = bg_data["stats"]["avg_rating"]
        demo_firms = [
            {"name": bg_data["firm"]["name"], "score": user_score, "is_user": True},
            {"name": "Startup Consulting", "score": 4.2, "is_user": False},
            {"name": "NewBiz Solutions", "score": 3.8, "is_user": False},
            {"name": "Fresh Leaders", "score": 3.5, "is_user": False},
            {"name": "Junior Advisors", "score": 3.0, "is_user": False},
            {"name": "Beginning Consultants", "score": 2.5, "is_user": False},
        ]
        score_label = "Średnia ocena"
        score_suffix = " ⭐"
    elif ranking_type == "🔥 Produktywność (30 dni)":
        user_score = bg_data["stats"].get("last_30_days", {}).get("contracts", 0)
        demo_firms = [
            {"name": bg_data["firm"]["name"], "score": user_score, "is_user": True},
            {"name": "Startup Consulting", "score": 8, "is_user": False},
            {"name": "NewBiz Solutions", "score": 6, "is_user": False},
            {"name": "Fresh Leaders", "score": 4, "is_user": False},
            {"name": "Junior Advisors", "score": 2, "is_user": False},
            {"name": "Beginning Consultants", "score": 1, "is_user": False},
        ]
        score_label = "Kontrakty (30 dni)"
        score_suffix = ""
    else:  # Overall Score (domyślnie)
        user_score = bg_data["ranking"]["overall_score"]
        demo_firms = [
            {"name": bg_data["firm"]["name"], "score": user_score, "is_user": True},
            {"name": "Startup Consulting", "score": 85, "is_user": False},
            {"name": "NewBiz Solutions", "score": 62, "is_user": False},
            {"name": "Fresh Leaders", "score": 45, "is_user": False},
            {"name": "Junior Advisors", "score": 28, "is_user": False},
            {"name": "Beginning Consultants", "score": 12, "is_user": False},
        ]
        score_label = "Overall Score"
        score_suffix = ""
    
    demo_firms.sort(key=lambda x: x["score"], reverse=True)
    
    # Pokaż wszystkie firmy (nie tylko top 5)
    for idx, firm in enumerate(demo_firms, 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
        
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
