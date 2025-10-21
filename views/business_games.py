"""
Business Games - UI
Widok główny z zakładkami: Dashboard, Rynek Kontraktów, Pracownicy, Rankingi
"""

import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go

from data.business_data import FIRM_LEVELS, EMPLOYEE_TYPES, GAME_CONFIG, FIRM_LOGOS, OFFICE_TYPES, OFFICE_UPGRADE_PATH
from utils.business_game import (
    initialize_business_game, refresh_contract_pool, accept_contract,
    submit_contract_solution, hire_employee, fire_employee,
    calculate_daily_costs, calculate_total_daily_costs, get_firm_summary, get_revenue_chart_data,
    get_category_distribution, calculate_overall_score, can_accept_contract,
    can_hire_employee, update_user_ranking
)
from utils.components import zen_header
from utils.material3_components import apply_material3_theme
from utils.scroll_utils import scroll_to_top

# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def play_coin_sound():
    """Odtwarza dźwięk brzęczących monet przy nagrodzie"""
    # Prosty dźwięk za pomocą HTML audio z CDN
    # Użyj darmowego dźwięku monet z freesound.org lub podobnego
    st.markdown(
        """
        <audio autoplay>
            <source src="https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

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
    
    # MIGRACJA: Dodaj brakujące transakcje dla starych wydarzeń z monetami
    from utils.business_game import migrate_event_transactions
    user_data, migrated_count = migrate_event_transactions(user_data)
    if migrated_count > 0:
        # Zapisz zmigrowane dane (cicho, bez komunikatu dla użytkownika)
        save_user_data(username, user_data)
        bg_data = user_data["business_game"]  # Odśwież referencję
    
    # Odśwież pulę kontraktów
    bg_data = refresh_contract_pool(bg_data)
    user_data["business_game"] = bg_data
    
    # Nagłówek z podsumowaniem firmy
    render_header(user_data)
    
    st.markdown("---")
    
    # Główne zakładki
    tabs = st.tabs(["📖 Instrukcja", "🏢 Dashboard", "💼 Rynek Kontraktów", "🏢 Biuro i Pracownicy", "📊 Raporty Finansowe", "📜 Historia & Wydarzenia", "🏆 Rankingi"])
    
    with tabs[0]:
        show_instructions_tab()
    
    with tabs[1]:
        show_dashboard_tab(username, user_data)
    
    with tabs[2]:
        show_contracts_tab(username, user_data)
    
    with tabs[3]:
        show_employees_tab(username, user_data)
    
    with tabs[4]:
        show_financial_reports_tab(username, user_data)
    
    with tabs[5]:
        show_history_tab(username, user_data)
    
    with tabs[6]:
        show_rankings_tab(username, user_data)

# =============================================================================
# NAGŁÓWEK
# =============================================================================

def render_header(user_data):
    """Renderuje nagłówek z profesjonalnymi kartami w stylu gamifikacji"""
    bg_data = user_data["business_game"]
    firm = bg_data["firm"]
    level_info = FIRM_LEVELS[firm["level"]]
    
    # BACKWARD COMPATIBILITY: Dodaj logo jeśli nie istnieje
    if "logo" not in firm:
        firm["logo"] = level_info['ikona']  # Użyj ikony poziomu jako domyślnej
    
    # CSS dla profesjonalnych kart z efektami
    st.markdown("""
    <style>
    .game-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
    }
    .game-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    .firm-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .firm-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(102, 126, 234, 0.6);
    }
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
        border-left: 4px solid;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }
    .stat-card.gold { border-left-color: #f59e0b; }
    .stat-card.purple { border-left-color: #8b5cf6; }
    .stat-card.blue { border-left-color: #3b82f6; }
    .stat-card.green { border-left-color: #10b981; }
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        margin: 8px 0;
        color: #1e293b;
    }
    .stat-label {
        font-size: 13px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # JEDEN WIERSZ: Logo+Nazwa | Saldo | Reputacja | Rating
    summary = get_firm_summary(user_data)
    
    col_firm, col1, col2, col3 = st.columns([1.5, 1, 1, 1])
    
    with col_firm:
        st.markdown(f"""
        <div class='firm-card' style='padding: 20px; display: flex; align-items: center; gap: 16px; min-height: 140px; height: 100%;'>
            <div style='font-size: 48px;'>{firm['logo']}</div>
            <div style='flex: 1;'>
                <h2 style='margin:0; font-size: 22px; font-weight: 700;'>{firm['name']}</h2>
                <p style='margin:4px 0 0 0; opacity:0.9; font-size: 14px;'>
                    Poziom {firm['level']}: {level_info['nazwa']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card gold'>
            <div class='stat-label'>💰 Saldo</div>
            <div class='stat-value'>{user_data.get('degencoins', 0):,}</div>
            <div style='font-size: 12px; color: #64748b;'>monet</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Oblicz następny próg reputacji
        current_rep = firm['reputation']
        next_level_rep = None
        if firm['level'] == 1:
            next_level_rep = GAME_CONFIG["reputation_to_level_2"]
            next_level_name = "Boutique Consulting"
        elif firm['level'] == 2:
            next_level_rep = GAME_CONFIG["reputation_to_level_3"]
            next_level_name = "CIQ Advisory Group"
        elif firm['level'] == 3:
            next_level_rep = GAME_CONFIG["reputation_to_level_4"]
            next_level_name = "Global CIQ Partners"
        else:
            next_level_rep = None
            next_level_name = "MAX"
        
        progress_info = ""
        if next_level_rep:
            progress_pct = min(100, (current_rep / next_level_rep) * 100)
            progress_info = f"<div style='margin-top: 8px;'><div style='background: #e2e8f0; border-radius: 4px; height: 4px; overflow: hidden;'><div style='background: #8b5cf6; height: 100%; width: {progress_pct}%;'></div></div><div style='font-size: 10px; color: #64748b; margin-top: 2px;'>Do {next_level_name}: {next_level_rep}</div></div>"
        
        st.markdown(f"""
        <div class='stat-card purple'>
            <div class='stat-label'>📈 Reputacja</div>
            <div class='stat-value'>{current_rep}</div>
            <div style='font-size: 12px; color: #64748b;'>punktów</div>
            {progress_info}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Rating - używamy oficjalnej funkcji z business_game
        overall_score = calculate_overall_score(bg_data)
        st.markdown(f"""
        <div class='stat-card blue'>
            <div class='stat-label'>🏆 Rating</div>
            <div class='stat-value'>{overall_score:,.0f}</div>
            <div style='font-size: 12px; color: #64748b;'>punktów</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# WYKRES FINANSOWY
# =============================================================================

def create_financial_chart(bg_data, period=7, cumulative=False):
    """Tworzy wykres finansowy z przychodami, kosztami i zyskiem
    
    Args:
        bg_data: business_game data
        period: liczba dni do wyświetlenia (7, 14, 30)
        cumulative: czy pokazać wartości skumulowane
    
    Returns:
        Plotly figure object
    """
    from datetime import datetime, timedelta
    import plotly.graph_objects as go
    import pandas as pd
    
    # Pobierz transakcje
    transactions = bg_data.get("history", {}).get("transactions", [])
    
    if not transactions:
        # Pusty wykres jeśli brak danych
        fig = go.Figure()
        fig.add_annotation(
            text="Brak danych finansowych<br>Ukończ pierwszy kontrakt!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#64748b")
        )
        fig.update_layout(
            height=300,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white'
        )
        return fig
    
    # Przygotuj dane dzienne
    daily_data = {}
    for trans in transactions:
        try:
            date = trans["timestamp"][:10]  # YYYY-MM-DD
            if date not in daily_data:
                daily_data[date] = {"revenue": 0, "costs": 0}
            
            trans_type = trans.get("type", "")
            amount = trans.get("amount", 0)  # Bezpieczne pobieranie amount
            
            if trans_type in ["contract_reward", "event_reward"]:
                # Przychody z kontraktów i pozytywnych wydarzeń
                daily_data[date]["revenue"] += amount
            elif trans_type in ["daily_costs", "employee_hired", "employee_hire", "event_cost", "office_rent", "office_upgrade"]:
                # Koszty: pracownicy + biuro + negatywne wydarzenia
                daily_data[date]["costs"] += abs(amount)
            # employee_fired nie wpływa na wykres (amount = 0), ale jest w historii
        except Exception as e:
            continue
    
    # Stwórz range dat dla wybranego okresu
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period - 1)
    
    dates = []
    revenues = []
    costs = []
    
    for i in range(period):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date)
        
        day_data = daily_data.get(date, {"revenue": 0, "costs": 0})
        revenues.append(day_data["revenue"])
        costs.append(day_data["costs"])
    
    # Oblicz zysk
    profits = [r - c for r, c in zip(revenues, costs)]
    
    # Jeśli cumulative, oblicz wartości narastające
    if cumulative:
        revenues_cum = []
        costs_cum = []
        profits_cum = []
        
        rev_sum = 0
        cost_sum = 0
        
        for r, c in zip(revenues, costs):
            rev_sum += r
            cost_sum += c
            revenues_cum.append(rev_sum)
            costs_cum.append(cost_sum)
            profits_cum.append(rev_sum - cost_sum)
        
        revenues = revenues_cum
        costs = costs_cum
        profits = profits_cum
    
    # Formatuj daty (krótko)
    dates_formatted = [datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m") for d in dates]
    
    # Twórz wykres
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates_formatted,
        y=revenues,
        name='Przychody',
        mode='lines+markers',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates_formatted,
        y=costs,
        name='Koszty',
        mode='lines+markers',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(239, 68, 68, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates_formatted,
        y=profits,
        name='Zysk',
        mode='lines+markers',
        line=dict(color='#8b5cf6', width=3, dash='dot'),
        marker=dict(size=8)
    ))
    
    # Layout
    title_text = f"{'Skumulowane ' if cumulative else ''}Finanse (ostatnie {period} dni)"
    
    fig.update_layout(
        title=dict(text=title_text, font=dict(size=14, color='#64748b')),
        xaxis=dict(
            title="",
            showgrid=True,
            gridcolor='#f1f5f9'
        ),
        yaxis=dict(
            title="Monety 💰",
            showgrid=True,
            gridcolor='#f1f5f9'
        ),
        height=300,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=20, t=60, b=40)
    )
    
    return fig

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
    
    st.markdown("---")
    # =============================================================================
    # SEKCJA DZIENNEGO WYDARZENIA - RAZ NA DOBĘ
    # =============================================================================
    
    from utils.business_game_events import get_random_event, apply_event_effects, get_latest_event
    from datetime import datetime, timedelta
    
    # Sprawdź czy dzisiaj było już losowanie
    last_roll = bg_data.get("events", {}).get("last_roll")
    today = datetime.now().strftime("%Y-%m-%d")
    should_roll = True
    
    if last_roll:
        last_roll_date = last_roll.split(" ")[0]  # Pobierz tylko datę (bez godziny)
        if last_roll_date == today:
            should_roll = False
    
    # Jeśli jeszcze dziś nie było losowania - WYLOSUJ TERAZ
    if should_roll:
        event_result = get_random_event(bg_data, user_data.get("degencoins", 0))
        
        if event_result:
            event_id, event_data = event_result
            
            # Sprawdź czy wymaga wyboru
            if event_data["type"] == "neutral" and "choices" in event_data:
                # Zapisz w session_state i wyświetl modal
                st.session_state["pending_event"] = (event_id, event_data)
            else:
                # Bezpośrednio aplikuj (positive i negative)
                user_data = apply_event_effects(event_id, event_data, None, user_data)
                save_user_data(username, user_data)
                
                if event_data["type"] == "positive":
                    st.balloons()
        
        # Przeładuj bg_data po zapisie
        bg_data = user_data["business_game"]
        last_roll = bg_data.get("events", {}).get("last_roll")
    
    # Pending event (jeśli neutralne wymaga wyboru - blocking modal)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data)
    
    st.markdown("---")
    
    # Pobierz podsumowanie
    summary = get_firm_summary(user_data)
    
    # Dwie kolumny: Aktywne kontrakty i Wydarzenie
    col_contracts, col_event = st.columns([2, 1])
    
    # LEWA KOLUMNA - AKTYWNE KONTRAKTY
    with col_contracts:
        st.subheader("📋 Aktywne Kontrakty")
        
        # Lista aktywnych kontraktów
        active_contracts = bg_data["contracts"]["active"]
        
        if len(active_contracts) == 0:
            st.info("Brak aktywnych kontraktów. Przejdź do zakładki 'Rynek Kontraktów' aby przyjąć nowe zlecenie!")
        else:
            for contract in active_contracts:
                render_active_contract_card(contract, username, user_data, bg_data)
    
    # PRAWA KOLUMNA - DZISIEJSZE WYDARZENIE
    with col_event:
        st.subheader("🎲 Dzisiejsze Wydarzenie")
        
        # Pokaż dzisiejsze wydarzenie (jeśli jest)
        latest_event = get_latest_event(bg_data)
        if latest_event:
            # Sprawdź czy wydarzenie jest z dzisiaj
            event_date = latest_event.get("timestamp", "").split(" ")[0]
            if event_date == today:
                show_active_event_card(latest_event)
            else:
                st.info("Dzisiaj nie ma żadnego wydarzenia.")
        else:
            st.info("Dzisiaj nie ma żadnego wydarzenia.")
    
    st.markdown("---")
    
    # NOWY WYKRES FINANSOWY z kontrolkami
    st.subheader("� Analiza Finansowa")
    
    # Kontrolki
    col_chart1, col_chart2 = st.columns([3, 1])
    
    with col_chart2:
        st.markdown("**Okres:**")
        period = st.radio(
            "Wybierz okres",
            options=[7, 14, 30],
            format_func=lambda x: f"{x} dni",
            key="financial_chart_period",
            label_visibility="collapsed"
        )
        
        cumulative = st.checkbox(
            "📈 Wartość skumulowana",
            value=False,
            key="financial_chart_cumulative"
        )
    
    with col_chart1:
        # Generuj i wyświetl wykres
        fig = create_financial_chart(bg_data, period=period, cumulative=cumulative)
        st.plotly_chart(fig, use_container_width=True)
        
        # Podsumowanie sum
        if cumulative:
            transactions = bg_data.get("history", {}).get("transactions", [])
            # Przychody: kontrakty + pozytywne wydarzenia
            total_rev = sum(t.get("amount", 0) for t in transactions if t.get("type") in ["contract_reward", "event_reward"])
            # Koszty: pracownicy + negatywne wydarzenia
            total_cost = sum(abs(t.get("amount", 0)) for t in transactions if t.get("type") in ["daily_costs", "employee_hired", "employee_hire", "event_cost"])
            total_profit = total_rev - total_cost
            
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 12px; border-radius: 8px; margin-top: 8px;'>
                <div style='display: flex; justify-content: space-around; font-size: 14px;'>
                    <div><strong>📊 Suma przychodów:</strong> {total_rev:,} 💰</div>
                    <div><strong>💸 Suma kosztów:</strong> {total_cost:,} 💰</div>
                    <div><strong>💎 Suma zysku:</strong> <span style='color: {"#10b981" if total_profit >= 0 else "#ef4444"}'>{total_profit:,} 💰</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("⚙️ Ustawienia Firmy")
    
    col_settings1, col_settings2 = st.columns(2)
    
    with col_settings1:
        with st.expander("✏️ Zmień nazwę firmy"):
            new_name = st.text_input("Nowa nazwa firmy", value=bg_data["firm"]["name"], key="dashboard_firm_name_input")
            if st.button("💾 Zapisz nazwę", key="dashboard_save_firm_name"):
                bg_data["firm"]["name"] = new_name
                user_data["business_game"] = bg_data
                save_user_data(username, user_data)
                st.success("✅ Nazwa firmy zaktualizowana!")
                st.rerun()
    
    with col_settings2:
        with st.expander("🎨 Zmień logo firmy"):
            # Pokaż kategorie
            st.markdown("**Wybierz kategorię:**")
            categories = list(FIRM_LOGOS.keys())
            category_names = {
                "basic": "🏢 Budynki",
                "business": "💼 Biznes",
                "creative": "🎨 Kreatywne",
                "nature": "🌍 Natura",
                "tech": "💻 Technologia",
                "animals": "🦁 Zwierzęta"
            }
            
            selected_category = st.selectbox(
                "Kategoria:",
                categories,
                format_func=lambda x: category_names.get(x, x),
                key="logo_category"
            )
            
            # Wyświetl dostępne logo w gridzie
            st.markdown("**Wybierz logo:**")
            available_logos = FIRM_LOGOS[selected_category]["free"]
            
            # Grid 8 kolumn
            cols = st.columns(8)
            for idx, logo in enumerate(available_logos):
                with cols[idx % 8]:
                    if st.button(
                        logo,
                        key=f"logo_{selected_category}_{idx}",
                        help=f"Kliknij aby wybrać {logo}",
                        use_container_width=True
                    ):
                        bg_data["firm"]["logo"] = logo
                        user_data["business_game"] = bg_data
                        save_user_data(username, user_data)
                        st.success(f"✅ Logo zmienione na {logo}!")
                        st.rerun()
            
            # Podgląd aktualnego logo
            st.markdown("---")
            current_logo = bg_data["firm"].get("logo", "🏢")
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; color: white;'>
                <div style='font-size: 64px; margin-bottom: 8px;'>{current_logo}</div>
                <p style='margin: 0; opacity: 0.9;'>Aktualne logo</p>
            </div>
            """, unsafe_allow_html=True)

def render_active_contract_card(contract, username, user_data, bg_data):
    """Renderuje profesjonalną kartę aktywnego kontraktu w stylu game UI"""
    
    with st.container():
        # Oblicz pozostały czas
        deadline = datetime.strptime(contract["deadline"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        time_left = deadline - now
        hours_left = int(time_left.total_seconds() / 3600)
        
        # Kolory i ikony dla deadline
        if hours_left > 24:
            deadline_status = "� Na czasie"
            deadline_bg = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
        elif hours_left > 6:
            deadline_status = "🟡 Kończy się"
            deadline_bg = "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"
        else:
            deadline_status = "🔴 Pilne!"
            deadline_bg = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
        
        # Sprawdź czy kontrakt był dotknięty zdarzeniem
        event_affected = contract.get("affected_by_event")
        
        # Ustal kolor akcent na podstawie typu zdarzenia
        if event_affected:
            if event_affected.get("type") == "deadline_reduction":
                accent_color = "#ef4444"
                glow = "0 0 20px rgba(239, 68, 68, 0.4)"
            elif event_affected.get("type") == "deadline_extension":
                accent_color = "#10b981"
                glow = "0 0 20px rgba(16, 185, 129, 0.4)"
            else:
                accent_color = "#667eea"
                glow = "0 0 20px rgba(102, 126, 234, 0.3)"
        else:
            accent_color = "#667eea"
            glow = "0 0 20px rgba(102, 126, 234, 0.3)"
        
        # Karta kontraktu - profesjonalny design
        difficulty_stars = "🔥" * contract['trudnosc']
        reward_min = contract['nagroda_base']
        reward_max = contract['nagroda_5star']
        
        # Render HTML card
        # Przygotuj HTML dla alertu wydarzenia (jeśli jest)
        event_alert_html = ""
        if event_affected:
            if event_affected.get("type") == "deadline_reduction":
                alert_bg = "#fef2f2"
                alert_border = "#ef4444"
                alert_icon = "⚠️"
                alert_text = f"<strong>Zdarzenie: {event_affected.get('event_title')}</strong><br>Deadline skrócony o {event_affected.get('days_reduced')} dzień!"
            elif event_affected.get("type") == "deadline_extension":
                alert_bg = "#f0fdf4"
                alert_border = "#10b981"
                alert_icon = "✨"
                alert_text = f"<strong>Zdarzenie: {event_affected.get('event_title')}</strong><br>Deadline przedłużony o {event_affected.get('days_added')} dzień!"
            elif event_affected.get("type") == "deadline_boost":
                alert_bg = "#f0f9ff"
                alert_border = "#3b82f6"
                alert_icon = "⚡"
                alert_text = f"<strong>Boost Energii: {event_affected.get('event_title')}</strong><br>Bonus +{event_affected.get('days_added')} dni do realizacji!"
            elif event_affected.get("type") == "renegotiation":
                alert_bg = "#eff6ff"
                alert_border = "#3b82f6"
                alert_icon = "🔄"
                reward_change = int((event_affected.get('reward_multiplier', 1.0) - 1) * 100)
                time_bonus = event_affected.get('time_bonus', 0)
                if reward_change < 0 and time_bonus > 0:
                    alert_text = f"<strong>Renegocjacja: {event_affected.get('event_title')}</strong><br>Nagroda {reward_change}%, ale +{time_bonus} dni na realizację!"
                else:
                    alert_text = f"<strong>Renegocjacja: {event_affected.get('event_title')}</strong><br>Zmieniono warunki kontraktu"
            else:
                alert_bg = "#f9fafb"
                alert_border = "#9ca3af"
                alert_icon = "ℹ️"
                alert_text = f"<strong>Wydarzenie aktywne</strong>"
            
            event_alert_html = f"""<div style="background: {alert_bg}; border-left: 4px solid {alert_border}; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;"><div style="font-size: 24px;">{alert_icon}</div><div style="font-size: 13px; color: #1e293b; line-height: 1.4;">{alert_text}</div></div>"""
        
        html_content = f"""<div style="background: white; border-radius: 20px; padding: 24px; margin: 16px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1), {glow}; border-left: 6px solid {accent_color}; transition: all 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
<div style="flex: 1;">
<div style="font-size: 32px; margin-bottom: 8px;">{contract['emoji']}</div>
<h3 style="margin: 0; color: #1e293b; font-size: 20px; font-weight: 700;">{contract['tytul']}</h3>
<p style="margin: 4px 0 0 0; color: #64748b; font-size: 14px;">Klient: <strong>{contract['klient']}</strong> • {contract['kategoria']}</p>
</div>
<div style="background: {deadline_bg}; color: white; padding: 12px 20px; border-radius: 12px; text-align: center; min-width: 120px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
<div style="font-size: 24px; font-weight: 700; margin-bottom: 4px;">{hours_left}h</div>
<div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">{deadline_status}</div>
</div>
</div>
<div style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
<div style="color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; font-weight: 600;">📝 Opis sytuacji</div>
<div style="color: #334155; font-size: 14px; line-height: 1.6;">{contract['opis']}</div>
</div>
{event_alert_html}
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e8f0;">
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Nagroda</div>
<div style="color: #f59e0b; font-size: 20px; font-weight: 700;">💰 {reward_min}-{reward_max}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Trudność</div>
<div style="font-size: 20px;">{difficulty_stars}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Reputacja</div>
<div style="color: #8b5cf6; font-size: 20px; font-weight: 700;">⭐ +{contract['reputacja']}</div>
</div>
</div>
</div>"""
        
        st.markdown(html_content, unsafe_allow_html=True)
        
        # ROZWIĄZANIE - expander
        with st.expander("✍️ Pracuj nad rozwiązaniem", expanded=True):
            # Wyświetl zadanie na górze
            st.markdown("### 🎯 Zadanie")
            st.markdown(contract['zadanie'])
            st.markdown("---")
            
            # ANTI-CHEAT: Zapisz czas rozpoczęcia pisania
            solution_start_key = f"solution_start_{contract['id']}"
            if solution_start_key not in st.session_state:
                st.session_state[solution_start_key] = datetime.now()
            
            # ANTI-CHEAT: Tracking paste events
            paste_events_key = f"paste_events_{contract['id']}"
            if paste_events_key not in st.session_state:
                st.session_state[paste_events_key] = []
            
            # Wprowadzanie rozwiązania - mówienie + pisanie
            st.markdown("### 📝 Twoje rozwiązanie")
            
            solution_key = f"solution_{contract['id']}"
            
            # Inicjalizuj klucze session_state
            transcription_key = f"transcription_{contract['id']}"
            transcription_version_key = f"transcription_version_{contract['id']}"
            if transcription_key not in st.session_state:
                st.session_state[transcription_key] = ""
            if transcription_version_key not in st.session_state:
                st.session_state[transcription_version_key] = 0
            
            st.markdown("**🎤 Nagraj** (wielokrotnie, jeśli chcesz) **lub ✍️ pisz bezpośrednio w polu poniżej:**")
            
            audio_data = st.audio_input(
                "🎤 Nagrywanie...",
                key=f"audio_input_{contract['id']}"
            )
            
            if audio_data is not None:
                import speech_recognition as sr
                import tempfile
                import os
                from pydub import AudioSegment
                
                with st.spinner("🤖 Rozpoznaję mowę..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                            tmp_file.write(audio_data.getvalue())
                            tmp_path = tmp_file.name
                        
                        wav_path = None
                        try:
                            audio = AudioSegment.from_file(tmp_path)
                            wav_path = tmp_path.replace(".wav", "_converted.wav")
                            audio.export(wav_path, format="wav")
                            
                            recognizer = sr.Recognizer()
                            with sr.AudioFile(wav_path) as source:
                                audio_data_sr = recognizer.record(source)
                                
                            transcription = recognizer.recognize_google(audio_data_sr, language="pl-PL")
                            
                            # Post-processing: Dodaj interpunkcję przez Gemini
                            try:
                                import google.generativeai as genai
                                
                                # Konfiguracja Gemini (z secrets.toml)
                                api_key = st.secrets["API_KEYS"]["gemini"]
                                genai.configure(api_key=api_key)
                                
                                # Dodaj interpunkcję - użyj najnowszego stabilnego modelu
                                model = genai.GenerativeModel("models/gemini-2.5-flash")
                                prompt = f"""Dodaj interpunkcję (kropki, przecinki, pytajniki, wykrzykniki) do poniższego tekstu.
Nie zmieniaj słów, tylko dodaj znaki interpunkcyjne. Zachowaj strukturę i podział na zdania.
Zwróć tylko poprawiony tekst, bez dodatkowych komentarzy.

Tekst do poprawy:
{transcription}"""
                                
                                response = model.generate_content(prompt)
                                transcription_with_punctuation = response.text.strip()
                                
                                st.info("🤖 Gemini dodał interpunkcję do transkrypcji.")
                                transcription = transcription_with_punctuation
                                
                            except Exception as gemini_error:
                                st.warning(f"⚠️ Nie udało się dodać interpunkcji: {str(gemini_error)}")
                                # Kontynuuj z transkrypcją bez interpunkcji
                            
                            # DOPISZ do istniejącego tekstu (zamiast nadpisywać)
                            existing_text = st.session_state.get(transcription_key, "")
                            if existing_text.strip():
                                # Jeśli jest już jakiś tekst, dodaj nową linię i dopisz
                                st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
                            else:
                                # Jeśli to pierwsze nagranie, po prostu zapisz
                                st.session_state[transcription_key] = transcription
                            
                            st.session_state[transcription_version_key] += 1
                            
                            st.success("✅ Transkrypcja zakończona! Tekst pojawił się w polu poniżej.")
                            
                        except sr.UnknownValueError:
                            st.error("❌ Nie udało się rozpoznać mowy. Spróbuj ponownie lub mów wyraźniej.")
                        except sr.RequestError as e:
                            st.error(f"❌ Błąd połączenia z usługą rozpoznawania mowy: {str(e)}")
                        finally:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
                            if wav_path and os.path.exists(wav_path):
                                os.unlink(wav_path)
                            
                    except Exception as e:
                        st.error(f"❌ Błąd podczas transkrypcji: {str(e)}")
                        st.info("💡 Możesz wprowadzić tekst ręcznie w polu poniżej.")
            
            # Dynamiczny klucz który zmienia się po transkrypcji
            text_area_key = f"{solution_key}_v{st.session_state[transcription_version_key]}"
            current_text = st.session_state.get(transcription_key, contract.get("solution", ""))
            
            solution = st.text_area(
                "📝 Możesz edytować transkrypcję lub pisać bezpośrednio:",
                value=current_text,
                height=400,
                key=text_area_key,
                placeholder="Nagrywaj wielokrotnie lub pisz bezpośrednio tutaj..."
            )
            
            # WAŻNE: Synchronizuj wartość z pola tekstowego do session_state
            # Żeby zapisać to co użytkownik napisał ręcznie przed nagraniem
            if text_area_key in st.session_state:
                st.session_state[transcription_key] = st.session_state[text_area_key]
            
            # ANTI-CHEAT: Dodaj JavaScript do śledzenia wklejania
            st.markdown(f"""
            <script>
            (function() {{
                const textarea = document.querySelector('textarea[aria-label="📝 Możesz edytować transkrypcję lub pisać bezpośrednio:"]');
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
                        updated_user_data, success, message, _ = submit_contract_solution(
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
                            
                            # 💰 Odtwórz dźwięk monet!
                            play_coin_sound()
                            
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
        # Podziel kontrakty na 2 kolumny
        col1, col2 = st.columns(2)
        
        for idx, contract in enumerate(available_contracts):
            # Naprzemienne kolumny
            with col1 if idx % 2 == 0 else col2:
                render_contract_card(contract, username, user_data, bg_data, can_accept)

def render_contract_card(contract, username, user_data, bg_data, can_accept_new):
    """Renderuje profesjonalną kartę dostępnego kontraktu - taki sam layout jak aktywne"""
    
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
        # Kolory i style - jednolite jak aktywne kontrakty
        if has_bonus:
            accent_color = "#fbbf24"
            glow = "0 0 24px rgba(251, 191, 36, 0.5)"
        else:
            accent_color = "#667eea"
            glow = "0 0 20px rgba(102, 126, 234, 0.3)"
        
        # Oblicz nagrody z bonusem
        reward_min = int(contract['nagroda_base'] * bonus_multiplier) if has_bonus else contract['nagroda_base']
        reward_max = int(contract['nagroda_5star'] * bonus_multiplier) if has_bonus else contract['nagroda_5star']
        
        # Difficulty
        difficulty_stars = "🔥" * contract['trudnosc']
        
        # Czas realizacji jako "deadline badge"
        deadline_days = contract['czas_realizacji_dni']
        deadline_bg = "linear-gradient(135deg, #10b981 0%, #059669 100%)"  # Zielony dla dostępnych
        
        # Alert bonusu (jeśli aktywny)
        bonus_alert_html = ""
        if has_bonus:
            bonus_percent = int((bonus_multiplier - 1) * 100)
            bonus_alert_html = f"""<div style="background: #fef3c7; border-left: 4px solid #fbbf24; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;"><div style="font-size: 24px;">🌟</div><div style="font-size: 13px; color: #1e293b; line-height: 1.4;"><strong>BONUS AKTYWNY: +{bonus_percent}%!</strong><br>Zwiększona nagroda za ten kontrakt</div></div>"""
        
        # Karta kontraktu - IDENTYCZNY LAYOUT jak aktywne
        html_content = f"""<div style="background: white; border-radius: 20px; padding: 24px; margin: 16px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1), {glow}; border-left: 6px solid {accent_color}; transition: all 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
<div style="flex: 1;">
<div style="font-size: 32px; margin-bottom: 8px;">{contract['emoji']}</div>
<h3 style="margin: 0; color: #1e293b; font-size: 20px; font-weight: 700;">{contract['tytul']}</h3>
<p style="margin: 4px 0 0 0; color: #64748b; font-size: 14px;">Klient: <strong>{contract['klient']}</strong> • {contract['kategoria']}</p>
</div>
<div style="background: {deadline_bg}; color: white; padding: 12px 20px; border-radius: 12px; text-align: center; min-width: 120px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
<div style="font-size: 24px; font-weight: 700; margin-bottom: 4px;">{deadline_days}d</div>
<div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Czas realizacji</div>
</div>
</div>
<div style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
<div style="color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; font-weight: 600;">📝 Opis sytuacji</div>
<div style="color: #334155; font-size: 14px; line-height: 1.6;">{contract['opis']}</div>
</div>
{bonus_alert_html}
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e8f0;">
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Nagroda</div>
<div style="color: #f59e0b; font-size: 20px; font-weight: 700;">💰 {reward_min}-{reward_max}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Trudność</div>
<div style="font-size: 20px;">{difficulty_stars}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Reputacja</div>
<div style="color: #8b5cf6; font-size: 20px; font-weight: 700;">⭐ +{contract['reputacja']}</div>
</div>
</div>
</div>"""
        
        st.markdown(html_content, unsafe_allow_html=True)
        
        # Expander ze szczegółami zadania
        with st.expander("👁️ Zobacz szczegóły zadania"):
            st.markdown("### 🎯 Zadanie do wykonania")
            st.markdown(contract['zadanie'])
            
            st.markdown("---")
            
            st.markdown("### 📚 Wymagana wiedza z lekcji")
            for req in contract['wymagana_wiedza']:
                st.markdown(f"- {req}")
            
            st.markdown("---")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**🏆 Wymagany poziom firmy:** {contract['wymagany_poziom']}")
            with col_b:
                st.markdown(f"**📂 Kategoria:** {contract['kategoria']}")
        
        # Przycisk przyjęcia
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col2:
            # Sprawdź możliwość przyjęcia
            if not can_accept_new:
                st.error("❌ Brak miejsca")
            else:
                if st.button("✅ Przyjmij", key=f"accept_{contract['id']}", type="primary", use_container_width=True):
                    updated_bg, success, message, _ = accept_contract(bg_data, contract['id'], user_data)
                    
                    if success:
                        user_data["business_game"] = updated_bg
                        save_user_data(username, user_data)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

# =============================================================================
# TAB 3: PRACOWNICY
# =============================================================================

def show_employees_tab(username, user_data):
    """Zakładka Biuro i Pracownicy"""
    bg_data = user_data["business_game"]
    
    # Inicjalizacja biura jeśli nie istnieje (dla starych zapisów)
    if "office" not in bg_data:
        bg_data["office"] = {
            "type": "home_office",
            "upgraded_at": None
        }
        user_data["business_game"] = bg_data
        save_user_data(username, user_data)
    
    # =============================================================================
    # SEKCJA BIURA
    # =============================================================================
    
    st.subheader("🏢 Twoje Biuro")
    
    office_type = bg_data["office"]["type"]
    office_info = OFFICE_TYPES[office_type]
    
    # Kompaktowa karta informacyjna o biurze
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); 
                    padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 48px;">{office_info['ikona']}</div>
                <div style="flex: 1;">
                    <h3 style="margin: 0; color: #1a1a1a;">{office_info['nazwa']}</h3>
                    <p style="margin: 5px 0; color: #2a2a2a; font-size: 14px;">{office_info['opis']}</p>
                    <div style="display: flex; gap: 20px; margin-top: 10px; font-size: 13px; color: #333;">
                        <span>👥 Max: {office_info['max_pracownikow']} pracowników</span>
                        <span>💰 Koszt: {office_info['koszt_dzienny']} zł/dzień</span>
                        <span>⭐ Reputacja: +{office_info['bonus_reputacji']}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Przycisk ulepszenia (jeśli dostępny)
    current_index = OFFICE_UPGRADE_PATH.index(office_type)
    if current_index < len(OFFICE_UPGRADE_PATH) - 1:
        next_office_type = OFFICE_UPGRADE_PATH[current_index + 1]
        next_office = OFFICE_TYPES[next_office_type]
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"💡 **Dostępne ulepszenie:** {next_office['ikona']} {next_office['nazwa']}")
        with col2:
            st.write(f"💰 Koszt: **{next_office['koszt_ulepszenia']} zł**")
        with col3:
            # Pobierz monety z user_data (nie z bg_data)
            current_coins = user_data.get('degencoins', 0)
            
            if current_coins >= next_office['koszt_ulepszenia']:
                if st.button("⬆️ Ulepsz biuro", type="primary", use_container_width=True):
                    # Ulepsz biuro
                    user_data['degencoins'] -= next_office['koszt_ulepszenia']
                    bg_data["office"]["type"] = next_office_type
                    bg_data["office"]["upgraded_at"] = datetime.now().isoformat()
                    bg_data["stats"]["total_costs"] += next_office['koszt_ulepszenia']
                    
                    # Dodaj transakcję
                    if "transactions" not in bg_data.get("history", {}):
                        if "history" not in bg_data:
                            bg_data["history"] = {}
                        bg_data["history"]["transactions"] = []
                    
                    bg_data["history"]["transactions"].append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": "office_upgrade",
                        "description": f"Ulepszenie biura: {next_office['nazwa']}",
                        "amount": -next_office['koszt_ulepszenia']
                    })
                    
                    user_data["business_game"] = bg_data
                    save_user_data(username, user_data)
                    st.success(f"🎉 Biuro ulepszone do: {next_office['nazwa']}!")
                    st.balloons()
                    st.rerun()
            else:
                st.button("⬆️ Ulepsz biuro", disabled=True, use_container_width=True)
                st.caption(f"Potrzebujesz: {next_office['koszt_ulepszenia'] - current_coins:.0f} 💰")
    else:
        st.success("🌟 Posiadasz najlepsze możliwe biuro!")
    
    st.markdown("---")
    
    # =============================================================================
    # SEKCJA PRACOWNIKÓW
    # =============================================================================
    
    st.subheader("👥 Zarządzanie Zespołem")
    
    max_employees = office_info['max_pracownikow']
    current_count = len(bg_data["employees"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Zespół", f"{current_count}/{max_employees}")
    with col2:
        daily_cost = calculate_daily_costs(bg_data)
        st.metric("💸 Koszty dzienne (pracownicy)", f"{daily_cost:.0f} 💰")
    with col3:
        total_daily = daily_cost + office_info['koszt_dzienny']
        st.metric("� Łączne koszty dzienne", f"{total_daily:.0f} 💰")
    
    st.markdown("---")
    
    # SEKCJA 1: Obecnie zatrudnieni (2 kolumny)
    st.subheader("🏢 Obecnie zatrudnieni")
    
    if len(bg_data["employees"]) == 0:
        st.info("Nie masz jeszcze pracowników. Zatrudnij kogoś z sekcji poniżej!")
    else:
        # Wyświetl zatrudnionych w 2 kolumnach
        cols = st.columns(2)
        for idx, employee in enumerate(bg_data["employees"]):
            with cols[idx % 2]:
                render_employee_card(employee, username, user_data, bg_data)
    
    st.markdown("---")
    
    # SEKCJA 2: Dostępni do zatrudnienia (2 kolumny)
    st.subheader("💼 Dostępni do zatrudnienia")
    
    if current_count >= max_employees:
        st.warning(f"⚠️ Osiągnięto limit pracowników: {max_employees}")
    
    # Wyświetl dostępnych w 2 kolumnach
    available_employees = [emp_type for emp_type in EMPLOYEE_TYPES.keys() 
                          if not any(e["type"] == emp_type for e in bg_data["employees"])]
    
    if available_employees:
        cols = st.columns(2)
        for idx, emp_type in enumerate(available_employees):
            with cols[idx % 2]:
                render_hire_card(emp_type, EMPLOYEE_TYPES[emp_type], username, user_data, bg_data)
    else:
        st.success("✅ Wszystkie dostępne typy pracowników są już zatrudnione!")

def render_employee_card(employee, username, user_data, bg_data):
    """Renderuje kartę zatrudnionego pracownika - kompaktowa"""
    
    emp_data = EMPLOYEE_TYPES[employee["type"]]
    
    # Kompaktowa karta
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 15px; border-radius: 10px; margin-bottom: 10px; color: white;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 18px; font-weight: bold;">{emp_data['ikona']} {emp_data['nazwa']}</div>
                    <div style="font-size: 12px; opacity: 0.9; margin-top: 4px;">{emp_data['bonus']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 14px; font-weight: bold;">{emp_data['koszt_dzienny']} 💰/dzień</div>
                    <div style="font-size: 11px; opacity: 0.8;">od {employee['hired_date']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Przycisk zwolnienia
        if st.button("🗑️ Zwolnij", key=f"fire_{employee['id']}", type="secondary", use_container_width=True):
            updated_user_data, success, message = fire_employee(user_data, employee['id'])
            if success:
                user_data.update(updated_user_data)
                save_user_data(username, user_data)
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def render_hire_card(emp_type, emp_data, username, user_data, bg_data):
    """Renderuje kartę dostępnego pracownika - kompaktowa"""
    
    can_hire, reason = can_hire_employee(user_data, emp_type)
    
    with st.container():
        # Kompaktowa karta z gradientem (szary)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%); 
                    padding: 15px; border-radius: 10px; margin-bottom: 10px; color: #424242;">
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
                {emp_data['ikona']} {emp_data['nazwa']}
            </div>
            <div style="font-size: 12px; opacity: 0.8; margin-bottom: 8px;">
                {emp_data['bonus']}
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 13px;">
                <div>💰 Zatrudnienie: <strong>{emp_data['koszt_zatrudnienia']}</strong></div>
                <div>📅 Dzienny: <strong>{emp_data['koszt_dzienny']}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Przycisk zatrudnienia
        if not can_hire:
            st.button("🔒 Niedostępny", key=f"hire_{emp_type}_locked", disabled=True, 
                     help=reason, use_container_width=True)
        else:
            if st.button("✅ Zatrudnij", key=f"hire_{emp_type}", type="primary", use_container_width=True):
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
# TAB 4: RAPORTY FINANSOWE
# =============================================================================

def show_financial_reports_tab(username, user_data):
    """Zakładka Raporty Finansowe - zaawansowana analiza P&L i KPI"""
    bg_data = user_data["business_game"]
    
    st.subheader("📊 Raporty Finansowe")
    st.markdown("Zaawansowana analiza wyników finansowych Twojej firmy")
    
    # Wybór okresu analizy
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        period_type = st.selectbox(
            "Okres analizy:",
            ["Ostatni dzień", "Ostatnie 7 dni", "Ostatnie 14 dni", "Ostatnie 30 dni", "Ostatnie 90 dni", "Cały czas"],
            index=1,  # Domyślnie "Ostatnie 7 dni"
            key="financial_period"
        )

    
    with col2:
        comparison = st.checkbox("Porównaj z poprzednim okresem", value=True, key="financial_compare")
    
    with col3:
        if st.button("🔄 Odśwież", key="refresh_reports"):
            st.rerun()
    
    # Mapowanie okresu na dni
    period_days = {
        "Ostatni dzień": 1,
        "Ostatnie 7 dni": 7,
        "Ostatnie 14 dni": 14,
        "Ostatnie 30 dni": 30,
        "Ostatnie 90 dni": 90,
        "Cały czas": 9999
    }
    days = period_days[period_type]
    
    # Pobierz dane finansowe
    financial_data = calculate_financial_data(bg_data, days, comparison)
    
    st.markdown("---")
    
    # Sub-tabs w raportach
    report_tabs = st.tabs(["📈 KPI Dashboard", "📋 P&L Statement", "💰 Analiza Rentowności", "👥 ROI Pracowników", "📊 Analiza Kategorii"])
    
    with report_tabs[0]:
        show_kpi_dashboard(financial_data, bg_data)
    
    with report_tabs[1]:
        show_pl_statement(financial_data, period_type, comparison)
    
    with report_tabs[2]:
        show_profitability_analysis(financial_data, bg_data)
    
    with report_tabs[3]:
        show_employee_roi_analysis(financial_data, bg_data)
    
    with report_tabs[4]:
        show_category_analysis(financial_data, bg_data)


def calculate_financial_data(bg_data, days, include_comparison=False):
    """Oblicza wszystkie dane finansowe dla raportów"""
    from datetime import datetime, timedelta
    
    transactions = bg_data.get("history", {}).get("transactions", [])
    completed_contracts = bg_data.get("contracts", {}).get("completed", [])
    
    # Daty
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days) if days < 9999 else datetime(2000, 1, 1)
    
    # Filtruj transakcje w okresie
    current_transactions = [
        t for t in transactions
        if datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S") >= start_date
    ]
    
    # Filtruj kontrakty w okresie (obsługa różnych formatów daty)
    current_contracts = []
    for c in completed_contracts:
        completed_date_str = c.get("completed_date", "2000-01-01")
        try:
            # Spróbuj format z czasem
            contract_date = datetime.strptime(completed_date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                # Spróbuj format tylko data
                contract_date = datetime.strptime(completed_date_str, "%Y-%m-%d")
            except ValueError:
                # Jeśli niepoprawny format, pomiń
                continue
        
        if contract_date >= start_date:
            current_contracts.append(c)
    
    # CURRENT PERIOD
    # Przychody: kontrakty + pozytywne wydarzenia
    contract_revenue = sum(t.get("amount", 0) for t in current_transactions if t.get("type") == "contract_reward")
    event_revenue = sum(t.get("amount", 0) for t in current_transactions if t.get("type") == "event_reward")
    revenue = contract_revenue + event_revenue
    
    # Koszty: pracownicy + biuro + negatywne wydarzenia
    employee_hire_costs = sum(abs(t.get("amount", 0)) for t in current_transactions if t.get("type") in ["employee_hired", "employee_hire"])
    daily_costs = sum(abs(t.get("amount", 0)) for t in current_transactions if t.get("type") == "daily_costs")
    office_costs = sum(abs(t.get("amount", 0)) for t in current_transactions if t.get("type") in ["office_rent", "office_upgrade"])
    event_costs = sum(abs(t.get("amount", 0)) for t in current_transactions if t.get("type") == "event_cost")
    total_costs = employee_hire_costs + daily_costs + office_costs + event_costs
    profit = revenue - total_costs
    
    # Kontrakty
    num_contracts = len(current_contracts)
    avg_contract_value = revenue / num_contracts if num_contracts > 0 else 0
    avg_rating = sum(c.get("rating", 0) for c in current_contracts) / num_contracts if num_contracts > 0 else 0
    
    # Pracownicy
    num_employees = len(bg_data.get("employees", []))
    revenue_per_employee = revenue / num_employees if num_employees > 0 else 0
    
    # Marże
    profit_margin = (profit / revenue * 100) if revenue > 0 else 0
    cost_to_revenue_ratio = (total_costs / revenue * 100) if revenue > 0 else 0
    
    result = {
        "period": {
            "revenue": revenue,
            "revenue_breakdown": {
                "contracts": contract_revenue,
                "events": event_revenue
            },
            "costs": {
                "employee_hire": employee_hire_costs,
                "daily_costs": daily_costs,
                "office": office_costs,
                "events": event_costs,
                "total": total_costs
            },
            "profit": profit,
            "contracts": {
                "count": num_contracts,
                "avg_value": avg_contract_value,
                "avg_rating": avg_rating
            },
            "employees": {
                "count": num_employees,
                "revenue_per_employee": revenue_per_employee
            },
            "metrics": {
                "profit_margin": profit_margin,
                "cost_to_revenue_ratio": cost_to_revenue_ratio
            }
        }
    }
    
    # PREVIOUS PERIOD (dla porównania)
    if include_comparison and days < 9999:
        prev_end = start_date
        prev_start = prev_end - timedelta(days=days)
        
        prev_transactions = [
            t for t in transactions
            if prev_start <= datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S") < prev_end
        ]
        
        # Filtruj kontrakty z poprzedniego okresu (obsługa różnych formatów daty)
        prev_contracts = []
        for c in completed_contracts:
            completed_date_str = c.get("completed_date", "2000-01-01")
            try:
                # Spróbuj format z czasem
                contract_date = datetime.strptime(completed_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    # Spróbuj format tylko data
                    contract_date = datetime.strptime(completed_date_str, "%Y-%m-%d")
                except ValueError:
                    # Jeśli niepoprawny format, pomiń
                    continue
            
            if prev_start <= contract_date < prev_end:
                prev_contracts.append(c)
        
        # Przychody: kontrakty + wydarzenia
        prev_contract_revenue = sum(t.get("amount", 0) for t in prev_transactions if t.get("type") == "contract_reward")
        prev_event_revenue = sum(t.get("amount", 0) for t in prev_transactions if t.get("type") == "event_reward")
        prev_revenue = prev_contract_revenue + prev_event_revenue
        
        # Koszty: pracownicy + biuro + wydarzenia
        prev_costs = sum(abs(t.get("amount", 0)) for t in prev_transactions if t.get("type") in ["employee_hired", "employee_hire", "daily_costs", "office_rent", "office_upgrade", "event_cost"])
        prev_profit = prev_revenue - prev_costs
        prev_num_contracts = len(prev_contracts)
        
        result["previous"] = {
            "revenue": prev_revenue,
            "costs": prev_costs,
            "profit": prev_profit,
            "contracts": prev_num_contracts
        }
    
    return result


def show_kpi_dashboard(financial_data, bg_data):
    """Wyświetla dashboard z kluczowymi KPI"""
    st.markdown("### 🎯 Kluczowe Wskaźniki Wydajności")
    
    period = financial_data["period"]
    has_prev = "previous" in financial_data
    
    # Główne KPI w 3 kolumnach
    col1, col2, col3 = st.columns(3)
    
    with col1:
        revenue = period["revenue"]
        revenue_change = 0
        if has_prev and financial_data["previous"]["revenue"] > 0:
            revenue_change = ((revenue - financial_data["previous"]["revenue"]) / financial_data["previous"]["revenue"]) * 100
        
        render_kpi_card(
            "💰 Przychody",
            f"{revenue:,.0f} 💰",
            revenue_change if has_prev else None,
            "positive"
        )
    
    with col2:
        profit = period["profit"]
        profit_change = 0
        if has_prev and financial_data["previous"]["profit"] != 0:
            profit_change = ((profit - financial_data["previous"]["profit"]) / abs(financial_data["previous"]["profit"])) * 100
        
        render_kpi_card(
            "💎 Zysk Netto",
            f"{profit:,.0f} 💰",
            profit_change if has_prev else None,
            "positive" if profit >= 0 else "negative"
        )
    
    with col3:
        margin = period["metrics"]["profit_margin"]
        render_kpi_card(
            "📊 Marża Zysku",
            f"{margin:.1f}%",
            None,
            "positive" if margin >= 20 else "neutral" if margin >= 10 else "negative"
        )
    
    st.markdown("---")
    
    # Dodatkowe KPI w 4 kolumnach
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_kpi_card(
            "📝 Kontrakty",
            f"{period['contracts']['count']}",
            None,
            "neutral"
        )
    
    with col2:
        render_kpi_card(
            "⭐ Śr. Ocena",
            f"{period['contracts']['avg_rating']:.2f}",
            None,
            "positive" if period['contracts']['avg_rating'] >= 4 else "neutral"
        )
    
    with col3:
        render_kpi_card(
            "👥 Pracownicy",
            f"{period['employees']['count']}",
            None,
            "neutral"
        )
    
    with col4:
        rpe = period['employees']['revenue_per_employee']
        render_kpi_card(
            "💼 Rev/Employee",
            f"{rpe:,.0f} 💰",
            None,
            "positive" if rpe > 1000 else "neutral"
        )


def render_kpi_card(title, value, change_percent=None, sentiment="neutral"):
    """Renderuje kartę KPI z opcjonalnym trendem"""
    
    # Kolory na podstawie sentymentu
    colors = {
        "positive": {"bg": "#f0fdf4", "border": "#10b981", "text": "#065f46"},
        "negative": {"bg": "#fef2f2", "border": "#ef4444", "text": "#991b1b"},
        "neutral": {"bg": "#f8f9fa", "border": "#94a3b8", "text": "#475569"}
    }
    
    color = colors.get(sentiment, colors["neutral"])
    
    # Strzałka trendu
    trend_html = ""
    if change_percent is not None:
        if change_percent > 0:
            trend_html = f"<div style='color: #10b981; font-size: 14px;'>▲ +{change_percent:.1f}%</div>"
        elif change_percent < 0:
            trend_html = f"<div style='color: #ef4444; font-size: 14px;'>▼ {change_percent:.1f}%</div>"
        else:
            trend_html = f"<div style='color: #94a3b8; font-size: 14px;'>➡ 0%</div>"
    
    st.markdown(f"""
    <div style="background: {color['bg']}; 
                border-left: 4px solid {color['border']}; 
                padding: 16px; 
                border-radius: 8px;
                height: 100%;">
        <div style="color: {color['text']}; font-size: 12px; font-weight: 600; margin-bottom: 8px;">
            {title}
        </div>
        <div style="font-size: 24px; font-weight: bold; color: {color['text']}; margin-bottom: 4px;">
            {value}
        </div>
        {trend_html}
    </div>
    """, unsafe_allow_html=True)


def show_pl_statement(financial_data, period_type, show_comparison):
    """Wyświetla rachunek zysków i strat (P&L Statement)"""
    st.markdown("### 📋 Rachunek Zysków i Strat (P&L)")
    st.markdown(f"**Okres:** {period_type}")
    
    period = financial_data["period"]
    has_prev = "previous" in financial_data and show_comparison
    
    # Tworzenie tabeli P&L
    import pandas as pd
    
    pl_data = {
        "Pozycja": [
            "PRZYCHODY OPERACYJNE",
            "  Przychody z kontraktów",
            "  Przychody z wydarzeń",
            "  RAZEM PRZYCHODY",
            "",
            "KOSZTY OPERACYJNE",
            "  Koszty zatrudnienia (jednorazowe)",
            "  Koszty pracowników (dzienne)",
            "  Koszty biura (wynajem + ulepszenia)",
            "  Koszty z wydarzeń",
            "  RAZEM KOSZTY",
            "",
            "ZYSK/STRATA OPERACYJNA",
            "",
            "WSKAŹNIKI",
            "  Marża zysku",
            "  Stosunek kosztów do przychodów"
        ],
        "Bieżący okres": [
            "",
            f"{period['revenue_breakdown']['contracts']:,.0f} 💰",
            f"{period['revenue_breakdown']['events']:,.0f} 💰",
            f"{period['revenue']:,.0f} 💰",
            "",
            "",
            f"-{period['costs']['employee_hire']:,.0f} 💰",
            f"-{period['costs']['daily_costs']:,.0f} 💰",
            f"-{period['costs']['office']:,.0f} 💰",
            f"-{period['costs']['events']:,.0f} 💰",
            f"-{period['costs']['total']:,.0f} 💰",
            "",
            f"{period['profit']:,.0f} 💰",
            "",
            "",
            f"{period['metrics']['profit_margin']:.1f}%",
            f"{period['metrics']['cost_to_revenue_ratio']:.1f}%"
        ]
    }
    
    if has_prev:
        prev = financial_data["previous"]
        pl_data["Poprzedni okres"] = [
            "",
            "-",  # Rozbicie przychodów niedostępne dla poprzedniego okresu
            "-",
            f"{prev['revenue']:,.0f} 💰",
            "",
            "",
            "-",  # Rozbicie kosztów niedostępne
            "-",
            "-",
            "-",
            f"-{prev['costs']:,.0f} 💰",
            "",
            f"{prev['profit']:,.0f} 💰",
            "",
            "",
            "-",
            "-"
        ]
        
        # Zmiana
        rev_change = period['revenue'] - prev['revenue']
        profit_change = period['profit'] - prev['profit']
        cost_change = period['costs']['total'] - prev['costs']
        
        pl_data["Zmiana"] = [
            "",
            "-",
            "-",
            f"{rev_change:+,.0f} 💰",
            "",
            "",
            "-",
            "-",
            "-",
            "-",
            f"{-cost_change:+,.0f} 💰",
            "",
            f"{profit_change:+,.0f} 💰",
            "",
            "",
            "-",
            "-"
        ]
    
    df = pd.DataFrame(pl_data)
    
    # Stylowanie tabeli
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    # Waterfall chart
    st.markdown("#### 💧 Analiza Waterfall (Przepływ Środków)")
    
    import plotly.graph_objects as go
    
    # Buduj waterfall dynamicznie (tylko niezerowe pozycje)
    x_labels = ["Przychody"]
    y_values = [period['revenue']]
    measures = ["relative"]
    texts = [f"{period['revenue']:,.0f}"]
    
    if period['costs']['employee_hire'] > 0:
        x_labels.append("Koszty<br>zatrudnienia")
        y_values.append(-period['costs']['employee_hire'])
        measures.append("relative")
        texts.append(f"-{period['costs']['employee_hire']:,.0f}")
    
    if period['costs']['daily_costs'] > 0:
        x_labels.append("Koszty<br>pracowników")
        y_values.append(-period['costs']['daily_costs'])
        measures.append("relative")
        texts.append(f"-{period['costs']['daily_costs']:,.0f}")
    
    if period['costs']['office'] > 0:
        x_labels.append("Koszty<br>biura")
        y_values.append(-period['costs']['office'])
        measures.append("relative")
        texts.append(f"-{period['costs']['office']:,.0f}")
    
    if period['costs']['events'] > 0:
        x_labels.append("Koszty<br>wydarzeń")
        y_values.append(-period['costs']['events'])
        measures.append("relative")
        texts.append(f"-{period['costs']['events']:,.0f}")
    
    x_labels.append("Zysk Netto")
    y_values.append(period['profit'])
    measures.append("total")
    texts.append(f"{period['profit']:,.0f}")
    
    fig = go.Figure(go.Waterfall(
        x = x_labels,
        y = y_values,
        measure = measures,
        text = texts,
        textposition = "outside",
        connector = {"line": {"color": "#cbd5e1"}},
        decreasing = {"marker": {"color": "#ef4444"}},
        increasing = {"marker": {"color": "#10b981"}},
        totals = {"marker": {"color": "#8b5cf6"}}
    ))
    
    fig.update_layout(
        title="Przepływ środków: Od przychodów do zysku",
        showlegend=False,
        height=400,
        yaxis_title="Monety 💰",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_profitability_analysis(financial_data, bg_data):
    """Analiza rentowności"""
    st.markdown("### 💰 Analiza Rentowności")
    
    period = financial_data["period"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Wskaźniki Rentowności")
        
        # Gross Profit Margin
        st.metric(
            "Marża Zysku Brutto",
            f"{period['metrics']['profit_margin']:.1f}%",
            help="Zysk / Przychody * 100"
        )
        
        # Cost Efficiency
        efficiency = 100 - period['metrics']['cost_to_revenue_ratio']
        st.metric(
            "Efektywność Kosztowa",
            f"{efficiency:.1f}%",
            help="Im wyższa, tym lepiej zarządzasz kosztami"
        )
        
        # Average Contract Profitability
        avg_profit_per_contract = period['profit'] / period['contracts']['count'] if period['contracts']['count'] > 0 else 0
        st.metric(
            "Średni Zysk na Kontrakt",
            f"{avg_profit_per_contract:,.0f} 💰"
        )
        
        # Break-even point
        if period['costs']['daily_costs'] > 0:
            contracts_completed = period['contracts']['count']
            days_in_period = 7  # Można dynamicznie obliczyć
            daily_revenue = period['revenue'] / days_in_period if days_in_period > 0 else 0
            daily_op_costs = period['costs']['daily_costs'] / days_in_period if days_in_period > 0 else 0
            
            st.metric(
                "Dzienny Przychód",
                f"{daily_revenue:,.0f} 💰"
            )
            st.metric(
                "Dzienny Koszt Operacyjny",
                f"{daily_op_costs:,.0f} 💰"
            )
    
    with col2:
        st.markdown("#### 📈 Benchmark")
        
        # Porównanie z celami
        targets = {
            "Marża zysku": {"current": period['metrics']['profit_margin'], "target": 30, "unit": "%"},
            "Ocena klientów": {"current": period['contracts']['avg_rating'], "target": 4.5, "unit": "⭐"},
            "Rev per Employee": {"current": period['employees']['revenue_per_employee'], "target": 2000, "unit": "💰"}
        }
        
        for name, data in targets.items():
            current = data["current"]
            target = data["target"]
            # Ogranicz progress do zakresu 0-100 (obsługa wartości ujemnych)
            progress = max(0, min((current / target) * 100, 100)) if target > 0 else 0
            
            st.markdown(f"**{name}**")
            st.progress(progress / 100)
            st.markdown(f"{current:.1f}{data['unit']} / {target}{data['unit']}")
            st.markdown("")


def show_employee_roi_analysis(financial_data, bg_data):
    """Analiza ROI pracowników"""
    st.markdown("### 👥 ROI Pracowników")
    
    from data.business_data import EMPLOYEE_TYPES
    
    employees = bg_data.get("employees", [])
    period = financial_data["period"]
    
    if not employees:
        st.info("📭 Nie masz jeszcze pracowników. Zatrudnij kogoś, aby zobaczyć analizę ROI!")
        return
    
    st.markdown(f"""
    **Analiza:** Czy Twoi pracownicy generują wystarczające przychody, aby pokryć swoje koszty?
    
    - **Przychody w okresie:** {period['revenue']:,.0f} 💰
    - **Liczba pracowników:** {len(employees)}
    - **Przychód na pracownika:** {period['employees']['revenue_per_employee']:,.0f} 💰
    """)
    
    st.markdown("---")
    
    # Analiza per typ pracownika
    st.markdown("#### 📊 Analiza per typ pracownika")
    
    employee_stats = {}
    for emp in employees:
        emp_type = emp["type"]
        if emp_type not in employee_stats:
            employee_stats[emp_type] = {
                "count": 0,
                "daily_cost": EMPLOYEE_TYPES[emp_type]["koszt_dzienny"],
                "hire_cost": EMPLOYEE_TYPES[emp_type]["koszt_zatrudnienia"],
                "bonus": EMPLOYEE_TYPES[emp_type]["bonus"]
            }
        employee_stats[emp_type]["count"] += 1
    
    # Tabela ROI
    import pandas as pd
    
    roi_data = []
    for emp_type, stats in employee_stats.items():
        emp_data = EMPLOYEE_TYPES[emp_type]
        total_daily_cost = stats["daily_cost"] * stats["count"] * 7  # Zakładając 7 dni
        roi_data.append({
            "Typ": f"{emp_data['ikona']} {emp_data['nazwa']}",
            "Ilość": stats["count"],
            "Koszt/dzień": f"{stats['daily_cost']} 💰",
            "Koszt tygodniowy": f"{total_daily_cost:,.0f} 💰",
            "Bonus": stats["bonus"]
        })
    
    df = pd.DataFrame(roi_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Wykres kosztów pracowników
    if employee_stats:
        import plotly.graph_objects as go
        
        labels = [f"{EMPLOYEE_TYPES[t]['ikona']} {EMPLOYEE_TYPES[t]['nazwa']}" for t in employee_stats.keys()]
        values = [s['count'] * s['daily_cost'] * 7 for s in employee_stats.values()]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#f5576c'])
        )])
        
        fig.update_layout(
            title="Rozkład kosztów tygodniowych pracowników",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)


def show_category_analysis(financial_data, bg_data):
    """Analiza wydajności kategorii kontraktów"""
    st.markdown("### 📊 Analiza Kategorii Kontraktów")
    
    completed = bg_data.get("contracts", {}).get("completed", [])
    
    if not completed:
        st.info("📭 Brak ukończonych kontraktów do analizy.")
        return
    
    # Grupuj po kategoriach
    import pandas as pd
    
    category_stats = {}
    
    for contract in completed:
        category = contract.get("kategoria", "other")
        reward = contract.get("reward", {}).get("coins", 0)
        rating = contract.get("rating", 0)
        
        if category not in category_stats:
            category_stats[category] = {"count": 0, "total_reward": 0, "total_rating": 0, "contracts": []}
        
        category_stats[category]["count"] += 1
        category_stats[category]["total_reward"] += reward
        category_stats[category]["total_rating"] += rating
        category_stats[category]["contracts"].append(contract)
    
    # Przygotuj dane do tabeli
    table_data = []
    for category, stats in category_stats.items():
        count = stats["count"]
        avg_reward = stats["total_reward"] / count if count > 0 else 0
        avg_rating = stats["total_rating"] / count if count > 0 else 0
        
        table_data.append({
            "Kategoria": category.upper(),
            "Liczba kontraktów": count,
            "Łączny przychód": f"{stats['total_reward']:,.0f} 💰",
            "Średni przychód": f"{avg_reward:,.0f} 💰",
            "Średnia ocena": f"{avg_rating:.2f} ⭐"
        })
    
    # Sortuj po przychodzie
    table_data.sort(key=lambda x: float(x["Średni przychód"].replace(" 💰", "").replace(",", "")), reverse=True)
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Wykres słupkowy - przychody per kategoria
    import plotly.graph_objects as go
    
    categories = [d["Kategoria"] for d in table_data]
    revenues = [float(d["Łączny przychód"].replace(" 💰", "").replace(",", "")) for d in table_data]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=revenues,
            marker_color='#667eea',
            text=revenues,
            texttemplate='%{text:,.0f} 💰',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Łączne przychody per kategoria",
        xaxis_title="Kategoria",
        yaxis_title="Przychód (💰)",
        height=400,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top kontrakty
    st.markdown("#### 🏆 Top 5 Najbardziej Dochodowych Kontraktów")
    
    all_contracts = []
    for category, stats in category_stats.items():
        all_contracts.extend(stats["contracts"])
    
    top_contracts = sorted(all_contracts, key=lambda x: x.get("reward", {}).get("coins", 0), reverse=True)[:5]
    
    for i, contract in enumerate(top_contracts, 1):
        reward = contract.get("reward", {}).get("coins", 0)
        rating = contract.get("rating", 0)
        st.markdown(f"""
        **{i}. {contract.get('emoji', '📋')} {contract.get('tytul', 'Nieznany')}**  
        💰 {reward:,} monet | ⭐ {rating}/5 | 🏢 {contract.get('klient', 'Nieznany klient')}
        """)

# =============================================================================
# TAB 5: HISTORIA KONTRAKTÓW
# =============================================================================

def show_history_tab(username, user_data):
    """Zakładka Historia & Wydarzenia - chronologiczna oś czasu"""
    bg_data = user_data["business_game"]
    
    st.subheader("📜 Historia & Wydarzenia Firmy")
    
    # Sekcja losowania wydarzeń na górze
    st.markdown("### 🎲 Losowanie Wydarzenia")
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
        user_data["business_game"] = bg_data
        save_user_data(username, user_data)
    
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
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if can_roll:
            st.success("✅ **Możesz wylosować zdarzenie!** (Szansa: 20%)")
        else:
            st.warning(f"⏰ Następne losowanie za: **{hours_left}h {minutes_left}min**")
    
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
    
    # Zbierz wszystkie zdarzenia (kontrakty + wydarzenia)
    timeline_items = []
    
    # Dodaj ukończone kontrakty
    completed = bg_data["contracts"]["completed"]
    for contract in completed:
        timeline_items.append({
            "type": "contract",
            "date": contract.get("completed_date", ""),
            "data": contract
        })
    
    # Dodaj wydarzenia
    events_history = bg_data.get("events", {}).get("history", [])
    for event in events_history:
        timeline_items.append({
            "type": "event",
            "date": event.get("date", ""),
            "data": event
        })
    
    # Sortuj chronologicznie (najnowsze najpierw)
    timeline_items.sort(key=lambda x: x["date"], reverse=True)
    
    if not timeline_items:
        st.info("📭 Brak historii. Wykonuj kontrakty i losuj wydarzenia, aby wypełnić oś czasu!")
        return
    
    # Filtry
    st.markdown("### 🔍 Filtry")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox(
            "Typ:",
            ["Wszystko", "Tylko kontrakty", "Tylko wydarzenia"],
            key="history_filter_type"
        )
    with col2:
        show_count = st.selectbox(
            "Pokaż:",
            [10, 25, 50, "Wszystko"],
            key="history_show_count"
        )
    with col3:
        # Dodatkowy filtr dla kontraktów
        filter_rating = st.selectbox(
            "Ocena kontraktów:",
            ["Wszystkie", "⭐⭐⭐⭐⭐ (5)", "⭐⭐⭐⭐ (4+)", "⭐⭐⭐ (3+)"],
            key="history_filter_rating"
        )
    
    # Filtrowanie
    filtered = timeline_items
    
    if filter_type == "Tylko kontrakty":
        filtered = [item for item in filtered if item["type"] == "contract"]
    elif filter_type == "Tylko wydarzenia":
        filtered = [item for item in filtered if item["type"] == "event"]
    
    if filter_rating != "Wszystkie":
        if filter_rating == "⭐⭐⭐⭐⭐ (5)":
            filtered = [item for item in filtered if item["type"] != "contract" or item["data"].get("rating", 0) == 5]
        elif filter_rating == "⭐⭐⭐⭐ (4+)":
            filtered = [item for item in filtered if item["type"] != "contract" or item["data"].get("rating", 0) >= 4]
        elif filter_rating == "⭐⭐⭐ (3+)":
            filtered = [item for item in filtered if item["type"] != "contract" or item["data"].get("rating", 0) >= 3]
    
    # Limit
    if show_count != "Wszystko":
        filtered = filtered[:show_count]
    
    st.markdown("---")
    st.markdown(f"**Znaleziono:** {len(filtered)} pozycji")
    st.markdown("---")
    
    # Wyświetl chronologiczną oś czasu
    st.markdown("### ⏰ Oś Czasu")
    
    for item in filtered:
        if item["type"] == "contract":
            render_completed_contract_card(item["data"])
        else:  # event
            render_event_history_card(item["data"])


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
# WYDARZENIA (HELPER FUNCTIONS)
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
    """Renderuje małą kartę z najnowszym zdarzeniem na Dashboard (stara wersja)"""
    
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

def show_active_event_card(event: dict):
    """Wyświetla aktywne wydarzenie jako wyróżnioną kartę (Material Design)
    
    Args:
        event: Słownik z danymi wydarzenia (latest_event)
    """
    from utils.business_game_events import get_active_effects
    
    # Kolory w zależności od typu
    if event["type"] == "positive":
        gradient_start = "#10b981"
        gradient_end = "#059669"
        emoji_bg = "rgba(255,255,255,0.2)"
        icon = "✨"
    elif event["type"] == "negative":
        gradient_start = "#ef4444"
        gradient_end = "#dc2626"
        emoji_bg = "rgba(255,255,255,0.2)"
        icon = "⚠️"
    else:  # neutral
        gradient_start = "#f59e0b"
        gradient_end = "#d97706"
        emoji_bg = "rgba(255,255,255,0.2)"
        icon = "⚖️"
    
    # Buduj HTML z efektami
    effects_html = ""
    if event.get("effects"):
        effects = event["effects"]
        effects_items = []
        
        # Monety
        if effects.get("coins"):
            coin_value = effects["coins"]
            if coin_value > 0:
                effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>💰</span><div><strong>+{coin_value}</strong><br><span style='font-size: 11px; opacity: 0.9;'>monet</span></div></div>")
            else:
                effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>💸</span><div><strong>{coin_value}</strong><br><span style='font-size: 11px; opacity: 0.9;'>monet</span></div></div>")
        
        # Reputacja
        if effects.get("reputation"):
            rep_value = effects["reputation"]
            if rep_value > 0:
                effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>⭐</span><div><strong>+{rep_value}</strong><br><span style='font-size: 11px; opacity: 0.9;'>reputacji</span></div></div>")
            else:
                effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>📉</span><div><strong>{rep_value}</strong><br><span style='font-size: 11px; opacity: 0.9;'>reputacji</span></div></div>")
        
        # Bonus do kontraktu
        if effects.get("next_contract_bonus"):
            bonus_pct = int((effects["next_contract_bonus"] - 1) * 100)
            effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>🎁</span><div><strong>+{bonus_pct}%</strong><br><span style='font-size: 11px; opacity: 0.9;'>bonus nagrody</span></div></div>")
        
        # Przedłużenie deadline
        if effects.get("deadline_extension"):
            ext_hours = effects["deadline_extension"]
            effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>⏰</span><div><strong>+{ext_hours}h</strong><br><span style='font-size: 11px; opacity: 0.9;'>dodatkowy czas</span></div></div>")
        
        # Boost pojemności
        if effects.get("capacity_boost"):
            boost = effects["capacity_boost"]
            duration = effects.get("duration_days", "?")
            effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>📈</span><div><strong>+{boost}</strong><br><span style='font-size: 11px; opacity: 0.9;'>pojemność ({duration}d)</span></div></div>")
        
        # Skrócenie deadline (negatywne)
        if effects.get("deadline_reduction"):
            red_hours = effects["deadline_reduction"]
            effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>⏱️</span><div><strong>-{red_hours}h</strong><br><span style='font-size: 11px; opacity: 0.9;'>mniej czasu</span></div></div>")
        
        if effects_items:
            effects_html = f"<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-top: 16px;'>{''.join(effects_items)}</div>"
    
    # Flavor text (jeśli istnieje)
    flavor_html = ""
    if event.get("flavor_text"):
        flavor_html = f"""<div style='background: rgba(0,0,0,0.15); border-left: 3px solid rgba(255,255,255,0.5); padding: 12px 16px; border-radius: 8px; margin-top: 16px; font-style: italic; font-size: 13px; line-height: 1.5;'>
"{event['flavor_text']}"
</div>"""
    
    # Wyświetl kartę
    event_card_html = f"""<div style="background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%); color: white; border-radius: 20px; padding: 24px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);">
<div style="display: flex; align-items: start; gap: 20px;">
<div style="font-size: 56px; line-height: 1;">{event['emoji']}</div>
<div style="flex: 1;">
<div style="font-size: 14px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">{icon} Wydarzenie dnia</div>
<div style="font-size: 22px; font-weight: 700; margin-bottom: 12px;">{event['title']}</div>
<div style="font-size: 15px; opacity: 0.95; line-height: 1.7;">{event['description']}</div>
{flavor_html}
{effects_html}
</div>
</div>
</div>"""
    
    st.markdown(event_card_html, unsafe_allow_html=True)

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
# TAB 7: RANKINGI
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
        ["🏆 Rating (Overall Score)", "💰 Przychody", "⭐ Jakość (średnia ocena)", "🔥 Produktywność (30 dni)"],
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
    else:  # Rating (domyślnie)
        score_label = "Rating"
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
            else:  # Rating
                score = ranking.get("overall_score", 0)
            
            all_firms.append({
                "name": firm.get("name", f"{user}'s Consulting"),
                "logo": firm.get("logo", "🏢"),  # Dodaj logo firmy
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
                <h3 style='margin:0;'>{medal} <span style='font-size: 1.2em;'>{firm['logo']}</span> {firm['name']} (Ty!)</h3>
                <p style='margin:5px 0 0 0;'>{score_label}: {score_display}{score_suffix}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <h4 style='margin:0;'>{medal} <span style='font-size: 1.2em;'>{firm['logo']}</span> {firm['name']}</h4>
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
                <strong>Rating</strong><br>
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
# TAB 0: INSTRUKCJA GRY
# =============================================================================

def show_instructions_tab():
    """Zakładka z instrukcją gry"""
    
    st.markdown("## 📖 Jak grać w Business Games?")
    
    st.markdown("---")
    
    # Cel gry
    st.markdown("""
    ### 🎯 Cel Gry
    
    Twoim celem jest **zbudowanie i rozwinięcie firmy konsultingowej**, realizując kontrakty dla klientów,
    zarządzając zespołem pracowników i reagując na losowe wydarzenia rynkowe.
    
    **Wygrywasz, gdy:**
    - Osiągniesz najwyższy poziom firmy
    - Zdobędziesz najwięcej przychodów
    - Uzyskasz najlepszą średnią ocenę kontraktów
    """)
    
    st.markdown("---")
    
    # Podstawy rozgrywki
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💼 Kontrakty
        
        **Jak działają kontrakty?**
        1. W zakładce **"Rynek Kontraktów"** wybierz dostępne zlecenia
        2. Każdy kontrakt ma:
           - 🔥 **Trudność** (1-5 płomyków)
           - 💰 **Nagrodę** (zależną od oceny 1-5⭐)
           - ⏱️ **Czas realizacji** (dni do deadline)
           - 📋 **Kategorię** (Konflikt, Coaching, Kryzys, Leadership, Kultura)
        
        **Przyjmowanie kontraktów:**
        - Możesz mieć max **3 aktywne kontrakty** jednocześnie
        - Dziennie możesz przyjąć **2 nowe kontrakty** (zależy od poziomu firmy)
        - Nie możesz przyjąć więcej niż masz pojemności
        
        **Wykonywanie kontraktów:**
        1. Nagrywasz audio lub wpisujesz tekst
        2. AI ocenia Twoją odpowiedź (1-5⭐)
        3. Otrzymujesz nagrodę zgodnie z oceną
        4. Masz **3 próby** na każdy kontrakt
        """)
    
    with col2:
        st.markdown("""
        ### 👥 Pracownicy
        
        **Zatrudniaj specjalistów:**
        - **Junior** (500💰) - podstawowe wsparcie
        - **Mid** (1500💰) - lepsze bonusy
        - **Senior** (3500💰) - najlepsze korzyści
        
        **Typy pracowników:**
        - 📊 **Analityk** - bonus do oceny kontraktów (+0.5⭐)
        - 💼 **Manager** - zwiększa pojemność dzienną (+1 kontrakt)
        - 🎯 **Specjalista** - redukuje koszty dzienne (-20%)
        - 🚀 **Ekspert** - zwiększa nagrody (+15%)
        
        **Pamiętaj:**
        - Każdy pracownik generuje **koszty dzienne**
        - Możesz zwolnić pracownika, ale stracisz bonusy
        - Im wyższy poziom, tym lepsze korzyści
        """)
    
    st.markdown("---")
    
    # Mechaniki gry
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        ### 🎲 Wydarzenia Losowe
        
        Co jakiś czas wystąpią **wydarzenia rynkowe**:
        
        **Typy wydarzeń:**
        - ✅ **Pozytywne** - bonusy, rabaty, nagrody
        - ❌ **Negatywne** - koszty, trudności, ograniczenia
        - ⚖️ **Neutralne** - wybierasz opcję A lub B
        
        **Przykłady:**
        - 💰 Bonus do następnego kontraktu (+50% nagrody)
        - 📉 Spadek na rynku (dodatkowe koszty)
        - 🎁 Darmowy pracownik na 3 dni
        - 🎯 Wybór: inwestycja lub oszczędności
        
        Wydarzenia są **losowe** i wpływają na strategię!
        """)
    
    with col4:
        st.markdown("""
        ### 📈 Rozwój Firmy
        
        **Poziomy firmy (1-5):**
        
        Każdy poziom wymaga **określonej liczby monet** (💰):
        - Poziom 2: 2000💰
        - Poziom 3: 5000💰
        - Poziom 4: 10000💰
        - Poziom 5: 20000💰
        
        **Korzyści wyższego poziomu:**
        - Więcej miejsc na pracowników
        - Większa pojemność dzienna kontraktów
        - Odblokowujesz trudniejsze (i lepiej płatne) zlecenia
        
        **Jak zdobywać monety?**
        - Wykonuj kontrakty (nagrody)
        - Unikaj zbyt wysokich kosztów
        - Zarządzaj zespołem efektywnie
        """)
    
    st.markdown("---")
    
    # Wskazówki strategiczne
    st.markdown("""
    ### 💡 Wskazówki i Strategia
    
    #### ✅ Dobre praktyki:
    - **Na początku:** Bierz łatwe kontrakty (🔥), buduj kapitał i doświadczenie
    - **Zatrudniaj mądrze:** Junior Analityk to świetny pierwszy pracownik (bonus do ocen)
    - **Sprawdzaj deadline:** Nie przyjmuj więcej niż możesz wykonać w terminie
    - **Wykorzystuj bonusy:** Gdy masz event z bonusem, weź najlepszy kontrakt
    - **Balansuj koszty:** Zbyt wielu pracowników = wysokie koszty dzienne
    
    #### ❌ Unikaj:
    - Przyjmowania kontraktów na ostatnią chwilę przed deadline
    - Zatrudniania za dużo pracowników bez stabilnych przychodów
    - Ignorowania wydarzeń - mogą dać duże korzyści!
    - Marnowania wszystkich 3 prób na trudny kontrakt bez przygotowania
    
    #### 🎯 Pro tipy:
    - **Senior Analityk** daje +1⭐ do oceny - świetna inwestycja!
    - **Mid Manager** zwiększa pojemność - więcej kontraktów = więcej pieniędzy
    - Obserwuj **Rankingi** - zobacz co robią najlepsi gracze
    - **Historia transakcji** pokazuje Twoje przychody i koszty - analizuj!
    """)
    
    st.markdown("---")
    
    # FAQ
    with st.expander("❓ Najczęściej zadawane pytania (FAQ)"):
        st.markdown("""
        **Q: Ile razy mogę próbować wykonać kontrakt?**  
        A: Masz **3 próby** na każdy kontrakt. Po 3 nieudanych próbach kontrakt przepada.
        
        **Q: Co się stanie jak przekroczę deadline?**  
        A: Kontrakt automatycznie przepada i tracisz szansę na nagrodę. Uważaj na czas!
        
        **Q: Czy mogę zmienić pracownika?**  
        A: Tak, możesz zwolnić i zatrudnić nowego, ale stracisz bonusy poprzedniego.
        
        **Q: Jak często odświeża się pula kontraktów?**  
        A: Co **24 godziny** (o północy). Możesz też użyć przycisku "Wymuś odświeżenie".
        
        **Q: Co daje wyższy poziom firmy?**  
        A: Więcej miejsc na pracowników, większa pojemność dzienna, dostęp do lepszych kontraktów.
        
        **Q: Czy wydarzenia są obowiązkowe?**  
        A: Wydarzenia pozytywne/negatywne działają automatycznie. Neutralne wymagają wyboru.
        
        **Q: Jak zdobyć najwyższą ocenę kontraktu?**  
        A: Odpowiedz szczegółowo, merytorycznie, użyj wiedzy z kursu. Analityk zwiększa szansę!
        
        **Q: Czy mogę mieć kilku pracowników tego samego typu?**  
        A: Tak, ale pamiętaj o kosztach dziennych i limitach miejsc w firmie.
        """)
    
    st.markdown("---")
    
    st.success("""
    **🎮 Gotowy do gry?**  
    Wróć do zakładki **Dashboard** i zacznij swoją przygodę biznesową!  
    Powodzenia! 🚀
    """)

# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def save_user_data(username, user_data):
    """Zapisuje dane użytkownika"""
    from data.users import load_user_data, save_user_data as save_all_users
    all_users = load_user_data()
    all_users[username] = user_data
    save_all_users(all_users)
