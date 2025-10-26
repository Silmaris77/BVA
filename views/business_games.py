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
from data.users_new import save_single_user as save_user_data
from utils.business_game import (
    initialize_business_game, initialize_business_game_with_scenario, refresh_contract_pool, accept_contract,
    submit_contract_solution, submit_contract_conversation, hire_employee, fire_employee,
    calculate_daily_costs, calculate_total_daily_costs, get_firm_summary, get_revenue_chart_data,
    get_category_distribution, calculate_overall_score, can_accept_contract,
    can_hire_employee, update_user_ranking, get_objectives_summary, update_objectives_progress
)
from utils.components import zen_header
from utils.material3_components import apply_material3_theme
from utils.scroll_utils import scroll_to_top

# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def get_contract_reward_coins(contract: Dict) -> int:
    """Bezpieczne pobranie nagród w monetach z kontraktu (obsługa starych i nowych formatów)"""
    reward_data = contract.get("reward", 0)
    if isinstance(reward_data, dict):
        return reward_data.get("coins", 0)
    return reward_data  # Stary format - reward jako int


def get_contract_reward_reputation(contract: Dict) -> int:
    """Bezpieczne pobranie nagród w reputacji z kontraktu"""
    reward_data = contract.get("reward", 0)
    if isinstance(reward_data, dict):
        return reward_data.get("reputation", 0)
    return 0  # Stary format nie miał reputacji w reward


def get_game_data(user_data, industry_id="consulting"):
    """Pobiera dane gry dla wybranej branży (z backward compatibility)"""
    # Najpierw spróbuj nowej struktury
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        return user_data["business_games"][industry_id]
    # Fallback na starą strukturę (backward compatibility)
    elif "business_game" in user_data:
        return user_data["business_game"]
    # Jeśli nic nie znaleziono - zwróć pustą strukturę (nie None!)
    return {}

def save_game_data(user_data, bg_data, industry_id="consulting"):
    """Zapisuje dane gry dla wybranej branży (z backward compatibility)"""
    # Zapisz w nowej strukturze
    if "business_games" not in user_data:
        user_data["business_games"] = {}
    user_data["business_games"][industry_id] = bg_data
    # Dla backward compatibility - zapisz też w starej strukturze jeśli istnieje
    if "business_game" in user_data and industry_id == "consulting":
        user_data["business_game"] = bg_data
    return user_data

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
# GŁÓWNA FUNKCJA - META WIDOK
# =============================================================================

def show_business_games(username, user_data):
    """Meta-widok Business Games Suite - wybór branży lub gra"""
    
    # Przewiń na górę strony
    scroll_to_top()
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # MIGRACJA: Stara struktura business_game → business_games.consulting
    if "business_game" in user_data and "business_games" not in user_data:
        user_data["business_games"] = {
            "consulting": user_data["business_game"]
        }
        # Nie usuwamy starego klucza dla backward compatibility podczas przejścia
        save_user_data(username, user_data)
    
    # Inicjalizacja nowej struktury
    if "business_games" not in user_data:
        user_data["business_games"] = {}
    
    # Sprawdź czy jest aktywna branża w session_state
    if "selected_industry" not in st.session_state:
        # Sprawdź czy gracz ma już rozpoczętą grę w jakiejś branży
        if "consulting" in user_data["business_games"]:
            st.session_state["selected_industry"] = "consulting"
        else:
            st.session_state["selected_industry"] = None
    
    # ROUTING: Jeśli wybrano branżę → idź do gry, inaczej → selector
    if st.session_state["selected_industry"]:
        industry_id = st.session_state["selected_industry"]
        
        # Sprawdź czy gra dla tej branży już istnieje
        if industry_id in user_data["business_games"]:
            # Gra istnieje → pokaż rozgrywkę
            show_industry_game(username, user_data, industry_id)
        else:
            # Gra nie istnieje → pokaż selektor scenariuszy
            show_scenario_selector(username, user_data, industry_id)
    else:
        show_industry_selector(username, user_data)

# =============================================================================
# SELECTOR BRANŻY
# =============================================================================

def show_industry_selector(username, user_data):
    """Ekran wyboru branży - karty z różnymi grami branżowymi"""
    
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
            slogan="Od debiutu na półce do brand leadera - zdobądź serca konsumentów!",
            description="Zarządzaj markami konsumenckimi. Wprowadzaj produkty, prowadź kampanie, zdobywaj rynek.",
            features=["📦 Product launches", "📺 Marketing campaigns", "🏪 Distribution"],
            available=False,
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
        if st.button(button_label, key=f"start_{industry_id}", type="primary", width="stretch"):
            # Ustaw aktywną branżę (routing w show_business_games zdecyduje czy pokazać scenariusze czy grę)
            st.session_state["selected_industry"] = industry_id
            st.rerun()
    else:
        st.button("🔒 Wkrótce dostępne", key=f"locked_{industry_id}", disabled=True, width="stretch")
    
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

# =============================================================================
# HALL OF FAME - Globalny widok
# =============================================================================

def show_hall_of_fame():
    """Hall of Fame - legendarne zamknięte firmy"""
    
    st.markdown("---")
    st.markdown("## 🏛️ Hall of Fame - Legendarne Firmy")
    st.caption("Firmy, które osiągnęły sukces i zostały zamknięte z honorem")
    
    # Zbierz wszystkie zamknięte firmy ze wszystkich użytkowników
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
    if st.button("← Powrót do wyboru branży", key="back_to_industries", width="stretch"):
        st.session_state["selected_industry"] = None
        st.rerun()

def render_scenario_card(scenario_id, scenario_data, industry_id, username, user_data):
    """Renderuje kartę pojedynczego scenariusza w stylu spójnym z kartami kontraktów"""
    
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
    money = initial.get('money', 50000)
    reputation = initial.get('reputation', 50)
    office = initial.get('office_type', 'home_office')
    objectives = scenario_data.get('objectives', [])
    total_reward = sum(obj.get('reward_money', 0) for obj in objectives) if not is_lifetime else 0
    
    # Formatuj nazwę biura
    office_name = office.replace('_', ' ').title()
    
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
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Kapitał startowy</div>
<div style="color: #10b981; font-size: 18px; font-weight: 700;">💰 {money:,}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Reputacja</div>
<div style="color: #f59e0b; font-size: 18px; font-weight: 700;">⭐ {reputation}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Biuro</div>
<div style="color: #8b5cf6; font-size: 18px; font-weight: 700;">🏢 {office_name}</div>
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
        user_data["business_games"][industry_id] = initialize_business_game_with_scenario(
            username, industry_id, scenario_id
        )
        save_user_data(username, user_data)
        st.success(f"🎉 Scenariusz '{scenario_data.get('name')}' rozpoczęty! Powodzenia!")
        st.rerun()

# =============================================================================
# GRA BRANŻOWA
# =============================================================================

def show_industry_game(username, user_data, industry_id):
    """Widok gry dla wybranej branży"""
    
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
    
    # Pobierz dane branży
    bg_data = user_data["business_games"][industry_id]
    
    # MIGRACJA: Dodaj brakujące transakcje dla starych wydarzeń z monetami
    from utils.business_game import migrate_event_transactions
    user_data, migrated_count = migrate_event_transactions(user_data, industry_id)
    if migrated_count > 0:
        save_user_data(username, user_data)
        bg_data = user_data["business_games"][industry_id]
    
    # Odśwież pulę kontraktów
    bg_data = refresh_contract_pool(bg_data)
    user_data["business_games"][industry_id] = bg_data
    
    # Nagłówek z podsumowaniem firmy
    render_header(user_data, industry_id)
    
    st.markdown("---")
    
    # Główne zakładki (bez Instrukcji - teraz w Dashboard)
    tabs = st.tabs(["🏢 Dashboard", "💼 Rynek Kontraktów", "🏢 Zarządzanie", "⚙️ Ustawienia"])
    
    with tabs[0]:
        show_dashboard_tab(username, user_data, industry_id)
    
    with tabs[1]:
        show_contracts_tab(username, user_data, industry_id)
    
    with tabs[2]:
        # Pod-taby w Zarządzaniu
        management_tabs = st.tabs(["🏢 Biuro", "👥 Pracownicy", "📊 Raporty Finansowe", "📜 Historia & Wydarzenia"])
        
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

