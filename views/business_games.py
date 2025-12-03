"""
Business Games - UI
Widok główny z zakładkami: Dashboard, Rynek Kontraktów, Pracownicy, Rankingi
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
import plotly.graph_objects as go

from data.business_data import FIRM_LEVELS, EMPLOYEE_TYPES, GAME_CONFIG, FIRM_LOGOS, OFFICE_TYPES, OFFICE_UPGRADE_PATH
from data.scenarios import get_available_scenarios, get_scenario
from data.users_sql import save_single_user as save_user_data
from utils.business_game import (
    initialize_business_game, initialize_business_game_with_scenario, refresh_contract_pool, accept_contract,
    submit_contract_solution, submit_contract_conversation, hire_employee, fire_employee,
    calculate_daily_costs, calculate_total_daily_costs, get_firm_summary, get_revenue_chart_data,
    get_category_distribution, calculate_overall_score, can_accept_contract,
    can_hire_employee, update_user_ranking, get_objectives_summary, update_objectives_progress,
    save_ranking_position, get_ranking_chart_data, get_ranking_chart_data_for_players
)
from utils.components import zen_header
from utils.material3_components import apply_material3_theme
from utils.scroll_utils import scroll_to_top

# Importy z modułów refactored
from views.business_games_refactored.helpers import (
    get_contract_reward_coins, get_contract_reward_reputation,
    get_game_data, save_game_data, play_coin_sound
)
from views.business_games_refactored.components.charts import create_financial_chart
from views.business_games_refactored.components.headers import render_header, render_fmcg_header
from views.business_games_refactored.components.event_card import (
    render_active_effects_badge, render_latest_event_card, show_active_event_card
)
from views.business_games_refactored.components.contract_card import (
    render_active_contract_card, render_completed_contract_card, render_contract_card
)
from views.business_games_refactored.components.employee_card import render_employee_card, render_hire_card
from views.business_games_refactored.industries import fmcg

# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def show_business_games(username, user_data):
    """Główna funkcja obsługująca Business Games"""
    
    # Przewiń na górę strony
    scroll_to_top()
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # MIGRACJA: Stara struktura business_game → business_games.consulting
    if "business_game" in user_data and "business_games" not in user_data:
        user_data["business_games"] = {
            "consulting": user_data["business_game"]
        }
        save_user_data(username, user_data)
    
    # Inicjalizacja nowej struktury
    if "business_games" not in user_data:
        user_data["business_games"] = {}
    
    # Sprawdź stan nawigacji
    if "bg_view" not in st.session_state:
        st.session_state["bg_view"] = "home"  # home, industry_selector, scenario_selector, game, rankings
    
    if "selected_industry" not in st.session_state:
        st.session_state["selected_industry"] = None
    
    # Flaga inicjalizacji (ustawiana podczas tworzenia nowej gry)
    if "initializing_game" not in st.session_state:
        st.session_state["initializing_game"] = False
    
    # RESET session_state jeśli selected_industry jest ustawione ale gra nie istnieje
    # TYLKO jeśli NIE jesteśmy w trakcie inicjalizacji
    # ORAZ pomiń dla FMCG i CONSULTING (które mają własną inicjalizację w UI)
    if (st.session_state["selected_industry"] is not None and 
        st.session_state["bg_view"] == "game" and
        st.session_state["selected_industry"] not in user_data.get("business_games", {}) and
        not st.session_state["initializing_game"] and
        st.session_state["selected_industry"] not in ["fmcg", "consulting"]):
        st.warning("⚠️ Znaleziono nieaktualny stan sesji - resetuję...")
        st.session_state["bg_view"] = "home"
        st.session_state["selected_industry"] = None
        st.session_state["selected_industry"] = None
    
    # =========================================================================
    # ROUTING
    # =========================================================================
    
    if st.session_state["bg_view"] == "home":
        show_business_games_home(username, user_data)
    
    elif st.session_state["bg_view"] == "industry_selector":
        show_industry_selector(username, user_data)
    
    elif st.session_state["bg_view"] == "scenario_selector":
        industry_id = st.session_state["selected_industry"]
        show_scenario_selector(username, user_data, industry_id)
    
    elif st.session_state["bg_view"] == "hall_of_fame":
        show_hall_of_fame()
    
    elif st.session_state["bg_view"] == "game":
        industry_id = st.session_state["selected_industry"]
        
        # SPECJALNE ZABEZPIECZENIE: Jeśli initializing_game=True i gra nie istnieje,
        # przeładuj user_data z dysku (może być opóźniony zapis)
        if (st.session_state.get("initializing_game", False) and 
            industry_id not in user_data.get("business_games", {})):
            from data.users_new import get_current_user_data
            user_data = get_current_user_data(username)
            if not user_data:
                st.error("❌ Błąd ładowania danych użytkownika!")
                st.session_state["bg_view"] = "home"
                st.rerun()
        
        # ZABEZPIECZENIE: Sprawdź czy gra dla tej branży istnieje
        # ALE pomiń to sprawdzenie jeśli jesteśmy w trakcie inicjalizacji
        # ORAZ pomiń dla FMCG (które ma własną inicjalizację w UI)
        if (industry_id not in user_data.get("business_games", {}) and 
            not st.session_state.get("initializing_game", False) and
            industry_id != "fmcg"):
            st.error(f"❌ Błąd: Gra dla branży '{industry_id}' nie została zainicjalizowana!")
            st.warning("Zostaniesz przekierowany do wyboru scenariusza...")
            st.session_state["bg_view"] = "scenario_selector"
            st.rerun()
            st.rerun()
        
        show_industry_game(username, user_data, industry_id)


# =============================================================================
# STRONA GŁÓWNA BUSINESS GAMES
# =============================================================================

def show_business_games_home(username, user_data):
    """Strona główna Business Games z menu wyboru"""
    
    zen_header("Business Games Suite")
    
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #667eea;'>🎮 Centrum Gier Biznesowych</h2>
        <p style='color: #64748b; font-size: 16px;'>Wybierz co chcesz zrobić</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pobierz aktywne gry gracza
    active_games = user_data.get("business_games", {})
    
    # Grid 3 kolumny
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # KONTYNUUJ GRY (jeśli są aktywne)
        if active_games:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 30px; border-radius: 20px; text-align: center; 
                        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4); min-height: 300px;
                        display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 64px; margin-bottom: 16px;'>▶️</div>
                <h3 style='color: white; margin: 0 0 12px 0;'>Kontynuuj Gry</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 0;'>
                    Wróć do swoich aktywnych gier biznesowych
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
            
            # Przyciski dla każdej aktywnej gry
            for industry_id, game_data in active_games.items():
                industry_names = {
                    "consulting": "💼 Consulting",
                    "fmcg": "🛒 FMCG",
                    "pharma": "💊 Pharma",
                    "banking": "🏦 Banking",
                    "insurance": "🛡️ Insurance",
                    "automotive": "🚗 Automotive"
                }
                industry_name = industry_names.get(industry_id, industry_id.title())
                
                if st.button(f"▶️ {industry_name}", key=f"continue_{industry_id}", use_container_width=True):
                    st.session_state["selected_industry"] = industry_id
                    st.session_state["bg_view"] = "game"
                    st.rerun()
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%); 
                        padding: 30px; border-radius: 20px; text-align: center; 
                        min-height: 300px;
                        display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 64px; margin-bottom: 16px; opacity: 0.5;'>▶️</div>
                <h3 style='color: #64748b; margin: 0 0 12px 0;'>Brak aktywnych gier</h3>
                <p style='color: #94a3b8; font-size: 14px; margin: 0;'>
                    Rozpocznij nową grę aby zobaczyć tutaj swoje postępy
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # NOWA GRA
        st.markdown("""
        <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 30px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4); min-height: 300px;
                    display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 64px; margin-bottom: 16px;'>🎯</div>
            <h3 style='color: white; margin: 0 0 12px 0;'>Nowa Gra</h3>
            <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 0;'>
                Rozpocznij nową przygodę biznesową w wybranej branży
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
        
        if st.button("🚀 Wybierz branżę", key="new_game", type="primary", use_container_width=True):
            st.session_state["bg_view"] = "industry_selector"
            st.session_state["selected_industry"] = None
            st.rerun()
    
    with col3:
        # HALL OF FAME
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                    padding: 30px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 8px 32px rgba(245, 158, 11, 0.4); min-height: 300px;
                    display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 64px; margin-bottom: 16px;'>🏆</div>
            <h3 style='color: white; margin: 0 0 12px 0;'>Hall of Fame</h3>
            <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 0;'>
                Zobacz najlepszych graczy i legendarne firmy
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
        
        if st.button("👑 Zobacz Hall of Fame", key="hall_of_fame", use_container_width=True):
            st.session_state["bg_view"] = "hall_of_fame"
            st.rerun()


# =============================================================================
# SELECTOR BRANŻY
# =============================================================================

def show_industry_selector(username, user_data):
    """Ekran wyboru branży - karty z różnymi grami branżowymi"""
    
    # Przycisk powrotu do menu głównego
    if st.button("← Powrót do menu", key="back_to_home_from_industries"):
        st.session_state["bg_view"] = "home"
        st.rerun()
    
    zen_header("Business Games Suite")
    
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #667eea;'>🎯 Wybierz swoją specjalizację biznesową</h2>
        <p style='color: #64748b; font-size: 16px;'>Każda branża to unikalna gra z własnymi wyzwaniami i możliwościami</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pierwsza linia - 3 karty branż
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_industry_card(
            industry_id="consulting",
            title="💼 Consulting",
            slogan="Od freelancera do lidera rynku - zbuduj swoją konsultingową potęgę!",
            description="Prowadź firmę konsultingową. Realizuj projekty, zatrudniaj ekspertów, buduj reputację.",
            features=["🎯 Projekty strategiczne", "👥 Team management", "📈 Reputation system"],
            available=True,
            username=username,
            user_data=user_data
        )
    
    with col2:
        render_industry_card(
            industry_id="fmcg",
            title="🛒 FMCG",
            slogan="Od Junior Repa do Chief Sales Officer - zdobądź rynek FMCG!",
            description="Kariera w sprzedaży FMCG. Awansuj przez 10 poziomów, zarządzaj zespołem, buduj market share.",
            features=["� Career progression", "� Team management", "🏪 Territory sales"],
            available=True,  # ✅ WŁĄCZONE!
            username=username,
            user_data=user_data
        )
    
    with col3:
        render_industry_card(
            industry_id="pharma",
            title="💊 Pharma",
            slogan="Od przedstawiciela do lidera sprzedaży - zdominuj rynek farmaceutyczny!",
            description="Zarządzaj sprzedażą farmaceutyczną. Buduj relacje z lekarzami, zdobywaj apteki, ekspanduj.",
            features=["💊 Medical reps", "🏥 KOL relations", "🌍 Market expansion"],
            available=False,
            username=username,
            user_data=user_data
        )
    
    # Druga linia - 3 nowe karty
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    
    with col4:
        render_industry_card(
            industry_id="banking",
            title="🏦 Banking",
            slogan="Od doradcy do prezesa banku - zbuduj imperium finansowe!",
            description="Kieruj bankiem. Oferuj produkty finansowe, zarządzaj kredytami, buduj sieć oddziałów.",
            features=["� Produkty bankowe", "👥 Obsługa klientów", "📊 Portfel kredytowy"],
            available=False,
            username=username,
            user_data=user_data
        )
    
    with col5:
        render_industry_card(
            industry_id="insurance",
            title="🛡️ Insurance",
            slogan="Od agenta do lidera ubezpieczeń - chroń i zarabiaj!",
            description="Rozwijaj firmę ubezpieczeniową. Sprzedawaj polisy, buduj sieć agentów, zarządzaj ryzykiem.",
            features=["📋 Polisy i produkty", "🤝 Sieć agentów", "📈 Zarządzanie ryzykiem"],
            available=False,
            username=username,
            user_data=user_data
        )
    
    with col6:
        render_industry_card(
            industry_id="automotive",
            title="🚗 Automotive",
            slogan="Od dealera do lidera rynku - sprzedaj każdy model!",
            description="Prowadź salon motoryzacyjny. Sprzedawaj pojazdy, zarządzaj serwisem, buduj sieć dealerską.",
            features=["🚙 Sprzedaż pojazdów", "🔧 Serwis i parts", "🏪 Sieć dealerska"],
            available=False,
            username=username,
            user_data=user_data
        )
    
    # Hall of Fame - Galeria legendarnych firm
    st.markdown("---")
    st.markdown("<div style='margin: 40px 0 20px 0;'></div>", unsafe_allow_html=True)
    show_hall_of_fame()

def render_industry_card(industry_id, title, slogan, description, features, available, username, user_data):
    """Renderuje kartę branży"""
    
    # Sprawdź czy gracz ma dane w tej branży
    has_progress = industry_id in user_data.get("business_games", {})
    
    if available:
        card_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: 2px solid #667eea;"
        text_color = "white"
        button_disabled = False
        status_badge = "✅ Dostępne" if not has_progress else "▶️ Kontynuuj"
    else:
        card_style = "background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%); border: 2px solid #cbd5e1;"
        text_color = "#475569"
        button_disabled = True
        status_badge = "🔒 Wkrótce"
    
    # Karta
    st.markdown(f"""
    <div style='{card_style} padding: 24px; border-radius: 16px; min-height: 450px; 
                display: flex; flex-direction: column; color: {text_color};'>
        <h2 style='margin: 0 0 12px 0; font-size: 28px;'>{title}</h2>
        <div style='padding: 8px 16px; background: rgba(255,255,255,0.2); border-radius: 8px; 
                    display: inline-block; margin-bottom: 12px; font-size: 13px; font-weight: 600;'>
            {status_badge}
        </div>
        <p style='margin: 0 0 16px 0; font-size: 15px; font-weight: 600; font-style: italic; line-height: 1.4; 
                   opacity: 0.95; border-left: 3px solid rgba(255,255,255,0.3); padding-left: 12px;'>
            {slogan}
        </p>
        <p style='margin: 16px 0; line-height: 1.6; flex: 1; font-size: 14px;'>{description}</p>
        <div style='margin: 16px 0 0 0;'>
            {''.join([f"<div style='margin: 8px 0; font-size: 13px;'>• {feature}</div>" for feature in features])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Przycisk
    if available:
        button_label = "🎮 Kontynuuj" if has_progress else "🚀 Zacznij grę"
        if st.button(button_label, key=f"start_{industry_id}", type="primary", use_container_width=True):
            # Ustaw aktywną branżę
            st.session_state["selected_industry"] = industry_id
            
            # Jeśli gracz już ma grę w tej branży → idź do gry
            if has_progress:
                st.session_state["bg_view"] = "game"
            else:
                # FMCG ma własny selektor scenariuszy wbudowany w fmcg_playable.py
                # Inne branże używają ogólnego show_scenario_selector()
                if industry_id == "fmcg":
                    # FMCG: Idź od razu do gry, tam jest selektor scenariuszy
                    st.session_state["bg_view"] = "game"
                else:
                    # Inne branże: Pokaż ogólny selektor scenariuszy
                    st.session_state["bg_view"] = "scenario_selector"
            
            st.rerun()
    else:
        st.button("🔒 Wkrótce dostępne", key=f"locked_{industry_id}", disabled=True, use_container_width=True)
    
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

# =============================================================================
# HALL OF FAME - Globalny widok
# =============================================================================

def show_hall_of_fame():
    """Hall of Fame - legendarne zamknięte firmy"""
    
    # Przycisk powrotu do menu głównego
    if st.button("🏠 Powrót do menu głównego", key="back_from_hof"):
        st.session_state["bg_view"] = "home"
        st.rerun()
    
    zen_header("Hall of Fame")
    
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #f59e0b;'>🏛️ Legendarne Firmy</h2>
        <p style='color: #64748b; font-size: 16px;'>Firmy, które osiągnęły sukces i zostały zamknięte z honorem</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    from data.users_new import load_user_data
    all_users = load_user_data()
    
    hall_entries = []
    for user, data in all_users.items():
        if "hall_of_fame" in data:
            for entry in data["hall_of_fame"]:
                hall_entries.append(entry)
    
    if not hall_entries:
        st.info("🏛️ Hall of Fame jest jeszcze pusty. Bądź pierwszym, który zamknie firmę z sukcesem!")
        return
    
    # Filtry
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        # Pobierz unikalne branże
        industries = list(set(e.get("industry_id", "unknown") for e in hall_entries))
        industry_names = {
            "consulting": "💼 Consulting",
            "fmcg": "🛒 FMCG",
            "pharma": "💊 Pharma",
            "banking": "🏦 Banking",
            "insurance": "🛡️ Insurance",
            "automotive": "🚗 Automotive"
        }
        selected_industry = st.selectbox(
            "Branża:",
            ["Wszystkie"] + [industry_names.get(i, i) for i in sorted(industries)],
            key="hof_industry_filter"
        )
    
    with col_filter2:
        # Pobierz unikalne scenariusze
        scenarios = list(set(e.get("scenario_id", "unknown") for e in hall_entries))
        from data.scenarios import get_scenario
        scenario_names_map = {}
        for s_id in scenarios:
            # Spróbuj znaleźć nazwę scenariusza
            for ind_id in industries:
                scenario = get_scenario(ind_id, s_id)
                if scenario:
                    scenario_names_map[s_id] = scenario.get("name", s_id)
                    break
            if s_id not in scenario_names_map:
                scenario_names_map[s_id] = s_id
        
        selected_scenario = st.selectbox(
            "Scenariusz:",
            ["Wszystkie"] + sorted(list(set(scenario_names_map.values()))),
            key="hof_scenario_filter"
        )
    
    with col_filter3:
        sort_by = st.selectbox(
            "Sortuj według:",
            ["Rating (najwyższy)", "Transfer (najwyższy)", "Data zamknięcia (najnowsze)"],
            key="hof_sort"
        )
    
    # Filtruj
    filtered = hall_entries.copy()
    
    if selected_industry != "Wszystkie":
        # Odwróć mapowanie
        industry_id = next((k for k, v in industry_names.items() if v == selected_industry), None)
        if industry_id:
            filtered = [e for e in filtered if e.get("industry_id") == industry_id]
    
    if selected_scenario != "Wszystkie":
        # Znajdź scenario_id dla wybranej nazwy
        scenario_ids = [k for k, v in scenario_names_map.items() if v == selected_scenario]
        if scenario_ids:
            filtered = [e for e in filtered if e.get("scenario_id") in scenario_ids]
    
    # Sortuj
    if sort_by == "Rating (najwyższy)":
        filtered.sort(key=lambda x: x.get("final_score", 0), reverse=True)
    elif sort_by == "Transfer (najwyższy)":
        filtered.sort(key=lambda x: x.get("total_transfer", 0), reverse=True)
    else:  # Data zamknięcia
        filtered.sort(key=lambda x: x.get("closed_at", ""), reverse=True)
    
    st.markdown(f"**Znaleziono:** {len(filtered)} firm")
    st.markdown("---")
    
    # Wyświetl firmy
    for idx, entry in enumerate(filtered[:20], 1):  # Top 20
        industry_icon = industry_names.get(entry.get("industry_id", ""), "🏢")
        firm_name = entry.get("firm_name", "Firma")
        username_display = entry.get("username", "Gracz")
        
        final_score = entry.get("final_score", 0)
        final_level = entry.get("final_level", 1)
        final_reputation = entry.get("final_reputation", 0)
        final_money = entry.get("final_money", 0)
        total_transfer = entry.get("total_transfer", 0)
        closed_at = entry.get("closed_at", "N/A")
        
        # Medal dla TOP 3
        if idx <= 3:
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉"
        else:
            medal = f"#{idx}"
        
        # Kolor karty w zależności od transferu
        if total_transfer >= 100000:
            border_color = "#FFD700"  # Złoty - mega sukces
        elif total_transfer >= 50000:
            border_color = "#C0C0C0"  # Srebrny - duży sukces
        elif total_transfer >= 0:
            border_color = "#4CAF50"  # Zielony - sukces
        else:
            border_color = "#FF5722"  # Czerwony - strata
        
        st.markdown(f"""
        <div style='border-left: 4px solid {border_color}; background: #f9f9f9; 
                    padding: 16px; border-radius: 8px; margin-bottom: 12px;'>
            <div style='display: flex; justify-content: space-between; align-items: start;'>
                <div style='flex: 1;'>
                    <h4 style='margin: 0 0 8px 0;'>{medal} {industry_icon} {firm_name}</h4>
                    <p style='margin: 4px 0; color: #666; font-size: 13px;'>
                        👤 {username_display} · 🎯 {scenario_names_map.get(entry.get('scenario_id', ''), 'Scenariusz')}
                    </p>
                    <p style='margin: 8px 0; font-size: 14px;'>
                        🏆 Rating: <strong>{final_score}</strong> · 
                        📈 Poziom: <strong>{final_level}</strong> · 
                        ⭐ Reputacja: <strong>{final_reputation}</strong>
                    </p>
                    <p style='margin: 4px 0; font-size: 13px; color: #888;'>
                        💼 Saldo końcowe: {final_money:,} PLN · 
                        💰 Transfer: <strong style='color: {"green" if total_transfer >= 0 else "red"};'>{total_transfer:,}</strong> monet
                    </p>
                </div>
                <div style='text-align: right; font-size: 11px; color: #999;'>
                    🗓️ {closed_at}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# SELEKTOR SCENARIUSZY
# =============================================================================

def show_scenario_selector(username, user_data, industry_id):
    """Widok wyboru scenariusza dla wybranej branży"""
    from data.scenarios import get_available_scenarios
    from utils.business_game import initialize_business_game_with_scenario
    
    # Nazwy branż
    industry_names = {
        "consulting": "🎯 Consulting",
        "fmcg": "🛒 FMCG",
        "pharma": "💊 Pharma",
        "banking": "🏦 Banking",
        "insurance": "🛡️ Insurance",
        "automotive": "🚗 Automotive"
    }
    
    # Kompaktowy nagłówek bez zbędnej przestrzeni
    st.markdown(f"<h2 style='margin: 0; padding: 0;'>{industry_names.get(industry_id, 'Business Game')}</h2>", unsafe_allow_html=True)
    st.caption("Wybierz scenariusz rozgrywki")
    
    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    
    # Pobierz dostępne scenariusze
    scenarios = get_available_scenarios(industry_id)
    
    if not scenarios:
        st.warning("Brak dostępnych scenariuszy dla tej branży.")
        return
    
    # Filtruj scenariusze według uprawnień użytkownika
    from utils.permissions import has_access_to_business_game_scenario
    from data.repositories.user_repository import UserRepository
    from database.connection import session_scope
    
    try:
        from database.models import User
        with session_scope() as session:
            user_repo = UserRepository(session)
            user_obj = session.query(User).filter_by(username=username).first()
            user_dict = user_obj.to_dict() if user_obj else {}
            
            # Filtruj scenariusze - zostawiamy tylko te, do których użytkownik ma dostęp
            accessible_scenarios = {
                s_id: s_data for s_id, s_data in scenarios.items()
                if has_access_to_business_game_scenario(s_id, user_dict)
            }
            scenarios = accessible_scenarios
    except Exception as e:
        print(f"Error filtering scenarios: {e}")
        # W przypadku błędu, pozostawiamy wszystkie scenariusze
    
    if not scenarios:
        st.warning("Nie masz dostępu do żadnych scenariuszy w tej branży. Skontaktuj się z administratorem.")
        return
    
    # Sortuj scenariusze - lifetime na końcu
    scenario_list = list(scenarios.items())
    lifetime_scenarios = [s for s in scenario_list if s[1].get("is_lifetime", False)]
    regular_scenarios = [s for s in scenario_list if not s[1].get("is_lifetime", False)]
    scenario_list = regular_scenarios + lifetime_scenarios
    
    # Wyświetl scenariusze w siatce 2x2
    for row in range(0, len(scenario_list), 2):
        cols = st.columns(2)
        
        for col_idx in range(2):
            idx = row + col_idx
            if idx < len(scenario_list):
                scenario_id, scenario_data = scenario_list[idx]
                with cols[col_idx]:
                    render_scenario_card(scenario_id, scenario_data, industry_id, username, user_data)
    
    # Przycisk powrotu na dole
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
    if st.button("← Powrót do wyboru branży", key="back_to_industries", use_container_width=True):
        st.session_state["selected_industry"] = None
        st.session_state["bg_view"] = "industry_selector"
        st.rerun()

def render_scenario_card(scenario_id, scenario_data, industry_id, username, user_data):
    """Renderuje kartę pojedynczego scenariusza w stylu spójnym z kartami kontraktów
    
    Returns:
        bool: True jeśli gra została rozpoczęta (przycisk kliknięty), False w przeciwnym razie
    """
    
    # Sprawdź czy to tryb lifetime
    is_lifetime = scenario_data.get("is_lifetime", False)
    
    # Mapowanie trudności na kolory (spójne z resztą UI)
    difficulty_config = {
        "easy": {
            "gradient": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            "badge": "🟢 Łatwy",
            "accent": "#10b981",
            "glow": "0 0 20px rgba(16, 185, 129, 0.3)"
        },
        "medium": {
            "gradient": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
            "badge": "🟡 Średni",
            "accent": "#f59e0b",
            "glow": "0 0 20px rgba(245, 158, 11, 0.3)"
        },
        "hard": {
            "gradient": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
            "badge": "🔴 Trudny",
            "accent": "#ef4444",
            "glow": "0 0 20px rgba(239, 68, 68, 0.3)"
        },
        "expert": {
            "gradient": "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)",
            "badge": "💜 Ekspert",
            "accent": "#8b5cf6",
            "glow": "0 0 20px rgba(139, 92, 246, 0.4)"
        },
        "open": {
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "badge": "♾️ OPEN",
            "accent": "#667eea",
            "glow": "0 0 20px rgba(102, 126, 234, 0.4)"
        }
    }
    
    difficulty = scenario_data.get("difficulty", "medium")
    config = difficulty_config.get(difficulty, difficulty_config["medium"])
    
    # Pobierz dane scenariusza
    initial = scenario_data.get('initial_conditions', {})
    
    # CONSULTING: money, reputation, office
    # FMCG: level, monthly_sales, market_share
    is_fmcg = industry_id == "fmcg"
    
    if is_fmcg:
        param1_label = "Poziom kariery"
        param1_value = f"⭐ Lvl {initial.get('level', 1)}"
        param1_color = "#667eea"
        
        param2_label = "Monthly Sales"
        param2_value = f"💰 {initial.get('monthly_sales', 0):,}"
        param2_color = "#10b981"
        
        param3_label = "Market Share"
        param3_value = f"📊 {initial.get('market_share', 0)}%"
        param3_color = "#8b5cf6"
    else:
        # CONSULTING
        money = initial.get('money', 50000)
        reputation = initial.get('reputation', 50)
        office = initial.get('office_type', 'home_office')
        office_name = office.replace('_', ' ').title()
        
        param1_label = "Kapitał startowy"
        param1_value = f"💰 {money:,}"
        param1_color = "#10b981"
        
        param2_label = "Reputacja"
        param2_value = f"⭐ {reputation}"
        param2_color = "#f59e0b"
        
        param3_label = "Biuro"
        param3_value = f"🏢 {office_name}"
        param3_color = "#8b5cf6"
    
    objectives = scenario_data.get('objectives', [])
    total_reward = sum(obj.get('reward_money', 0) for obj in objectives) if not is_lifetime else 0
    
    # Karta w stylu kontraktów - HTML bez wcięć w środku
    html_content = f"""<div style="background: white; border-radius: 20px; padding: 24px; margin: 16px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1), {config["glow"]}; border-left: 6px solid {config["accent"]}; transition: all 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
<div style="flex: 1;">
<div style="font-size: 32px; margin-bottom: 8px;">{scenario_data.get('icon', '🎮')}</div>
<h3 style="margin: 0; color: #1e293b; font-size: 20px; font-weight: 700;">{scenario_data.get('name', 'Scenariusz')}</h3>
<p style="margin: 4px 0 0 0; color: #64748b; font-size: 14px;">{industry_id.upper()} • {'Tryb nieskończony' if is_lifetime else f'{len(objectives)} celów'}</p>
</div>
<div style="background: {config["gradient"]}; color: white; padding: 12px 20px; border-radius: 12px; text-align: center; min-width: 120px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
<div style="font-size: 18px; font-weight: 700; margin-bottom: 4px;">{config["badge"]}</div>
<div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">POZIOM</div>
</div>
</div>
<div style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
<div style="color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; font-weight: 600;">📖 Opis scenariusza</div>
<div style="color: #334155; font-size: 14px; line-height: 1.6;">{scenario_data.get('description', '')}</div>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e8f0;">
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">{param1_label}</div>
<div style="color: {param1_color}; font-size: 18px; font-weight: 700;">{param1_value}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">{param2_label}</div>
<div style="color: {param2_color}; font-size: 18px; font-weight: 700;">{param2_value}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">{param3_label}</div>
<div style="color: {param3_color}; font-size: 18px; font-weight: 700;">{param3_value}</div>
</div>
</div>
</div>"""
    
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Szczegóły scenariusza w expanderze - profesjonalny layout
    with st.expander("📋 Cele i modyfikatory", expanded=False):
        # Cele - tylko jeśli to NIE jest tryb lifetime
        if objectives and not is_lifetime:
            objectives_html = ""
            for obj in objectives:
                reward = obj.get('reward_money', 0)
                desc = obj.get('description', 'Cel')
                objectives_html += f"<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px; display: flex; justify-content: space-between; align-items: center;'><span>✓ {desc}</span><span style='color: #10b981; font-weight: 700;'>💎 {reward:,} PLN</span></div>"
            
            st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #667eea; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px;'>
<div style='color: #667eea; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>🎯 CELE DO OSIĄGNIĘCIA</div>
{objectives_html}
<div style='margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(102, 126, 234, 0.2); text-align: center; color: #667eea; font-size: 15px; font-weight: 700;'>Łączna nagroda: 💎 {total_reward:,} PLN</div>
</div>
            """, unsafe_allow_html=True)
        elif is_lifetime:
            st.markdown("""
<div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #8b5cf6; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px;'>
<div style='color: #8b5cf6; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 8px;'>♾️ TRYB NIESKOŃCZONY</div>
<div style='color: #334155; font-size: 14px; line-height: 1.6;'>Graj bez ograniczeń i rywalizuj z innymi o najwyższy wynik w rankingu! Buduj swoją firmę, realizuj kontrakty i zdobywaj doświadczenie bez limitów czasowych czy celów do osiągnięcia.</div>
</div>
            """, unsafe_allow_html=True)
        
        # Modyfikatory jeśli istnieją
        modifiers = scenario_data.get('modifiers', {})
        has_modifiers = any(v != 1.0 for v in modifiers.values() if isinstance(v, (int, float)))
        
        if has_modifiers:
            modifiers_html = ""
            
            if modifiers.get('reputation_gain_multiplier', 1.0) != 1.0:
                mult = modifiers['reputation_gain_multiplier']
                change = f"+{int((mult - 1) * 100)}%" if mult > 1 else f"{int((mult - 1) * 100)}%"
                color = "#10b981" if mult > 1 else "#ef4444"
                modifiers_html += f"<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px; display: flex; justify-content: space-between; align-items: center;'><span>⭐ Zmiany reputacji</span><span style='color: {color}; font-weight: 700;'>{change}</span></div>"
            
            if modifiers.get('revenue_multiplier', 1.0) != 1.0:
                mult = modifiers['revenue_multiplier']
                change = f"+{int((mult - 1) * 100)}%" if mult > 1 else f"{int((mult - 1) * 100)}%"
                color = "#10b981" if mult > 1 else "#ef4444"
                modifiers_html += f"<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px; display: flex; justify-content: space-between; align-items: center;'><span>💵 Przychody</span><span style='color: {color}; font-weight: 700;'>{change}</span></div>"
            
            if modifiers.get('cost_multiplier', 1.0) != 1.0:
                mult = modifiers['cost_multiplier']
                change = f"+{int((mult - 1) * 100)}%" if mult > 1 else f"{int((mult - 1) * 100)}%"
                color = "#ef4444" if mult > 1 else "#10b981"
                modifiers_html += f"<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px; display: flex; justify-content: space-between; align-items: center;'><span>💸 Koszty</span><span style='color: {color}; font-weight: 700;'>{change}</span></div>"
            
            st.markdown(f"""
<div style='background: linear-gradient(135deg, #f59e0b15 0%, #d9770615 100%); border-left: 4px solid #f59e0b; border-radius: 12px; padding: 16px 20px;'>
<div style='color: #f59e0b; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>⚙️ MODYFIKATORY SCENARIUSZA</div>
{modifiers_html}
</div>
            """, unsafe_allow_html=True)
    
    # Przycisk rozpoczęcia - profesjonalny, pełna szerokość
    if st.button(f"🚀 Rozpocznij {scenario_data.get('name', 'scenariusz')}", 
                 key=f"start_scenario_{scenario_id}", 
                 type="primary", 
                 use_container_width=True):
        # Inicjalizuj grę z tym scenariuszem
        try:
            # WAŻNE: Ustaw flagę PRZED zapisem - ochroni przed resetem podczas st.rerun()
            st.session_state["initializing_game"] = True
            
            # KLUCZOWE: Załaduj świeże user_data z dysku przed modyfikacją
            from data.users_new import get_current_user_data
            fresh_user_data = get_current_user_data(username)
            
            if not fresh_user_data:
                st.error("❌ Błąd ładowania danych użytkownika!")
                st.session_state["initializing_game"] = False
                return False
            
            # Inicjalizuj FMCG game
            bg_data = initialize_business_game_with_scenario(username, industry_id, scenario_id)
            
            # Upewnij się, że business_games istnieje
            if "business_games" not in fresh_user_data:
                fresh_user_data["business_games"] = {}
            
            # Zapisz dane FMCG
            fresh_user_data["business_games"][industry_id] = bg_data
            
            # KLUCZOWE: Zapisz bezpośrednio do JSON (omiń repository z wadliwą migracją)
            import json
            try:
                with open('users_data.json', 'r', encoding='utf-8') as f:
                    all_users = json.load(f)
                all_users[username] = fresh_user_data
                with open('users_data.json', 'w', encoding='utf-8') as f:
                    json.dump(all_users, f, indent=2, ensure_ascii=False)
            except Exception as e:
                st.error(f"❌ Błąd zapisu: {e}")
                st.session_state["initializing_game"] = False
                return False
            
            # Ustaw bg_view (NIE resetuj initializing_game - zostanie zresetowane w show_industry_game)
            st.session_state["bg_view"] = "game"
            
            st.success(f"🎉 Scenariusz '{scenario_data.get('name')}' rozpoczęty! Powodzenia!")
            st.rerun()  # Przeładuj stronę, żeby pokazać dashboard
        except Exception as e:
            st.session_state["initializing_game"] = False  # Reset tylko przy błędzie
            st.error(f"❌ Błąd inicjalizacji: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    return False  # Gra nie została rozpoczęta

# =============================================================================
# FMCG TABS
# =============================================================================

def show_fmcg_company_info_tab(username, user_data, industry_id):
    """Zakładka z informacjami o firmie FreshLife Poland i portfolio produktów"""
    from data.industries.fmcg_company import COMPANY_INFO, PRODUCT_PORTFOLIO
    
    st.markdown("# 🏢 FreshLife Poland - Twoja Firma")
    
    # Sekcja O Firmie
    st.markdown("## 📋 O Firmie")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
**{COMPANY_INFO['full_name']}**

{COMPANY_INFO['description']}

**Misja:** {COMPANY_INFO['mission']}
""")
    
    with col2:
        st.markdown(f"""
**📊 Dane Podstawowe**
- **Rok założenia:** {COMPANY_INFO['founded']}
- **Firma matka:** {COMPANY_INFO['parent_company']}
- **Pracownicy:** {COMPANY_INFO['employees_poland']}
- **Siedziba:** {COMPANY_INFO['hq_location']}
""")
    
    # Wartości firmy
    st.markdown("### 💎 Nasze Wartości")
    cols = st.columns(len(COMPANY_INFO['values']))
    for i, value in enumerate(COMPANY_INFO['values']):
        with cols[i]:
            st.info(f"**{value}**")
    
    # Pozycja rynkowa
    st.markdown("### 📈 Pozycja Rynkowa")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;'>
    <div style='font-size: 24px; margin-bottom: 8px;'>🧴</div>
    <div style='font-size: 14px; opacity: 0.9;'>Personal Care</div>
    <div style='font-size: 20px; font-weight: 700; margin-top: 8px;'>{COMPANY_INFO['market_position']['personal_care']}</div>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;'>
    <div style='font-size: 24px; margin-bottom: 8px;'>🍽️</div>
    <div style='font-size: 14px; opacity: 0.9;'>Food & Beverages</div>
    <div style='font-size: 20px; font-weight: 700; margin-top: 8px;'>{COMPANY_INFO['market_position']['food']}</div>
</div>
""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;'>
    <div style='font-size: 24px; margin-bottom: 8px;'>🏠</div>
    <div style='font-size: 14px; opacity: 0.9;'>Home Care</div>
    <div style='font-size: 20px; font-weight: 700; margin-top: 8px;'>{COMPANY_INFO['market_position']['home_care']}</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Portfolio Produktów
    st.markdown("## 🛍️ Portfolio Produktów")
    st.info("💡 **Wskazówka:** Zapoznaj się z naszymi produktami - przydadzą Ci się w rozmowach z klientami!")
    
    # Zakładki dla kategorii
    tab_pc, tab_food, tab_hc = st.tabs(["🧴 Personal Care", "🍽️ Food & Beverages", "🏠 Home Care"])
    
    with tab_pc:
        show_product_category(PRODUCT_PORTFOLIO['personal_care'])
    
    with tab_food:
        show_product_category(PRODUCT_PORTFOLIO['food'])
    
    with tab_hc:
        show_product_category(PRODUCT_PORTFOLIO['home_care'])