# =============================================================================
# NAGŁÓWEK
# =============================================================================

def render_header(user_data, industry_id="consulting"):
    """Renderuje nagłówek z profesjonalnymi kartami w stylu gamifikacji"""
    bg_data = user_data["business_games"][industry_id]
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
        firm_money = bg_data.get('money', 0)
        st.markdown(f"""
        <div class='stat-card gold'>
            <div class='stat-label'>💰 Saldo firmy</div>
            <div class='stat-value'>{firm_money:,}</div>
            <div style='font-size: 12px; color: #64748b;'>PLN</div>
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
            if "timestamp" not in trans:
                continue  # Pomiń transakcje bez timestamp
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

def show_dashboard_tab(username, user_data, industry_id="consulting"):
    """Zakładka Dashboard - podsumowanie firmy"""
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
    # INSTRUKCJA GRY - EXPANDER
    # =============================================================================
    
    with st.expander("📖 Jak grać w Business Games? (Instrukcja)", expanded=False):
        # Sekcja 1: Szybki start
        st.markdown("""
<div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #667eea; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px;'>
<div style='color: #667eea; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 12px;'>🚀 SZYBKI START (5 KROKÓW)</div>
<div style='color: #334155; font-size: 14px; line-height: 1.8;'>
<strong>1️⃣ Przyjmij kontrakt</strong> → Zakładka "💼 Rynek Kontraktów"<br>
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
        st.markdown("---")
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
    
# Koniec expandera instrukcji - wcięcie wraca do 4 spacji (poziom funkcji)

    st.markdown("---")
    
    # =============================================================================
    # SEKCJA CELÓW SCENARIUSZA
    # =============================================================================
    
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
        bg_data = get_game_data(user_data, industry_id)
        last_roll = bg_data.get("events", {}).get("last_roll")
    
    # Pending event (jeśli neutralne wymaga wyboru - blocking modal)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data, context="dashboard")
    
    st.markdown("---")
    
    # Pobierz podsumowanie
    summary = get_firm_summary(user_data, industry_id)
    
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
    
    # =============================================================================
    # SEKCJA OSTATNIO UKOŃCZONYCH KONTRAKTÓW - NOWOŚĆ!
    # =============================================================================
    
    completed_contracts = bg_data.get("contracts", {}).get("completed", [])
    
    # Pokaż maksymalnie 3 ostatnio ukończone kontrakty
    recent_completed = sorted(
        completed_contracts,
        key=lambda x: x.get("completed_date", ""),
        reverse=True
    )[:3]
    
    if recent_completed:
        st.subheader("🎯 Ostatnio Ukończone Kontrakty")
        st.caption("Zobacz wyniki swoich ostatnich kontraktów - nie musisz wchodzić w Historię!")
        
        # Wyświetl w kompaktowej formie
        for contract in recent_completed:
            rating = contract.get("rating", 0)
            reward_coins = get_contract_reward_coins(contract)
            rep_change = get_contract_reward_reputation(contract)
            
            # Kolor na podstawie oceny
            if rating >= 4:
                border_color = "#10b981"
                bg_color = "#f0fdf4"
            elif rating >= 3:
                border_color = "#f59e0b"
                bg_color = "#fffbeb"
            else:
                border_color = "#ef4444"
                bg_color = "#fef2f2"
            
            with st.expander(
                f"{contract.get('emoji', '📋')} {contract.get('tytul', 'Kontrakt')} · {'⭐' * rating} · {reward_coins:,} 💰",
                expanded=False
            ):
                # Kompaktowy widok wyniku
                st.markdown(f"""
                <div style='border-left: 5px solid {border_color}; 
                            background: {bg_color};
                            padding: 15px; 
                            margin: 10px 0; 
                            border-radius: 8px;'>
                    <p style='margin: 0; color: #666; font-size: 0.9em;'>
                        <strong>Klient:</strong> {contract.get('klient', 'N/A')} | 
                        <strong>Ukończono:</strong> {contract.get('completed_date', 'N/A')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Metryki w karcie
                rep_display = f"+{rep_change}" if rep_change >= 0 else str(rep_change)
                
                st.markdown(f"""
                <div style='background: linear-gradient(to right, #f8fafc, #f1f5f9); 
                            border-left: 4px solid #3b82f6; 
                            border-radius: 8px; 
                            padding: 16px; 
                            margin: 16px 0;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
                    <div style='display: flex; justify-content: space-around; text-align: center;'>
                        <div>
                            <div style='font-size: 24px; margin-bottom: 4px;'>⭐</div>
                            <div style='font-weight: 600; color: #1e293b;'>{rating}/5</div>
                            <div style='font-size: 12px; color: #64748b;'>Ocena</div>
                        </div>
                        <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                        <div>
                            <div style='font-size: 24px; margin-bottom: 4px;'>💰</div>
                            <div style='font-weight: 600; color: #1e293b;'>{reward_coins:,}</div>
                            <div style='font-size: 12px; color: #64748b;'>Zarobiono</div>
                        </div>
                        <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                        <div>
                            <div style='font-size: 24px; margin-bottom: 4px;'>📈</div>
                            <div style='font-weight: 600; color: #1e293b;'>{rep_display}</div>
                            <div style='font-size: 12px; color: #64748b;'>Reputacja</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Feedback od klienta
                feedback = contract.get("feedback", "Brak feedbacku")
                
                st.markdown("---")
                st.subheader("💬 Feedback od klienta")
                st.info(feedback)
                
                # Link do pełnej historii
                st.info("💡 Pełne szczegóły kontraktu (opis, zadanie, Twoje rozwiązanie) znajdziesz w zakładce **'📜 Historia & Wydarzenia'**")
        
        st.markdown("---")
    
    # NOWY WYKRES FINANSOWY z kontrolkami
    st.subheader("📊 Analiza Finansowa")
    
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

def render_active_contract_card(contract, username, user_data, bg_data):
    """Renderuje profesjonalną kartę aktywnego kontraktu w stylu game UI"""
    
    # Backward compatibility: ai_conversation → conversation
    contract_type = contract.get("contract_type")
    if contract_type == "ai_conversation":
        contract_type = "conversation"
    
    # Sprawdź czy to Decision Tree Contract
    if contract_type == "decision_tree":
        industry_id = bg_data.get("industry", "consulting")
        render_decision_tree_contract(contract, username, user_data, bg_data, industry_id)
        return
    
    # Sprawdź czy to Conversation Contract
    if contract_type == "conversation":
        industry_id = bg_data.get("industry", "consulting")
        render_conversation_contract(contract, username, user_data, bg_data, industry_id)
        return
    
    # Sprawdź czy to Speed Challenge Contract
    if contract_type == "speed_challenge":
        industry_id = bg_data.get("industry", "consulting")
        render_speed_challenge_contract(contract, username, user_data, bg_data, industry_id)
        return
    
    # Standardowy kontrakt (pisanie/mówienie)
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

def render_decision_tree_contract(contract, username, user_data, bg_data, industry_id="consulting"):
    """Renderuje interaktywny Decision Tree Contract"""
    from utils.decision_tree_engine import (
        initialize_decision_tree_state,
        get_current_node,
        make_choice,
        calculate_final_score,
        reset_decision_tree,
        get_decision_tree_summary,
        calculate_replay_value
    )
    
    contract_id = contract["id"]
    nodes = contract.get("nodes", {})
    start_node_id = contract.get("start_node", "scene_1")
    scoring_config = contract.get("scoring", {})
    
    # Initialize state
    initialize_decision_tree_state(contract_id, start_node_id)
    
    # Check if completed
    is_completed = st.session_state.get(f"dt_{contract_id}_completed", False)
    
    if is_completed:
        # Show final results
        final_results = calculate_final_score(contract_id, nodes, scoring_config)
        replay_info = calculate_replay_value(contract_id, nodes)
        
        st.success(f"🎉 **Ukończono Decision Tree Contract!**")
        
        # Beautiful results card
        ending_node = nodes.get(final_results["ending_id"])
        outcome = final_results.get("outcome", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⭐ Gwiazdki", f"{final_results['stars']}/5")
        with col2:
            st.metric("🎯 Punkty", final_results['total_points'])
        with col3:
            st.metric("🛤️ Długość ścieżki", final_results['path_length'])
        
        # Ending card
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 24px; border-radius: 16px; margin: 16px 0;'>
            <h2 style='margin: 0 0 12px 0;'>{final_results['ending_title']}</h2>
            <p style='margin: 0; font-size: 14px; line-height: 1.6; opacity: 0.95;'>
                {ending_node.get('text', '') if ending_node else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Outcome details
        if outcome:
            st.markdown("### 📊 Konsekwencje Twoich Decyzji")
            outcome_cols = st.columns(3)
            col_idx = 0
            for key, value in outcome.items():
                if key not in ['points', 'rating']:
                    with outcome_cols[col_idx % 3]:
                        if isinstance(value, (int, float)):
                            st.metric(key.replace('_', ' ').title(), f"{value:+,}" if value != 0 else str(value))
                        else:
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
                        col_idx += 1
        
        # Journey summary
        with st.expander("🗺️ Zobacz swoją ścieżkę decyzji"):
            summary = get_decision_tree_summary(contract_id)
            st.text(summary)
        
        # Replay value
        if replay_info['replay_recommended']:
            st.info(f"""
            🔄 **Warto zagrać ponownie!**
            
            - Odkryłeś **1** z **{replay_info['total_endings']}** zakończeń
            - To {'nie było najlepsze zakończenie' if not replay_info['is_best_ending'] else 'było najlepsze zakończenie! 🏆'}
            - Pozostało **{replay_info['undiscovered_endings']}** innych zakończeń do odkrycia
            
            Każda ścieżka uczy innych lekcji przywództwa!
            """)
        else:
            st.success(f"""
            🏆 **Gratulacje! Osiągnąłeś najlepsze zakończenie!**
            
            Możesz zagrać ponownie aby odkryć {replay_info['undiscovered_endings']} innych zakończeń.
            """)
        
        # Action buttons
        col_action1, col_action2, col_action3 = st.columns(3)
        
        with col_action1:
            if st.button("🔄 Zagraj ponownie", width="stretch", key=f"replay_{contract_id}"):
                reset_decision_tree(contract_id, start_node_id)
                st.rerun()
        
        with col_action2:
            if st.button("✅ Prześlij wynik", type="primary", width="stretch", key=f"submit_{contract_id}"):
                # Calculate reward based on stars
                base_reward = contract.get("nagroda_base", 500)
                reward_5star = contract.get("nagroda_5star", 1000)
                
                stars = final_results['stars']
                if stars == 5:
                    reward = reward_5star
                elif stars == 4:
                    reward = contract.get("nagroda_4star", int((base_reward + reward_5star) / 2))
                elif stars == 3:
                    reward = int((base_reward + reward_5star) / 2 * 0.8)
                elif stars == 2:
                    reward = int(base_reward * 0.8)
                else:
                    reward = base_reward
                
                # Mark contract as completed in bg_data
                # from utils.business_game import complete_contract_decision_tree
                updated_bg, success, message = complete_contract_decision_tree(
                    bg_data, 
                    contract_id, 
                    stars, 
                    reward, 
                    contract.get("reputacja", 20),
                    final_results,
                    user_data
                )
                
                if success:
                    save_game_data(user_data, updated_bg, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"{message} 💰 +{reward} monet | ⭐ +{contract.get('reputacja', 20)} reputacji")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(message)
        
        with col_action3:
            if st.button("← Powrót", width="stretch", key=f"back_{contract_id}"):
                st.session_state["view_contract"] = None
                st.rerun()
    
    else:
        # Show current scene
        current_node = get_current_node(contract_id, nodes)
        
        if not current_node:
            st.error("❌ Błąd: Nie znaleziono węzła w drzewie decyzji")
            return
        
        # Progress indicator
        path = st.session_state.get(f"dt_{contract_id}_path", [])
        current_points = st.session_state.get(f"dt_{contract_id}_points", 0)
        
        col_prog1, col_prog2 = st.columns([3, 1])
        with col_prog1:
            st.progress(min(len(path) / 10, 1.0), text=f"Scena {len(path) + 1}")
        with col_prog2:
            st.metric("Punkty", current_points)
        
        # Scene card
        st.markdown(f"""
        <div style='background: white; border-radius: 20px; padding: 32px; margin: 24px 0; 
                    box-shadow: 0 8px 32px rgba(0,0,0,0.12); border-left: 6px solid #667eea;'>
            <h2 style='margin: 0 0 16px 0; color: #1e293b; font-size: 24px;'>
                {current_node.get('title', 'Scena')}
            </h2>
            <div style='color: #475569; font-size: 16px; line-height: 1.8; white-space: pre-wrap;'>
                {current_node.get('text', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Choices
        if current_node.get('is_revelation'):
            # Auto-advance for revelation nodes
            st.info("ℹ️ *Mark się otwiera...*")
            time.sleep(1)
            choice = current_node['choices'][0]
            make_choice(contract_id, choice, nodes)
            st.rerun()
        else:
            st.markdown("### 🤔 Twój wybór:")
            
            for i, choice in enumerate(current_node.get('choices', [])):
                choice_text = choice['text']
                
                # Button dla każdego wyboru
                if st.button(
                    choice_text, 
                    key=f"{contract_id}_choice_{i}",
                    width="stretch",
                    type="secondary"
                ):
                    # Make choice
                    make_choice(contract_id, choice, nodes)
                    
                    # Show immediate feedback
                    feedback = choice.get('feedback', '')
                    if feedback:
                        if '✅' in feedback or '🏆' in feedback:
                            st.success(feedback)
                        elif '❌' in feedback:
                            st.error(feedback)
                        else:
                            st.info(feedback)
                        time.sleep(1.5)
                    
                    st.rerun()
                
                st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
        
        # Show path so far
        if len(path) > 0:
            with st.expander(f"📜 Twoja dotychczasowa ścieżka ({len(path)} decyzji)"):
                for i, step in enumerate(path, 1):
                    points_color = "green" if step['points'] > 0 else "red" if step['points'] < 0 else "gray"
                    st.markdown(f"""
                    **{i}.** {step['choice_text']}  
                    <span style='color: {points_color}; font-weight: bold;'>
                        {'+' if step['points'] > 0 else ''}{step['points']} pkt
                    </span>
                    """, unsafe_allow_html=True)
                    if step.get('feedback'):
                        st.caption(step['feedback'])
    
    # =============================================================================
    # SEKCJA RANKINGÓW
    # =============================================================================
    
    st.markdown("---")
    st.subheader("🏆 Rankingi")
    
    # Wywołaj funkcję rankingów (będzie wyświetlana jako część Dashboard)
    show_rankings_content(username, user_data, industry_id)

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
    
    st.subheader("📋 Aktywne Kontrakty")
    
    active_contracts = bg_data["contracts"]["active"]
    
    if len(active_contracts) == 0:
        st.info("✨ Brak aktywnych kontraktów. Przyjmij nowe zlecenie poniżej!")
    else:
        for contract in active_contracts:
            render_active_contract_card(contract, username, user_data, bg_data)
    
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
            ["Wszystkie", "Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership", "Conversation"],
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
    
    # Filtrowanie
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


def render_conversation_contract(contract, username, user_data, bg_data, industry_id="consulting"):
    """Renderuje interaktywny Conversation Contract - dynamiczna rozmowa z NPC"""
    from utils.ai_conversation_engine import (
        initialize_ai_conversation,
        get_conversation_state,
        process_player_message,
        calculate_final_conversation_score,
        reset_conversation
    )
    
    contract_id = contract["id"]
    npc_config = contract.get("npc_config", {})
    scenario_context = contract.get("scenario_context", "")
    
    # Inicjalizacja (per user!)
    conversation = get_conversation_state(contract_id, username)
    if not conversation:
        initialize_ai_conversation(contract_id, npc_config, scenario_context, username)
        conversation = get_conversation_state(contract_id, username)
    
    # Sprawdź czy zakończono
    is_completed = not conversation.get("conversation_active", True)
    
    # Sprawdź czy TTS jest dostępne
    from utils.ai_conversation_engine import TTS_AVAILABLE
    if not TTS_AVAILABLE:
        st.warning("🔇 Text-to-Speech niedostępne. Zainstaluj gTTS: `pip install gTTS`")
    
    # === NAGŁÓWEK KONTRAKTU ===
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 24px; border-radius: 16px; margin-bottom: 24px;'>
        <h2 style='margin: 0 0 8px 0;'>💬 {contract['tytul']}</h2>
        <p style='margin: 0; opacity: 0.9; font-size: 14px;'>{contract['opis']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if is_completed:
        # === WIDOK ZAKOŃCZENIA ===
        final_results = calculate_final_conversation_score(contract_id, username)
        
        st.success(f"🎉 **Rozmowa zakończona!**")
        
        # Metryki w kompaktowej karcie (jak inne kontrakty)
        stars = final_results.get('stars', 1)
        total_points = final_results.get('total_points', 0)
        
        # Oblicz nagrodę dla wyświetlenia
        reward_base = contract.get("nagroda_base", 500)
        reward_5star = contract.get("nagroda_5star", reward_base * 2)
        reward = int(reward_base + ((stars - 1) / 4.0) * (reward_5star - reward_base))
        rep_change = int(contract.get("reputacja", 20) * stars / 3)
        rep_display = f"+{rep_change}" if rep_change >= 0 else str(rep_change)
        
        st.markdown(f"""
        <div style='background: linear-gradient(to right, #f8fafc, #f1f5f9); 
                    border-left: 4px solid #3b82f6; 
                    border-radius: 8px; 
                    padding: 16px; 
                    margin: 16px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: space-around; text-align: center;'>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>⭐</div>
                    <div style='font-weight: 600; color: #1e293b;'>{stars}/5</div>
                    <div style='font-size: 12px; color: #64748b;'>Ocena</div>
                </div>
                <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>💰</div>
                    <div style='font-weight: 600; color: #1e293b;'>{reward:,}</div>
                    <div style='font-size: 12px; color: #64748b;'>Zarobiono</div>
                </div>
                <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>📈</div>
                    <div style='font-weight: 600; color: #1e293b;'>{rep_display}</div>
                    <div style='font-size: 12px; color: #64748b;'>Reputacja</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Feedback od klienta (jak w innych kontraktach)
        feedback = final_results.get('summary', 'Brak feedbacku')
        
        st.markdown("---")
        st.subheader("💬 Feedback od klienta")
        st.info(feedback)
        
        # Link do pełnej historii
        st.info("� Pełne szczegóły rozmowy znajdziesz w zakładce **'📜 Historia & Wydarzenia'**")
        
        st.markdown("---")
        
        # Historia rozmowy
        with st.expander("💬 Zobacz całą rozmowę"):
            messages = conversation.get("messages", [])
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("text", msg.get("content", ""))  # Obsługa obu kluczy
                timestamp = msg.get("timestamp", "")
                audio_data = msg.get("audio")
                
                if role == "npc":
                    st.markdown(f"""
                    <div style='background: #f1f5f9; padding: 12px; border-radius: 8px; 
                                margin: 8px 0; border-left: 4px solid #667eea;'>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>
                            👤 <strong>{npc_config.get('name', 'NPC')}</strong> · {timestamp}
                        </div>
                        <div style='color: #1e293b;'>{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Odtwórz audio jeśli dostępne
                    if audio_data:
                        import base64
                        audio_bytes = base64.b64decode(audio_data)
                        st.audio(audio_bytes, format="audio/mp3")
                        
                elif role == "player":
                    content_text = msg.get("text", msg.get("content", ""))
                    st.markdown(f"""
                    <div style='background: #dbeafe; padding: 12px; border-radius: 8px; 
                                margin: 8px 0; border-left: 4px solid #3b82f6;'>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>
                            🎮 <strong>Ty</strong> · {timestamp}
                        </div>
                        <div style='color: #1e293b;'>{content_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Przyciski akcji
        col_replay, col_submit = st.columns(2)
        with col_replay:
            if st.button("🔄 Zagraj ponownie", key=f"replay_{contract_id}", width="stretch"):
                reset_conversation(contract_id, npc_config, scenario_context, username)
                st.rerun()
        
        with col_submit:
            if st.button("✅ Zakończ kontrakt", key=f"submit_{contract_id}", 
                        type="primary", width="stretch"):
                # Import funkcji calculate_final_conversation_score
                from utils.ai_conversation_engine import calculate_final_conversation_score
                
                # Znajdź kontrakt
                contract_found = next((c for c in bg_data["contracts"]["active"] if c["id"] == contract_id), None)
                if not contract_found:
                    st.error("Kontrakt nie znaleziony w aktywnych")
                else:
                    try:
                        # Pobierz wynik z engine (per user!)
                        result = calculate_final_conversation_score(contract_id, username)
                        stars = result.get("stars", 1)
                        total_points = result.get("total_points", 0)
                        metrics = result.get("metrics", {})
                        feedback_summary = result.get("summary", "")
                        
                        # Oblicz nagrodę
                        reward_base = contract_found.get("nagroda_base", 500)
                        reward_5star = contract_found.get("nagroda_5star", reward_base * 2)
                        reward = int(reward_base + ((stars - 1) / 4.0) * (reward_5star - reward_base))
                        
                        # Dodaj nagrody
                        user_data["degencoins"] = user_data.get("degencoins", 0) + reward
                        bg_data["firm"]["reputation"] += contract_found.get("reputacja", 20) * stars / 3
                        bg_data["stats"]["total_revenue"] += reward
                        
                        # Przenieś do completed
                        completed_contract = contract_found.copy()
                        completed_contract["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        completed_contract["rating"] = stars  # Używamy "rating" jak inne kontrakty
                        completed_contract["stars"] = stars  # Dla kompatybilności
                        completed_contract["points"] = total_points
                        completed_contract["reward"] = reward
                        completed_contract["metrics"] = metrics
                        completed_contract["feedback"] = feedback_summary
                        completed_contract["status"] = "completed"
                        
                        bg_data["contracts"]["completed"].append(completed_contract)
                        bg_data["contracts"]["active"] = [c for c in bg_data["contracts"]["active"] if c["id"] != contract_id]
                        
                        # Zaktualizuj statystyki
                        bg_data["stats"]["contracts_completed"] = bg_data["stats"].get("contracts_completed", 0) + 1
                        rating_key = f"contracts_{stars}star"
                        bg_data["stats"][rating_key] = bg_data["stats"].get(rating_key, 0) + 1
                        
                        # Dodaj transakcję
                        if "history" not in bg_data:
                            bg_data["history"] = {"transactions": [], "level_ups": []}
                        if "transactions" not in bg_data["history"]:
                            bg_data["history"]["transactions"] = []
                        
                        bg_data["history"]["transactions"].append({
                            "type": "contract_reward",
                            "amount": reward,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "description": f"Conversation: {contract_found['tytul']} ({stars}⭐)"
                        })
                        
                        # Zapisz dane
                        save_game_data(user_data, bg_data, industry_id)
                        save_user_data(username, user_data)
                        
                        st.success(f"✅ Zakończono! 💰 +{reward} DegenCoins | ⭐ {stars}/5")
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Błąd przy zakończeniu kontraktu: {e}")
        
    else:
        # === WIDOK AKTYWNEJ ROZMOWY ===
        
        # Informacja o scenariuszu
        with st.expander("📖 Kontekst sytuacji", expanded=False):
            st.markdown(scenario_context)
        
        # Pobierz current_turn (potrzebny w logice, ale bez wyświetlania)
        current_turn = conversation.get("current_turn", 1)
        
        # === HISTORIA KONWERSACJI ===
        st.markdown("### 💬 Rozmowa")
        
        messages = conversation.get("messages", [])
        
        # Container dla wiadomości
        chat_container = st.container()
        with chat_container:
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("text", msg.get("content", ""))  # Obsługa obu kluczy
                timestamp = msg.get("timestamp", "")
                emotion = msg.get("emotion", "neutral")
                
                if role == "npc":
                    # Emotikon dla emocji NPC
                    emotion_emoji = {
                        "happy": "😊", "concerned": "😟", "frustrated": "😤",
                        "neutral": "😐", "thoughtful": "🤔", "relieved": "😌",
                        "angry": "😠", "satisfied": "😌"
                    }.get(emotion, "😐")
                    
                    st.markdown(f"""
                    <div style='background: #f1f5f9; padding: 16px; border-radius: 12px; 
                                margin: 12px 0; border-left: 4px solid #667eea; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                            <span style='font-size: 24px; margin-right: 8px;'>{emotion_emoji}</span>
                            <div>
                                <div style='font-weight: 600; color: #1e293b;'>
                                    {npc_config.get('name', 'NPC')} <span style='color: #64748b; font-size: 12px;'>({npc_config.get('role', 'Rozmówca')})</span>
                                </div>
                                <div style='font-size: 11px; color: #94a3b8;'>{timestamp}</div>
                            </div>
                        </div>
                        <div style='color: #334155; line-height: 1.6;'>{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Odtwórz audio jeśli dostępne
                    audio_data = msg.get("audio")
                    if audio_data:
                        # Dekoduj base64 i wyświetl odtwarzacz
                        import base64
                        audio_bytes = base64.b64decode(audio_data)
                        st.audio(audio_bytes, format="audio/mp3")
                    
                elif role == "player":
                    st.markdown(f"""
                    <div style='background: #dbeafe; padding: 16px; border-radius: 12px; 
                                margin: 12px 0; border-left: 4px solid #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                            <span style='font-size: 24px; margin-right: 8px;'>🎮</span>
                            <div>
                                <div style='font-weight: 600; color: #1e293b;'>Ty</div>
                                <div style='font-size: 11px; color: #64748b;'>{timestamp}</div>
                            </div>
                        </div>
                        <div style='color: #1e3a8a; line-height: 1.6;'>{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Feedback AI usunięty - realistyczna rozmowa bez "ściąg"
                
                elif role == "evaluation":
                    # Feedback od AI - również usunięty (był duplikat)
                    pass
        
        # === INPUT GRACZA ===
        st.markdown("---")
        st.markdown("### ✍️ Twoja odpowiedź")
        
        # Wskazówki kontekstowe
        if current_turn == 1:
            st.info(f"💡 **Wskazówka**: {npc_config.get('name', 'Rozmówca')} ma swoją perspektywę i cele. Spróbuj zrozumieć sytuację z jego punktu widzenia.")
        
        # === SPEECH-TO-TEXT INTERFACE (jak w "Feedback dla nowego pracownika") ===
        st.markdown("**🎤 Nagraj** (wielokrotnie, jeśli chcesz) **lub ✍️ pisz bezpośrednio w polu poniżej:**")
        
        # Klucze dla transkrypcji i wersjonowania
        transcription_key = f"ai_conv_transcription_{contract_id}"
        transcription_version_key = f"ai_conv_transcription_version_{contract_id}"
        last_audio_hash_key = f"ai_conv_last_audio_hash_{contract_id}"
        
        # Inicjalizacja
        if transcription_key not in st.session_state:
            st.session_state[transcription_key] = ""
        if transcription_version_key not in st.session_state:
            st.session_state[transcription_version_key] = 0
        if last_audio_hash_key not in st.session_state:
            st.session_state[last_audio_hash_key] = None
        
        audio_data = st.audio_input(
            "🎤 Nagrywanie...",
            key=f"audio_input_ai_conv_{contract_id}"
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
                                
                                api_key = st.secrets["API_KEYS"]["gemini"]
                                genai.configure(api_key=api_key)
                                
                                model = genai.GenerativeModel("models/gemini-2.5-flash")
                                prompt = f"""Dodaj interpunkcję (kropki, przecinki, pytajniki, wykrzykniki) do poniższego tekstu.
Nie zmieniaj słów, tylko dodaj znaki interpunkcyjne. Zachowaj strukturę i podział na zdania.
Zwróć tylko poprawiony tekst, bez dodatkowych komentarzy.

Tekst do poprawy:
{transcription}"""
                                response = model.generate_content(prompt)
                                transcription_with_punctuation = response.text.strip()
                                
                                # Komunikat usunięty - ciche działanie
                                transcription = transcription_with_punctuation
                                
                            except Exception as gemini_error:
                                # Błąd Gemini - cicho kontynuuj z surową transkrypcją
                                pass
                            
                            # DOPISZ do istniejącego tekstu (jak w "Feedback")
                            # Użytkownik może nagrywać wielokrotnie i budować odpowiedź
                            existing_text = st.session_state.get(transcription_key, "")
                            if existing_text.strip():
                                # Jeśli jest już jakiś tekst, dodaj nową linię i dopisz
                                st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
                            else:
                                # Jeśli to pierwsze nagranie, po prostu zapisz
                                st.session_state[transcription_key] = transcription
                            
                            # Inkrementuj wersję - to wymusi re-render text_area z nową wartością!
                            st.session_state[transcription_version_key] += 1
                            
                            # Komunikat usunięty - ciche działanie
                            
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
        
        # Dynamiczny klucz który zmienia się po transkrypcji (wymusza re-render)
        text_area_key = f"ai_conv_input_{contract_id}_{current_turn}_v{st.session_state[transcription_version_key]}"
        current_text = st.session_state.get(transcription_key, "")
        
        # Oblicz dynamiczną wysokość na podstawie liczby linii
        num_lines = current_text.count('\n') + 1
        # Minimalna wysokość: 120px, każda linia dodatkowa to ~25px
        dynamic_height = max(120, min(400, 120 + (num_lines - 3) * 25))
        
        # Text area dla odpowiedzi
        player_message = st.text_area(
            "📝 Możesz edytować transkrypcję lub pisać bezpośrednio:",
            value=current_text,
            height=dynamic_height,
            key=text_area_key,
            placeholder=f"Wpisz swoją odpowiedź do {npc_config.get('name', 'rozmówcy')}... lub użyj mikrofonu powyżej"
        )
        
        # Synchronizuj wartość z pola tekstowego do session_state
        if text_area_key in st.session_state:
            st.session_state[transcription_key] = st.session_state[text_area_key]
        
        # Przyciski
        col_send, col_end = st.columns([3, 1])
        
        with col_send:
            if st.button("📤 Wyślij wiadomość", type="primary", width="stretch", 
                        disabled=not player_message.strip()):
                if player_message.strip():
                    with st.spinner("🤖 AI analizuje Twoją odpowiedź i generuje reakcję..."):
                        # Get Gemini API key
                        api_key = st.secrets.get("API_KEYS", {}).get("gemini", "")
                        if not api_key:
                            st.error("❌ Brak klucza API Gemini. Skonfiguruj secrets.")
                        else:
                            try:
                                # Process message through AI engine (per user!)
                                evaluation, npc_reaction = process_player_message(
                                    contract_id, 
                                    player_message, 
                                    api_key,
                                    username
                                )
                                
                                # Wyczyść pole tekstowe po wysłaniu (NOWY klucz!)
                                st.session_state[transcription_key] = ""
                                st.session_state[transcription_version_key] += 1  # Wymusza re-render
                                
                                # Success - rerun to show new messages
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Błąd podczas przetwarzania: {str(e)}")
        
        with col_end:
            if st.button("🏁 Zakończ", width="stretch"):
                # Zakończ i od razu przenieś do completed (jak "Zakończ kontrakt")
                from utils.ai_conversation_engine import calculate_final_conversation_score
                
                # Znajdź kontrakt
                contract_found = next((c for c in bg_data["contracts"]["active"] if c["id"] == contract_id), None)
                if not contract_found:
                    st.error("Kontrakt nie znaleziony w aktywnych")
                else:
                    try:
                        # Pobierz wynik z engine (per user!)
                        result = calculate_final_conversation_score(contract_id, username)
                        stars = result.get("stars", 1)
                        total_points = result.get("total_points", 0)
                        metrics = result.get("metrics", {})
                        feedback_summary = result.get("summary", "")
                        
                        # Oblicz nagrodę
                        reward_base = contract_found.get("nagroda_base", 500)
                        reward_5star = contract_found.get("nagroda_5star", reward_base * 2)
                        reward = int(reward_base + ((stars - 1) / 4.0) * (reward_5star - reward_base))
                        
                        # Dodaj nagrody
                        user_data["degencoins"] = user_data.get("degencoins", 0) + reward
                        bg_data["firm"]["reputation"] += contract_found.get("reputacja", 20) * stars / 3
                        bg_data["stats"]["total_revenue"] += reward
                        
                        # Przenieś do completed
                        completed_contract = contract_found.copy()
                        completed_contract["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        completed_contract["rating"] = stars  # Używamy "rating" jak inne kontrakty
                        completed_contract["stars"] = stars  # Dla kompatybilności
                        completed_contract["points"] = total_points
                        completed_contract["reward"] = reward
                        completed_contract["metrics"] = metrics
                        completed_contract["feedback"] = feedback_summary
                        completed_contract["status"] = "completed"
                        
                        bg_data["contracts"]["completed"].append(completed_contract)
                        bg_data["contracts"]["active"] = [c for c in bg_data["contracts"]["active"] if c["id"] != contract_id]
                        
                        # Zaktualizuj statystyki
                        bg_data["stats"]["contracts_completed"] = bg_data["stats"].get("contracts_completed", 0) + 1
                        rating_key = f"contracts_{stars}star"
                        bg_data["stats"][rating_key] = bg_data["stats"].get(rating_key, 0) + 1
                        
                        # Dodaj transakcję
                        if "history" not in bg_data:
                            bg_data["history"] = {"transactions": [], "level_ups": []}
                        if "transactions" not in bg_data["history"]:
                            bg_data["history"]["transactions"] = []
                        
                        bg_data["history"]["transactions"].append({
                            "type": "contract_reward",
                            "amount": reward,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "description": f"Conversation: {contract_found['tytul']} ({stars}⭐)"
                        })
                        
                        # Zapisz dane
                        save_game_data(user_data, bg_data, industry_id)
                        save_user_data(username, user_data)
                        
                        # Wyczyść stan konwersacji
                        conv_key = f"ai_conv_{username}_{contract_id}"
                        if conv_key in st.session_state:
                            del st.session_state[conv_key]
                        
                        st.success(f"✅ Zakończono! 💰 +{reward} DegenCoins | ⭐ {stars}/5")
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Błąd przy zakończeniu kontraktu: {e}")


def render_speed_challenge_contract(contract, username, user_data, bg_data, industry_id="consulting"):
    """Renderuje Speed Challenge Contract - kontrakt z limitem czasu"""
    from utils.speed_challenge_engine import (
        initialize_speed_challenge,
        get_challenge_state,
        start_challenge,
        get_remaining_time,
        render_timer,
        complete_speed_challenge,
        reset_challenge
    )
    
    contract_id = contract["id"]
    challenge_config = contract.get("challenge_config", {})
    time_limit = contract.get("time_limit_seconds", 60)
    speed_bonus_multiplier = contract.get("speed_bonus_multiplier", 1.5)
    pressure_level = contract.get("pressure_level", "medium")
    
    # Inicjalizacja
    initialize_speed_challenge(contract_id, challenge_config, time_limit)
    state = get_challenge_state(contract_id)
    
    is_completed = state.get("completed", False)
    
    # === NAGŁÓWEK KONTRAKTU ===
    pressure_colors = {
        "low": ("#10b981", "#d1fae5"),
        "medium": ("#f59e0b", "#fef3c7"),
        "high": ("#ef4444", "#fee2e2")
    }
    pressure_color, pressure_bg = pressure_colors.get(pressure_level, pressure_colors["medium"])
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {pressure_color} 0%, {pressure_color}dd 100%); 
                color: white; padding: 24px; border-radius: 16px; margin-bottom: 24px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <div style='display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <h2 style='margin: 0 0 8px 0; font-size: 24px;'>⚡ {contract['tytul']}</h2>
                <p style='margin: 0; opacity: 0.95; font-size: 14px;'>{contract['opis']}</p>
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 12px 20px; border-radius: 8px;'>
                <div style='font-size: 32px; font-weight: bold; margin: 0;'>{time_limit}s</div>
                <div style='font-size: 12px; opacity: 0.9; margin-top: 4px;'>LIMIT CZASU</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if is_completed:
        # === WIDOK ZAKOŃCZENIA ===
        evaluation = state.get("evaluation_result", {})
        
        stars = evaluation.get("stars", 3)
        points = evaluation.get("points", 0)
        base_points = evaluation.get("base_points", 0)
        speed_bonus = evaluation.get("speed_bonus_applied", 0)
        time_taken = evaluation.get("time_taken", 0)
        on_time = evaluation.get("on_time", True)
        
        # Pokaż wyniki
        st.success("🎉 **Challenge zakończony!**" if on_time else "⏰ **Challenge zakończony (po czasie)**")
        
        st.markdown("---")
        
        # Metryki
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("### ⭐")
            st.markdown(f"**Ocena:** {stars}/5")
        
        with col2:
            st.markdown("### 🎯")
            if speed_bonus > 0:
                st.markdown(f"**Punkty:** ~~{base_points}~~ **{points}**")
                st.caption(f"💨 Speed bonus: +{int(speed_bonus * 100)}%")
            else:
                st.markdown(f"**Punkty:** {points}")
        
        with col3:
            st.markdown("### ⏱️")
            time_color = "green" if on_time else "red"
            st.markdown(f"**Czas:** :{time_color}[{time_taken:.1f}s]")
            st.caption(f"Limit: {time_limit}s")
        
        with col4:
            result_emoji = "🏆" if stars >= 4 and on_time else ("🤝" if on_time else "⏰")
            st.markdown(f"### {result_emoji}")
            st.markdown(f"**{'SUCCESS' if stars >= 4 and on_time else ('OK' if on_time else 'TIMEOUT')}**")
        
        st.markdown("---")
        
        # Feedback
        feedback_text = evaluation.get("feedback", "Brak szczegółowego feedbacku")
        st.markdown(f"""
        <div style='background: {pressure_bg}; border-left: 4px solid {pressure_color}; 
                    padding: 16px; border-radius: 8px; margin: 16px 0;'>
            <h4 style='margin: 0 0 8px 0; color: #1f2937;'>💭 Feedback</h4>
            <p style='margin: 0; color: #4b5563;'>{feedback_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Strengths & Improvements
        col_str, col_imp = st.columns(2)
        
        with col_str:
            st.markdown("#### ✅ Mocne strony")
            strengths = evaluation.get("strengths", [])
            if strengths:
                for strength in strengths:
                    st.markdown(f"- {strength}")
            else:
                st.caption("Brak szczegółów")
        
        with col_imp:
            st.markdown("#### 🎯 Do poprawy")
            improvements = evaluation.get("improvements", [])
            if improvements:
                for improvement in improvements:
                    st.markdown(f"- {improvement}")
            else:
                st.caption("Świetna robota!")
        
        st.markdown("---")
        
        # Twoja odpowiedź
        with st.expander("📝 Twoja odpowiedź", expanded=False):
            st.markdown(state.get("player_response", ""))
        
        # Kontekst problemu
        with st.expander("📋 Problem do rozwiązania"):
            st.markdown(challenge_config.get("problem", "Brak opisu"))
        
        st.markdown("---")
        
        # Przyciski akcji
        col_close, col_retry = st.columns(2)
        
        with col_close:
            if st.button("✅ Zamknij i kompletuj", use_container_width=True, type="primary"):
                # Zapisz wyniki do kontraktu
                final_reward = 0  # Initialize
                
                # Aktualizuj kontrakt
                for i, c in enumerate(bg_data["contracts"]["active"]):
                    if c["id"] == contract_id:
                        bg_data["contracts"]["active"][i].update({
                            "status": "completed",
                            "rating": stars,
                            "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "speed_challenge_results": {
                                "time_taken": time_taken,
                                "time_limit": time_limit,
                                "on_time": on_time,
                                "speed_bonus": speed_bonus,
                                "pressure_level": pressure_level
                            }
                        })
                        
                        # Przenieś do completed
                        completed_contract = bg_data["contracts"]["active"].pop(i)
                        bg_data["contracts"]["completed"].append(completed_contract)
                        
                        # Dodaj nagrody
                        reward_multiplier = {1: 0.5, 2: 0.7, 3: 1.0, 4: 1.3, 5: 1.6}.get(stars, 1.0)
                        base_reward = contract.get("nagroda_base", 500)
                        final_reward = int(base_reward * reward_multiplier * (1 + speed_bonus * 0.3))
                        
                        user_data["degencoins"] = user_data.get("degencoins", 0) + final_reward
                        bg_data["stats"]["total_revenue"] += final_reward
                        bg_data["firm"]["reputation"] += contract.get("reputacja", 20) * stars / 3
                        
                        # Dodaj transakcję
                        if "history" not in bg_data:
                            bg_data["history"] = {"transactions": [], "level_ups": []}
                        if "transactions" not in bg_data["history"]:
                            bg_data["history"]["transactions"] = []
                        
                        bg_data["history"]["transactions"].append({
                            "type": "contract_reward",
                            "amount": final_reward,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "description": f"Speed Challenge: {contract['tytul']} ({stars}⭐)"
                        })
                        
                        break
                
                # Zapisz i resetuj
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                reset_challenge(contract_id)
                st.success(f"💰 Otrzymujesz {final_reward} DegenCoins!")
                st.rerun()
        
        with col_retry:
            if st.button("🔄 Spróbuj ponownie", use_container_width=True):
                reset_challenge(contract_id)
                st.rerun()
    
    else:
        # === WIDOK GRY ===
        
        # Kontekst challenge
        client_name = challenge_config.get("client_name", "Klient")
        client_role = challenge_config.get("client_role", "")
        urgency_reason = challenge_config.get("urgency_reason", "Pilna sprawa!")
        
        st.markdown(f"""
        <div style='background: #f8fafc; padding: 16px; border-radius: 12px; margin-bottom: 20px;
                    border: 2px solid {pressure_color};'>
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
                <div style='background: {pressure_color}; color: white; 
                            padding: 8px 16px; border-radius: 20px; font-weight: bold;'>
                    {client_name}
                </div>
                <div style='color: #64748b; font-size: 14px;'>{client_role}</div>
            </div>
            <div style='background: {pressure_bg}; padding: 12px; border-radius: 8px;
                        border-left: 4px solid {pressure_color};'>
                <div style='font-weight: bold; color: {pressure_color}; margin-bottom: 8px;'>
                    ⚡ {urgency_reason}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Problem do rozwiązania
        problem = challenge_config.get("problem", "Brak opisu problemu")
        
        # Konwertuj Markdown na HTML
        import re
        problem_html = problem.replace(chr(10), '<br>')
        problem_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', problem_html)  # **bold**
        problem_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', problem_html)  # *italic*
        
        st.markdown(f"""
        <div style='background: white; padding: 20px; border-radius: 12px; 
                    border: 1px solid #e5e7eb; margin-bottom: 24px;
                    line-height: 1.6; color: #1f2937;'>
            {problem_html}
        </div>
        """, unsafe_allow_html=True)
        
        
        # Start button lub timer
        if not state.get("started", False):
            st.markdown("---")
            st.markdown(f"""
            <div style='background: {pressure_bg}; padding: 20px; border-radius: 12px; text-align: center;'>
                <h3 style='color: {pressure_color}; margin: 0 0 12px 0;'>⏱️ Gotowy na challenge?</h3>
                <p style='margin: 0; color: #64748b;'>
                    Masz **{time_limit} sekund** na odpowiedź.<br>
                    Im szybciej odpowiesz, tym większy bonus! 💨
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            
            if st.button("🚀 START TIMER", use_container_width=True, type="primary"):
                start_challenge(contract_id)
                st.rerun()
        
        else:
            # Timer aktywny - JavaScript countdown (bez reruns!)
            remaining = get_remaining_time(contract_id)
            time_out = remaining <= 0
            
            # JavaScript timer
            timer_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    }}
                    @keyframes pulse {{
                        0%, 100% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.05); }}
                    }}
                </style>
            </head>
            <body>
                <div id="timer-container"></div>
                <script>
                (function() {{
                    const container = document.getElementById('timer-container');
                    let secondsLeft = {max(0, int(remaining))};
                    const totalSeconds = {time_limit};
                    
                    function updateTimer() {{
                        const minutes = Math.floor(secondsLeft / 60);
                        const seconds = secondsLeft % 60;
                        const percentage = (secondsLeft / totalSeconds) * 100;
                        
                        let color, bgColor;
                        if (percentage > 50) {{
                            color = '#4ade80';
                            bgColor = '#f0fdf4';
                        }} else if (percentage > 25) {{
                            color = '#fbbf24';
                            bgColor = '#fffbeb';
                        }} else {{
                            color = '#f87171';
                            bgColor = '#fef2f2';
                        }}
                        
                        if (secondsLeft <= 0) {{
                            container.innerHTML = '<div style="background: #fee; border: 2px solid #f00; padding: 16px; border-radius: 8px; text-align: center; animation: pulse 1s infinite;"><h2 style="color: #c00; margin: 0; font-size: 32px;">⏰ CZAS MINĄŁ!</h2><p style="margin: 8px 0 0 0; color: #666;">Zbyt późno na odpowiedź...</p></div>';
                        }} else {{
                            const minutesStr = String(minutes).padStart(2, '0');
                            const secondsStr = String(seconds).padStart(2, '0');
                            
                            container.innerHTML = '<div style="background: ' + bgColor + '; border: 2px solid ' + color + '; padding: 16px; border-radius: 8px; text-align: center;"><h2 style="color: ' + color + '; margin: 0; font-size: 48px; font-family: monospace; font-weight: bold;">' + minutesStr + ':' + secondsStr + '</h2><p style="margin: 8px 0 0 0; color: #666; font-size: 14px;">Pozostały czas</p></div>';
                            
                            secondsLeft--;
                            setTimeout(updateTimer, 1000);
                        }}
                    }}
                    
                    updateTimer();
                }})();
                </script>
            </body>
            </html>
            """
            
            st.components.v1.html(timer_html, height=120)
            
            st.markdown("---")
            
            # Pole odpowiedzi
            st.markdown("### ✍️ Twoja odpowiedź")
            
            response = st.text_area(
                "Wpisz swoją poradę dla klienta:",
                height=200,
                placeholder="Bądź konkretny, zwięzły i actionable...",
                key=f"speed_response_{contract_id}",
                disabled=time_out
            )
            
            st.markdown("")
            
            # Przyciski
            col_submit, col_cancel = st.columns([3, 1])
            
            with col_submit:
                submit_disabled = not response.strip() or time_out
                if st.button(
                    "📤 Wyślij odpowiedź" if not time_out else "⏰ Czas minął",
                    use_container_width=True,
                    type="primary",
                    disabled=submit_disabled
                ):
                    # Oceń odpowiedź
                    with st.spinner("🤖 AI ocenia twoją odpowiedź..."):
                        evaluation = complete_speed_challenge(
                            contract_id,
                            response,
                            challenge_config
                        )
                    
                    st.rerun()
            
            with col_cancel:
                if st.button("❌ Anuluj", use_container_width=True):
                    reset_challenge(contract_id)
                    st.rerun()


def render_contract_card(contract, username, user_data, bg_data, can_accept_new, industry_id="consulting"):
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
        
        # Expander ze szczegółami zadania - kompaktowy layout z kartami
        with st.expander("👁️ Zobacz szczegóły zadania", expanded=False):
            # Zadanie w karcie (opcjonalne - dla standardowych kontraktów)
            if 'zadanie' in contract:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                            border-left: 4px solid #667eea; 
                            border-radius: 12px; 
                            padding: 16px 20px; 
                            margin-bottom: 16px;'>
                    <div style='color: #667eea; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 8px;'>
                        🎯 ZADANIE DO WYKONANIA
                    </div>
                    <div style='color: #334155; font-size: 14px; line-height: 1.6;'>
                        {contract['zadanie']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Wymagana wiedza w karcie (opcjonalne)
            if 'wymagana_wiedza' in contract and contract['wymagana_wiedza']:
                knowledge_items = "".join([f"<div style='padding: 6px 12px; background: white; border-radius: 6px; margin-bottom: 6px; color: #475569; font-size: 13px;'>✓ {req}</div>" for req in contract['wymagana_wiedza']])
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #10b98115 0%, #05966915 100%); 
                            border-left: 4px solid #10b981; 
                            border-radius: 12px; 
                            padding: 16px 20px; 
                            margin-bottom: 16px;'>
                    <div style='color: #10b981; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 12px;'>
                        📚 WYMAGANA WIEDZA
                    </div>
                    {knowledge_items}
                </div>
                """, unsafe_allow_html=True)
            
            # Dodatkowe info w kompaktowej formie
            st.markdown(f"""
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 12px;'>
                <div style='background: #f8fafc; border-radius: 8px; padding: 12px; text-align: center;'>
                    <div style='color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Wymagany poziom</div>
                    <div style='color: #1e293b; font-size: 18px; font-weight: 700;'>🏆 {contract['wymagany_poziom']}</div>
                </div>
                <div style='background: #f8fafc; border-radius: 8px; padding: 12px; text-align: center;'>
                    <div style='color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Kategoria</div>
                    <div style='color: #1e293b; font-size: 18px; font-weight: 700;'>📂 {contract['kategoria']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Przycisk przyjęcia - szerszy dla lepszej czytelności na laptopach
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Sprawdź możliwość przyjęcia
            if not can_accept_new:
                st.button("❌ Brak miejsca", key=f"no_space_{contract['id']}", disabled=True, width="stretch")
            else:
                if st.button("✅ Przyjmij kontrakt", key=f"accept_{contract['id']}", type="primary", width="stretch"):
                    updated_bg, success, message, _ = accept_contract(bg_data, contract['id'], user_data)
                    
                    if success:
                        save_game_data(user_data, updated_bg, industry_id)
                        save_user_data(username, user_data)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

# =============================================================================
# TAB 3: PRACOWNICY
# =============================================================================

# =============================================================================
# TAB 3A: BIURO
# =============================================================================

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
        if st.button("🗑️ Zwolnij", key=f"fire_{employee['id']}", type="secondary", width="stretch"):
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
                     help=reason, width="stretch")
        else:
            if st.button("✅ Zatrudnij", key=f"hire_{emp_type}", type="primary", width="stretch"):
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
        width="stretch",
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
    st.dataframe(df, width="stretch", hide_index=True)
    
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
    st.dataframe(df, width="stretch", hide_index=True)
    
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
    """Zakładka Historia & Wydarzenia - chronologiczna oś czasu"""
    bg_data = get_game_data(user_data, industry_id)
    
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
    reward_coins = get_contract_reward_coins(contract)
    
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
        
        # Metryki w karcie
        rep_change = get_contract_reward_reputation(contract)
        rep_display = f"+{rep_change}" if rep_change >= 0 else str(rep_change)
        
        st.markdown(f"""
        <div style='background: linear-gradient(to right, #f8fafc, #f1f5f9); 
                    border-left: 4px solid #3b82f6; 
                    border-radius: 8px; 
                    padding: 16px; 
                    margin: 16px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: space-around; text-align: center;'>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>⭐</div>
                    <div style='font-weight: 600; color: #1e293b;'>{rating}/5</div>
                    <div style='font-size: 12px; color: #64748b;'>Ocena</div>
                </div>
                <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>💰</div>
                    <div style='font-weight: 600; color: #1e293b;'>{reward_coins:,}</div>
                    <div style='font-size: 12px; color: #64748b;'>Zarobiono</div>
                </div>
                <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>📈</div>
                    <div style='font-weight: 600; color: #1e293b;'>{rep_display}</div>
                    <div style='font-size: 12px; color: #64748b;'>Reputacja</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Feedback od klienta
        st.subheader("💬 Feedback od klienta")
        st.info(feedback)
        
        # Expander z pełnymi szczegółami
        with st.expander("📋 Zobacz szczegóły kontraktu i Twoje rozwiązanie"):
            # Karta 1: Opis sytuacji - Header
            st.markdown("""
            <div style='background: linear-gradient(135deg, #8b5cf615 0%, #6d28d915 100%); 
                        border-left: 4px solid #8b5cf6; 
                        border-radius: 12px 12px 0 0; 
                        padding: 12px 20px 8px 20px; 
                        margin-bottom: 0;'>
                <div style='color: #8b5cf6; 
                            font-size: 11px; 
                            text-transform: uppercase; 
                            letter-spacing: 1px; 
                            font-weight: 600;'>
                    📄 OPIS SYTUACJI
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Content
            st.markdown("""
            <div style='background: linear-gradient(135deg, #8b5cf615 0%, #6d28d915 100%); 
                        border-left: 4px solid #8b5cf6; 
                        border-radius: 0 0 12px 12px; 
                        padding: 8px 20px 16px 20px; 
                        margin: 0 0 16px 0;'>
            """, unsafe_allow_html=True)
            
            st.markdown(contract['opis'])
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Karta 2: Zadanie - Header
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f59e0b15 0%, #d9770615 100%); 
                        border-left: 4px solid #f59e0b; 
                        border-radius: 12px 12px 0 0; 
                        padding: 12px 20px 8px 20px; 
                        margin-bottom: 0;'>
                <div style='color: #f59e0b; 
                            font-size: 11px; 
                            text-transform: uppercase; 
                            letter-spacing: 1px; 
                            font-weight: 600;'>
                    🎯 ZADANIE
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Content
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f59e0b15 0%, #d9770615 100%); 
                        border-left: 4px solid #f59e0b; 
                        border-radius: 0 0 12px 12px; 
                        padding: 8px 20px 16px 20px; 
                        margin: 0 0 16px 0;'>
            """, unsafe_allow_html=True)
            
            st.markdown(contract['zadanie'])
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Karta 3: Twoje rozwiązanie - Header
            st.markdown("""
            <div style='background: linear-gradient(135deg, #06b6d415 0%, #0891b215 100%); 
                        border-left: 4px solid #06b6d4; 
                        border-radius: 12px 12px 0 0; 
                        padding: 12px 20px 8px 20px; 
                        margin-bottom: 0;'>
                <div style='color: #06b6d4; 
                            font-size: 11px; 
                            text-transform: uppercase; 
                            letter-spacing: 1px; 
                            font-weight: 600;'>
                    ✍️ TWOJE ROZWIĄZANIE
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Content
            solution = contract.get("solution", "Brak zapisanego rozwiązania")
            st.markdown("""
            <div style='background: linear-gradient(135deg, #06b6d415 0%, #0891b215 100%); 
                        border-left: 4px solid #06b6d4; 
                        border-radius: 0 0 12px 12px; 
                        padding: 8px 20px 16px 20px; 
                        margin: 0 0 0 0;'>
            """, unsafe_allow_html=True)
            
            st.markdown(f"```\n{solution}\n```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
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
<div style="display: flex; align-items: start; gap: 20px; margin-bottom: 12px;">
<div style="font-size: 56px; line-height: 1;">{event['emoji']}</div>
<div>
<div style="font-size: 14px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">{icon} Wydarzenie dnia</div>
<div style="font-size: 22px; font-weight: 700;">{event['title']}</div>
</div>
</div>
<div style="font-size: 15px; opacity: 0.95; line-height: 1.7;">{event['description']}</div>
{flavor_html}
{effects_html}
</div>"""
    
    st.markdown(event_card_html, unsafe_allow_html=True)

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
            if st.button(choice["text"], key=f"event_choice_{event_hash}_{idx}", type="primary" if idx == 0 else "secondary", width="stretch"):
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
    
    st.markdown("---")
    
    # Twoja pozycja (highlight)
    render_user_rank_highlight(bg_data, ranking_type)
    
    st.markdown("---")
    
    # Pobierz PRAWDZIWE dane wszystkich użytkowników
    from data.users_new import load_user_data
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
# FUNKCJE POMOCNICZE
# =============================================================================

def save_user_data(username, user_data):
    """Zapisuje dane użytkownika"""
    from data.users_new import load_user_data, save_user_data as save_all_users
    all_users = load_user_data()
    all_users[username] = user_data
    save_all_users(all_users)