def show_product_category(category):
    """Wyświetla produkty z danej kategorii"""
    st.markdown(f"### {category['category_name']}")
    st.markdown(f"*{category['description']}*")
    st.markdown(f"**Udział w rynku:** {category['market_share']}%")
    
    st.markdown("---")
    
    for product in category['products']:
        with st.expander(f"📦 **{product['name']}** - {product['subcategory']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
**USP (Unique Selling Proposition):**  
{product['usp']}

**Warianty:**  
{', '.join(product['variants'])}

**Grupa docelowa:** {product['target_group']}

**Opakowanie:** {product['packaging']}

**Termin przydatności:** {product['shelf_life']}
""")
                
                if product.get('awards'):
                    st.markdown(f"**🏆 Nagrody:** {', '.join(product['awards'])}")
            
            with col2:
                st.markdown(f"""
<div style='background: #f8fafc; padding: 16px; border-radius: 8px; border: 2px solid #e2e8f0;'>
    <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>Cena detaliczna</div>
    <div style='font-size: 18px; font-weight: 700; color: #0f172a;'>{product['price_range']}</div>
    
    <div style='font-size: 12px; color: #64748b; margin-top: 12px; margin-bottom: 4px;'>Marża</div>
    <div style='font-size: 18px; font-weight: 700; color: #10b981;'>{product['margin_percent']}%</div>
    
    <div style='font-size: 12px; color: #64748b; margin-top: 12px; margin-bottom: 4px;'>Potencjał wolumenu</div>
    <div style='font-size: 16px; font-weight: 600; color: #8b5cf6;'>{product['volume_potential'].upper()}</div>
</div>
""", unsafe_allow_html=True)


def show_fmcg_dashboard_tab(username, user_data, industry_id):
    """Dashboard FMCG - przegląd kariery, cele, postępy"""
    bg_data = user_data["business_games"][industry_id]
    
    from data.industries.fmcg import CAREER_LEVELS as FMCG_LEVELS
    from data.scenarios import get_scenario
    
    career = bg_data["career"]
    metrics = bg_data["metrics"]
    level = career["level"]
    scenario_id = bg_data.get("scenario_id")
    
    # 📋 CELE SCENARIUSZA
    st.markdown("### 🎯 Cele Scenariusza")
    
    if scenario_id:
        scenario = get_scenario("fmcg", scenario_id)
        objectives = bg_data.get("scenario_objectives", [])
        completed = bg_data.get("objectives_completed", [])
        
        if objectives:
            for i, obj in enumerate(objectives):
                is_completed = i in completed
                icon = "✅" if is_completed else "⏳"
                progress_color = "#10b981" if is_completed else "#f59e0b"
                
                st.markdown(f"""
                <div style='background: white; padding: 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid {progress_color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <strong>{icon} {obj['description']}</strong>
                        </div>
                        <div style='color: {progress_color}; font-weight: 700;'>
                            {obj.get('reward_money', 0):,} PLN
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Brak celów dla tego scenariusza.")
    else:
        st.info("Tryb swobodny - brak celów scenariusza.")
    
    st.markdown("---")
    
    # 📊 POSTĘP KARIERY
    st.markdown("### 📈 Postęp Kariery")
    
    level_info = FMCG_LEVELS[level]
    next_level = level + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        html = f"""<div class='game-card'>
<h4 style='margin-top:0;'>💼 Obecna Pozycja</h4>
<p style='font-size: 18px; font-weight: 700; color: #8b5cf6;'>{career['title']}</p>
<p style='opacity: 0.8;'>Poziom {level}/10</p>
<p style='font-size: 13px; margin-top: 12px;'><strong>Obowiązki:</strong></p>
<ul style='font-size: 12px; opacity: 0.9;'>
{"".join([f"<li>{resp}</li>" for resp in level_info['responsibilities'][:3]])}
</ul>
</div>"""
        st.markdown(html, unsafe_allow_html=True)
    
    with col2:
        if next_level <= 10:
            next_level_info = FMCG_LEVELS[next_level]
            required = next_level_info['required_metrics']
            
            # Oblicz progress
            sales_progress = min(100, (metrics.get('monthly_sales', 0) / required.get('monthly_sales', 1)) * 100) if 'monthly_sales' in required else 0
            share_progress = min(100, (metrics.get('market_share', 0) / required.get('market_share', 1)) * 100) if 'market_share' in required else 0
            csat_progress = min(100, (metrics.get('customer_satisfaction', 0) / required.get('customer_satisfaction', 1)) * 100) if 'customer_satisfaction' in required else 0
            
            # Zbuduj HTML (bez wcięć!)
            html = f"""<div class='game-card'>
<h4 style='margin-top:0;'>🎯 Następny Poziom</h4>
<p style='font-size: 18px; font-weight: 700; color: #10b981;'>{next_level_info['role']}</p>
<p style='opacity: 0.8;'>Poziom {next_level}/10</p>
<p style='font-size: 13px; margin-top: 12px;'><strong>Wymagania:</strong></p>
<div style='margin-top: 8px;'>
<div style='font-size: 12px; margin-bottom: 4px;'>💰 Sprzedaż: {metrics.get('monthly_sales', 0):,.0f} / {required.get('monthly_sales', 0):,.0f} PLN</div>
<div style='background: #e2e8f0; border-radius: 4px; height: 6px;'>
<div style='background: #f59e0b; height: 100%; width: {sales_progress}%; border-radius: 4px;'></div>
</div>
<div style='font-size: 12px; margin-bottom: 4px; margin-top: 8px;'>📊 Market Share: {metrics.get('market_share', 0):.1f}% / {required.get('market_share', 0)}%</div>
<div style='background: #e2e8f0; border-radius: 4px; height: 6px;'>
<div style='background: #8b5cf6; height: 100%; width: {share_progress}%; border-radius: 4px;'></div>
</div>
<div style='font-size: 12px; margin-bottom: 4px; margin-top: 8px;'>⭐ CSAT: {metrics.get('customer_satisfaction', 0)}% / {required.get('customer_satisfaction', 0)}%</div>
<div style='background: #e2e8f0; border-radius: 4px; height: 6px;'>
<div style='background: #10b981; height: 100%; width: {csat_progress}%; border-radius: 4px;'></div>
</div>
</div>
</div>"""
            
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.success("🏆 Osiągnąłeś najwyższy poziom - Chief Sales Officer!")
    
    # =============================================================================
    # RANKINGI - Na dole Dashboard
    # =============================================================================
    
    st.markdown("---")
    st.markdown("<div style='margin: 40px 0 20px 0;'></div>", unsafe_allow_html=True)
    show_rankings_content(username, user_data, industry_id)


def show_fmcg_tasks_tab(username, user_data, industry_id):
    """Zadania - dostępne zadania do wykonania"""
    from data.industries.fmcg_tasks import get_random_tasks, get_task_by_id
    
    bg_data = user_data["business_games"][industry_id]
    career = bg_data["career"]
    metrics = bg_data["metrics"]
    level = career["level"]
    
    # Pobierz zadania
    active_tasks = bg_data.get("tasks", {}).get("active", [])
    available_pool = bg_data.get("tasks", {}).get("available_pool", [])
    
    if not available_pool or len(available_pool) < 5:
        # Wygeneruj 6 losowych zadań dla poziomu
        new_tasks = get_random_tasks(level, count=6)
        
        # Zapisz do bg_data
        if "tasks" not in bg_data:
            bg_data["tasks"] = {"active": [], "completed": [], "available_pool": []}
        bg_data["tasks"]["available_pool"] = new_tasks
        
        # Zapisz do user_data
        from data.users_new import save_single_user
        save_single_user(username, user_data)
        
        # Odśwież available_pool ze zapisanych danych (bez rerun!)
        available_pool = new_tasks
    
    # =============================================================================
    # AKTYWNE ZADANIA
    # =============================================================================
    if active_tasks:
        st.markdown("### ⚡ Aktywne Zadania")
        st.markdown("Twoje bieżące zadania. Kliknij 'Wykonaj' aby je rozwiązać.")
        
        for task_id in active_tasks:
            task = get_task_by_id(task_id)
            if not task:
                continue
            
            # Mapowanie kategorii
            category_config = {
                "field_sales": {"emoji": "🚗", "color": "#3b82f6", "name": "Sprzedaż w Terenie"},
                "key_accounts": {"emoji": "🏢", "color": "#8b5cf6", "name": "Key Accounts"},
                "team_management": {"emoji": "👥", "color": "#10b981", "name": "Zarządzanie Zespołem"},
                "trade_marketing": {"emoji": "📊", "color": "#f59e0b", "name": "Trade Marketing"},
                "strategy": {"emoji": "🎯", "color": "#ec4899", "name": "Strategia"},
                "crisis": {"emoji": "⚠️", "color": "#ef4444", "name": "Kryzys"}
            }
            cat_info = category_config.get(task["category"], {"emoji": "📋", "color": "#64748b", "name": task["category"]})
            
            with st.expander(f"{cat_info['emoji']} **{task['title']}** - {cat_info['name']}", expanded=False):
                st.markdown(f"**Sytuacja:**")
                st.markdown(task['scenario'])
                
                st.markdown("---")
                st.markdown("**💡 Jak chcesz rozwiązać to zadanie?**")
                
                solution = st.text_area(
                    "Twoje rozwiązanie:",
                    placeholder="Opisz swoje podejście do rozwiązania tego zadania (min. 50 znaków)...",
                    key=f"solution_{task_id}",
                    height=150
                )
                
                col_submit, col_cancel = st.columns([1, 1])
                
                with col_submit:
                    if st.button("✅ Wyślij rozwiązanie", key=f"submit_{task_id}", use_container_width=True):
                        if len(solution.strip()) < 50:
                            st.error("⚠️ Rozwiązanie musi mieć co najmniej 50 znaków!")
                        else:
                            # WYKONAJ ZADANIE
                            # Podstawowa ocena jakości (bez AI - na podstawie długości)
                            quality_score = min(1.0, len(solution.strip()) / 200)  # Max 1.0 przy 200+ znakach
                            
                            # Oblicz nagrody z modyfikatorem jakości (FMCG uses direct keys)
                            actual_sales = int(task.get('sales_impact', 0) * quality_score)
                            actual_share = task.get('reputation_impact', 0) * quality_score
                            actual_csat = task.get('satisfaction_impact', 0) * quality_score  # if exists
                            actual_money = int(task.get('base_reward', 0) * quality_score)
                            
                            # Aktualizuj metryki
                            metrics['monthly_sales'] = metrics.get('monthly_sales', 0) + actual_sales
                            metrics['market_share'] = min(100, metrics.get('market_share', 0) + actual_share)
                            if actual_csat > 0:
                                metrics['customer_satisfaction'] = min(100, metrics.get('customer_satisfaction', 0) + actual_csat)
                            
                            # Aktualizuj finanse (jeśli istnieją)
                            if 'finances' in bg_data:
                                bg_data['finances']['cash'] = bg_data['finances'].get('cash', 0) + actual_money
                            
                            # Przenieś zadanie do completed
                            bg_data["tasks"]["active"].remove(task_id)
                            if "completed" not in bg_data["tasks"]:
                                bg_data["tasks"]["completed"] = []
                            bg_data["tasks"]["completed"].append({
                                "task_id": task_id,
                                "solution": solution,
                                "quality_score": quality_score,
                                "rewards_earned": {
                                    "sales": actual_sales,
                                    "market_share": actual_share,
                                    "csat": actual_csat,
                                    "money": actual_money
                                }
                            })
                            
                            # Sprawdź cele scenariusza
                            scenario_id = bg_data.get("scenario_id")
                            if scenario_id:
                                objectives = bg_data.get("scenario_objectives", [])
                                completed_objectives = bg_data.get("objectives_completed", [])
                                
                                for idx, obj in enumerate(objectives):
                                    if idx not in completed_objectives:
                                        # Sprawdź warunki
                                        completed = True
                                        if 'required_sales' in obj and metrics.get('monthly_sales', 0) < obj['required_sales']:
                                            completed = False
                                        if 'required_market_share' in obj and metrics.get('market_share', 0) < obj['required_market_share']:
                                            completed = False
                                        if 'required_tasks' in obj and len(bg_data["tasks"]["completed"]) < obj['required_tasks']:
                                            completed = False
                                        
                                        if completed:
                                            completed_objectives.append(idx)
                                            # Dodaj nagrodę za cel
                                            if 'reward_money' in obj:
                                                if 'finances' in bg_data:
                                                    bg_data['finances']['cash'] = bg_data['finances'].get('cash', 0) + obj['reward_money']
                                
                                bg_data["objectives_completed"] = completed_objectives
                            
                            # Sprawdź awans
                            from data.industries.fmcg import can_advance_to_next_level, get_career_stage, CAREER_LEVELS as FMCG_LEVELS
                            career_stage = get_career_stage(career['level'])
                            can_advance, advance_reason = can_advance_to_next_level(career['level'], metrics, career_stage)
                            
                            # Zapisz BEZPOŚREDNIO do JSON (workaround dla repository bug)
                            import json
                            users_file = "users_data.json"
                            with open(users_file, "r", encoding="utf-8") as f:
                                all_users = json.load(f)
                            all_users[username] = user_data
                            with open(users_file, "w", encoding="utf-8") as f:
                                json.dump(all_users, f, ensure_ascii=False, indent=2)
                            
                            # Pokaż rezultat
                            st.success(f"✅ Zadanie wykonane!")
                            st.balloons()
                            
                            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                            with col_r1:
                                st.metric("💰 Sprzedaż", f"+{actual_sales:,} PLN")
                            with col_r2:
                                st.metric("📊 Market Share", f"+{actual_share:.1f}%")
                            with col_r3:
                                st.metric("⭐ CSAT", f"+{actual_csat:.0f}%")
                            with col_r4:
                                st.metric("💵 Gotówka", f"+{actual_money:,} PLN")
                            
                            if can_advance:
                                next_level = career['level'] + 1
                                next_role = FMCG_LEVELS[next_level]['role']
                                st.success(f"🎉 Gratulacje! Możesz awansować na: **{next_role}**!")
                            
                            st.rerun()
                
                with col_cancel:
                    if st.button("❌ Anuluj zadanie", key=f"cancel_{task_id}", use_container_width=True):
                        # Usuń z aktywnych, dodaj z powrotem do available_pool
                        bg_data["tasks"]["active"].remove(task_id)
                        
                        # Dodaj pełny obiekt zadania z powrotem do available_pool
                        bg_data["tasks"]["available_pool"].append(task)
                        
                        # Zapisz BEZPOŚREDNIO do JSON (workaround dla repository bug)
                        import json
                        users_file = "users_data.json"
                        with open(users_file, "r", encoding="utf-8") as f:
                            all_users = json.load(f)
                        all_users[username] = user_data
                        with open(users_file, "w", encoding="utf-8") as f:
                            json.dump(all_users, f, ensure_ascii=False, indent=2)
                        
                        st.warning(f"⚠️ Anulowano zadanie: {task['title']}")
                        st.rerun()
        
        st.markdown("---")
    
    # =============================================================================
    # DOSTĘPNE ZADANIA
    # =============================================================================
    st.markdown("### 💼 Dostępne Zadania")
    st.markdown("Wybierz zadanie aby je zaakceptować. Możesz mieć maksymalnie 3 aktywne zadania jednocześnie.")
    
    # Wyświetl ile aktywnych zadań ma użytkownik
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.metric("Aktywne zadania", f"{len(active_tasks)}/3")
    with col_info2:
        st.metric("Dostępne zadania", len(available_pool))
    
    st.markdown("---")
    
    # Mapowanie kategorii i trudności (wspólne dla wszystkich zadań)
    category_config = {
        "field_sales": {"emoji": "🚗", "color": "#3b82f6", "name": "Sprzedaż w Terenie"},
        "key_accounts": {"emoji": "🏢", "color": "#8b5cf6", "name": "Key Accounts"},
        "team_management": {"emoji": "👥", "color": "#10b981", "name": "Zarządzanie Zespołem"},
        "trade_marketing": {"emoji": "📊", "color": "#f59e0b", "name": "Trade Marketing"},
        "strategy": {"emoji": "🎯", "color": "#ec4899", "name": "Strategia"},
        "crisis": {"emoji": "⚠️", "color": "#ef4444", "name": "Kryzys"}
    }
    
    difficulty_config = {
        "easy": {"label": "Łatwe", "color": "#10b981"},
        "medium": {"label": "Średnie", "color": "#f59e0b"},
        "hard": {"label": "Trudne", "color": "#ef4444"}
    }
    
    # Filtruj available_pool - usuń zadania które są już aktywne (fix dla duplikatów)
    available_pool_filtered = [t for t in available_pool if t['id'] not in active_tasks]
    
    # Wyświetl zadania w gridzie 2 kolumny
    for i in range(0, len(available_pool_filtered), 2):
        col1, col2 = st.columns(2)
        
        # Zadanie 1
        with col1:
            if i < len(available_pool_filtered):
                task = available_pool_filtered[i]  # available_pool zawiera pełne obiekty zadań, nie ID!
                
                if task:
                    cat_info = category_config.get(task["category"], {"emoji": "📋", "color": "#64748b", "name": task["category"]})
                    diff_info = difficulty_config.get(task["difficulty"], {"label": "?", "color": "#64748b"})
                    
                    html = f"""<div class='game-card' style='border-left: 4px solid {cat_info['color']}; min-height: 280px;'>
<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
<div>
<span style='font-size: 20px;'>{cat_info['emoji']}</span>
<span style='font-size: 13px; color: {cat_info['color']}; font-weight: 600; margin-left: 8px;'>{cat_info['name']}</span>
</div>
<span style='background: {diff_info['color']}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 700;'>{diff_info['label']}</span>
</div>
<h4 style='margin: 8px 0; font-size: 16px; line-height: 1.4;'>{task['title']}</h4>
<p style='font-size: 13px; opacity: 0.8; margin: 12px 0; line-height: 1.5;'>{task['scenario'][:120]}...</p>
<div style='margin-top: 16px; padding-top: 12px; border-top: 1px solid #e2e8f0;'>
<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>
<strong>Nagrody:</strong>
</div>
<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 11px;'>
<div>💰 Sprzedaż: +{task.get('sales_impact', 0):,} PLN</div>
<div>📊 Market Share: +{task.get('reputation_impact', 0)}%</div>
<div>💵 Gotówka: +{task.get('base_reward', 0):,} PLN</div>
<div>⏱️ Czas: {task.get('time_days', 1)} dni</div>
</div>
</div>
</div>"""
                    
                    st.markdown(html, unsafe_allow_html=True)
                    
                    # Przycisk akceptacji
                    can_accept = len(active_tasks) < 3
                    if can_accept:
                        if st.button(f"✅ Akceptuj zadanie", key=f"accept_{task['id']}", use_container_width=True):
                            # Sprawdź czy zadanie już nie jest w active (fix dla duplikatów)
                            if task['id'] not in bg_data["tasks"]["active"]:
                                # Dodaj do aktywnych zadań (tylko ID!)
                                bg_data["tasks"]["active"].append(task['id'])
                                
                                # Usuń z available_pool - znajdź zadanie po ID i usuń
                                bg_data["tasks"]["available_pool"] = [
                                    t for t in bg_data["tasks"]["available_pool"] 
                                    if t['id'] != task['id']
                                ]
                                
                                # Zapisz BEZPOŚREDNIO do JSON (workaround dla repository bug)
                                import json
                                users_file = "users_data.json"
                                with open(users_file, "r", encoding="utf-8") as f:
                                    all_users = json.load(f)
                                all_users[username] = user_data
                                with open(users_file, "w", encoding="utf-8") as f:
                                    json.dump(all_users, f, ensure_ascii=False, indent=2)
                                
                                st.success(f"✅ Zaakceptowano zadanie: {task['title']}")
                            st.rerun()
                    else:
                        st.button("❌ Limit aktywnych zadań (3/3)", key=f"limit_{task['id']}", disabled=True, use_container_width=True)
        
        # Zadanie 2
        with col2:
            if i+1 < len(available_pool_filtered):
                task = available_pool_filtered[i+1]  # available_pool zawiera pełne obiekty zadań, nie ID!
                
                if task:
                    cat_info = category_config.get(task["category"], {"emoji": "📋", "color": "#64748b", "name": task["category"]})
                    diff_info = difficulty_config.get(task["difficulty"], {"label": "?", "color": "#64748b"})
                    
                    html = f"""<div class='game-card' style='border-left: 4px solid {cat_info['color']}; min-height: 280px;'>
<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
<div>
<span style='font-size: 20px;'>{cat_info['emoji']}</span>
<span style='font-size: 13px; color: {cat_info['color']}; font-weight: 600; margin-left: 8px;'>{cat_info['name']}</span>
</div>
<span style='background: {diff_info['color']}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 700;'>{diff_info['label']}</span>
</div>
<h4 style='margin: 8px 0; font-size: 16px; line-height: 1.4;'>{task['title']}</h4>
<p style='font-size: 13px; opacity: 0.8; margin: 12px 0; line-height: 1.5;'>{task.get('description', task['scenario'][:120])}...</p>
<div style='margin-top: 16px; padding-top: 12px; border-top: 1px solid #e2e8f0;'>
<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>
<strong>Nagrody:</strong>
</div>
<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 11px;'>
<div>💰 Sprzedaż: +{task.get('sales_impact', 0):,} PLN</div>
<div>📊 Market Share: +{task.get('reputation_impact', 0)}%</div>
<div>💵 Gotówka: +{task.get('base_reward', 0):,} PLN</div>
<div>⏱️ Czas: {task.get('time_days', 1)} dni</div>
</div>
</div>
</div>"""
                    
                    st.markdown(html, unsafe_allow_html=True)
                    
                    can_accept = len(active_tasks) < 3
                    if can_accept:
                        if st.button(f"✅ Akceptuj zadanie", key=f"accept_{task['id']}", use_container_width=True):
                            # Sprawdź czy zadanie już nie jest w active (fix dla duplikatów)
                            if task['id'] not in bg_data["tasks"]["active"]:
                                # Dodaj do aktywnych zadań (tylko ID!)
                                bg_data["tasks"]["active"].append(task['id'])
                                
                                # Usuń z available_pool - znajdź zadanie po ID i usuń
                                bg_data["tasks"]["available_pool"] = [
                                    t for t in bg_data["tasks"]["available_pool"] 
                                    if t['id'] != task['id']
                                ]
                                
                                # Zapisz BEZPOŚREDNIO do JSON (workaround dla repository bug)
                                import json
                                users_file = "users_data.json"
                                with open(users_file, "r", encoding="utf-8") as f:
                                    all_users = json.load(f)
                                all_users[username] = user_data
                                with open(users_file, "w", encoding="utf-8") as f:
                                    json.dump(all_users, f, ensure_ascii=False, indent=2)
                                
                                st.success(f"✅ Zaakceptowano zadanie: {task['title']}")
                            st.rerun()
                            
                            st.success(f"✅ Zaakceptowano zadanie: {task['title']}")
                            st.rerun()
                    else:
                        st.button("❌ Limit aktywnych zadań (3/3)", key=f"limit_{task['id']}", disabled=True, use_container_width=True)


def show_fmcg_onboarding(username, user_data, industry_id):
    """Onboarding FMCG - prezentacja firmy i wybór klientów docelowych"""
    from data.industries.fmcg_company import COMPANY_INFO, PRODUCT_PORTFOLIO, get_company_pitch
    from data.industries.fmcg_customers import get_customers_by_segment, get_segment_info
    
    bg_data = user_data["business_games"][industry_id]
    
    st.markdown("# 🎯 Witaj w FreshLife Poland!")
    
    st.markdown(f"""
### Gratulacje! Zaczynasz karierę jako **{bg_data['career']['title']}**

Przed Tobą długa droga od przedstawiciela handlowego do Chief Sales Officer.
Ale najpierw - poznaj firmę i wybierz swoich pierwszych klientów!
""")
    
    # KROK 1: Poznaj FreshLife
    st.markdown("---")
    st.markdown("## 📋 Krok 1: Poznaj FreshLife Poland")
    
    with st.expander("🏢 O firmie", expanded=True):
        st.markdown(f"""
**{COMPANY_INFO['full_name']}**
        
{COMPANY_INFO['description']}

**Nasza misja:** {COMPANY_INFO['mission']}

**Wartości:**
""")
        for value in COMPANY_INFO['values']:
            st.markdown(f"• {value}")
        
        st.markdown(f"""
**Pozycja rynkowa:**
• Personal Care: {COMPANY_INFO['market_position']['personal_care']}
• Food: {COMPANY_INFO['market_position']['food']}
• Home Care: {COMPANY_INFO['market_position']['home_care']}
""")
    
    # KROK 2: Portfolio produktów
    st.markdown("## 📦 Krok 2: Poznaj nasze produkty")
    
    tab_pc, tab_food, tab_hc = st.tabs(["🧴 Personal Care", "🍽️ Food", "🏠 Home Care"])
    
    with tab_pc:
        category = PRODUCT_PORTFOLIO['personal_care']
        st.markdown(f"**{category['category_name']}** - {category['description']}")
        st.markdown(f"*Market share: {category['market_share']}%*")
        
        for product in category['products']:
            with st.expander(f"{product['name']} - {product['subcategory']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**USP:** {product['usp']}")
                    st.markdown(f"**Warianty:** {', '.join(product['variants'])}")
                    st.markdown(f"**Target:** {product['target_group']}")
                with col2:
                    st.metric("Cena", product['price_range'])
                    st.metric("Marża", f"{product['margin_percent']}%")
                    st.metric("Potencjał", product['volume_potential'])
    
    with tab_food:
        category = PRODUCT_PORTFOLIO['food']
        st.markdown(f"**{category['category_name']}** - {category['description']}")
        st.markdown(f"*Market share: {category['market_share']}%*")
        
        for product in category['products']:
            with st.expander(f"{product['name']} - {product['subcategory']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**USP:** {product['usp']}")
                    st.markdown(f"**Warianty:** {', '.join(product['variants'])}")
                with col2:
                    st.metric("Cena", product['price_range'])
                    st.metric("Marża", f"{product['margin_percent']}%")
    
    with tab_hc:
        category = PRODUCT_PORTFOLIO['home_care']
        st.markdown(f"**{category['category_name']}** - {category['description']}")
        st.markdown(f"*Market share: {category['market_share']}%*")
        
        for product in category['products']:
            with st.expander(f"{product['name']} - {product['subcategory']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**USP:** {product['usp']}")
                    st.markdown(f"**Warianty:** {', '.join(product['variants'])}")
                with col2:
                    st.metric("Cena", product['price_range'])
                    st.metric("Marża", f"{product['margin_percent']}%")
    
    # KROK 3: Wybór targetu
    st.markdown("---")
    st.markdown("## 🎯 Krok 3: Wybierz swoich pierwszych klientów")
    
    st.info("""
💡 **Ważne:** Na początek skup się na **Traditional Trade** (sklepy osiedlowe, kioski).
To najłatwiejszy segment do zdobycia pierwszych klientów.

Wybierz **2-3 sklepy** które chcesz pozyskać jako pierwsze.
""")
    
    # Lista klientów Traditional Trade
    customers = get_customers_by_segment("traditional_trade")
    
    st.markdown("### Dostępni klienci:")
    
    # Session state dla wyborów
    if 'selected_customers' not in st.session_state:
        st.session_state.selected_customers = []
    
    for customer in customers:
        with st.expander(f"🏪 {customer['name']} - {customer['location']} (Potencjał: {customer['potential_monthly']:,} PLN/mies)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(customer['description'])
                
                st.markdown(f"""
**Charakterystyka:**
• Obrót: {customer['characteristics']['monthly_revenue']}
• Klienci/dzień: {customer['characteristics']['customers_per_day']}
• Konkurencja: {customer['characteristics']['competition']}

**Co ich boli:**
""")
                for pain in customer['pain_points']:
                    st.markdown(f"• {pain}")
                
                st.markdown("**Szanse:**")
                for opp in customer['opportunities']:
                    st.markdown(f"• {opp}")
            
            with col2:
                # Checkbox do wyboru
                is_selected = customer['id'] in st.session_state.selected_customers
                if st.checkbox(
                    "Wybierz",
                    value=is_selected,
                    key=f"select_{customer['id']}"
                ):
                    if customer['id'] not in st.session_state.selected_customers:
                        st.session_state.selected_customers.append(customer['id'])
                else:
                    if customer['id'] in st.session_state.selected_customers:
                        st.session_state.selected_customers.remove(customer['id'])
    
    # Przycisk zakończenia onboardingu
    st.markdown("---")
    
    selected_count = len(st.session_state.selected_customers)
    
    if selected_count < 2:
        st.warning(f"⚠️ Wybierz przynajmniej 2 klientów ({selected_count}/2)")
    elif selected_count > 3:
        st.warning(f"⚠️ Na początek maksymalnie 3 klientów ({selected_count}/3)")
    else:
        st.success(f"✅ Wybrano {selected_count} klientów. Możesz rozpocząć!")
        
        if st.button("🚀 Rozpocznij pracę z wybranymi klientami", type="primary", use_container_width=True):
            # Zapisz wybór i oznacz onboarding jako ukończony
            bg_data["customers"]["selected_targets"] = st.session_state.selected_customers
            bg_data["customers"]["prospects"] = st.session_state.selected_customers.copy()
            bg_data["customers"]["onboarding_completed"] = True
            
            # Inicjalizuj conversation history dla każdego klienta
            for customer_id in st.session_state.selected_customers:
                bg_data["conversations"][customer_id] = []
            
            # Zapisz
            import json
            users_file = "users_data.json"
            with open(users_file, "r", encoding="utf-8") as f:
                all_users = json.load(f)
            all_users[username] = user_data
            with open(users_file, "w", encoding="utf-8") as f:
                json.dump(all_users, f, ensure_ascii=False, indent=2)
            
            st.success("✅ Świetnie! Przekierowuję do panelu klientów...")
            st.rerun()


def show_fmcg_customers_tab(username, user_data, industry_id):
    """Tab Klienci - lista klientów, umów spotkania, historia"""
    from data.industries.fmcg_customers import get_customer_by_id
    
    bg_data = user_data["business_games"][industry_id]
    customers_data = bg_data.get("customers", {})
    
    # Sprawdź czy jest aktywna rozmowa
    if st.session_state.get('fmcg_conversation_active', False):
        customer_id = st.session_state.get('fmcg_conversation_customer')
        customer = get_customer_by_id(customer_id)
        
        if customer:
            render_fmcg_customer_conversation(customer, username, user_data, bg_data, industry_id)
            return
        else:
            # Błąd - reset
            st.session_state.fmcg_conversation_active = False
            st.rerun()
    
    st.markdown("# 👥 Moi Klienci")
    
    # Podsumowanie
    prospects = customers_data.get("prospects", [])
    active = customers_data.get("active_clients", [])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Prospects", len(prospects))
    with col2:
        st.metric("✅ Aktywni", len(active))
    with col3:
        total_potential = sum(
            get_customer_by_id(c_id).get('potential_monthly', 0) 
            for c_id in prospects + active
        )
        st.metric("💰 Potencjał", f"{total_potential:,} PLN/mies")
    
    st.markdown("---")
    
    # Lista prospects
    if prospects:
        st.markdown("## 🎯 Prospects (w trakcie pozyskiwania)")
        
        for customer_id in prospects:
            customer = get_customer_by_id(customer_id)
            if not customer:
                continue
            
            with st.expander(f"🏪 {customer['name']} - {customer['location']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Właściciel:** {customer['owner']}")
                    st.markdown(f"**Typ:** {customer['type']}")
                    st.markdown(f"**Potencjał:** {customer['potential_monthly']:,} PLN/miesiąc")
                    
                    # Historia rozmów
                    conversations = bg_data.get("conversations", {}).get(customer_id, [])
                    if conversations:
                        st.markdown(f"**Spotkań:** {len(conversations)}")
                        last_conv = conversations[-1]
                        st.markdown(f"**Ostatnie:** {last_conv.get('date', 'brak daty')}")
                
                with col2:
                    st.markdown("###")
                    if st.button("📞 Umów spotkanie", key=f"meeting_{customer_id}", use_container_width=True):
                        # Otwórz conversation
                        st.session_state.fmcg_conversation_customer = customer_id
                        st.session_state.fmcg_conversation_active = True
                        st.rerun()
    
    # Lista aktywnych
    if active:
        st.markdown("## ✅ Aktywni Klienci")
        st.info("🚧 Lista aktywnych klientów - wkrótce!")
    
    # Jeśli brak klientów
    if not prospects and not active:
        st.warning("Nie masz jeszcze żadnych klientów. Wróć do onboardingu i wybierz klientów!")


def render_fmcg_customer_conversation(customer, username, user_data, bg_data, industry_id):
    """Renderuje rozmowę z klientem FMCG - wykorzystuje AI Conversation Engine"""
    from data.industries.fmcg_conversations import build_conversation_prompt
    from datetime import datetime
    import google.generativeai as genai
    import os
    
    customer_id = customer['id']
    
    # Nagłówek
    st.markdown(f"""
<div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
            color: white; padding: 24px; border-radius: 16px; margin-bottom: 24px;'>
    <h2 style='margin: 0 0 8px 0;'>🏪 Spotkanie: {customer['name']}</h2>
    <p style='margin: 0; opacity: 0.9; font-size: 14px;'>Właściciel: {customer['owner']} | {customer['location']}</p>
</div>
""", unsafe_allow_html=True)
    
    # Pobierz historię rozmów
    conversation_history = bg_data.get("conversations", {}).get(customer_id, [])
    
    # Informacja o historii
    if conversation_history:
        st.info(f"📋 Spotkanie #{len(conversation_history) + 1} z {customer['owner']}")
    else:
        st.info(f"🆕 Pierwsze spotkanie z {customer['owner']} - czas na prospecting!")
    
    # Historia wiadomości (przechowujemy w session_state)
    if f'fmcg_conv_messages_{customer_id}' not in st.session_state:
        st.session_state[f'fmcg_conv_messages_{customer_id}'] = []
    
    messages = st.session_state[f'fmcg_conv_messages_{customer_id}']
    
    # Current turn - liczba wiadomości gracza (do klucza text_area)
    player_messages_count = len([m for m in messages if m['role'] == 'player'])
    current_turn = player_messages_count + 1
    
    # Wyświetl historię rozmowy
    st.markdown("### 💬 Rozmowa")
    
    for msg in messages:
        if msg['role'] == 'player':
            st.markdown(f"""
<div style='background: #e0f2fe; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #0284c7;'>
    <strong>🎯 Ty:</strong><br>{msg['content']}
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div style='background: #f3f4f6; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #6b7280;'>
    <strong>🏪 {customer['owner']}:</strong><br>{msg['content']}
</div>
""", unsafe_allow_html=True)
    
    # Pole wpisywania wiadomości
    st.markdown("---")
    
    # === SPEECH-TO-TEXT INTERFACE (jak w kontraktach conversation) ===
    st.markdown("**🎤 Nagraj** (wielokrotnie, jeśli chcesz) **lub ✍️ pisz bezpośrednio w polu poniżej:**")
    
    # Klucze dla transkrypcji i wersjonowania
    transcription_key = f"fmcg_transcription_{customer_id}"
    transcription_version_key = f"fmcg_transcription_version_{customer_id}"
    last_audio_hash_key = f"fmcg_last_audio_hash_{customer_id}"
    
    # Inicjalizacja (setdefault nie powoduje re-render jeśli klucz już istnieje!)
    st.session_state.setdefault(transcription_key, "")
    st.session_state.setdefault(transcription_version_key, 0)
    st.session_state.setdefault(last_audio_hash_key, None)
    
    audio_data = st.audio_input(
        "🎤 Nagrywanie...",
        key=f"audio_input_fmcg_{customer_id}_{current_turn}"
    )
    
    # Przetwarzanie nagrania audio (tylko jeśli to NOWE nagranie!)
    if audio_data is not None:
        import hashlib
        
        # Oblicz hash audio aby wykryć duplikaty
        audio_bytes = audio_data.getvalue()
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        
        # Sprawdź czy to to samo nagranie co poprzednio
        if audio_hash != st.session_state[last_audio_hash_key]:
            # NOWE nagranie - przetwarzaj!
            st.session_state[last_audio_hash_key] = audio_hash
            
            import speech_recognition as sr
            import tempfile
            import os
            from pydub import AudioSegment
            
            with st.spinner("🤖 Rozpoznaję mowę..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(audio_bytes)
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
                            
                            # Pobierz API key
                            api_key = None
                            try:
                                api_key = st.secrets["API_KEYS"]["gemini"]
                            except:
                                try:
                                    with open("config/gemini_api_key.txt", "r") as f:
                                        api_key = f.read().strip()
                                except:
                                    api_key = os.getenv("GEMINI_API_KEY")
                            
                            if api_key:
                                genai.configure(api_key=api_key)
                                model = genai.GenerativeModel("models/gemini-2.5-flash")
                                prompt = f"""Dodaj interpunkcję (kropki, przecinki, pytajniki, wykrzykniki) do poniższego tekstu.
Nie zmieniaj słów, tylko dodaj znaki interpunkcyjne. Zachowaj strukturę i podział na zdania.
Zwróć tylko poprawiony tekst, bez dodatkowych komentarzy.

Tekst do poprawy:
{transcription}"""
                                response = model.generate_content(prompt)
                                transcription_with_punctuation = response.text.strip()
                                transcription = transcription_with_punctuation
                                
                        except Exception as gemini_error:
                            # Błąd Gemini - cicho kontynuuj z surową transkrypcją
                            pass
                        
                        # DOPISZ do istniejącego tekstu (z session_state)
                        # Pobierz aktualną wartość z transcription_key (tam zapisujemy wartości)
                        existing_text = st.session_state.get(transcription_key, "")
                        
                        if existing_text.strip():
                            st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
                        else:
                            st.session_state[transcription_key] = transcription
                        
                        # Inkrementuj wersję - to wymusi re-render text_area z nową wartością!
                        st.session_state[transcription_version_key] += 1
                        
                        # Ciche działanie - brak st.info() przed rerun!
                        st.rerun()
                        
                    finally:
                        # Cleanup temp files
                        try:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
                            if wav_path and os.path.exists(wav_path):
                                os.unlink(wav_path)
                        except:
                            pass
                            
                except sr.UnknownValueError:
                    st.session_state.fmcg_stt_error = "🎤 Nie rozpoznano mowy. Spróbuj ponownie (mów wyraźniej, bliżej mikrofonu)."
                    st.rerun()
                except sr.RequestError as e:
                    st.session_state.fmcg_stt_error = f"❌ Błąd usługi rozpoznawania mowy: {e}"
                    st.rerun()
                except Exception as e:
                    st.session_state.fmcg_stt_error = f"❌ Błąd podczas transkrypcji: {str(e)}"
                    st.rerun()
    
    # Wyświetl błędy STT (jeśli są)
    if "fmcg_stt_error" in st.session_state:
        st.warning(st.session_state.fmcg_stt_error)
        del st.session_state.fmcg_stt_error
    
    col_input, col_btn = st.columns([4, 1])
    
    with col_input:
        # Callback - synchronizuj wartość text_area z transcription_key
        def sync_textarea_to_state():
            textarea_key = f"msg_input_{customer_id}_{current_turn}_{st.session_state.get(transcription_version_key, 0)}"
            if textarea_key in st.session_state:
                st.session_state[transcription_key] = st.session_state[textarea_key]
        
        # Użyj wartości z transkrypcji jako value (+ wersja w kluczu wymusza re-render)
        player_message = st.text_area(
            "Twoja wiadomość:",
            value=st.session_state.get(transcription_key, ""),
            placeholder="Napisz co chcesz powiedzieć klientowi...",
            height=100,
            key=f"msg_input_{customer_id}_{current_turn}_{st.session_state.get(transcription_version_key, 0)}",
            on_change=sync_textarea_to_state
        )
    
    with col_btn:
        st.markdown("###")
        send_clicked = st.button("📤 Wyślij", use_container_width=True, type="primary")
        
        st.markdown("###")
        if st.button("🚪 Zakończ spotkanie", use_container_width=True):
            # Zapisz conversation do historii
            if messages:
                conversation_record = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "messages": messages.copy(),
                    "topic": "Prospecting" if not conversation_history else "Follow-up",
                    "customer_impression": "neutral"  # TODO: AI evaluation
                }
                
                if customer_id not in bg_data["conversations"]:
                    bg_data["conversations"][customer_id] = []
                bg_data["conversations"][customer_id].append(conversation_record)
                
                # Zapisz
                import json
                users_file = "users_data.json"
                with open(users_file, "r", encoding="utf-8") as f:
                    all_users = json.load(f)
                all_users[username] = user_data
                with open(users_file, "w", encoding="utf-8") as f:
                    json.dump(all_users, f, ensure_ascii=False, indent=2)
            
            # Wyczyść session state
            st.session_state.fmcg_conversation_active = False
            if f'fmcg_conv_messages_{customer_id}' in st.session_state:
                del st.session_state[f'fmcg_conv_messages_{customer_id}']
            
            # Wyczyść transkrypcję
            if transcription_key in st.session_state:
                del st.session_state[transcription_key]
            if transcription_version_key in st.session_state:
                del st.session_state[transcription_version_key]
            if last_audio_hash_key in st.session_state:
                del st.session_state[last_audio_hash_key]
            
            st.success("✅ Spotkanie zakończone!")
            st.rerun()
    
    # Wyślij wiadomość
    if send_clicked and player_message and player_message.strip():
        st.write(f"🔍 DEBUG START - player_message: {player_message[:50]}...")
        st.write(f"🔍 DEBUG - messages przed append: {len(messages)}")
        
        # Wyczyść transkrypcję po wysłaniu (jak w kontraktach conversation)
        st.session_state[transcription_key] = ""
        st.session_state[transcription_version_key] += 1
        
        # Dodaj wiadomość gracza
        messages.append({
            "role": "player",
            "content": player_message
        })
        
        
        st.write(f"🔍 DEBUG - messages po append gracza: {len(messages)}")
        
        # Przygotuj kontekst dla AI
        context = {
            "relationship_status": "prospect",  # TODO: dynamicznie
            "products_sold": [],
            "relationship_score": 0
        }
        
        # Zbuduj prompt
        prompt = build_conversation_prompt(
            customer=customer,
            conversation_history=conversation_history,
            player_message=player_message,
            context=context,
            current_messages=messages  # Przekaż bieżącą historię rozmowy
        )
        
        # Wywołaj AI
        try:
            # Konfiguracja Gemini - czytaj z secrets.toml
            api_key = None
            try:
                # Najpierw próbuj secrets.toml (bezpieczne)
                api_key = st.secrets["API_KEYS"]["GEMINI_API_KEY"]
            except:
                # Fallback - plik (deprecated)
                try:
                    with open("config/gemini_api_key.txt", "r") as f:
                        api_key = f.read().strip()
                except:
                    api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                st.error("❌ Brak klucza API Gemini! Dodaj do .streamlit/secrets.toml w sekcji [API_KEYS]")
                return
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            with st.spinner(f"{customer['owner']} myśli..."):
                response = model.generate_content(prompt)
                npc_response = response.text
                
                # Dodaj odpowiedź NPC
                messages.append({
                    "role": "npc",
                    "content": npc_response
                })
                
                st.write(f"🔍 DEBUG - messages po append NPC: {len(messages)}")
                st.write(f"🔍 DEBUG - npc_response: {npc_response[:100]}...")
                st.write("🔍 DEBUG - przed rerun")
                
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Błąd AI: {str(e)}")


def show_fmcg_stats_tab(username, user_data, industry_id):
    """Statystyki Kariery - wykresy, historia, osiągnięcia"""
    st.info("🚧 Statystyki Kariery - w budowie! 🚧")
    st.write("Tutaj będą statystyki i wykresy.")

# =============================================================================
# GRA BRANŻOWA
# =============================================================================

def show_industry_game(username, user_data, industry_id):
    """Widok gry dla wybranej branży"""
    
    try:
        # KLUCZOWE: Jeśli initializing_game=True, przeładuj user_data z dysku
        if st.session_state.get("initializing_game", False):
            from data.users_new import get_current_user_data
            user_data = get_current_user_data(username)
            
            if not user_data:
                st.error("❌ Błąd ładowania danych użytkownika!")
                st.session_state["bg_view"] = "home"
                st.session_state["initializing_game"] = False
                st.rerun()
            # Reset flagi po przeładowaniu
            st.session_state["initializing_game"] = False
        
        # Pokaż wiadomość o przełączeniu (jeśli istnieje)
        if "switch_message" in st.session_state:
            st.success(st.session_state["switch_message"])
            del st.session_state["switch_message"]
        
        # Nagłówek z nazwą branży
        industry_names = {
            "consulting": "💼 Consulting Game",
            "fmcg": "🛒 FMCG Game",
            "pharma": "💊 Pharma Game",
            "banking": "🏦 Banking Game",
            "insurance": "🛡️ Insurance Game",
            "automotive": "🚗 Automotive Game"
        }
        zen_header(industry_names.get(industry_id, "Business Game"))
        
        # ========== FMCG - Use new playable mechanics ==========
        if industry_id == "fmcg":
            # Import new playable UI
            from views.business_games_refactored.industries.fmcg_playable import show_fmcg_playable_game
            
            # Show playable game interface
            show_fmcg_playable_game(username)
            return
        
        # Pobierz dane branży (tylko dla innych branż)
        if "business_games" not in user_data:
            user_data["business_games"] = {}
        
        if industry_id not in user_data["business_games"]:
            st.warning(f"⚠️ Brak danych dla {industry_id}, inicjalizuję...")
            
            # Automatyczna inicjalizacja
            from utils.business_game import initialize_business_game
            
            new_game_data = initialize_business_game(username)
            user_data["business_games"][industry_id] = new_game_data
            
            save_user_data(username, user_data)
            st.success("✅ Gra została zainicjalizowana! Zapisano do bazy.")
            
            # IMPORTANT: Set bg_view to "game" so it stays on game view
            st.session_state["bg_view"] = "game"
            st.session_state["selected_industry"] = industry_id
        
        # Ensure business_games exists after reload
        if "business_games" not in user_data:
            st.error("❌ business_games zniknęło po reloadzie!")
            user_data["business_games"] = {}
        
        # Ensure industry exists
        if industry_id not in user_data["business_games"]:
            st.error(f"❌ Błąd: {industry_id} nie istnieje w business_games po inicjalizacji!")
            st.json(user_data.get("business_games", {}))
            if st.button("🔄 Powrót do menu"):
                st.session_state["bg_view"] = "home"
                st.session_state["selected_industry"] = None
                st.rerun()
            return
        
        bg_data = user_data["business_games"][industry_id]
        
        # ========== CONSULTING - Original logic ==========
        # MIGRACJA: Dodaj brakujące transakcje dla starych wydarzeń z monetami
        from utils.business_game import migrate_event_transactions
        user_data, migrated_count = migrate_event_transactions(user_data, industry_id)
        if migrated_count > 0:
            save_user_data(username, user_data)
            bg_data = user_data["business_games"][industry_id]
        
        # Odśwież pulę kontraktów
        bg_data = refresh_contract_pool(bg_data)
        user_data["business_games"][industry_id] = bg_data
        
        # SAVE after refresh!
        save_user_data(username, user_data)
        
        # CRITICAL: Reload user_data from disk to ensure consistency
        from data.users_new import get_current_user_data
        user_data = get_current_user_data(username)
        bg_data = user_data["business_games"][industry_id]
        
        # Nagłówek z podsumowaniem firmy
        render_header(user_data, industry_id)
        
        st.markdown("---")
        
        # Główne zakładki (bez Instrukcji - teraz w Dashboard)
        tabs = st.tabs(["🏢 Dashboard", "💼 Kontrakty", "🏢 Zarządzanie", "⚙️ Ustawienia"])
        
        with tabs[0]:
            show_dashboard_tab(username, user_data, industry_id)
        
        with tabs[1]:
            show_contracts_tab(username, user_data, industry_id)
        
        with tabs[2]:
            # Pod-taby w Zarządzaniu
            management_tabs = st.tabs(["🏢 Biuro", "👥 Pracownicy", "📊 Raporty Finansowe", "📜 Historia"])
            
            with management_tabs[0]:
                show_office_tab(username, user_data, industry_id)
            
            with management_tabs[1]:
                show_employees_tab(username, user_data, industry_id)
            
            with management_tabs[2]:
                show_financial_reports_tab(username, user_data, industry_id)
            
            with management_tabs[3]:
                show_history_tab(username, user_data, industry_id)
        
        with tabs[3]:
            # Pod-taby w Ustawieniach
            settings_tabs = st.tabs(["🏢 Ustawienia Firmy", "⚙️ Zarządzanie Grą"])
            
            with settings_tabs[0]:
                show_firm_settings_tab(username, user_data, industry_id)
            
            with settings_tabs[1]:
                show_game_management_tab(username, user_data, industry_id)
        
        # Przycisk powrotu do menu na samym dole
        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
        if st.button("← Powrót do menu", key="back_to_home", use_container_width=True):
            st.session_state["bg_view"] = "home"
            st.session_state["selected_industry"] = None
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ Błąd renderowania gry dla {industry_id}:")
        st.error(f"**Error:** {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        
        # Debug info
        st.markdown("### 🔍 Debug Info:")
        st.write(f"Username: {username}")
        st.write(f"Industry: {industry_id}")
        st.write(f"bg_view: {st.session_state.get('bg_view')}")
        st.write(f"Has business_games: {'business_games' in user_data}")
        if "business_games" in user_data:
            st.write(f"Industries: {list(user_data['business_games'].keys())}")

# =============================================================================
# NAGŁÓWEK
# =============================================================================

def show_dashboard_tab(username, user_data, industry_id="consulting"):
    """Zakładka Dashboard - podsumowanie firmy"""
    from utils.business_game_events import get_latest_event, get_random_event, apply_event_effects
    from datetime import datetime, timedelta
    
    bg_data = get_game_data(user_data, industry_id)
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,  # Legacy pole (nieużywane)
            "last_auto_event": None,  # Automatyczne wydarzenie dzienne
            "last_manual_roll": None,  # Ręczne losowanie przez gracza
            "active_effects": []
        }
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
    # =============================================================================
    # AUTOMATYCZNE WYDARZENIE DZIENNE (raz dziennie przy wejściu)
    # =============================================================================
    
    today = datetime.now().strftime("%Y-%m-%d")
    last_auto_event = bg_data.get("events", {}).get("last_auto_event")
    should_auto_roll = True
    
    if last_auto_event:
        last_auto_date = last_auto_event.split(" ")[0]  # Tylko data
        if last_auto_date == today:
            should_auto_roll = False
    
    # Jeśli jeszcze dziś nie było automatycznego wydarzenia - WYLOSUJ TERAZ
    if should_auto_roll:
        event_result = get_random_event(bg_data, user_data.get("degencoins", 0))  # 20% szansa
        
        if event_result:
            event_id, event_data = event_result
            
            # Sprawdź czy wymaga wyboru
            if event_data["type"] == "neutral" and "choices" in event_data:
                # Zapisz w session_state i wyświetl modal
                st.session_state["pending_event"] = (event_id, event_data)
                st.session_state["pending_event_type"] = "auto"
            else:
                # Bezpośrednio aplikuj (positive i negative)
                user_data = apply_event_effects(event_id, event_data, None, user_data, industry_id)
                save_user_data(username, user_data)
                
                if event_data["type"] == "positive":
                    st.balloons()
        
        # Zapisz timestamp automatycznego losowania
        bg_data.setdefault("events", {})["last_auto_event"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
        
        # Przeładuj bg_data po zapisie
        bg_data = get_game_data(user_data, industry_id)
    
    # =============================================================================
    # SPRAWDŹ DEADLINE I NAŁÓŻ KARY ZA SPÓŹNIENIE
    # =============================================================================
    
    from utils.business_game import check_and_apply_deadline_penalties
    bg_data, penalty_messages = check_and_apply_deadline_penalties(bg_data, user_data)
    
    if penalty_messages:
        for msg in penalty_messages:
            st.error(msg)
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
    # =============================================================================
    # WYDARZENIA W DWÓCH KOLUMNACH (Dzisiejsze + Losowanie)
    # =============================================================================
    
    col_event_today, col_event_roll = st.columns(2)
    
    # LEWA KOLUMNA - DZISIEJSZE WYDARZENIE (AUTOMATYCZNE)
    with col_event_today:
        st.markdown("""
        <div style='margin-top: 0 !important; padding-top: 0 !important;'>
            <h3 style='margin: 0 0 0.5rem 0 !important; padding: 0 !important; font-size: 1.3em;'>🎲 Dzisiejsze Wydarzenie</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Pokaż dzisiejsze AUTOMATYCZNE wydarzenie (manual_roll=False)
        today = datetime.now().strftime("%Y-%m-%d")
        auto_event_today = None
        
        # Znajdź automatyczne wydarzenie z dzisiaj
        for event in reversed(bg_data.get("events", {}).get("history", [])):
            event_date = event.get("timestamp", "").split(" ")[0]
            # Automatyczne = manual_roll jest False lub nie istnieje
            if event_date == today and not event.get("manual_roll", False):
                auto_event_today = event
                break
        
        if auto_event_today:
            show_active_event_card(auto_event_today)
        else:
            st.info("Dzisiaj nie ma żadnego wydarzenia.")
    
    # PRAWA KOLUMNA - LOSOWANIE DODATKOWEGO WYDARZENIA
    with col_event_roll:
        st.markdown("""
        <div style='margin-top: 0 !important; padding-top: 0 !important;'>
            <h3 style='margin: 0 0 0.5rem 0 !important; padding: 0 !important; font-size: 1.3em;'>🎲 Losowanie Wydarzenia</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Sprawdź cooldown dla RĘCZNEGO losowania (oddzielny od automatycznego!)
        last_manual_roll = bg_data.get("events", {}).get("last_manual_roll")
        can_roll = True
        hours_left = 0
        minutes_left = 0
        manual_event_today = None
        
        if last_manual_roll:
            last_dt = datetime.strptime(last_manual_roll, "%Y-%m-%d %H:%M:%S")
            next_roll = last_dt + timedelta(hours=24)
            now = datetime.now()
            
            # Sprawdź czy wylosowano dziś
            manual_roll_date = last_manual_roll.split(" ")[0]
            if manual_roll_date == today:
                # Znajdź wydarzenie z dzisiaj które było ręczne (ma flagę manual=True w historii)
                for event in reversed(bg_data.get("events", {}).get("history", [])):
                    event_date = event.get("timestamp", "").split(" ")[0]
                    if event_date == today and event.get("manual_roll", False):
                        manual_event_today = event
                        break
            
            if now < next_roll:
                can_roll = False
                time_until_next = next_roll - now
                hours_left = int(time_until_next.total_seconds() / 3600)
                minutes_left = int((time_until_next.total_seconds() % 3600) / 60)
        
        # Jeśli dziś było ręczne losowanie - pokaż wydarzenie
        if manual_event_today:
            show_active_event_card(manual_event_today)
        else:
            # Info box
            if can_roll:
                st.success("✅ **Gotowe do losowania!**")
                st.caption("💡 Wydarzenia: pozytywne 🎉, neutralne ⚖️, negatywne 💥")
            else:
                st.warning(f"⏰ Następne za: **{hours_left}h {minutes_left}min**")
            
            # Przycisk losowania
            if st.button("🎲 LOSUJ!", disabled=not can_roll, type="primary", key="roll_event_dashboard", use_container_width=True):
                # SZANSA 100% (dla testów)
                event_result = get_random_event(bg_data, user_data.get("degencoins", 0), force_trigger=True)
                
                if event_result:
                    event_id, event_data = event_result
                    
                    # Sprawdź czy wymaga wyboru
                    if event_data["type"] == "neutral" and "choices" in event_data:
                        # Zapisz zdarzenie tymczasowo w session_state
                        st.session_state["pending_event"] = (event_id, event_data)
                        st.session_state["pending_event_manual"] = True  # Oznacz jako ręczne
                        st.rerun()
                    else:
                        # Bezpośrednio aplikuj - RĘCZNE LOSOWANIE
                        user_data = apply_event_effects(event_id, event_data, None, user_data, industry_id, manual_roll=True)
                        
                        # Zapisz timestamp RĘCZNEGO losowania
                        bg_data.setdefault("events", {})["last_manual_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_game_data(user_data, bg_data, industry_id)
                        save_user_data(username, user_data)
                        
                        st.success(f"{event_data['emoji']} **{event_data['title']}**")
                        st.balloons() if event_data["type"] == "positive" else None
                        st.rerun()
                else:
                    # Brak zdarzenia - zapisz timestamp RĘCZNEGO losowania
                    bg_data.setdefault("events", {})["last_manual_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_game_data(user_data, bg_data, industry_id)
                    save_user_data(username, user_data)
                    st.info("😐 Spokojny dzień!")
                    st.rerun()
    
    # Pending event (jeśli neutralne wymaga wyboru)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data, context="dashboard")
    
    st.markdown("---")
    
    # =============================================================================
    # AKTYWNE KONTRAKTY W DWÓCH KOLUMNACH
    # =============================================================================
    
    st.markdown("""
    <div style='margin-top: 0 !important; padding-top: 0 !important;'>
        <h3 style='margin: 0 0 0.5rem 0 !important; padding: 0 !important; font-size: 1.3em;'>📋 Aktywne Kontrakty</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Lista aktywnych kontraktów
    active_contracts = bg_data["contracts"]["active"]
    
    if len(active_contracts) == 0:
        st.info("Brak aktywnych kontraktów. Przejdź do zakładki 'Kontrakty' aby przyjąć nowe zlecenie!")
    else:
        # Podziel na dwie kolumny
        col_contract1, col_contract2 = st.columns(2)
        
        for idx, contract in enumerate(active_contracts):
            # Naprzemienne kolumny
            with col_contract1 if idx % 2 == 0 else col_contract2:
                render_active_contract_card(contract, username, user_data, bg_data, contract_index=f"dashboard_{idx}")
    
    st.markdown("---")
    
    # =============================================================================
    # WYKRES FINANSOWY - pełna szerokość - kompaktowy nagłówek
    # =============================================================================
    
    st.markdown("""
    <div style='margin-top: 0 !important; padding-top: 0 !important;'>
        <h3 style='margin: 0.5rem 0 0.5rem 0 !important; padding: 0 !important; font-size: 1.3em;'>📊 Analiza Finansowa</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Generuj i wyświetl wykres na pełną szerokość
    fig = create_financial_chart(
        bg_data, 
        period=st.session_state.get("financial_chart_period", 7),
        cumulative=st.session_state.get("financial_chart_cumulative", False)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Kontrolki POD wykresem - kompaktowy layout
    col_controls, col_summary = st.columns([1, 2])
    
    with col_controls:
        st.markdown("**⚙️ Ustawienia wykresu:**")
        
        period = st.radio(
            "Okres",
            options=[7, 14, 30],
            format_func=lambda x: f"📅 {x} dni",
            key="financial_chart_period",
            horizontal=True
        )
        
        cumulative = st.checkbox(
            "📈 Wartość skumulowana",
            value=False,
            key="financial_chart_cumulative"
        )
    
    with col_summary:
        # Podsumowanie sum - tylko jeśli cumulative
        if st.session_state.get("financial_chart_cumulative", False):
            transactions = bg_data.get("history", {}).get("transactions", [])
            # Przychody: kontrakty + pozytywne wydarzenia
            total_rev = sum(t.get("amount", 0) for t in transactions if t.get("type") in ["contract_reward", "event_reward"])
            # Koszty: pracownicy + negatywne wydarzenia
            total_cost = sum(abs(t.get("amount", 0)) for t in transactions if t.get("type") in ["daily_costs", "employee_hired", "employee_hire", "event_cost"])
            total_profit = total_rev - total_cost
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #667eea; border-radius: 8px; padding: 12px 16px; margin-top: 8px;'>
                <div style='color: #667eea; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 8px;'>💎 PODSUMOWANIE TOTAL</div>
                <div style='display: flex; justify-content: space-around; font-size: 13px;'>
                    <div><strong>📊 Przychody:</strong> <span style='color: #10b981;'>{total_rev:,} 💰</span></div>
                    <div><strong>💸 Koszty:</strong> <span style='color: #ef4444;'>{total_cost:,} 💰</span></div>
                    <div><strong>💎 Zysk:</strong> <span style='color: {"#10b981" if total_profit >= 0 else "#ef4444"}; font-weight: 700;'>{total_profit:,} 💰</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # =============================================================================
    # RANKINGI - Na dole Dashboard
    # =============================================================================
    
    st.markdown("---")
    st.markdown("<div style='margin: 40px 0 20px 0;'></div>", unsafe_allow_html=True)
    show_rankings_content(username, user_data, industry_id)
    
    # =============================================================================
    # SEKCJA CELÓW SCENARIUSZA - POD RANKINGAMI
    # =============================================================================
    
    st.markdown("---")
    
    # Sprawdź czy gra ma scenariusz i cele (klucze: scenario_id, scenario_objectives)
    if "scenario_objectives" in bg_data and bg_data.get("scenario_objectives"):
        try:
            # Aktualizuj postęp celów (sprawdza automatycznie co zostało ukończone)
            newly_completed = update_objectives_progress(bg_data, user_data)
            
            # Jeśli jakieś cele zostały właśnie ukończone - nagroda!
            if newly_completed:
                for obj in newly_completed:
                    reward = obj.get("reward_money", 0)
                    if reward > 0:
                        bg_data["money"] = bg_data.get("money", 0) + reward
                        st.success(f"🎉 Cel ukończony: {obj.get('description')}! Nagroda: +{reward:,} PLN!")
                        st.balloons()
                
                # Zapisz zmiany
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
            
            objectives_data = get_objectives_summary(bg_data, user_data)
            
            if objectives_data and objectives_data.get("total", 0) > 0:
                # Material 3 style - kompaktowy widok celów
                completed_count = objectives_data.get("completed_count", 0)
                total = objectives_data["total"]
                
                # Emoji zależne od postępu
                progress_pct = (completed_count / total) * 100 if total > 0 else 0
                if progress_pct == 100:
                    header_emoji = "🏆"
                elif progress_pct >= 50:
                    header_emoji = "🎯"
                else:
                    header_emoji = "📋"
                
                with st.expander(f"{header_emoji} **Cele** · {completed_count}/{total}", expanded=False):
                    # Pobierz dane scenariusza
                    from data.scenarios import get_scenario
                    scenario_id = bg_data.get("scenario_id")
                    scenario = get_scenario(industry_id, scenario_id) if scenario_id else None
                    
                    if scenario:
                        # Nagłówek scenariusza - HTML w jednej linii dla poprawnego renderowania
                        scenario_name = scenario.get("name", "Nieznany scenariusz")
                        scenario_desc = scenario.get("description", "")
                        st.markdown(f"""<div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #667eea; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px;'><div style='color: #667eea; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 8px;'>🎮 SCENARIUSZ</div><div style='color: #212121; font-weight: 700; font-size: 1.1em; margin-bottom: 6px;'>{scenario_name}</div><div style='color: #64748b; font-size: 0.9em; line-height: 1.5;'>{scenario_desc}</div></div>""", unsafe_allow_html=True)
                    
                    # Siatka celów - 1 lub 2 kolumny w zależności od ilości
                    if total <= 2:
                        cols = st.columns(1)
                    else:
                        cols = st.columns(2)
                    
                    for idx, obj_status in enumerate(objectives_data["objectives"]):
                        is_completed = obj_status.get("completed", False)
                        current_value = obj_status.get("current", 0)
                        target = obj_status.get("target", 0)
                        description = obj_status.get("description", "Cel")
                        reward = obj_status.get("reward", 0)
                        obj_type = obj_status.get("type", "")
                        
                        # Ikony typów
                        type_icons = {
                            "revenue_total": "💰",
                            "reputation": "⭐",
                            "level": "📈",
                            "money": "💵",
                            "employees": "👥"
                        }
                        icon = type_icons.get(obj_type, "🎯")
                        
                        # Progress
                        obj_progress = min(1.0, current_value / target) if target > 0 else (1.0 if is_completed else 0.0)
                        
                        # Material 3 kompaktowa karta - jednolity layout dla wszystkich celów
                        with cols[idx % len(cols)]:
                            # Kolor progress bara zależy od stanu
                            if is_completed:
                                progress_color = "#00c853"  # Zielony dla ukończonych
                                bg_color = "#f1f8f4"  # Subtelne zielone tło
                                border_color = "#00c853"
                            else:
                                progress_color = "#2196f3" if obj_progress >= 0.5 else "#90a4ae"
                                bg_color = "#f5f5f5"
                                border_color = "#e0e0e0"
                            
                            # Prefix dla ukończonych
                            status_prefix = "✅ Ukończono · " if is_completed else ""
                            
                            st.markdown(f"""<div style='background: {bg_color}; border: 1px solid {border_color}; padding: 12px; border-radius: 12px; margin-bottom: 8px;'><div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;'><div style='flex: 1;'><div style='color: #212121; font-weight: 600; font-size: 0.9em;'>{icon} {description}</div></div><div style='background: {"#e8f5e9" if is_completed else "#fff3e0"}; padding: 4px 8px; border-radius: 6px; color: {"#00c853" if is_completed else "#f57c00"}; font-weight: bold; font-size: 0.75em;'>{"💎" if is_completed else "🎁"} {reward:,}</div></div><div style='color: #616161; font-size: 0.75em; margin-bottom: 4px;'>{status_prefix}{current_value:,} / {target:,} · {obj_progress*100:.0f}%</div><div style='background: #e0e0e0; height: 4px; border-radius: 2px; overflow: hidden;'><div style='background: {progress_color}; height: 100%; width: {obj_progress*100}%; transition: width 0.3s ease;'></div></div></div>""", unsafe_allow_html=True)
            else:
                # Scenariusz ma puste cele (tryb lifetime/otwarty)
                # Nie wyświetlamy nic - to OK dla trybu bez celów
                pass
        except Exception as e:
            st.error(f"⚠️ Błąd podczas ładowania celów scenariusza: {str(e)}")
    else:
        # Brak scenariusza lub scenariusz bez celów - to normalne dla trybu Lifetime
        # Nie wyświetlamy nic
        pass
    
    # =============================================================================
    # INSTRUKCJA GRY - EXPANDER - W TYM SAMYM SEPARATORZE CO CELE
    # =============================================================================
    
    with st.expander("📖 Jak grać w Business Games? (Instrukcja)", expanded=False):
        # Sekcja 1: Szybki start
        st.markdown("""
<div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #667eea; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px;'>
<div style='color: #667eea; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>🚀 SZYBKI START (5 KROKÓW)</div>
<div style='color: #334155; font-size: 14px; line-height: 1.8;'>
<strong>1️⃣ Przyjmij kontrakt</strong> → Zakładka "💼 Kontrakty"<br>
<strong>2️⃣ Wykonaj zadanie</strong> → Wróć do "🏢 Dashboard" → Aktywne Kontrakty<br>
<strong>3️⃣ Prześlij rozwiązanie</strong> → Tekst/Audio → Klient oceni 1-5⭐<br>
<strong>4️⃣ Zbieraj pieniądze</strong> → 500-3000 PLN za kontrakt<br>
<strong>5️⃣ Rozwijaj firmę</strong> → Poziom 1 → 10 (180k PLN, 5500 reputacji)
</div>
</div>
        """, unsafe_allow_html=True)
        
        # Grid 2 kolumny
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Typy kontraktów
            st.markdown("""
<div style='background: linear-gradient(135deg, #10b98115 0%, #05966915 100%); border-left: 4px solid #10b981; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px;'>
<div style='color: #10b981; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>💼 TYPY KONTRAKTÓW</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px;'>
<strong>💼 Standard</strong><br>
<span style='font-size: 12px; color: #64748b;'>Podstawowe zlecenia • Tekst/Audio → Klient ocenia</span>
</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px;'>
<strong>💬 Conversation</strong><br>
<span style='font-size: 12px; color: #64748b;'>Rozmowy z NPC • Text-to-Speech 🔊 • Dynamiczne reakcje</span>
</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px;'>
<strong>⚡ Speed Challenge</strong><br>
<span style='font-size: 12px; color: #64748b;'>Kontrakt na czas • Timer • Wysokie bonusy</span>
</div>
</div>
            """, unsafe_allow_html=True)
            
            # Pracownicy
            st.markdown("""
<div style='background: linear-gradient(135deg, #f59e0b15 0%, #d9770615 100%); border-left: 4px solid #f59e0b; border-radius: 12px; padding: 16px 20px;'>
<div style='color: #f59e0b; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>👥 PRACOWNICY</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px; display: flex; justify-content: space-between;'>
<span><strong>📊 Analityk</strong> - Bonus do ocen</span>
<span style='color: #f59e0b; font-weight: 700;'>+0.5⭐</span>
</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px; display: flex; justify-content: space-between;'>
<span><strong>💼 Manager</strong> - Więcej kontraktów</span>
<span style='color: #f59e0b; font-weight: 700;'>+1/dzień</span>
</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 8px; color: #334155; font-size: 14px; display: flex; justify-content: space-between;'>
<span><strong>🎯 Specjalista</strong> - Niższe koszty</span>
<span style='color: #10b981; font-weight: 700;'>-20%</span>
</div>
<div style='margin-top: 12px; padding: 8px; background: rgba(239, 68, 68, 0.1); border-radius: 6px; color: #ef4444; font-size: 12px; text-align: center;'>
⚠️ Koszt: 500 PLN/dzień/pracownik<br>Zatrudniaj mądrze!
</div>
</div>
            """, unsafe_allow_html=True)
        
        with col_right:
            # Poziomy firmy (skrócone)
            st.markdown("""
<div style='background: linear-gradient(135deg, #8b5cf615 0%, #7c3aed15 100%); border-left: 4px solid #8b5cf6; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px;'>
<div style='color: #8b5cf6; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>📈 POZIOMY FIRMY</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 6px; color: #334155; font-size: 13px;'>
<strong>Lvl 1:</strong> Solo Consultant → 0 PLN, 0 rep
</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 6px; color: #334155; font-size: 13px;'>
<strong>Lvl 4:</strong> Strategic Partners → 10k PLN, 600 rep, <span style='color: #10b981;'>★ 2 kontrakty/dzień</span>
</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 6px; color: #334155; font-size: 13px;'>
<strong>Lvl 7:</strong> National Authority → 55k PLN, 2200 rep, <span style='color: #10b981;'>★ 3 kontrakty/dzień</span>
</div>
<div style='padding: 8px 12px; background: white; border-radius: 8px; margin-bottom: 6px; color: #334155; font-size: 13px;'>
<strong>Lvl 10:</strong> CIQ Empire → 180k PLN, 5500 rep, <span style='color: #10b981;'>★ 5 kontraktów/dzień</span>
</div>
<div style='margin-top: 12px; padding: 8px; background: rgba(139, 92, 246, 0.1); border-radius: 6px; color: #8b5cf6; font-size: 12px; text-align: center;'>
💡 Wyższy poziom = więcej możliwości!
</div>
</div>
            """, unsafe_allow_html=True)
            
            # Wydarzenia
            st.markdown("""
<div style='background: linear-gradient(135deg, #3b82f615 0%, #2563eb15 100%); border-left: 4px solid #3b82f6; border-radius: 12px; padding: 16px 20px;'>
<div style='color: #3b82f6; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>🎲 WYDARZENIA LOSOWE</div>
<div style='color: #334155; font-size: 14px; line-height: 1.6;'>
Co dzień <strong>10% szansa</strong> na wydarzenie:<br><br>
✅ <strong>60%</strong> pozytywne/neutralne<br>
❌ <strong>40%</strong> negatywne<br><br>
<span style='font-size: 12px; color: #64748b;'>
Przykłady: Nagroda branżowa (+500 rep), Awaria (-1000 PLN), Polecenie klienta (+bonus)
</span>
</div>
</div>
            """, unsafe_allow_html=True)
        
        # Wskazówki strategiczne
        st.markdown("""
<div style='background: linear-gradient(135deg, #ef444415 0%, #dc262615 100%); border-left: 4px solid #ef4444; border-radius: 12px; padding: 16px 20px;'>
<div style='color: #ef4444; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>⚠️ NAJCZĘSTSZE BŁĘDY</div>
<div style='color: #334155; font-size: 14px; line-height: 1.8;'>
❌ <strong>Zatrudnianie za wcześnie</strong> - Poziom 1-2: 500 PLN/dzień to za dużo!<br>
❌ <strong>Ignorowanie reputacji</strong> - Poziom 4+ wymaga 600+ reputacji<br>
❌ <strong>Przyjmowanie za dużo kontraktów</strong> - Max 1 kontrakt/dzień (początkowo)<br>
❌ <strong>Brak kapitału awaryjnego</strong> - Trzymaj 3x koszty dzienne
</div>
</div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
<div style='background: linear-gradient(135deg, #10b98115 0%, #05966915 100%); border-left: 4px solid #10b981; border-radius: 12px; padding: 16px 20px; margin-top: 16px;'>
<div style='color: #10b981; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>✅ ZŁOTE ZASADY</div>
<div style='color: #334155; font-size: 14px; line-height: 1.8;'>
✅ <strong>Poziom 1-3:</strong> Zbieraj kapitał, NIE zatrudniaj (jeszcze!)<br>
✅ <strong>Poziom 4+:</strong> 2 kontrakty/dzień = możesz zatrudniać rentownie<br>
✅ <strong>Buduj reputację:</strong> Wysokie oceny (4-5⭐) = szybszy awans<br>
✅ <strong>Conversations 💬:</strong> Text-to-Speech 🔊 + dobre nagrody + trening komunikacji<br>
✅ <strong>Sprawdzaj Dashboard:</strong> Wszystkie wyniki kontraktów tu są!
</div>
</div>
        """, unsafe_allow_html=True)

def show_contracts_tab(username, user_data, industry_id="consulting"):
    """Zakładka Rynek Kontraktów"""
    bg_data = get_game_data(user_data, industry_id)
    
    # =============================================================================
    # SPRAWDŹ DEADLINE I NAŁÓŻ KARY ZA SPÓŹNIENIE
    # =============================================================================
    
    from utils.business_game import check_and_apply_deadline_penalties
    bg_data, penalty_messages = check_and_apply_deadline_penalties(bg_data, user_data)
    
    if penalty_messages:
        for msg in penalty_messages:
            st.error(msg)
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
    # =============================================================================
    # SEKCJA 1: AKTYWNE KONTRAKTY (pracuj nad nimi)
    # =============================================================================
    
    # CRITICAL FIX: Wyczyść flagi rendered_ na początku każdego renderowania
    # Zapobiega blokowaniu kontraktów po st.rerun()
    # WAŻNE: Kasuj WSZYSTKIE flagi rendered_, niezależnie od formatu klucza
    keys_to_clear = [k for k in st.session_state.keys() if isinstance(k, str) and k.startswith("rendered_")]
    if keys_to_clear:
        print(f"DEBUG show_contracts_tab: Kasowanie {len(keys_to_clear)} flag rendered_: {keys_to_clear[:5]}...")  # pokaż pierwsze 5
    for k in keys_to_clear:
        del st.session_state[k]
    
    st.subheader("📋 Aktywne Kontrakty")
    
    active_contracts = bg_data["contracts"]["active"]
    
    # CRITICAL FIX: Usuń duplikaty kontraktów (po ID)
    # Może się zdarzyć, że ten sam kontrakt został dodany wielokrotnie
    seen_ids = set()
    unique_contracts = []
    for contract in active_contracts:
        contract_id = contract.get('id')
        if not contract_id:
            print(f"⚠️ WARNING: Kontrakt bez ID! Pomijam. Dane: {contract}")
            continue  # Pomiń kontrakty bez ID
        if contract_id not in seen_ids:
            seen_ids.add(contract_id)
            unique_contracts.append(contract)
        else:
            print(f"⚠️ WARNING: Duplikat kontraktu {contract_id} - usuwam!")
    
    # Jeśli znaleziono duplikaty, zaktualizuj listę i zapisz
    if len(unique_contracts) < len(active_contracts):
        st.warning(f"⚠️ Wykryto i usunięto {len(active_contracts) - len(unique_contracts)} zduplikowanych kontraktów.")
        bg_data["contracts"]["active"] = unique_contracts
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
        active_contracts = unique_contracts
    
    if len(active_contracts) == 0:
        st.info("✨ Brak aktywnych kontraktów. Przyjmij nowe zlecenie poniżej!")
    else:
        # DEBUG: Sprawdź listę kontraktów
        contract_ids_debug = [c.get('id', 'NO_ID') for c in active_contracts]
        print(f"DEBUG show_contracts_tab: Renderowanie {len(active_contracts)} kontraktów: {contract_ids_debug}")
        
        for idx, contract in enumerate(active_contracts):
            print(f"DEBUG: Renderowanie kontraktu idx={idx}, id={contract.get('id', 'NO_ID')}")
            render_active_contract_card(contract, username, user_data, bg_data, contract_index=idx)
    
    st.markdown("---")
    
    # =============================================================================
    # SEKCJA 2: DOSTĘPNE KONTRAKTY DO PRZYJĘCIA
    # =============================================================================
    
    st.subheader("💼 Dostępne Kontrakty")
    
    # Info o pojemności
    can_accept, reason = can_accept_contract(bg_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        firm_level = bg_data["firm"]["level"]
        employees = bg_data["employees"]
        capacity = FIRM_LEVELS[firm_level]["limit_kontraktow_dzienny"]
        for emp in employees:
            emp_type = EMPLOYEE_TYPES.get(emp["type"])
            if emp_type and emp_type["bonus_type"] == "capacity":
                capacity += emp_type["bonus_value"]
        
        # Policz ile kontraktów przyjęto/ukończono dzisiaj
        today = datetime.now().strftime("%Y-%m-%d")
        today_accepted = sum(1 for c in bg_data["contracts"]["active"] if c.get("accepted_date", "").startswith(today))
        today_completed = sum(1 for c in bg_data["contracts"]["completed"] if c.get("completed_date", "").startswith(today))
        today_total = today_accepted + today_completed
        
        st.info(f"🎯 Dzienna pojemność: **{today_total}/{int(capacity)} kontraktów**")
    
    with col2:
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
            save_game_data(user_data, bg_data, industry_id)
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
            ["Wszystkie", "Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership", "AI Conversation", "Conversation"],
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
            ["Trudność: rosnąco", "Nagroda: najwyższe", "Nagroda: najniższe", "Czas: najkrótsze"],
            key="contracts_sort_by"
        )
    
    st.markdown("---")
    
    # Lista kontraktów
    available_contracts = bg_data["contracts"]["available_pool"]
    
    # Filtruj kontrakty według uprawnień użytkownika do typów gier
    from utils.permissions import has_access_to_business_game_type
    from data.repositories.user_repository import UserRepository
    from database.connection import session_scope
    
    try:
        from database.models import User
        with session_scope() as session:
            user_repo = UserRepository(session)
            user_obj = session.query(User).filter_by(username=username).first()
            user_dict = user_obj.to_dict() if user_obj else {}
            
            # Filtruj kontrakty - zostawiamy tylko te typy, do których użytkownik ma dostęp
            accessible_contracts = []
            for contract in available_contracts:
                contract_type = contract.get("contract_type", "standard")
                # Obsługa starych nazw
                if contract_type == "ai_conversation":
                    contract_type = "conversation"
                
                if has_access_to_business_game_type(contract_type, user_dict):
                    accessible_contracts.append(contract)
            
            available_contracts = accessible_contracts
    except Exception as e:
        print(f"Error filtering contract types: {e}")
        # W przypadku błędu, pozostawiamy wszystkie kontrakty
    
    # Filtrowanie po kategorii
    if category_filter != "Wszystkie":
        available_contracts = [c for c in available_contracts if c["kategoria"] == category_filter]
    
    if difficulty_filter != "Wszystkie":
        diff_level = len(difficulty_filter)
        available_contracts = [c for c in available_contracts if c["trudnosc"] == diff_level]
    
    # Sortowanie (domyślnie: Trudność rosnąco - najłatwiejsze na początku)
    if sort_by == "Trudność: rosnąco":
        available_contracts = sorted(available_contracts, key=lambda x: x["trudnosc"])
    elif sort_by == "Nagroda: najwyższe":
        available_contracts = sorted(available_contracts, key=lambda x: x["nagroda_5star"], reverse=True)
    elif sort_by == "Nagroda: najniższe":
        available_contracts = sorted(available_contracts, key=lambda x: x["nagroda_base"])
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
                render_contract_card(contract, username, user_data, bg_data, can_accept, industry_id)


def show_office_tab(username, user_data, industry_id="consulting"):
    """Zakładka Biuro - zarządzanie przestrzenią"""
    from datetime import datetime
    
    bg_data = get_game_data(user_data, industry_id)
    
    # Inicjalizacja biura jeśli nie istnieje (dla starych zapisów)
    if "office" not in bg_data:
        bg_data["office"] = {
            "type": "home_office",
            "upgraded_at": None
        }
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
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
            st.write(f"💰 Koszt: **{next_office['koszt_ulepszenia']} PLN**")
        with col3:
            # Pobierz saldo firmy (nie osobiste DegenCoins!)
            current_money = bg_data.get('money', 0)
            
            if current_money >= next_office['koszt_ulepszenia']:
                if st.button("⬆️ Ulepsz biuro", type="primary", use_container_width=True):
                    # Ulepsz biuro - płacimy Z FIRMY!
                    bg_data["money"] = current_money - next_office['koszt_ulepszenia']
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
                    
                    # Dodaj do historii biur (dla zakładki Historia)
                    if "offices" not in bg_data.setdefault("history", {}):
                        bg_data["history"]["offices"] = []
                    
                    bg_data["history"]["offices"].append({
                        "office_type": next_office['nazwa'],
                        "cost": next_office['koszt_dzienny'],
                        "capacity": next_office['max_pracownikow'],
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    save_game_data(user_data, bg_data, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"🎉 Biuro ulepszone do: {next_office['nazwa']}!")
                    st.balloons()
                    st.rerun()
            else:
                st.button("⬆️ Ulepsz biuro", disabled=True, use_container_width=True)
                st.caption(f"Potrzebujesz: {next_office['koszt_ulepszenia'] - current_money:.0f} PLN więcej")
    else:
        st.success("🌟 Posiadasz najlepsze możliwe biuro!")

# =============================================================================
# TAB 4A: USTAWIENIA FIRMY
# =============================================================================

def show_firm_settings_tab(username, user_data, industry_id="consulting"):
    """Ustawienia firmy - nazwa, logo, archiwum firm"""
    bg_data = get_game_data(user_data, industry_id)
    
    # Wszystkie ustawienia w jednym miejscu z tabami
    settings_tab1, settings_tab2, settings_tab3, settings_tab4, settings_tab5, settings_tab6 = st.tabs([
        "✏️ Nazwa i logo",
        "� Informacje",
        "🎨 Personalizacja",
        "💰 Cele finansowe",
        "🔔 Powiadomienia",
        "� Zarządzanie firmą"
    ])
    
    # TAB 1: Nazwa i logo
    with settings_tab1:
        col_name, col_logo = st.columns([1, 1])
        
        with col_name:
            st.markdown("### ✏️ Zmień nazwę firmy")
            new_name = st.text_input(
                "Nowa nazwa firmy", 
                value=bg_data["firm"]["name"], 
                key="settings_firm_name_input"
            )
            if st.button("💾 Zapisz nazwę", key="settings_save_firm_name", type="primary"):
                bg_data["firm"]["name"] = new_name
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                st.success("✅ Nazwa firmy zaktualizowana!")
                st.rerun()
        
        with col_logo:
            st.markdown("### 🎨 Zmień logo firmy")
            
            # Kategorie logo
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
                key="settings_logo_category"
            )
            
            # Grid logo (mniejszy - 6 kolumn)
            available_logos = FIRM_LOGOS[selected_category]["free"]
            cols = st.columns(6)
            for idx, logo in enumerate(available_logos[:12]):  # Max 12 logo
                with cols[idx % 6]:
                    if st.button(
                        logo,
                        key=f"settings_logo_{selected_category}_{idx}",
                        help=f"Wybierz {logo}"
                    ):
                        bg_data["firm"]["logo"] = logo
                        save_game_data(user_data, bg_data, industry_id)
                        save_user_data(username, user_data)
                        st.success(f"✅ Logo: {logo}")
                        st.rerun()
        
        # Podgląd na całej szerokości
        st.markdown("---")
        st.markdown("### 👀 Podgląd")
        current_logo = bg_data["firm"].get("logo", "🏢")
        current_name = bg_data["firm"]["name"]
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; color: white;'>
            <div style='font-size: 72px; margin-bottom: 12px;'>{current_logo}</div>
            <h2 style='margin: 0; color: white;'>{current_name}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 2: Informacje o firmie
    with settings_tab2:
        st.markdown("### 📊 Informacje o firmie")
        
        # Pobierz dane
        founded_date = bg_data["firm"].get("founded", datetime.now().strftime("%Y-%m-%d"))
        founded_dt = datetime.strptime(founded_date, "%Y-%m-%d")
        days_active = (datetime.now() - founded_dt).days
        
        # Grid z informacjami
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>📅 Data założenia</div>
                <div style='font-size: 24px; font-weight: 700;'>{}</div>
            </div>
            """.format(founded_dt.strftime("%d.%m.%Y")), unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>⏱️ Dni działalności</div>
                <div style='font-size: 24px; font-weight: 700;'>{days_active}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            level = bg_data["firm"].get("level", 1)
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>🏆 Poziom firmy</div>
                <div style='font-size: 24px; font-weight: 700;'>Level {level}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Slogan/Motto
        st.markdown("### 💬 Motto firmy")
        current_motto = bg_data["firm"].get("motto", "")
        new_motto = st.text_area(
            "Motto lub slogan Twojej firmy:",
            value=current_motto,
            max_chars=200,
            height=80,
            placeholder="Np. 'Jakość przede wszystkim' lub 'Innowacje dla ludzi'",
            key="firm_motto"
        )
        
        if new_motto != current_motto:
            if st.button("💾 Zapisz motto", type="primary", key="save_motto"):
                bg_data["firm"]["motto"] = new_motto
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                st.success("✅ Motto zaktualizowane!")
                st.rerun()
        
        st.markdown("---")
        
        # Dodatkowe informacje
        st.markdown("### 📋 Szczegóły")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.info(f"""
            **🏢 Branża:** {industry_id.capitalize()}  
            **📊 Scenariusz:** {bg_data.get('scenario_id', 'N/A')}  
            **⭐ Reputacja:** {bg_data['firm'].get('reputation', 0)}  
            """)
        
        with info_col2:
            total_employees = len(bg_data.get("employees", []))
            total_completed = len(bg_data.get("contracts", {}).get("completed", []))
            total_revenue = bg_data.get("stats", {}).get("total_revenue", 0)
            
            st.success(f"""
            **👥 Pracownicy:** {total_employees}  
            **✅ Ukończone kontrakty:** {total_completed}  
            **💰 Łączny przychód:** {total_revenue:,} PLN  
            """)
    
    # TAB 3: Personalizacja
    with settings_tab3:
        st.markdown("### 🎨 Schemat kolorów firmy")
        st.info("💡 Wybierz schemat kolorów, który będzie reprezentował Twoją firmę w interfejsie")
        
        # Dostępne schematy kolorów
        color_schemes = {
            "purple": {"name": "🟣 Fioletowy (Classic)", "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "primary": "#667eea"},
            "blue": {"name": "🔵 Niebieski (Professional)", "gradient": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "primary": "#3b82f6"},
            "green": {"name": "🟢 Zielony (Growth)", "gradient": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "primary": "#10b981"},
            "orange": {"name": "🟠 Pomarańczowy (Energy)", "gradient": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)", "primary": "#f59e0b"},
            "red": {"name": "🔴 Czerwony (Bold)", "gradient": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "primary": "#ef4444"},
            "pink": {"name": "🌸 Różowy (Creative)", "gradient": "linear-gradient(135deg, #ec4899 0%, #db2777 100%)", "primary": "#ec4899"},
            "teal": {"name": "💎 Turkusowy (Innovation)", "gradient": "linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)", "primary": "#14b8a6"},
            "indigo": {"name": "💜 Indygo (Premium)", "gradient": "linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)", "primary": "#6366f1"}
        }
        
        # Obecny schemat
        current_scheme = bg_data["firm"].get("color_scheme", "purple")
        
        # Grid z podglądem schematów
        cols = st.columns(4)
        for idx, (scheme_id, scheme_data) in enumerate(color_schemes.items()):
            with cols[idx % 4]:
                is_current = scheme_id == current_scheme
                border = "4px solid #10b981" if is_current else "2px solid #e5e7eb"
                
                st.markdown(f"""
                <div style='border: {border}; border-radius: 12px; padding: 12px; margin-bottom: 12px; background: white;'>
                    <div style='background: {scheme_data["gradient"]}; height: 80px; border-radius: 8px; margin-bottom: 8px;'></div>
                    <div style='font-size: 12px; text-align: center; color: #64748b;'>{scheme_data["name"]}</div>
                    {"<div style='text-align: center; color: #10b981; font-size: 11px; margin-top: 4px;'>✓ Aktywny</div>" if is_current else ""}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Wybierz", key=f"color_{scheme_id}", disabled=is_current, use_container_width=True):
                    bg_data["firm"]["color_scheme"] = scheme_id
                    save_game_data(user_data, bg_data, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"✅ Zmieniono na {scheme_data['name']}")
                    st.rerun()
        
        st.markdown("---")
        
        # Podgląd wizytówki w rankingach
        st.markdown("### 👀 Podgląd wizytówki")
        current_logo = bg_data["firm"].get("logo", "🏢")
        current_name = bg_data["firm"]["name"]
        current_gradient = color_schemes[current_scheme]["gradient"]
        
        st.markdown(f"""
        <div style='background: {current_gradient}; padding: 24px; border-radius: 16px; color: white; margin: 16px 0;'>
            <div style='display: flex; align-items: center; gap: 20px;'>
                <div style='font-size: 64px;'>{current_logo}</div>
                <div style='flex: 1;'>
                    <h2 style='margin: 0; color: white; font-size: 28px;'>{current_name}</h2>
                    <div style='opacity: 0.9; margin-top: 8px;'>Level {bg_data["firm"].get("level", 1)} • {industry_id.capitalize()}</div>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 32px; font-weight: 700;'>#{1}</div>
                    <div style='opacity: 0.9; font-size: 14px;'>w rankingu</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 4: Cele finansowe
    with settings_tab4:
        st.markdown("### 💰 Zarządzanie celami finansowymi")
        
        # Inicjalizuj ustawienia finansowe jeśli nie istnieją
        if "financial_settings" not in bg_data:
            bg_data["financial_settings"] = {
                "savings_goal": 0,
                "low_balance_alert": -10000,
                "high_balance_alert": 50000,
                "auto_transfer_enabled": False,
                "auto_transfer_threshold": 30000,
                "auto_transfer_amount": 5000
            }
        
        fin_settings = bg_data["financial_settings"]
        current_balance = bg_data.get("money", 0)
        
        # Obecne saldo
        balance_color = "#10b981" if current_balance >= 0 else "#ef4444"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 24px; border-radius: 16px; color: white; margin-bottom: 24px;'>
            <div style='font-size: 14px; opacity: 0.8; margin-bottom: 8px;'>💰 Obecne saldo firmy</div>
            <div style='font-size: 42px; font-weight: 700; color: {balance_color};'>{current_balance:,} PLN</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Cel oszczędnościowy
        st.markdown("### 🎯 Cel oszczędnościowy")
        st.caption("Ustaw minimalną kwotę, którą chcesz utrzymać jako bufor bezpieczeństwa")
        
        savings_goal = st.number_input(
            "Cel oszczędnościowy (PLN):",
            min_value=0,
            max_value=1000000,
            value=fin_settings.get("savings_goal", 0),
            step=5000,
            key="savings_goal_input"
        )
        
        if current_balance >= savings_goal and savings_goal > 0:
            st.success(f"✅ Cel osiągnięty! Masz {current_balance - savings_goal:,} PLN powyżej celu")
        elif savings_goal > 0:
            deficit = savings_goal - current_balance
            st.warning(f"⚠️ Brakuje {deficit:,} PLN do osiągnięcia celu")
        
        st.markdown("---")
        
        # Alerty salda
        st.markdown("### 🔔 Alerty salda")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⚠️ Alert niskiego salda")
            low_alert = st.number_input(
                "Powiadom gdy saldo spadnie poniżej:",
                min_value=-100000,
                max_value=0,
                value=fin_settings.get("low_balance_alert", -10000),
                step=1000,
                key="low_alert_input"
            )
            
            if current_balance < low_alert:
                st.error(f"🚨 ALERT! Saldo poniżej progu: {current_balance:,} PLN < {low_alert:,} PLN")
        
        with col2:
            st.markdown("#### 🎉 Alert wysokiego salda")
            high_alert = st.number_input(
                "Powiadom gdy saldo przekroczy:",
                min_value=0,
                max_value=1000000,
                value=fin_settings.get("high_balance_alert", 50000),
                step=5000,
                key="high_alert_input"
            )
            
            if current_balance > high_alert:
                st.success(f"🎉 Gratulacje! Saldo powyżej progu: {current_balance:,} PLN > {high_alert:,} PLN")
        
        st.markdown("---")
        
        # Auto-transfer do DegenCoins
        st.markdown("### 💎 Automatyczny transfer zysków")
        st.caption("Automatycznie przenoś nadwyżki do swojego portfela DegenCoins")
        
        auto_transfer = st.checkbox(
            "Włącz automatyczny transfer",
            value=fin_settings.get("auto_transfer_enabled", False),
            key="auto_transfer_enabled"
        )
        
        if auto_transfer:
            col1, col2 = st.columns(2)
            with col1:
                transfer_threshold = st.number_input(
                    "Transfer gdy saldo przekroczy:",
                    min_value=0,
                    max_value=1000000,
                    value=fin_settings.get("auto_transfer_threshold", 30000),
                    step=5000,
                    key="transfer_threshold"
                )
            with col2:
                transfer_amount = st.number_input(
                    "Kwota transferu:",
                    min_value=1000,
                    max_value=100000,
                    value=fin_settings.get("auto_transfer_amount", 5000),
                    step=1000,
                    key="transfer_amount"
                )
            
            st.info(f"💡 Gdy saldo firmy przekroczy {transfer_threshold:,} PLN, automatycznie przelej {transfer_amount:,} PLN do DegenCoins")
        
        # Zapisz ustawienia
        if st.button("💾 Zapisz ustawienia finansowe", type="primary", key="save_financial_settings"):
            bg_data["financial_settings"] = {
                "savings_goal": savings_goal,
                "low_balance_alert": low_alert,
                "high_balance_alert": high_alert,
                "auto_transfer_enabled": auto_transfer,
                "auto_transfer_threshold": transfer_threshold if auto_transfer else fin_settings.get("auto_transfer_threshold", 30000),
                "auto_transfer_amount": transfer_amount if auto_transfer else fin_settings.get("auto_transfer_amount", 5000)
            }
            save_game_data(user_data, bg_data, industry_id)
            save_user_data(username, user_data)
            st.success("✅ Ustawienia finansowe zapisane!")
            st.rerun()
    
    # TAB 5: Powiadomienia
    with settings_tab5:
        st.markdown("### 🔔 Centrum powiadomień")
        
        # Inicjalizuj ustawienia powiadomień
        if "notifications" not in bg_data:
            bg_data["notifications"] = {
                "deadline_alert_hours": 24,
                "deadline_alert_enabled": True,
                "new_contracts_alert": True,
                "balance_alerts_enabled": True,
                "events_alerts_enabled": True,
                "level_up_alerts": True,
                "employee_alerts": True
            }
        
        notif_settings = bg_data["notifications"]
        
        # Alerty deadline
        st.markdown("### ⏰ Alerty deadline kontraktów")
        deadline_enabled = st.checkbox(
            "Powiadamiaj o zbliżających się deadline'ach",
            value=notif_settings.get("deadline_alert_enabled", True),
            key="deadline_alert_enabled"
        )
        
        if deadline_enabled:
            deadline_hours = st.slider(
                "Powiadom X godzin przed deadline:",
                min_value=1,
                max_value=72,
                value=notif_settings.get("deadline_alert_hours", 24),
                step=1,
                key="deadline_hours"
            )
            st.caption(f"💡 Otrzymasz powiadomienie {deadline_hours}h przed upływem terminu każdego kontraktu")
        
        st.markdown("---")
        
        # Pozostałe powiadomienia
        st.markdown("### 📬 Inne powiadomienia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_contracts = st.checkbox(
                "📋 Nowe kontrakty w puli",
                value=notif_settings.get("new_contracts_alert", True),
                key="new_contracts_alert"
            )
            
            balance_alerts = st.checkbox(
                "💰 Alerty salda",
                value=notif_settings.get("balance_alerts_enabled", True),
                key="balance_alerts"
            )
            
            events_alerts = st.checkbox(
                "🎲 Wydarzenia losowe",
                value=notif_settings.get("events_alerts_enabled", True),
                key="events_alerts"
            )
        
        with col2:
            level_up = st.checkbox(
                "🏆 Awanse poziomów",
                value=notif_settings.get("level_up_alerts", True),
                key="level_up_alerts"
            )
            
            employee_alerts = st.checkbox(
                "👥 Zmiany w zespole",
                value=notif_settings.get("employee_alerts", True),
                key="employee_alerts"
            )
            
            reputation_alerts = st.checkbox(
                "⭐ Zmiany reputacji",
                value=notif_settings.get("reputation_alerts", True),
                key="reputation_alerts"
            )
        
        st.markdown("---")
        
        # Podsumowanie aktywnych alertów
        active_alerts = sum([
            deadline_enabled,
            new_contracts,
            balance_alerts,
            events_alerts,
            level_up,
            employee_alerts,
            reputation_alerts
        ])
        
        st.info(f"📊 Aktywnych alertów: **{active_alerts}**/7")
        
        # Zapisz ustawienia
        if st.button("💾 Zapisz ustawienia powiadomień", type="primary", key="save_notifications"):
            bg_data["notifications"] = {
                "deadline_alert_hours": deadline_hours if deadline_enabled else notif_settings.get("deadline_alert_hours", 24),
                "deadline_alert_enabled": deadline_enabled,
                "new_contracts_alert": new_contracts,
                "balance_alerts_enabled": balance_alerts,
                "events_alerts_enabled": events_alerts,
                "level_up_alerts": level_up,
                "employee_alerts": employee_alerts,
                "reputation_alerts": reputation_alerts
            }
            save_game_data(user_data, bg_data, industry_id)
            save_user_data(username, user_data)
            st.success("✅ Ustawienia powiadomień zapisane!")
            st.rerun()
    
    # TAB 6: Zarządzanie firmą
    with settings_tab6:
        # Sub-taby w zarządzaniu
        manage_tab1, manage_tab2 = st.tabs(["🆕 Nowa firma", "📦 Archiwum"])
        
        # Sub-tab: Nowa firma
        with manage_tab1:
            st.warning("⚠️ **Uwaga:** Te akcje mogą zmienić Twoją grę!")
            
            st.markdown("### 🆕 Rozpocznij nową firmę")
            st.info("""
            **Co się stanie:**
            - Obecna firma zostanie zarchiwizowana (dane nie zostaną utracone)
            - Stworzysz nową firmę od zera z nowym scenariuszem
            - Zachowasz swoje DegenCoins i doświadczenie
            - Będziesz mógł wrócić do poprzedniej firmy w zakładce "📦 Archiwum"
            """)
            
            if st.button("🚀 Rozpocznij nową firmę", type="primary", key="start_new_company"):
                # Zarchiwizuj obecną firmę
                if "archived_games" not in user_data:
                    user_data["archived_games"] = {}
                if industry_id not in user_data["archived_games"]:
                    user_data["archived_games"][industry_id] = []
                
                # Dodaj timestamp do archiwalnej gry
                archived_game = bg_data.copy()
                archived_game["archived_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                archived_game["firm"]["archived_name"] = f"{bg_data['firm']['name']} (zarchiwizowana {datetime.now().strftime('%d.%m.%Y')})"
                
                user_data["archived_games"][industry_id].append(archived_game)
                
                # Usuń obecną grę
                del user_data["business_games"][industry_id]
                
                # Zapisz zmiany
                save_user_data(username, user_data)
                
                # Resetuj session state
                st.session_state["selected_industry"] = industry_id
                
                st.success("✅ Firma zarchiwizowana! Przekierowuję do wyboru scenariusza...")
                time.sleep(1)
                st.rerun()
        
        # Sub-tab: Archiwum
        with manage_tab2:
            if "archived_games" in user_data and industry_id in user_data["archived_games"]:
                archived_count = len(user_data["archived_games"][industry_id])
                
                if archived_count > 0:
                    st.markdown(f"### 📦 Masz {archived_count} zarchiwizowanych firm")
                    st.info("💡 Możesz przywrócić dowolną firmę - obecna zostanie zarchiwizowana automatycznie")
                    
                    for idx, archived_game in enumerate(user_data["archived_games"][industry_id]):
                        firm_name = archived_game["firm"].get("archived_name", archived_game["firm"]["name"])
                        archived_at = archived_game.get("archived_at", "N/A")
                        level = archived_game["firm"].get("level", 1)
                        reputation = archived_game["firm"].get("reputation", 0)
                        logo = archived_game["firm"].get("logo", "🏢")
                        
                        # Karta firmy
                        with st.container():
                            col_logo, col_info, col_action = st.columns([1, 4, 2])
                            
                            with col_logo:
                                st.markdown(f"""
                                <div style='text-align: center; font-size: 48px; padding: 10px;'>
                                    {logo}
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col_info:
                                st.markdown(f"**{firm_name}**")
                                st.caption(f"📅 Zarchiwizowana: {archived_at}")
                                st.caption(f"🏢 Level {level} | ⭐ Reputacja {reputation}")
                            
                            with col_action:
                                if st.button("🔄 Przywróć", key=f"restore_game_{idx}", type="secondary"):
                                    # Zarchiwizuj obecną firmę jeśli istnieje
                                    if industry_id in user_data["business_games"]:
                                        current_game = user_data["business_games"][industry_id].copy()
                                        current_game["archived_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        current_game["firm"]["archived_name"] = f"{current_game['firm']['name']} (zarchiwizowana {datetime.now().strftime('%d.%m.%Y')})"
                                        user_data["archived_games"][industry_id].append(current_game)
                                    
                                    # Przywróć wybraną firmę
                                    restored_game = archived_game.copy()
                                    # Usuń metadane archiwum
                                    if "archived_at" in restored_game:
                                        del restored_game["archived_at"]
                                    if "archived_name" in restored_game["firm"]:
                                        del restored_game["firm"]["archived_name"]
                                    
                                    user_data["business_games"][industry_id] = restored_game
                                    
                                    # Usuń z archiwum
                                    user_data["archived_games"][industry_id].pop(idx)
                                    
                                    # Zapisz
                                    save_user_data(username, user_data)
                                    
                                    st.success(f"✅ Przywrócono firmę: {firm_name}")
                                    time.sleep(1)
                                    st.rerun()
                            
                            st.markdown("---")
                else:
                    st.info("📭 Brak zarchiwizowanych firm. Rozpocznij nową firmę w zakładce '🆕 Nowa firma'")
            else:
                st.info("📭 Brak zarchiwizowanych firm. Rozpocznij nową firmę w zakładce '🆕 Nowa firma'")

# =============================================================================
# TAB 4B: ZARZĄDZANIE GRĄ
# =============================================================================

def show_game_management_tab(username, user_data, industry_id="consulting"):
    """Zarządzanie grą - zmiana branży, reset, zamknięcie firmy"""
    import time
    from data.scenarios import get_scenario
    
    bg_data = get_game_data(user_data, industry_id)
    
    st.subheader("⚙️ Zarządzanie Grą")
    
    # Sprawdź czy to tryb lifetime
    is_lifetime = bg_data.get("scenario_id") == "lifetime"
    
    if is_lifetime:
        st.markdown("### ♾️ Tryb Lifetime Challenge")
        st.info("💡 Grasz w trybie nieskończonym! Rywalizuj z innymi w rankingu i buduj swoją firmę bez ograniczeń.")
        st.markdown("---")
    
    # Będzie reszta zawartości z expandera...
    st.info("🚧 Funkcje zarządzania grą wkrótce dostępne tutaj.")

# =============================================================================
# TAB 3B: PRACOWNICY
# =============================================================================

def show_employees_tab(username, user_data, industry_id="consulting"):
    """Zakładka Biuro i Pracownicy"""
    bg_data = get_game_data(user_data, industry_id)
    
    # Inicjalizacja biura jeśli nie istnieje (dla starych zapisów)
    if "office" not in bg_data:
        bg_data["office"] = {
            "type": "home_office",
            "upgraded_at": None
        }
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
    # =============================================================================
    # SEKCJA PRACOWNIKÓW
    # =============================================================================
    
    st.subheader("👥 Zarządzanie Zespołem")
    
    # Pobierz informacje o biurze (potrzebne do limitu pracowników)
    office_type = bg_data["office"]["type"]
    office_info = OFFICE_TYPES[office_type]
    
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
                render_employee_card(employee, username, user_data, bg_data, industry_id)
    
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
                render_hire_card(emp_type, EMPLOYEE_TYPES[emp_type], username, user_data, bg_data, industry_id)
    else:
        st.success("✅ Wszystkie dostępne typy pracowników są już zatrudnione!")

def render_employee_card(employee, username, user_data, bg_data, industry_id="consulting"):
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
            updated_user_data, success, message = fire_employee(user_data, employee['id'], industry_id)
            if success:
                user_data.update(updated_user_data)
                save_user_data(username, user_data)
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def render_hire_card(emp_type, emp_data, username, user_data, bg_data, industry_id="consulting"):
    """Renderuje kartę dostępnego pracownika - kompaktowa"""
    
    can_hire, reason = can_hire_employee(user_data, emp_type, industry_id)
    
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
                updated_user_data, success, message = hire_employee(user_data, emp_type, industry_id)
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

def show_financial_reports_tab(username, user_data, industry_id="consulting"):
    """Zakładka Raporty Finansowe - zaawansowana analiza P&L i KPI"""
    bg_data = get_game_data(user_data, industry_id)
    
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
    
    # Filtruj transakcje w okresie (z obsługą brakującego timestamp)
    current_transactions = []
    for t in transactions:
        if "timestamp" not in t:
            continue  # Pomiń transakcje bez timestamp
        try:
            if datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S") >= start_date:
                current_transactions.append(t)
        except (ValueError, KeyError):
            continue  # Pomiń transakcje z niepoprawnym formatem
    
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
        
        # Filtruj transakcje z poprzedniego okresu (z obsługą brakującego timestamp)
        prev_transactions = []
        for t in transactions:
            if "timestamp" not in t:
                continue
            try:
                if prev_start <= datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S") < prev_end:
                    prev_transactions.append(t)
            except (ValueError, KeyError):
                continue
        
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
        
        # Obsługa różnych formatów reward (dict lub int)
        reward_data = contract.get("reward", 0)
        if isinstance(reward_data, dict):
            reward = reward_data.get("coins", 0)
        else:
            reward = reward_data  # Stary format - reward jako int
        
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
    
    top_contracts = sorted(all_contracts, key=lambda x: get_contract_reward_coins(x), reverse=True)[:5]
    
    for i, contract in enumerate(top_contracts, 1):
        reward = get_contract_reward_coins(contract)
        rating = contract.get("rating", 0)
        st.markdown(f"""
        **{i}. {contract.get('emoji', '📋')} {contract.get('tytul', 'Nieznany')}**  
        💰 {reward:,} monet | ⭐ {rating}/5 | 🏢 {contract.get('klient', 'Nieznany klient')}
        """)

# =============================================================================
# TAB 5: HISTORIA KONTRAKTÓW
# =============================================================================

def show_history_tab(username, user_data, industry_id="consulting"):
    """Zakładka Historia - chronologiczna oś czasu z kontraktami, wydarzeniami, pracownikami i biurem"""
    bg_data = get_game_data(user_data, industry_id)
    
    st.subheader("📜 Historia Firmy")
    
    # Sekcja losowania wydarzeń na górze
    st.markdown("### 🎲 Losowanie Wydarzenia")
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
        save_game_data(user_data, bg_data, industry_id)
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
                    user_data = apply_event_effects(event_id, event_data, None, user_data, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"{event_data['emoji']} **{event_data['title']}**")
                    st.balloons() if event_data["type"] == "positive" else None
                    st.rerun()
            else:
                # Brak zdarzenia (80% przypadków)
                bg_data.setdefault("events", {})["last_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                st.info("😐 Tym razem nic się nie wydarzyło. Spokojny dzień!")
                st.rerun()
    
    # Pending event (jeśli neutralne wymaga wyboru)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data, context="history")
    
    st.markdown("---")
    
    # Zbierz wszystkie zdarzenia (kontrakty + wydarzenia + pracownicy + biuro)
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
    
    # Dodaj historię pracowników (zatrudnienia/zwolnienia)
    employee_history = bg_data.get("history", {}).get("employees", [])
    for emp_event in employee_history:
        timeline_items.append({
            "type": "employee",
            "date": emp_event.get("date", ""),
            "data": emp_event
        })
    
    # Dodaj historię biura (przeprowadzki)
    office_history = bg_data.get("history", {}).get("offices", [])
    for office_event in office_history:
        timeline_items.append({
            "type": "office",
            "date": office_event.get("date", ""),
            "data": office_event
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
            ["Wszystko", "Tylko kontrakty", "Tylko wydarzenia", "Tylko pracownicy", "Tylko biuro"],
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
    elif filter_type == "Tylko pracownicy":
        filtered = [item for item in filtered if item["type"] == "employee"]
    elif filter_type == "Tylko biuro":
        filtered = [item for item in filtered if item["type"] == "office"]
    
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
        elif item["type"] == "event":
            render_event_history_card(item["data"])
        elif item["type"] == "employee":
            render_employee_history_card(item["data"])
        elif item["type"] == "office":
            render_office_history_card(item["data"])


def show_events_tab(username, user_data, industry_id="consulting"):
    """Zakładka Wydarzenia - losowe zdarzenia"""
    bg_data = get_game_data(user_data, industry_id)
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
        save_game_data(user_data, bg_data, industry_id)
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
                    user_data = apply_event_effects(event_id, event_data, None, user_data, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"{event_data['emoji']} **{event_data['title']}**")
                    st.balloons() if event_data["type"] == "positive" else None
                    st.rerun()
            else:
                # Brak zdarzenia (80% przypadków)
                bg_data.setdefault("events", {})["last_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                st.info("😐 Tym razem nic się nie wydarzyło. Spokojny dzień!")
                st.rerun()
    
    # Pending event (jeśli neutralne wymaga wyboru)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data, context="events")
    
    st.markdown("---")
    
    # Historia wydarzeń
    st.markdown("### 📜 Historia Wydarzeń")
    
    if "events" not in bg_data or not bg_data["events"].get("history"):
        st.info("Brak wydarzeń w historii. Wylosuj pierwsze zdarzenie powyżej!")
    else:
        history = bg_data["events"]["history"]
        # Filtruj elementy bez timestamp przed sortowaniem
        history_with_timestamp = [h for h in history if "timestamp" in h]
        history_sorted = sorted(history_with_timestamp, key=lambda x: x["timestamp"], reverse=True)
        
        # Pokazuj tylko ostatnie 10
        for event in history_sorted[:10]:
            render_event_history_card(event)

def render_event_choice_modal(event_id: str, event_data: dict, username: str, user_data: dict, context: str = "default"):
    """Renderuje modal z wyborem dla neutralnego zdarzenia
    
    Args:
        event_id: ID wydarzenia
        event_data: Dane wydarzenia
        username: Nazwa użytkownika
        user_data: Dane użytkownika
        context: Kontekst wywołania (np. "dashboard", "history") - aby uniknąć duplikatów kluczy
    """
    
    # Utwórz unikalny klucz dla tego wywołania (aby uniknąć duplikatów)
    # Użyj hash z event_id i danych - będzie taki sam dla tego samego eventu w tej sesji
    import hashlib
    import json
    from datetime import datetime
    event_hash = hashlib.md5(json.dumps({"id": event_id, "data": event_data, "ctx": context}, sort_keys=True).encode()).hexdigest()[:8]
    
    
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
            if st.button(choice["text"], key=f"event_choice_{event_hash}_{idx}", type="primary" if idx == 0 else "secondary", use_container_width=True):
                # Sprawdź czy to ręczne losowanie
                is_manual = st.session_state.get("pending_event_manual", False)
                industry_id = st.session_state.get("selected_industry", "consulting")
                
                # Aplikuj wybór
                user_data = apply_event_effects(event_id, event_data, idx, user_data, industry_id=industry_id, manual_roll=is_manual)
                
                # Jeśli to było ręczne losowanie, zapisz timestamp
                if is_manual:
                    from data.repositories.user_repository import get_game_data, save_game_data
                    industry_id = st.session_state.get("selected_industry", "consulting")
                    bg_data = get_game_data(user_data, industry_id)
                    bg_data.setdefault("events", {})["last_manual_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_game_data(user_data, bg_data, industry_id)
                
                save_user_data(username, user_data)
                
                # Usuń pending
                del st.session_state["pending_event"]
                if "pending_event_manual" in st.session_state:
                    del st.session_state["pending_event_manual"]
                
                st.success(f"✅ Wybrano: {choice['text']}")
                st.rerun()

def render_employee_history_card(emp_event: dict):
    """Renderuje kartę zdarzenia pracowniczego w historii"""
    
    action = emp_event.get("action", "unknown")
    employee_name = emp_event.get("employee_name", "Pracownik")
    employee_type = emp_event.get("employee_type", "")
    date = emp_event.get("date", "Nieznana data")
    cost = emp_event.get("cost", 0)
    
    if action == "hired":
        icon = "✅"
        border_color = "#10b981"
        title = f"{icon} Zatrudniono: {employee_name} ({employee_type})"
    elif action == "fired":
        icon = "❌"
        border_color = "#ef4444"
        title = f"{icon} Zwolniono: {employee_name} ({employee_type})"
    else:
        icon = "👥"
        border_color = "#64748b"
        title = f"{icon} {employee_name} ({employee_type})"
    
    # DATA NA POCZĄTKU
    with st.expander(f"📅 {date} | {title}"):
        st.markdown(f"""
        <div style='border-left: 4px solid {border_color}; padding: 12px; background: #f8fafc; border-radius: 8px;'>
            <strong>Pracownik:</strong> {employee_name}<br>
            <strong>Stanowisko:</strong> {employee_type}<br>
            <strong>Data:</strong> {date}<br>
            <strong>Koszt (miesięczny):</strong> {cost:,} PLN
        </div>
        """, unsafe_allow_html=True)

def render_office_history_card(office_event: dict):
    """Renderuje kartę zdarzenia biurowego w historii"""
    
    office_type = office_event.get("office_type", "Nieznane biuro")
    date = office_event.get("date", "Nieznana data")
    cost = office_event.get("cost", 0)
    capacity = office_event.get("capacity", 0)
    
    icon = "🏢"
    border_color = "#3b82f6"
    title = f"{icon} Nowe biuro: {office_type}"
    
    # DATA NA POCZĄTKU
    with st.expander(f"📅 {date} | {title}"):
        st.markdown(f"""
        <div style='border-left: 4px solid {border_color}; padding: 12px; background: #f8fafc; border-radius: 8px;'>
            <strong>Typ biura:</strong> {office_type}<br>
            <strong>Data przeprowadzki:</strong> {date}<br>
            <strong>Koszt (miesięczny):</strong> {cost:,} PLN<br>
            <strong>Pojemność:</strong> {capacity} aktywnych kontraktów
        </div>
        """, unsafe_allow_html=True)

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
    
    # DATA NA POCZĄTKU
    with st.expander(f"📅 {event['timestamp']} | {event['emoji']} {event['title']}"):
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

def show_rankings_content(username, user_data, industry_id="consulting"):
    """Zawartość rankingów - może być wyświetlana jako osobny tab lub część Dashboard"""
    bg_data = get_game_data(user_data, industry_id)
    
    st.subheader("🏆 Rankingi Firm Konsultingowych")
    
    # Aktualizuj overall score
    bg_data = update_user_ranking(bg_data)
    save_game_data(user_data, bg_data, industry_id)
    
    # Selector
    ranking_type = st.selectbox(
        "Wybierz ranking:",
        ["🏆 Rating (Overall Score)", "💰 Przychody", "⭐ Jakość (średnia ocena)", "🔥 Produktywność (30 dni)"],
        key="rankings_type_selector"
    )
    
    # Mapowanie wyświetlanych nazw na typy wewnętrzne
    ranking_type_map = {
        "🏆 Rating (Overall Score)": "overall",
        "💰 Przychody": "revenue",
        "⭐ Jakość (średnia ocena)": "quality",
        "🔥 Produktywność (30 dni)": "productivity_30d"
    }
    internal_ranking_type = ranking_type_map.get(ranking_type, "overall")
    
    st.markdown("---")
    
    # Twoja pozycja (highlight)
    render_user_rank_highlight(bg_data, ranking_type)
    
    st.markdown("---")
    
    # Pobierz PRAWDZIWE dane wszystkich użytkowników
    from data.users_sql import load_user_data
    all_users = load_user_data()
    
    # Filtruj użytkowników według scope rankingów
    from utils.permissions import get_ranking_scope, is_visible_in_global_ranking
    from data.repositories.user_repository import UserRepository
    from database.connection import session_scope
    
    try:
        from database.models import User
        with session_scope() as session:
            user_repo = UserRepository(session)
            current_user_obj = session.query(User).filter_by(username=username).first()
            current_user_dict = current_user_obj.to_dict() if current_user_obj else {}
            
            # Sprawdź scope rankingu dla bieżącego użytkownika
            ranking_scope = get_ranking_scope(current_user_dict)
            current_user_company = current_user_dict.get('company', '')
            
            # Filtruj użytkowników według scope
            filtered_users = {}
            if ranking_scope == 'none':
                # Brak dostępu do rankingów - nie pokazuj nikogo (tylko siebie)
                filtered_users = {username: all_users.get(username, {})}
            elif ranking_scope == 'company':
                # Tylko użytkownicy z tej samej firmy
                for user, data in all_users.items():
                    # Pobierz dane użytkownika z SQL
                    user_obj = session.query(User).filter_by(username=user).first()
                    if user_obj:
                        user_dict = user_obj.to_dict()
                        user_company = user_dict.get('company', '')
                        # Dodaj jeśli z tej samej firmy
                        if user_company == current_user_company:
                            filtered_users[user] = data
            elif ranking_scope == 'global':
                # Wszyscy użytkownicy widoczni w globalnym rankingu
                for user, data in all_users.items():
                    user_obj = session.query(User).filter_by(username=user).first()
                    if user_obj:
                        user_dict = user_obj.to_dict()
                        # Dodaj jeśli użytkownik jest widoczny w globalnym rankingu
                        if is_visible_in_global_ranking(user_dict):
                            filtered_users[user] = data
            
            all_users = filtered_users
    except Exception as e:
        print(f"Error filtering ranking users: {e}")
        # W przypadku błędu, pozostawiamy wszystkich użytkowników
    
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
                            revenue_30d += get_contract_reward_coins(contract)
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
    
    # Zapisz pozycję użytkownika do historii
    if user_rank:
        bg_data = save_ranking_position(bg_data, user_rank, internal_ranking_type)
        save_game_data(user_data, bg_data, industry_id)
    
    st.info(f"""
    ℹ️ **Ranking aktywnych firm: {total_active}**
    
    {"🎉 Gratulacje! Jesteś na pozycji #" + str(user_rank) + "!" if user_rank else "Ukończ pierwszy kontrakt, aby pojawić się w rankingu!"}
    
    **Jak działają rankingi:**
    - Aktualizacja na żywo (przy każdym odświeżeniu)
    - Uwzględniamy: przychody, jakość pracy, reputację, poziom firmy
    - Rywalizuj z {total_active-1} innymi firmami!
    """)
    
    st.markdown("---")
    
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
        
        # Kolory podium - złoto, srebro, brąz
        if actual_rank == 1:
            podium_bg = "linear-gradient(135deg, #ffd70015 0%, #ffed4e15 100%)"
            podium_border = "#ffd700"
        elif actual_rank == 2:
            podium_bg = "linear-gradient(135deg, #c0c0c015 0%, #e8e8e815 100%)"
            podium_border = "#c0c0c0"
        elif actual_rank == 3:
            podium_bg = "linear-gradient(135deg, #cd7f3215 0%, #d4964815 100%)"
            podium_border = "#cd7f32"
        else:
            podium_bg = "white"
            podium_border = "#e2e8f0"
        
        # Format score zależnie od typu (liczba całkowita vs z przecinkiem)
        if ranking_type == "⭐ Jakość (średnia ocena)":
            score_display = f"{firm['score']:.1f}"
        else:
            score_display = f"{firm['score']:.0f}"
        
        if firm["is_user"]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; padding: 15px; border-radius: 10px; margin: 10px 0;
                        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
                <h3 style='margin:0;'>{medal} <span style='font-size: 1.2em;'>{firm['logo']}</span> {firm['name']} (Ty!)</h3>
                <p style='margin:5px 0 0 0;'>{score_label}: {score_display}{score_suffix}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background: {podium_bg}; border: 2px solid {podium_border}; 
                        padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <h4 style='margin:0;'>{medal} <span style='font-size: 1.2em;'>{firm['logo']}</span> {firm['name']}</h4>
                <p style='margin:5px 0 0 0; color: #666;'>{score_label}: {score_display}{score_suffix}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Wykres historii pozycji w rankingu
    st.markdown("---")
    render_ranking_history_chart(username, all_users, bg_data, internal_ranking_type, ranking_type, all_firms)
    
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

def render_ranking_history_chart(current_username, all_users, bg_data, internal_ranking_type, display_ranking_type, all_firms):
    """Renderuje wykres historii pozycji w rankingu z wyborem zakresu czasu i liniami dla TOP 10"""
    import plotly.graph_objects as go
    
    st.markdown(f"### 📊 Historia pozycji - {display_ranking_type}")
    
    # Wybór zakresu czasu
    col1, col2 = st.columns([3, 1])
    with col1:
        time_range = st.radio(
            "Zakres czasu:",
            ["📅 Ostatnie 7 dni", "📅 Ostatni miesiąc", "📅 Ostatni rok", "📅 Cała historia"],
            horizontal=True,
            key=f"ranking_time_range_{internal_ranking_type}"
        )
    
    # Mapowanie zakresu na liczbę dni
    days_map = {
        "📅 Ostatnie 7 dni": 7,
        "📅 Ostatni miesiąc": 30,
        "📅 Ostatni rok": 365,
        "📅 Cała historia": None
    }
    days = days_map.get(time_range)
    
    # Pobierz dane dla wszystkich graczy
    all_players_data = get_ranking_chart_data_for_players(all_users, internal_ranking_type, days, top_n=10)
    
    if not all_players_data:
        st.info("📊 Brak danych historycznych. Historia zacznie się zapisywać od teraz!")
        return
    
    # Debug info
    st.caption(f"🔍 Pokazuję dane dla typu rankingu: **{internal_ranking_type}** | Zakres: **{time_range}** | Graczy z danymi: **{len(all_players_data)}**")
    
    # Sortuj graczy po aktualnej pozycji (top 10)
    players_by_rank = sorted(
        [(username, data) for username, data in all_players_data.items() if data["current_rank"]],
        key=lambda x: x[1]["current_rank"]
    )[:10]
    
    # Dodaj aktualnego użytkownika jeśli nie jest w top 10
    if current_username not in [p[0] for p in players_by_rank]:
        if current_username in all_players_data:
            players_by_rank.append((current_username, all_players_data[current_username]))
    
    if not players_by_rank:
        st.info("📊 Brak danych historycznych. Historia zacznie się zapisywać od teraz!")
        return
    
    # Stwórz wykres
    fig = go.Figure()
    
    # Definicja kolorów
    color_map = {
        1: '#FFD700',      # Złoty
        2: '#C0C0C0',      # Srebrny
        3: '#CD7F32',      # Brązowy
        'top10': '#9CA3AF', # Szary dla reszty top 10
        'user': '#667eea'   # Niebieski dla użytkownika
    }
    
    # Dodaj linie dla każdego gracza
    for username, player_data in players_by_rank:
        current_rank = player_data["current_rank"]
        is_current_user = (username == current_username)
        
        # Określ kolor
        if is_current_user:
            # Użytkownik: jeśli jest na podium, to kolor podium, inaczej niebieski
            if current_rank in [1, 2, 3]:
                color = color_map[current_rank]
                line_width = 4
            else:
                color = color_map['user']
                line_width = 4
            name = f"{player_data['firm_logo']} {player_data['firm_name']} (Ty)"
            dash = 'solid'
        else:
            # Inni gracze: top 3 = kolor podium, reszta = szary
            if current_rank in [1, 2, 3]:
                color = color_map[current_rank]
                line_width = 3
            else:
                color = color_map['top10']
                line_width = 2
            name = f"{player_data['firm_logo']} {player_data['firm_name']}"
            dash = 'solid'
        
        # Dodaj linię
        fig.add_trace(go.Scatter(
            x=player_data["dates"],
            y=player_data["positions"],
            mode='lines+markers',
            name=name,
            line=dict(color=color, width=line_width, dash=dash),
            marker=dict(size=6 if is_current_user else 4, color=color),
            hovertemplate=f'<b>{name}</b><br>Data: %{{x}}<br>Pozycja: #%{{y}}<extra></extra>'
        ))
    
    # Zaktualizuj layout
    fig.update_layout(
        title=None,
        xaxis_title="Data",
        yaxis_title="Pozycja w rankingu",
        hovermode='x unified',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        yaxis=dict(
            autorange='reversed',  # Odwróć oś Y (1 na górze, większe liczby na dole)
            gridcolor='rgba(200,200,200,0.2)',
            tickformat='d'  # Liczby całkowite
        ),
        xaxis=dict(
            gridcolor='rgba(200,200,200,0.2)',
            tickangle=-45
        ),
        margin=dict(l=50, r=20, t=20, b=80),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        )
    )
    
    # Unikalna kombinacja dla cache busting
    chart_key = f"{internal_ranking_type}_{days}_{len(all_players_data)}"
    st.plotly_chart(fig, use_container_width=True, key=f"chart_{chart_key}")
    
    # Statystyki dla aktualnego użytkownika
    user_data = all_players_data.get(current_username)
    if user_data and len(user_data["positions"]) > 1:
        best_position = min(user_data["positions"])
        worst_position = max(user_data["positions"])
        current_position = user_data["positions"][-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Twoja najlepsza", f"#{best_position}")
        
        with col2:
            st.metric("Twoja obecna", f"#{current_position}")
        
        with col3:
            # Zmiana od poprzedniego pomiaru
            if len(user_data["positions"]) >= 2:
                prev_position = user_data["positions"][-2]
                change = prev_position - current_position  # Dodatnia = awans (lepiej)
                st.metric("Zmiana", f"#{current_position}", delta=change, delta_color="inverse")
            else:
                st.metric("Zmiana", "—")
        
        with col4:
            st.metric("Twoja najgorsza", f"#{worst_position}")


# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

# UWAGA: save_user_data jest importowane z data.users_new na początku pliku
# jako alias dla save_single_user

