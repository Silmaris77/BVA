"""
🛒 FMCG Playable Game UI
Minimal playable interface for FMCG sales simulation
Uses fmcg_mechanics.py backend
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from typing import Dict, Optional
import time
import folium
from streamlit_folium import st_folium, folium_static
import html
import os
import base64

# Import tasks system (Phase 1)
from data.tasks import (
    get_weekly_tasks,
    create_task_from_template,
    check_task_completion,
    payout_task_reward
)
from utils.task_tracking_helpers import (
    reset_weekly_task_stats,
    track_visit_for_tasks,
    track_client_activation,
    initialize_weekly_stats_if_needed
)

# Import FMCG mechanics
from utils.fmcg_mechanics import (
    execute_visit_placeholder,
    advance_day,
    update_fmcg_game_state_sql,
    load_fmcg_game_state_sql,
    get_client_status_summary,
    get_clients_needing_visit,
    calculate_visit_energy_cost,
    calculate_travel_time,
    calculate_distance_between_points,
    optimize_route,
    calculate_route_distance,
    get_route_geometry,
    get_route_geometry_split
)
from utils.fmcg_client_helpers import get_reputation_status
from utils.business_game import initialize_fmcg_game_new
from data.industries.fmcg_data_schema import FMCGClientData, FMCGGameState
from data.industries.fmcg_products import (
    FRESHLIFE_PRODUCTS,
    COMPETITOR_PRODUCTS,
    get_all_products,
    compare_products,
    get_competitors_for_product
)

# Import new client card extensions
from utils.fmcg_client_helpers import (
    migrate_fmcg_customers_to_new_structure,
    get_client_by_id,
    get_clients_by_status,
    is_visit_overdue,
    get_reputation_status,
    create_new_client_entry
)

# Import AI conversation
from utils.fmcg_ai_conversation import conduct_fmcg_conversation

from utils.fmcg_reputation import (
    update_client_reputation,
    record_visit,
    sign_contract,
    check_overdue_visits
)

# Import notes panel
from utils.notes_panel import render_notes_panel

# Import tasks system
from utils.fmcg_tasks import (
    ONBOARDING_TASKS,
    get_task_status,
    submit_task,
    get_static_feedback,
    complete_task,
    all_tasks_completed,
    get_pending_tasks_count,
    evaluate_task_with_ai
)
from utils.fmcg_products import (
    get_product_info,
    suggest_cross_sell_products,
    get_portfolio_summary,
    FRESHLIFE_PRODUCTS as FRESHLIFE_PRODUCTS_NEW
)

# Import client detail card component
from views.business_games_refactored.components.client_detail_card import render_client_detail_card
from views.business_games_refactored.components.visit_panel_advanced import render_visit_panel_advanced


def get_pin_color_by_days(days_since_visit):
    """
    Zwraca kolor pinu na mapie bazując na liczbie dni od ostatniej wizyty.
    
    Args:
        days_since_visit: liczba dni od ostatniej wizyty (None = nowy klient)
    
    Returns:
        str: nazwa koloru dla folium.Icon ('white', 'green', 'yellow', 'orange', 'red')
    """
    if days_since_visit is None:  # Nowy klient
        return 'white'
    elif days_since_visit <= 3:
        return 'green'
    elif days_since_visit <= 7:
        return 'yellow'  # lightgreen is deprecated, use yellow
    elif days_since_visit <= 14:
        return 'orange'
    else:  # 15+ dni
        return 'red'


def get_color_emoji_by_days(days_since_visit):
    """
    Zwraca emoji koloru dla lepszej wizualizacji w UI.
    
    Args:
        days_since_visit: liczba dni od ostatniej wizyty (None = nowy klient)
    
    Returns:
        str: emoji kolorowego kółka
    """
    if days_since_visit is None:
        return '⚪'
    elif days_since_visit <= 3:
        return '🟢'
    elif days_since_visit <= 7:
        return '🟡'
    elif days_since_visit <= 14:
        return '🟠'
    else:
        return '🔴'


def _count_discovered_fields(discovered_info: Dict) -> int:
    """Liczy ile pól zostało odkrytych (nie None, nie puste)"""
    if not discovered_info:
        return 0
    
    count = 0
    for value in discovered_info.values():
        if value is not None and value != "" and value != []:
            count += 1
    return count


def _get_product_price(product: Dict) -> float:
    """
    Pobiera cenę produktu obsługując różne struktury (retail/foodservice).
    
    Returns:
        float: Cena produktu
    """
    # Food Service (Heinz scenario)
    if "price_foodservice" in product:
        return product["price_foodservice"]
    
    # Retail (Quick Start, Lifetime)
    return product.get("price_retail", 0)


def _get_product_margin(product: Dict) -> tuple[float, float]:
    """
    Pobiera marżę produktu (% i PLN) obsługując różne struktury.
    
    Returns:
        tuple: (margin_percent, margin_pln)
    """
    # Nowa struktura (FreshLife przez hurtownię)
    if "margin_shop_percent" in product:
        return product["margin_shop_percent"], product.get("margin_shop_pln", 0)
    
    # Food Service (Heinz)
    if "margin_foodservice_pct" in product:
        margin_percent = product["margin_foodservice_pct"]
        price = _get_product_price(product)
        margin_pln = price * margin_percent / 100
        return margin_percent, margin_pln
    
    # Stara struktura (produkty konkurencji lub stare FreshLife)
    margin_percent = product.get("margin_percent", 0)
    margin_pln = product.get("margin_pln", 0)
    
    # Jeśli brak margin_pln, oblicz
    if margin_pln == 0 and margin_percent > 0:
        price = _get_product_price(product)
        margin_pln = price * margin_percent / 100
    
    return margin_percent, margin_pln


def _render_product_details(product: Dict, scenario_id: str = 'lifetime'):
    """
    Renderuje szczegółowy widok produktu ze storytellingiem i argumentami
    
    Args:
        product: Dict z danymi produktu (z FRESHLIFE_PRODUCTS lub COMPETITOR_PRODUCTS)
        scenario_id: ID scenariusza (heinz_food_service, quick_start, lifetime)
    """
    # Determine if product is "own brand" based on scenario
    if scenario_id == "heinz_food_service":
        # In Heinz scenario, Heinz and Pudliszki are own brands
        is_own_brand = product.get("brand") in ["Heinz", "Pudliszki"]
    else:
        # In FreshLife scenarios (lifetime, quick_start), FreshLife is own brand
        is_own_brand = product.get("brand") == "FreshLife"
    
    # Keep is_freshlife for backward compatibility in some code sections
    is_freshlife = is_own_brand
    
    # Header
    emoji_map = {
        "Personal Care": "🧴",
        "Food": "🍽️",
        "Home Care": "🧽",
        "Snacks": "🍪",
        "Beverages": "🥤"
    }
    category_emoji = product.get("emoji", emoji_map.get(product.get("category", ""), "📦"))
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #6366f115 0%, #6366f105 100%); 
                padding: 20px; border-radius: 12px; margin-bottom: 16px;'>
        <div style='text-align: center; font-size: 48px; margin-bottom: 8px;'>
            {category_emoji}
        </div>
        <div style='text-align: center; font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 4px;'>
            {product['name']}
        </div>
        <div style='text-align: center; font-size: 14px; color: #64748b;'>
            {product['brand']} • {product['category']} • {product.get('subcategory', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Basic info - różnie dla modelu bezpośredniego vs przez hurtownię
    distribution_model = product.get("distribution_model", "direct")
    
    # Get price and margin with backward compatibility
    price = _get_product_price(product)
    margin_percent, margin_pln = _get_product_margin(product)
    
    if distribution_model == "wholesale" and is_freshlife:
        # MODEL PRZEZ HURTOWNIĘ (realistyczny)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Cena detaliczna", f"{price:.2f} PLN")
        
        with col2:
            price_wholesale = product.get('price_wholesale_eurocash', 0)
            margin_shop_pln = product.get('margin_shop_pln', 0)
            margin_shop_percent = product.get('margin_shop_percent', 0)
            st.metric("🏪 Cena dla sklepu (Eurocash)", f"{price_wholesale:.2f} PLN")
            st.caption(f"Marża sklepu: {margin_shop_percent}% ({margin_shop_pln:.2f} PLN/szt)")
        
        with col3:
            moq = product.get('moq_freshlife', 6)
            moq_eurocash = product.get('moq_eurocash', 1)
            st.metric("📦 MOQ", f"{moq_eurocash} szt (Eurocash)")
            st.caption(f"Bezpośrednio od nas: {moq} szt")
        
        # Dostępność w hurtowniach
        available_at = product.get("available_at", [])
        if available_at:
            st.info(f"📍 **Dostępny w:** {', '.join(available_at)}")
            eurocash_sku = product.get("eurocash_sku", "")
            if eurocash_sku:
                st.caption(f"Kod w Eurocash: `{eurocash_sku}` 📋")
        
    else:
        # MODEL BEZPOŚREDNI (uproszczony) lub produkty konkurencji
        col_price, col_margin, col_pop = st.columns(3)
        
        with col_price:
            st.metric("💰 Cena detaliczna", f"{price:.2f} PLN")
        
        with col_margin:
            # Already calculated above
            st.metric("📊 Marża dla sklepu", f"{margin_percent}%")
            st.metric("💵 Marża", f"{margin_percent}% ({margin_pln:.2f} PLN)")
        
        with col_pop:
            pop = product.get('popularity', 0)
            st.metric("📊 Popularność", f"{pop}%")
    
    # For FreshLife products - show extended description
    if is_freshlife:
        st.markdown("---")
        
        # Description
        description = product.get("description", "Wysokiej jakości produkt marki FreshLife.")
        st.markdown(f"### 📖 O produkcie")
        st.markdown(description)
        
        # Target customer
        target = product.get("target_customer", "")
        if target:
            st.markdown(f"### 🎯 Dla kogo")
            st.info(target)
        
        # Rotation speed
        rotation = product.get("rotation_speed", "")
        rotation_context = product.get("rotation_speed_context", "")
        suggested_order = product.get("suggested_initial_order", "")
        
        if rotation or suggested_order:
            st.markdown("### 📦 Rotacja i zamówienie")
            col_rot, col_sug = st.columns(2)
            with col_rot:
                if rotation:
                    st.markdown(f"**� Rotacja:** {rotation}")
                    if rotation_context:
                        st.caption(rotation_context)
            with col_sug:
                if suggested_order:
                    st.markdown(f"**🏷️ Sugerowane zamówienie:** {suggested_order}")
        
        # Competitors comparison
        competitors = product.get("competitors", [])
        if competitors:
            st.markdown("---")
            st.markdown("### ✅ Przewagi nad konkurencją")
            
            for comp in competitors:
                comp_brand = comp.get("brand", "Konkurencja")
                comp_price_retail = comp.get("price_retail", 0)
                comp_price_wholesale_est = comp.get("price_wholesale_estimated", 0)
                comp_moq = comp.get("moq_estimated", "?")
                comp_rotation = comp.get("rotation_estimated", "?")
                advantages = comp.get("advantages", [])
                
                # Header konkurenta
                st.markdown(f"**vs {comp_brand}**")
                st.caption(f"Cena detaliczna: {comp_price_retail:.2f} PLN | "
                          f"Cena hurtowa: ~{comp_price_wholesale_est:.2f} PLN | "
                          f"MOQ: ~{comp_moq} szt | "
                          f"Rotacja: {comp_rotation}")
                
                # Przewagi
                for adv in advantages:
                    st.markdown(f"{adv}")
                st.markdown("")
        
        # Sales arguments
        sales_args = product.get("sales_arguments", [])
        if sales_args:
            st.markdown("---")
            st.markdown("### 💬 Argumenty sprzedażowe")
            st.caption("Kliknij, aby skopiować gotowy argument do rozmowy!")
            
            for i, arg in enumerate(sales_args, 1):
                # Button to copy
                if st.button(f"📋 Kopiuj #{i}", key=f"copy_arg_{product['id']}_{i}"):
                    st.code(arg, language=None)
                    st.success("✅ Skopiuj ten tekst i użyj w rozmowie!")
                
                st.markdown(f"""
                <div style='background: #f1f5f9; padding: 12px; border-radius: 8px; 
                            margin-bottom: 8px; border-left: 3px solid #10b981;'>
                    <div style='font-size: 14px; color: #1e293b;'>
                        {arg}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Copy all arguments button
            all_args_text = "\n\n".join([f"• {arg}" for arg in sales_args])
            if st.button("📋 Kopiuj wszystkie argumenty", key=f"copy_args_{product['id']}"):
                st.code(all_args_text, language=None)
                st.success("✅ Skopiuj tekst powyżej (Ctrl+C)")
        
        # USP
        usp = product.get("usp", "")
        if usp:
            st.markdown("---")
            st.info(f"**✨ USP:** {usp}")
    
    else:
        # For competitor products - basic info only
        st.markdown("---")
        if scenario_id == "heinz_food_service":
            st.info("ℹ️ To produkt konkurencji (nie należy do portfolio Heinz).")
        else:
            st.info("ℹ️ To produkt konkurencji. FreshLife nie sprzedaje tego produktu.")
        
        # Show basic details
        usp = product.get("usp", "")
        if usp:
            st.markdown(f"**Cechy produktu:** {usp}")


def show_fmcg_playable_game(username: str):
    """
    Main FMCG playable game interface
    
    Components:
    1. Dashboard (energy, stats, day/week)
    2. Client map (Folium with status colors)
    3. Visit interface (client select, quality slider, order input)
    4. Day advancement button
    """
    
    # Initialize selected_client_id to prevent UnboundLocalError
    # This variable may be set in different code paths (route mode, detail view, etc.)
    selected_client_id = None
    
    # Get scenario info for title
    scenario_id = st.session_state.get("fmcg_scenario", "quick_start")
    is_heinz_scenario = "heinz" in scenario_id.lower()
    
    scenario_titles = {
        "quick_start": "🚀 Quick Start - Piaseczno Territory",
        "heinz_food_service": "🍅 Heinz Food Service Challenge - Dzięgielów",
        "lifetime": "♾️ Lifetime Mode - Unlimited"
    }
    
    # Ensure territory/base coords are set to Pelikanów 2 if still using old defaults
    try:
        # New desired base coordinates (Piaseczno, ul. Pelikanów 2)
        desired_lat = 52.0534
        desired_lon = 21.0689

        current_lat = game_state.get("territory_latitude")
        current_lon = game_state.get("territory_longitude")

        # If missing or equal to old default, update and persist
        if (current_lat is None and current_lon is None) or (
            abs(current_lat - 52.0846) < 1e-6 and abs(current_lon - 21.0250) < 1e-6
        ):
            game_state["territory_latitude"] = desired_lat
            game_state["territory_longitude"] = desired_lon
            # Persist updated state (if DB save function available)
            try:
                update_fmcg_game_state_sql(username, game_state, clients)
            except Exception:
                # Non-fatal: just update session state
                pass
            # Also update session copy
            st.session_state["fmcg_game_state"] = game_state

    except Exception:
        # Don't block UI on failures here
        pass

    # =============================================================================
    # DATA MIGRATION CHECK
    # =============================================================================
    
    # Load user data and check if migration needed
    from data.users_new import get_current_user_data
    user_data = get_current_user_data(username)
    
    if user_data and "business_games" in user_data and "fmcg" in user_data["business_games"]:
        bg_data = user_data["business_games"]["fmcg"]
        customers_data = bg_data.get("customers", {})
        
        # Check if old structure exists (prospects/active_clients lists)
        if "clients" not in customers_data and ("prospects" in customers_data or "active_clients" in customers_data):
            st.info("🔄 Wykryto starą strukturę danych - migruję do nowego systemu...")
            
            migrated_data, count = migrate_fmcg_customers_to_new_structure(bg_data)
            bg_data.update(migrated_data)
            user_data["business_games"]["fmcg"] = bg_data
            
            # Save to JSON
            import json
            try:
                with open('users_data.json', 'r', encoding='utf-8') as f:
                    all_users = json.load(f)
                all_users[username] = user_data
                with open('users_data.json', 'w', encoding='utf-8') as f:
                    json.dump(all_users, f, ensure_ascii=False, indent=2)
                
                st.success(f"✅ Zmigrowano {count} klientów! Nowy system reputacji i portfolio aktywny.")
            except Exception as e:
                st.error(f"❌ Błąd migracji: {e}")
    
    # =============================================================================
    # LOAD OR INITIALIZE GAME
    # =============================================================================
    
    # Check if we should initialize (BEFORE loading from SQL!)
    if "fmcg_game_initialized" not in st.session_state:
        st.session_state["fmcg_game_initialized"] = False
    
    # Initialize new game with scenario selection (if not initialized)
    if not st.session_state["fmcg_game_initialized"]:
        st.markdown("### 🎮 Wybierz Scenariusz")
        st.markdown("---")
        
        # Scenario selection
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #10b98115 0%, #10b98105 100%); 
                        padding: 20px; border-radius: 12px; border: 2px solid #10b981; min-height: 320px;">
                <div style="font-size: 2.5rem; text-align: center; margin-bottom: 10px;">🚀</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #065f46; margin-bottom: 8px; text-align: center;">
                    Quick Start
                </div>
                <div style="font-size: 0.85rem; color: #047857; margin-bottom: 12px; text-align: center;">
                    Poziom: Łatwy
                </div>
                <div style="font-size: 0.9rem; color: #1f2937; line-height: 1.5;">
                    <strong>Idealne na początek!</strong><br><br>
                    • 12 klientów w Piaseczno<br>
                    • FreshLife produkty (10 SKU)<br>
                    • Podstawowe cele sprzedażowe<br>
                    • Tutorial i onboarding<br><br>
                    <em>⏱️ Czas gry: 4-6 tygodni</em>
                </div>
            </div>
            """, unsafe_allow_html=True)
            scenario_quick = st.button("Wybierz Quick Start", key="btn_quick", use_container_width=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #3b82f615 0%, #3b82f605 100%); 
                        padding: 20px; border-radius: 12px; border: 2px solid #3b82f6; min-height: 320px;">
                <div style="font-size: 2.5rem; text-align: center; margin-bottom: 10px;">🍅</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #1e40af; margin-bottom: 8px; text-align: center;">
                    Heinz Food Service
                </div>
                <div style="font-size: 0.85rem; color: #2563eb; margin-bottom: 12px; text-align: center;">
                    Poziom: Średni
                </div>
                <div style="font-size: 0.9rem; color: #1f2937; line-height: 1.5;">
                    <strong>Portfolio Management!</strong><br><br>
                    • 25 klientów Food Service<br>
                    • Heinz (premium) + Pudliszki (value)<br>
                    • Strategia dwóch marek<br>
                    • Przejmowanie z Kotlin<br><br>
                    <em>⏱️ Czas gry: 8 tygodni</em>
                </div>
            </div>
            """, unsafe_allow_html=True)
            scenario_heinz = st.button("Wybierz Heinz", key="btn_heinz", use_container_width=True, type="primary")
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f59e0b15 0%, #f59e0b05 100%); 
                        padding: 20px; border-radius: 12px; border: 2px solid #f59e0b; min-height: 320px;">
                <div style="font-size: 2.5rem; text-align: center; margin-bottom: 10px;">♾️</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #92400e; margin-bottom: 8px; text-align: center;">
                    Lifetime
                </div>
                <div style="font-size: 0.85rem; color: #b45309; margin-bottom: 12px; text-align: center;">
                    Poziom: Otwarty
                </div>
                <div style="font-size: 0.9rem; color: #1f2937; line-height: 1.5;">
                    <strong>Sandbox bez limitów!</strong><br><br>
                    • Nieograniczony czas gry<br>
                    • Brak konkretnych celów<br>
                    • Rywalizacja z innymi graczami<br>
                    • Eksperymentuj i ucz się<br><br>
                    <em>⏱️ Czas gry: ∞</em>
                </div>
            </div>
            """, unsafe_allow_html=True)
            scenario_lifetime = st.button("Wybierz Lifetime", key="btn_lifetime", use_container_width=True)
        
        st.markdown("---")
        
        # Handle scenario selection
        selected_scenario = None
        if scenario_quick:
            selected_scenario = "quick_start"
        elif scenario_heinz:
            selected_scenario = "heinz_food_service"
        elif scenario_lifetime:
            selected_scenario = "lifetime"
        
        if selected_scenario:
            with st.spinner(f"🎮 Inicjalizacja scenariusza..."):
                # Import scenario loader
                from data.scenarios import load_scenario_clients, SCENARIOS
                
                # Initialize game with scenario
                if selected_scenario == "heinz_food_service":
                    # Load Heinz scenario
                    scenario_config = SCENARIOS["fmcg"]["heinz_food_service"]
                    clients_db = load_scenario_clients(scenario_config.get("client_database"))
                    
                    # Initialize game state
                    game_data = initialize_fmcg_game_new(username, scenario=selected_scenario)
                    game_state = game_data["fmcg_state"]
                    
                    # Override with Heinz clients
                    if clients_db:
                        game_state["clients"] = clients_db
                        game_state["scenario_id"] = "heinz_food_service"
                        game_state["company"] = "Heinz Polska"
                        game_state["territory_name"] = "Dzięgielów Food Service"
                        game_state["territory_latitude"] = 49.7271667  # Lipowa 29 (49°43'37.8"N)
                        game_state["territory_longitude"] = 18.7025833  # 18°42'09.3"E
                        game_state["clients_total"] = 25
                        game_state["clients_prospect"] = 25
                        game_state["clients_active"] = 0
                        
                        st.info(f"✅ Załadowano {len(clients_db)} klientów Food Service z regionu Dzięgielów")
                    
                    clients = game_state.get("clients", {})
                else:
                    # Quick Start or Lifetime - standard initialization
                    game_data = initialize_fmcg_game_new(username, scenario=selected_scenario)
                    game_state = game_data["fmcg_state"]
                    game_state["scenario_id"] = selected_scenario
                    clients = game_state.get("clients", {})
                
                # Save initial state (will overwrite existing data)
                save_success = update_fmcg_game_state_sql(username, game_state, clients)
                
                if save_success:
                    st.success(f"✅ Scenariusz '{selected_scenario}' uruchomiony!")
                    st.session_state["fmcg_game_initialized"] = True
                    st.session_state["fmcg_game_state"] = game_state
                    st.session_state["fmcg_clients"] = clients
                    st.session_state["fmcg_scenario"] = selected_scenario
                    st.rerun()
                else:
                    st.error("❌ Błąd zapisu gry")
                    return
        else:
            st.info("👆 Wybierz scenariusz aby rozpocząć grę")
            return
    else:
        # Load from session state (or SQL if session empty)
        game_state = st.session_state.get("fmcg_game_state")
        clients = st.session_state.get("fmcg_clients")
        
        # If session state is empty, try loading from SQL
        if not game_state or not clients:
            loaded_data = load_fmcg_game_state_sql(username)
            
            if loaded_data:
                game_state, clients = loaded_data
                
                # Check scenario and set correct base coordinates
                scenario_id = game_state.get("scenario_id", "")
                
                if "heinz" in scenario_id.lower():
                    # Heinz scenario - Dzięgielów
                    desired_lat = 49.7271667  # Lipowa 29, Dzięgielów (49°43'37.8"N)
                    desired_lon = 18.7025833  # 18°42'09.3"E
                    territory_name = "Dzięgielów Food Service"
                else:
                    # Quick Start / Lifetime - Piaseczno
                    desired_lat = 52.0748  # Centrum Piaseczna (Rynek)
                    desired_lon = 21.0274
                    territory_name = game_state.get("territory_name", "Piaseczno")
                
                # Update coordinates based on scenario
                game_state["territory_latitude"] = desired_lat
                game_state["territory_longitude"] = desired_lon
                game_state["territory_name"] = territory_name
                
                # Update session state
                st.session_state["fmcg_game_state"] = game_state
                st.session_state["fmcg_clients"] = clients
            else:
                # No data in SQL either - reset initialization
                st.error("❌ Nie znaleziono zapisanej gry. Wybierz scenariusz.")
                st.session_state["fmcg_game_initialized"] = False
                st.rerun()
                return
    
    # =============================================================================
    # LOAD PRODUCTS FOR CURRENT SCENARIO
    # =============================================================================
    
    # Determine which products to use based on scenario
    scenario_id = game_state.get("scenario_id", "quick_start")
    
    if scenario_id == "heinz_food_service":
        # Load Heinz products from scenario config
        from data.scenarios import SCENARIOS
        scenario_config = SCENARIOS["fmcg"]["heinz_food_service"]
        scenario_products = scenario_config.get("products", {})
        
        # Convert to FRESHLIFE_PRODUCTS format (dict with product_id as key)
        CURRENT_PRODUCTS = {}
        for idx, prod in enumerate(scenario_products.get("own", [])):
            prod_id = prod.get("id", f"prod_{idx}")
            CURRENT_PRODUCTS[prod_id] = prod
        
        # Also load competitor products if available
        CURRENT_COMPETITOR_PRODUCTS = {}
        for idx, prod in enumerate(scenario_products.get("competitor", [])):
            prod_id = prod.get("id", f"comp_{idx}")
            CURRENT_COMPETITOR_PRODUCTS[prod_id] = prod
    else:
        # Use default FreshLife products for Quick Start and Lifetime
        CURRENT_PRODUCTS = FRESHLIFE_PRODUCTS
        CURRENT_COMPETITOR_PRODUCTS = COMPETITOR_PRODUCTS
    
    # =============================================================================
    # TABS NAVIGATION
    # =============================================================================
    
    # Initialize weekly task stats if needed
    initialize_weekly_stats_if_needed(game_state)
    
    # Pre-calculate common variables used across tabs
    energy_pct = game_state.get("energy", 100)
    status_summary = get_client_status_summary(clients)
    current_week = game_state.get("current_week", 1)
    visits_this_week = game_state.get("visits_this_week", 0)
    
    # Liczba zadań do wykonania
    pending_tasks = get_pending_tasks_count(st.session_state)
    tasks_badge = f" ({pending_tasks})" if pending_tasks > 0 else ""
    
    tab_dashboard, tab_sales, tab_hr, tab_instructions, tab_settings = st.tabs([
        f"📊 Dashboard{tasks_badge}",
        "🎯 Sprzedaż",
        "👥 HR & Team",
        "📖 Instrukcja",
        "⚙️ Ustawienia"
    ])
    
    # =============================================================================
    # TAB: DASHBOARD
    # =============================================================================
    
    with tab_dashboard:
        # =============================================================================
        # HERO SECTION (zawsze widoczny)
        # =============================================================================
        
        # Get values needed for Hero Section
        energy_pct = game_state.get("energy", 100)
        status_summary = get_client_status_summary(clients)
        current_week = game_state.get("current_week", 1)
        current_day = game_state.get("current_day", "Monday")
        tasks_completed_count = 3 - get_pending_tasks_count(st.session_state)
        all_done = all_tasks_completed(st.session_state)
        
        # Reputation System (NEW)
        from utils.reputation_system import (
            calculate_overall_rating,
            get_tier,
            get_next_tier
        )
        
        # Initialize reputation if not exists
        if "reputation" not in game_state:
            from utils.reputation_system import initialize_reputation_system
            game_state["reputation"] = initialize_reputation_system()
        
        # Use saved overall_rating if exists, otherwise calculate
        if "overall_rating" in game_state.get("reputation", {}):
            overall_rating = game_state["reputation"]["overall_rating"]
        else:
            overall_rating = calculate_overall_rating(game_state, clients)
            game_state["reputation"]["overall_rating"] = overall_rating
        
        current_tier = get_tier(overall_rating)
        next_tier = get_next_tier(current_tier["name"])
        
        unlock_tokens = game_state.get("reputation", {}).get("unlock_tokens", 0)
        training_credits = game_state.get("reputation", {}).get("training_credits", 0)
        
        # Progress to next tier
        if next_tier:
            progress_to_next = ((overall_rating - current_tier["min_rating"]) / 
                               (next_tier["min_rating"] - current_tier["min_rating"])) * 100
            points_needed = next_tier["min_rating"] - overall_rating
        else:
            progress_to_next = 100
            points_needed = 0
        
        # Format values for display
        overall_rating_fmt = f"{overall_rating:.1f}"
        progress_to_next_fmt = f"{progress_to_next:.0f}"
        points_needed_fmt = f"{points_needed:.0f}"
        current_tier_emoji = current_tier["emoji"]
        current_tier_name = current_tier["name"]
        next_tier_emoji = next_tier["emoji"] if next_tier else "✨"
        next_tier_name = next_tier["name"] if next_tier else "Maximum"
        next_tier_text = (f"Progress to {next_tier_emoji} {next_tier_name}: {points_needed_fmt} points needed" 
                         if next_tier else "✨ Maximum tier achieved!")

        
        # Energy emoji based on level
        if energy_pct > 66:
            energy_emoji = "⚡"
        elif energy_pct > 33:
            energy_emoji = "🔋"
        else:
            energy_emoji = "🪫"
        
        # Tasks status
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_index = day_names.index(current_day) if current_day in day_names else 0
        is_trial = (current_week == 1 and day_index < 2)
        
        if all_done:
            tasks_status = "✅ Komplet"
            tasks_color = "#10b981"
        elif is_trial:
            tasks_status = f"⏰ {tasks_completed_count}/3"
            tasks_color = "#f59e0b"
        else:
            tasks_status = f"❗ {tasks_completed_count}/3"
            tasks_color = "#ef4444"
        
        # Hero Section - Gaming Style
        st.markdown(f"""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; border-radius: 16px; color: white; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);'>
<div style='background: rgba(255,255,255,0.15); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 2px solid rgba(255,255,255,0.3);'>
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
<div>
<div style='font-size: 14px; opacity: 0.9; font-weight: 600; margin-bottom: 4px;'>⭐ OVERALL RATING</div>
<div style='font-size: 32px; font-weight: 700;'>{overall_rating_fmt}/100 {current_tier_emoji} {current_tier_name}</div>
</div>
<div style='text-align: right;'>
<div style='font-size: 14px; opacity: 0.9; font-weight: 600;'>🎟️ {unlock_tokens} Tokens</div>
<div style='font-size: 14px; opacity: 0.9; font-weight: 600;'>📚 {training_credits} Credits</div>
</div>
</div>
<div style='background: rgba(255,255,255,0.2); height: 24px; border-radius: 12px; overflow: hidden; box-shadow: inset 0 2px 8px rgba(0,0,0,0.2);'>
<div style='background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%); height: 100%; width: {progress_to_next_fmt}%; box-shadow: 0 0 12px rgba(251, 191, 36, 0.6); transition: width 0.3s ease;'></div>
</div>
<div style='font-size: 12px; opacity: 0.9; margin-top: 6px;'>
{next_tier_text}
</div>
</div>
<div style='margin-bottom: 20px;'>
<div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px; font-weight: 600;'>{energy_emoji} ENERGIA</div>
<div style='background: rgba(255,255,255,0.2); height: 32px; border-radius: 16px; overflow: hidden; box-shadow: inset 0 2px 8px rgba(0,0,0,0.2);'>
<div style='background: linear-gradient(90deg, #10b981 0%, #34d399 100%); height: 100%; width: {energy_pct}%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; box-shadow: 0 0 12px rgba(16, 185, 129, 0.6); transition: width 0.3s ease;'>{energy_pct}%</div>
</div>
</div>
<div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px;'>
<div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); border: 2px solid rgba(255,255,255,0.2);'>
<div style='font-size: 32px; font-weight: 700; margin-bottom: 4px;'>{status_summary.get("PROSPECT", 0)}</div>
<div style='font-size: 12px; opacity: 0.9; font-weight: 600;'>🔓 PROSPECT</div>
</div>
<div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); border: 2px solid rgba(255,255,255,0.2);'>
<div style='font-size: 32px; font-weight: 700; margin-bottom: 4px;'>{status_summary.get("ACTIVE", 0)}</div>
<div style='font-size: 12px; opacity: 0.9; font-weight: 600;'>✅ ACTIVE</div>
</div>
<div style='background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); border: 2px solid rgba(255,255,255,0.2);'>
<div style='font-size: 32px; font-weight: 700; margin-bottom: 4px;'>{status_summary.get("LOST", 0)}</div>
<div style='font-size: 12px; opacity: 0.9; font-weight: 600;'>❌ LOST</div>
</div>
<div style='background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); border: 2px solid rgba(255,255,255,0.2);'>
<div style='font-size: 28px; font-weight: 700; margin-bottom: 4px;'>{game_state.get('monthly_sales', 0):,}</div>
<div style='font-size: 12px; opacity: 0.9; font-weight: 600;'>💰 SPRZEDAŻ PLN</div>
</div>
</div>
<div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px;'>
<div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.2);'>
<div style='font-size: 20px; font-weight: 700; margin-bottom: 2px;'>{current_day}</div>
<div style='font-size: 11px; opacity: 0.9;'>📅 Dzień</div>
</div>
<div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.2);'>
<div style='font-size: 20px; font-weight: 700; margin-bottom: 2px;'>Tydzień {current_week}</div>
<div style='font-size: 11px; opacity: 0.9;'>📆 Okres</div>
</div>
<div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.2); border-left: 3px solid {tasks_color};'>
<div style='font-size: 20px; font-weight: 700; margin-bottom: 2px;'>{tasks_status}</div>
<div style='font-size: 11px; opacity: 0.9;'>📋 Zadania</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
        
        # Quick Actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⏭️ Zakończ dzień", use_container_width=True, type="primary"):
                st.session_state["advance_day"] = True
                st.rerun()
        with col2:
            if st.button("🗺️ Zaplanuj trasę", use_container_width=True):
                st.session_state["show_route_planner"] = True
                st.info("💡 Przejdź do zakładki **Sprzedaż** aby zaplanować trasę wizyt")
        with col3:
            if st.button("🎯 Zobacz cele", use_container_width=True):
                st.info("💡 Przewiń w dół do sekcji **Cele & Postęp** lub kliknij zakładkę **📊 Statystyki**")
        
        # =============================================================================
        # SUB-TABY dla szczegółów
        # =============================================================================
        
        dash_stats, dash_alerts, dash_tasks = st.tabs([
            "📊 Statystyki",
            "⚠️ Alerty & Akcje",
            "📋 Zadania & Onboarding"
        ])
        
        # ========================================================================
        # SUB-TAB: STATYSTYKI (Cele, Achievement, Historia)
        # ========================================================================
        
        with dash_stats:
            st.subheader("📈 Cele i Postępy")
            
            # ACHIEVEMENT TIER BADGE
            from utils.fmcg_progression import get_achievement_tier
            
            weekly_history_data = game_state.get("weekly_history", [])
            tier_data = get_achievement_tier(weekly_history_data)
            
            if tier_data["tier"] != "None":
                # Extract values
                tier_color = tier_data['tier_color']
                tier_color_grad = f"{tier_color}dd"
                tier_emoji = tier_data['tier_emoji']
                tier_name = tier_data['tier']
                requirements_text = ', '.join(tier_data['requirements_met'][:2])
                
                tier_badge_html = f"""<div style="background: linear-gradient(135deg, {tier_color} 0%, {tier_color_grad} 100%); color: white; padding: 12px 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
<div style="font-size: 32px; margin-bottom: 4px;">{tier_emoji}</div>
<div style="font-weight: 700; font-size: 20px;">{tier_name} Performer</div>
<div style="font-size: 12px; opacity: 0.9; margin-top: 4px;">
{requirements_text}
</div>
</div>"""
                st.markdown(tier_badge_html, unsafe_allow_html=True)
            
            # WEEKLY TARGET PROGRESS
            st.markdown("### 🎯 Cele Tygodniowe")
            
            weekly_target = game_state.get("weekly_target_sales", 8000)
            weekly_actual = game_state.get("weekly_actual_sales", 0)
            weekly_visits_target = game_state.get("weekly_target_visits", 6)
            weekly_visits_actual = game_state.get("visits_this_week", 0)
            weekly_streak = game_state.get("weekly_streak", 0)
            
            # Calculate progress percentage
            sales_progress = min(100, (weekly_actual / weekly_target * 100)) if weekly_target > 0 else 0
            visits_progress = min(100, (weekly_visits_actual / weekly_visits_target * 100)) if weekly_visits_target > 0 else 0
        
            # Determine status color
            if sales_progress >= 100:
                status_color = "#22c55e"  # Green - achieved
                status_emoji = "✅"
                status_text = "CEL OSIĄGNIĘTY!"
            elif sales_progress >= 75:
                status_color = "#eab308"  # Yellow - on track
                status_emoji = "🔥"
                status_text = "Blisko celu!"
            elif sales_progress >= 50:
                status_color = "#f97316"  # Orange - needs effort
                status_emoji = "⚠️"
                status_text = "Potrzebujesz przyspieszenia"
            else:
                status_color = "#ef4444"  # Red - at risk
                status_emoji = "🚨"
                status_text = "Zagrożony cel!"
        
            # EXTRACT all formatted values BEFORE f-string
            current_week = game_state.get('current_week', 1)
            weekly_actual_fmt = f"{weekly_actual:,}"
            weekly_target_fmt = f"{weekly_target:,}"
            sales_progress_pct = f"{sales_progress:.0f}"
            visits_progress_pct = f"{visits_progress:.0f}"
            status_color_grad1 = f"{status_color}15"
            status_color_grad2 = f"{status_color}05"
            status_color_grad3 = f"{status_color}dd"
        
            # Build progress card HTML
            progress_html = f"""<div style="border: 2px solid {status_color}; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, {status_color_grad1} 0%, {status_color_grad2} 100%); margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
    <h3 style="margin: 0; color: #1f2937;">{status_emoji} Tydzień {current_week}</h3>
    <div style="background: {status_color}; color: white; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 14px;">
    {status_text}
    </div>
    </div>
    <div style="margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
    <span style="font-weight: 600; color: #374151;">💰 Sprzedaż</span>
    <span style="font-weight: 600; color: {status_color};">{weekly_actual_fmt} / {weekly_target_fmt} PLN ({sales_progress_pct}%)</span>
    </div>
    <div style="background: #e5e7eb; height: 24px; border-radius: 12px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
    <div style="width: {sales_progress}%; height: 100%; background: linear-gradient(90deg, {status_color} 0%, {status_color_grad3} 100%); transition: width 0.5s ease; border-radius: 12px;"></div>
    </div>
    </div>
    <div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
    <span style="font-weight: 600; color: #374151;">📞 Wizyty</span>
    <span style="font-weight: 600; color: #6b7280;">{weekly_visits_actual} / {weekly_visits_target} ({visits_progress_pct}%)</span>
    </div>
    <div style="background: #e5e7eb; height: 18px; border-radius: 9px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
    <div style="width: {visits_progress}%; height: 100%; background: linear-gradient(90deg, #6b7280 0%, #9ca3af 100%); transition: width 0.5s ease; border-radius: 9px;"></div>
    </div>
    </div>
    </div>"""
        
            if weekly_streak > 0:
                # Determine streak text
                if weekly_streak == 1:
                    streak_text = "tydzień"
                elif weekly_streak < 5:
                    streak_text = "tygodnie"
                else:
                    streak_text = "tygodni"
            
                streak_html = f"""<div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: 600; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);">
    🔥 Seria: {weekly_streak} {streak_text} z rzędu!
    </div>"""
                st.markdown(streak_html, unsafe_allow_html=True)
        
            st.markdown(progress_html, unsafe_allow_html=True)
        
            # MONTHLY TARGET PROGRESS (Compact)
            monthly_target = game_state.get("monthly_target_sales", 35000)
            monthly_actual = game_state.get("monthly_actual_sales", 0)
            monthly_progress = min(100, (monthly_actual / monthly_target * 100)) if monthly_target > 0 else 0
        
            monthly_color = "#3b82f6" if monthly_progress >= 75 else "#6b7280"
        
            # Extract values
            monthly_actual_fmt = f"{monthly_actual:,}"
            monthly_target_fmt = f"{monthly_target:,}"
            monthly_progress_pct = f"{monthly_progress:.0f}"
            monthly_color_grad1 = f"{monthly_color}10"
            monthly_color_grad2 = f"{monthly_color}05"
            monthly_color_grad3 = f"{monthly_color}dd"
        
            monthly_html = f"""<div style="border: 1px solid {monthly_color}; border-radius: 8px; padding: 16px; background: linear-gradient(135deg, {monthly_color_grad1} 0%, {monthly_color_grad2} 100%); margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
    <span style="font-weight: 600; color: #374151;">📊 Cel Miesięczny</span>
    <span style="font-weight: 700; color: {monthly_color};">{monthly_actual_fmt} / {monthly_target_fmt} PLN ({monthly_progress_pct}%)</span>
    </div>
    <div style="background: #e5e7eb; height: 16px; border-radius: 8px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
    <div style="width: {monthly_progress}%; height: 100%; background: linear-gradient(90deg, {monthly_color} 0%, {monthly_color_grad3} 100%); transition: width 0.5s ease; border-radius: 8px;"></div>
    </div>
    </div>"""
            st.markdown(monthly_html, unsafe_allow_html=True)
            
            # =============================================================================
            # REPUTATION BREAKDOWN (NEW)
            # =============================================================================
            st.markdown("### 💎 Reputation Breakdown")
            
            from utils.reputation_system import (
                calculate_average_client_reputation,
                calculate_company_reputation
            )
            
            # Calculate components
            client_rep = calculate_average_client_reputation(game_state)
            company_rep = calculate_company_reputation(game_state)
            
            # Get company components
            task_perf = game_state.get("reputation", {}).get("company", {}).get("task_performance", 100)
            sales_perf = game_state.get("reputation", {}).get("company", {}).get("sales_performance", 0)
            prof = game_state.get("reputation", {}).get("company", {}).get("professionalism", 100)
            
            # Display breakdown
            col_rep1, col_rep2 = st.columns(2)
            
            with col_rep1:
                client_color = "#10b981" if client_rep >= 75 else "#f59e0b" if client_rep >= 50 else "#ef4444"
                st.markdown(f"""
                <div style='background: {client_color}15; border: 2px solid {client_color}; border-radius: 12px; padding: 20px;'>
                    <div style='font-size: 14px; font-weight: 600; color: #64748b; margin-bottom: 8px;'>👥 CLIENT REPUTATION (60% weight)</div>
                    <div style='font-size: 42px; font-weight: 700; color: {client_color}; margin-bottom: 12px;'>{client_rep:.1f}/100</div>
                    <div style='background: #e5e7eb; height: 12px; border-radius: 6px; overflow: hidden; margin-bottom: 16px;'>
                        <div style='width: {client_rep}%; height: 100%; background: {client_color};'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Top clients
                st.markdown("**🔝 Top Clients:**")
                clients_with_rep = []
                for client_id, client_data in clients.items():
                    if client_data.get("status") in ["ACTIVE", "PARTNER"]:
                        from utils.reputation_system import calculate_client_reputation
                        rep = calculate_client_reputation(client_data, game_state)
                        clients_with_rep.append((client_data.get("name", client_id), rep))
                
                clients_with_rep.sort(key=lambda x: x[1], reverse=True)
                for i, (name, rep) in enumerate(clients_with_rep[:3], 1):
                    emoji = "🟢" if rep >= 75 else "🟡" if rep >= 50 else "🔴"
                    st.markdown(f"{emoji} **{name}**: {rep:.0f}/100")
                
                if not clients_with_rep:
                    st.info("📊 Brak aktywnych klientów z reputacją")
            
            with col_rep2:
                company_color = "#3b82f6" if company_rep >= 75 else "#f59e0b" if company_rep >= 50 else "#ef4444"
                st.markdown(f"""
                <div style='background: {company_color}15; border: 2px solid {company_color}; border-radius: 12px; padding: 20px;'>
                    <div style='font-size: 14px; font-weight: 600; color: #64748b; margin-bottom: 8px;'>🏢 COMPANY REPUTATION (40% weight)</div>
                    <div style='font-size: 42px; font-weight: 700; color: {company_color}; margin-bottom: 12px;'>{company_rep:.1f}/100</div>
                    <div style='background: #e5e7eb; height: 12px; border-radius: 6px; overflow: hidden; margin-bottom: 16px;'>
                        <div style='width: {company_rep}%; height: 100%; background: {company_color};'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Components
                st.markdown("**📊 Components:**")
                st.markdown(f"📋 **Task Performance (30%)**: {task_perf:.0f}%")
                st.markdown(f"💰 **Sales Performance (40%)**: {sales_perf:.0f}%")
                st.markdown(f"💼 **Professionalism (30%)**: {prof:.0f}%")
            
            st.markdown("---")
            
            # SCENARIO-SPECIFIC GOALS
            st.markdown("### 🎯 Cele Scenariusza")
            
            if is_heinz_scenario:
                # HEINZ SCENARIO GOALS - Updated to 3 objectives
                st.markdown("**📋 Scenariusz Heinz Food Service**")
                
                # Goal 1: Numeric Distribution (15/25)
                active_clients = sum(1 for c in clients.values() if c.get("status") == "ACTIVE")
                distribution_target = 15
                
                # Goal 2: Monthly Sales (15,000 PLN)
                monthly_sales = game_state.get("total_revenue", 0)
                sales_target = 15000
                
                # Goal 3: Beat Kotlin (6 wins)
                kotlin_wins = sum(1 for c in clients.values() 
                                 if c.get("previous_supplier", "").lower() == "kotlin" 
                                 and c.get("status") == "ACTIVE")
                kotlin_target = 6
                
                col_g1, col_g2, col_g3 = st.columns(3)
                
                with col_g1:
                    dist_color = "#10b981" if active_clients >= distribution_target else "#f59e0b" if active_clients >= 10 else "#ef4444"
                    st.markdown(f"""
                    <div style='background: {dist_color}15; border: 2px solid {dist_color}; border-radius: 8px; padding: 16px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: {dist_color}; margin-bottom: 4px;'>{active_clients}/{distribution_target}</div>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Dystrybucja numeryczna</div>
                        <div style='font-size: 11px; color: #94a3b8;'>Cel: 60% (15/25)</div>
                        <div style='background: #e5e7eb; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;'>
                            <div style='width: {min(100, active_clients/distribution_target*100)}%; height: 100%; background: {dist_color};'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📖 Jak osiągnąć?"):
                        st.markdown("""
                        **💰 Nagroda:** 3,000 PLN | **Priorytet:** 🔴 CRITICAL
                        
                        **Co to znaczy:**  
                        Zdobądź co najmniej **15 aktywnych punktów sprzedaży** z 25 dostępnych w regionie Dzięgielów (60% dystrybucji).
                        
                        **Strategia:**
                        - ✅ Podpisz umowy z różnymi lokalami Food Service
                        - ✅ Nieważne czy kupują Heinz, Pudliszki, czy obie marki
                        - 🎯 Zacznij od Easy Wins (klienci znający markę)
                        - 🥊 Przejmuj klientów od Kotlin
                        - 📊 Portfolio play: Pudliszki dla budżetowych, Heinz dla premium
                        """)
                
                with col_g2:
                    sales_color = "#10b981" if monthly_sales >= sales_target else "#f59e0b" if monthly_sales >= 10000 else "#ef4444"
                    st.markdown(f"""
                    <div style='background: {sales_color}15; border: 2px solid {sales_color}; border-radius: 8px; padding: 16px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: {sales_color}; margin-bottom: 4px;'>{monthly_sales:,}</div>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Sprzedaż miesięczna</div>
                        <div style='font-size: 11px; color: #94a3b8;'>Cel: {sales_target:,} PLN</div>
                        <div style='background: #e5e7eb; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;'>
                            <div style='width: {min(100, monthly_sales/sales_target*100)}%; height: 100%; background: {sales_color};'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📖 Jak osiągnąć?"):
                        st.markdown("""
                        **💰 Nagroda:** 2,500 PLN | **Priorytet:** 🟠 HIGH
                        
                        **Co to znaczy:**  
                        Osiągnij łączną sprzedaż **15,000 PLN** w skali miesiąca (Heinz + Pudliszki).
                        
                        **Strategia:**
                        - 📦 Sprzedawaj regularnie do aktywnych klientów
                        - 📈 Zwiększaj wielkość zamówień (volume play)
                        - ⭐ Mix: Heinz (wyższa marża) + Pudliszki (wyższy wolumen)
                        - 🎯 Priorytetyzuj klientów z wysokim potencjałem (kg/mies)
                        
                        **Przykładowa ścieżka:**
                        - 10 klientów × 1,500 PLN = 15,000 PLN
                        - LUB: 6 premium (2k) + 8 value (750) = 18,000 PLN
                        """)
                
                with col_g3:
                    kotlin_color = "#10b981" if kotlin_wins >= kotlin_target else "#f59e0b" if kotlin_wins >= 4 else "#ef4444"
                    st.markdown(f"""
                    <div style='background: {kotlin_color}15; border: 2px solid {kotlin_color}; border-radius: 8px; padding: 16px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: {kotlin_color}; margin-bottom: 4px;'>{kotlin_wins}/{kotlin_target}</div>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Przejęcia z Kotlin</div>
                        <div style='font-size: 11px; color: #94a3b8;'>Beat competition</div>
                        <div style='background: #e5e7eb; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;'>
                            <div style='width: {min(100, kotlin_wins/kotlin_target*100)}%; height: 100%; background: {kotlin_color};'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📖 Jak osiągnąć?"):
                        st.markdown("""
                        **💰 Nagroda:** 1,500 PLN | **Priorytet:** 🟡 MEDIUM
                        
                        **Co to znaczy:**  
                        Przejmij **6 z 8 klientów** używających obecnie ketchupów Kotlin.
                        
                        **Strategia:**
                        - 🔍 Klienci Kotlin oznaczeni w bazie
                        - 💬 Techniki: FOZ, Kompensacja, Perspektywizacja
                        - 🎯 Argument: jakość Heinz / polska marka Pudliszki
                        - ✅ Pudliszki też się liczy jako win!
                        
                        **Easy Wins:**
                        - Kebab Express (problemy z dostawami)
                        - Pizza House (niespójna jakość)
                        - Burger Craft (chce uprościć dostawców)
                        """)
                
                st.markdown("---")
            
            else:
                # STANDARD SCENARIO GOALS (Quick Start, Lifetime)
                st.markdown("**🚀 Podstawowe Cele**")
                
                # Goal 1: Client acquisition
                total_clients = len(clients)
                active_clients = sum(1 for c in clients.values() if c.get("status") == "ACTIVE")
                client_target = 10  # Target: 10 active clients
                
                # Goal 2: Product diversity
                products_sold = len(set(game_state.get("products_sold_history", [])))
                products_target = 15  # Target: 15 different products
                
                # Goal 3: Customer satisfaction (avg reputation)
                total_rep = sum(c.get("reputation", 0) for c in clients.values() if c.get("status") == "ACTIVE")
                avg_reputation = (total_rep / active_clients) if active_clients > 0 else 0
                reputation_target = 50  # Target: +50 avg reputation
                
                col_g1, col_g2, col_g3 = st.columns(3)
                
                with col_g1:
                    clients_color = "#10b981" if active_clients >= client_target else "#f59e0b" if active_clients >= 6 else "#ef4444"
                    st.markdown(f"""
                    <div style='background: {clients_color}15; border: 2px solid {clients_color}; border-radius: 8px; padding: 16px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: {clients_color}; margin-bottom: 4px;'>{active_clients}/{client_target}</div>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Aktywni klienci</div>
                        <div style='font-size: 11px; color: #94a3b8;'>Portfolio</div>
                        <div style='background: #e5e7eb; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;'>
                            <div style='width: {min(100, active_clients/client_target*100)}%; height: 100%; background: {clients_color};'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📖 Jak osiągnąć?"):
                        st.markdown("""
                        **Cel:** Zdobądź co najmniej 10 aktywnych klientów w swoim portfolio.
                        
                        **Strategia:**
                        - 👥 Odwiedzaj prospectów i przekonuj ich do współpracy
                        - 💬 Używaj różnych technik sprzedażowych (FOZ, Kompensacja, etc.)
                        - 🤝 Dbaj o relacje z klientami (reputation)
                        - 📈 Regularnie odwiedzaj i obsługuj klientów
                        """)
                
                with col_g2:
                    products_color = "#10b981" if products_sold >= products_target else "#f59e0b" if products_sold >= 10 else "#ef4444"
                    st.markdown(f"""
                    <div style='background: {products_color}15; border: 2px solid {products_color}; border-radius: 8px; padding: 16px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: {products_color}; margin-bottom: 4px;'>{products_sold}/{products_target}</div>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Różne produkty</div>
                        <div style='font-size: 11px; color: #94a3b8;'>Dywersyfikacja</div>
                        <div style='background: #e5e7eb; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;'>
                            <div style='width: {min(100, products_sold/products_target*100)}%; height: 100%; background: {products_color};'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📖 Jak osiągnąć?"):
                        st.markdown("""
                        **Cel:** Sprzedaj co najmniej 15 różnych produktów ze swojego portfolio.
                        
                        **Strategia:**
                        - 🎯 Oferuj różnorodne produkty różnym klientom
                        - 🏪 Dostosuj ofertę do potrzeb segmentu
                        - 📦 Cross-selling: klient kupuje A → zaproponuj B
                        - ⬆️ Upselling: upgrade do produktów premium
                        """)
                
                with col_g3:
                    rep_color = "#10b981" if avg_reputation >= reputation_target else "#f59e0b" if avg_reputation >= 25 else "#ef4444"
                    st.markdown(f"""
                    <div style='background: {rep_color}15; border: 2px solid {rep_color}; border-radius: 8px; padding: 16px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: {rep_color}; margin-bottom: 4px;'>{avg_reputation:+.0f}</div>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Średnia reputacja</div>
                        <div style='font-size: 11px; color: #94a3b8;'>Cel: +{reputation_target}</div>
                        <div style='background: #e5e7eb; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;'>
                            <div style='width: {min(100, max(0, (avg_reputation+100)/200*100))}%; height: 100%; background: {rep_color};'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📖 Jak osiągnąć?"):
                        st.markdown("""
                        **Cel:** Utrzymuj średnią reputację na poziomie +50 punktów wśród aktywnych klientów.
                        
                        **Strategia:**
                        - ✅ Regularnie odwiedzaj klientów (nie zapomnij o nich!)
                        - 🤝 Dotrzymuj obietnic i terminów
                        - ⚡ Rozwiązuj problemy szybko i skutecznie
                        - 🎁 Oferuj wartość dodaną (porady, wsparcie)
                        """)
                
                st.markdown("---")
            
            # WEEKLY HISTORY - Last 4 weeks
            st.markdown("### 📅 Historia Tygodniowa")
            
            weekly_history = game_state.get("weekly_history", [])
            if weekly_history:
                # Show last 4 weeks
                recent_weeks = weekly_history[-4:]
                cols = st.columns(len(recent_weeks))
                
                for idx, week_data in enumerate(recent_weeks):
                    with cols[idx]:
                        week_num = week_data.get("week", idx + 1)
                        sales = week_data.get("sales", 0)
                        target = week_data.get("target", 8000)
                        achieved = sales >= target
                        
                        color = "#22c55e" if achieved else "#94a3b8"
                        emoji = "✅" if achieved else "📊"
                        
                        week_card = f"""
                        <div style='background: {color}15; border: 2px solid {color}; border-radius: 8px; padding: 12px; text-align: center;'>
                            <div style='font-size: 20px; margin-bottom: 4px;'>{emoji}</div>
                            <div style='font-weight: 700; color: {color}; margin-bottom: 4px;'>Tydz. {week_num}</div>
                            <div style='font-size: 14px; color: #64748b;'>{sales:,} PLN</div>
                            <div style='font-size: 11px; color: #94a3b8;'>Cel: {target:,}</div>
                        </div>
                        """
                        st.markdown(week_card, unsafe_allow_html=True)
            else:
                st.info("📊 Rozpocznij grę aby zobaczyć historię wyników")
        
        # ========================================================================
        # SUB-TAB: ALERTY & AKCJE (Reputacja, Status Klientów)
        # ========================================================================
        
        with dash_alerts:
            st.subheader("⚠️ Alerty Reputacji")
        
            # Analyze clients by reputation
            at_risk_clients = []  # -49 to 0
            critical_clients = []  # -100 to -50 (LOST)
            overdue_clients = []  # ACTIVE with overdue visits
        
            for client_id, client_data in clients.items():
                if client_data.get("status", "PROSPECT").upper() == "ACTIVE":
                    reputation = client_data.get("reputation", 0)
                
                    # Check reputation thresholds
                    if reputation <= -50:
                        critical_clients.append({
                            "id": client_id,
                            "name": client_data.get("name", client_id),
                            "reputation": reputation
                        })
                    elif reputation < 0:
                        at_risk_clients.append({
                            "id": client_id,
                            "name": client_data.get("name", client_id),
                            "reputation": reputation
                        })
                
                    # Check overdue visits
                    if is_visit_overdue(client_data):
                        next_visit = client_data.get("next_visit_due", "")
                        if next_visit:
                            days_overdue = (datetime.now() - datetime.fromisoformat(next_visit)).days
                            overdue_clients.append({
                                "id": client_id,
                                "name": client_data.get("name", client_id),
                                "days_overdue": days_overdue,
                                "reputation": reputation
                            })
        
            # Display alerts
            alerts_shown = False
        
            if critical_clients:
                alerts_shown = True
                st.error(f"""
                🚨 **KRYTYCZNE: {len(critical_clients)} klient(ów) na granicy LOST!**
            
                Reputacja ≤ -50 - natychmiastowa wizyta wymagana!
                """)
            
                for client in critical_clients[:3]:  # Show max 3
                    st.markdown(f"- **{client['name']}**: Reputacja {client['reputation']} 💀")
        
            if at_risk_clients:
                alerts_shown = True
                st.warning(f"""
                ⚠️ **UWAGA: {len(at_risk_clients)} klient(ów) zagrożonych!**
            
                Reputacja poniżej 0 - ryzyko utraty klienta
                """)
            
                for client in at_risk_clients[:3]:  # Show max 3
                    st.markdown(f"- **{client['name']}**: Reputacja {client['reputation']} ⚠️")
        
            if overdue_clients:
                alerts_shown = True
                # Sort by days overdue (most critical first)
                overdue_clients.sort(key=lambda x: x['days_overdue'], reverse=True)
            
                st.info(f"""
                📅 **{len(overdue_clients)} klient(ów) z przeterminowaną wizytą**
            
                Zaplanuj wizyty aby utrzymać reputację!
                """)
            
                for client in overdue_clients[:3]:  # Show max 3
                    rep_status = get_reputation_status(client['reputation'])
                    st.markdown(f"- **{client['name']}**: {client['days_overdue']} dni opóźnienia | {rep_status['emoji']} Reputacja {client['reputation']}")
        
            if not alerts_shown:
                st.success("""
                ✅ **Wszystko w porządku!**
            
                Brak klientów zagrożonych - dobra robota! 🎉
                """)
            
            # CLIENT STATUS BREAKDOWN
            st.markdown("---")
            st.markdown("### 📊 Status Klientów")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                prospect_count = status_summary.get("PROSPECT", 0)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 16px; border-radius: 12px; text-align: center;'>
                    <div style='font-size: 36px; font-weight: 700; margin-bottom: 4px;'>{prospect_count}</div>
                    <div style='font-size: 14px; opacity: 0.9;'>🔓 PROSPECT</div>
                    <div style='font-size: 11px; opacity: 0.7; margin-top: 4px;'>Potencjalni klienci</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                active_count = status_summary.get("ACTIVE", 0)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 16px; border-radius: 12px; text-align: center;'>
                    <div style='font-size: 36px; font-weight: 700; margin-bottom: 4px;'>{active_count}</div>
                    <div style='font-size: 14px; opacity: 0.9;'>✅ ACTIVE</div>
                    <div style='font-size: 11px; opacity: 0.7; margin-top: 4px;'>Aktywni klienci</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                lost_count = status_summary.get("LOST", 0)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 16px; border-radius: 12px; text-align: center;'>
                    <div style='font-size: 36px; font-weight: 700; margin-bottom: 4px;'>{lost_count}</div>
                    <div style='font-size: 14px; opacity: 0.9;'>❌ LOST</div>
                    <div style='font-size: 11px; opacity: 0.7; margin-top: 4px;'>Utraceni klienci</div>
                </div>
                """, unsafe_allow_html=True)
        
        with dash_tasks:
            # =============================================================================
            # ZADANIA TYGODNIOWE (PHASE 1 - Weekly Tasks)
            # =============================================================================
            
            current_week = game_state.get("current_week", 1)
            
            # Initialize weekly tasks if not exists or if new week
            if "weekly_tasks" not in st.session_state:
                st.session_state.weekly_tasks = []
            
            if "last_task_week" not in st.session_state:
                st.session_state.last_task_week = 0
            
            # Assign new tasks if new week started
            if current_week > st.session_state.last_task_week and current_week > 1:
                # Get tasks for this week
                week_tasks = get_weekly_tasks(scenario_id, current_week, game_state)
                
                if week_tasks:
                    # Create task instances with dates
                    for template in week_tasks:
                        task_instance = create_task_from_template(template, datetime.now())
                        st.session_state.weekly_tasks.append(task_instance)
                    
                    st.session_state.last_task_week = current_week
                    st.success(f"📋 **Nowe zadania tygodniowe!** Otrzymałeś {len(week_tasks)} nowych zadań.")
            
            # Auto-check task completion
            completed_tasks_this_check = []
            for task in st.session_state.weekly_tasks:
                if task["status"] == "active":
                    just_completed = check_task_completion(task, game_state, clients)
                    if just_completed:
                        completed_tasks_this_check.append(task)
            
            # Payout rewards for just-completed tasks
            for task in completed_tasks_this_check:
                reward_summary = payout_task_reward(task, game_state, clients)
                
                # Task completion popup with multi-currency rewards
                st.balloons()
                st.success(f"🎉 **ZADANIE UKOŃCZONE!** {task['title']}")
                
                # Build reward display
                reward_parts = []
                
                if reward_summary.get("xp"):
                    reward_parts.append(f"🔹 **+{reward_summary['xp']} XP**")
                
                if reward_summary.get("unlock_tokens"):
                    reward_parts.append(f"� **+{reward_summary['unlock_tokens']} Unlock Tokens** 🎟️")
                
                if reward_summary.get("client_reputation_boost"):
                    clients_affected = reward_summary.get("clients_affected", 0)
                    reward_parts.append(
                        f"🔹 **+{reward_summary['client_reputation_boost']} Client Reputation** "
                        f"({clients_affected} klientów)"
                    )
                
                if reward_summary.get("company_reputation_boost"):
                    reward_parts.append(
                        f"🔹 **+{reward_summary['company_reputation_boost']} Company Reputation** "
                        f"(Task Performance)"
                    )
                
                if reward_summary.get("training_credits"):
                    reward_parts.append(f"🔹 **+{reward_summary['training_credits']} Training Credits** 📚")
                
                # Show rewards
                if reward_parts:
                    st.markdown("**NAGRODY:**")
                    for part in reward_parts:
                        st.markdown(part)
                
                # Show tier progression
                if reward_summary.get("tier_up"):
                    st.success(f"⭐ **AWANS!** Nowy tier: **{reward_summary['tier_up']}**")
                elif reward_summary.get("rating_change", 0) > 0:
                    new_rating = game_state.get("reputation", {}).get("overall_rating", 0)
                    st.info(f"⭐ **Overall Rating:** {new_rating:.1f}/100 (+{reward_summary['rating_change']:.1f})")
                
                # Story completion message
                if task.get("story", {}).get("completion"):
                    st.markdown(f"💬 {task['story']['completion']}")
            
            # Display weekly tasks
            active_tasks = [t for t in st.session_state.weekly_tasks if t["status"] == "active"]
            completed_tasks = [t for t in st.session_state.weekly_tasks if t["status"] == "completed"]
            
            if current_week > 1 and (active_tasks or completed_tasks):
                st.markdown("### 📅 Zadania Tygodniowe")
                
                # Show active tasks
                if active_tasks:
                    for task in active_tasks:
                        priority = task.get("priority", "MEDIUM")
                        priority_colors = {
                            "CRITICAL": {"bg": "#fef2f2", "border": "#ef4444", "icon": "🔴"},
                            "HIGH": {"bg": "#fef3c7", "border": "#f59e0b", "icon": "🟡"},
                            "MEDIUM": {"bg": "#eff6ff", "border": "#3b82f6", "icon": "🔵"},
                            "LOW": {"bg": "#f0fdf4", "border": "#10b981", "icon": "🟢"}
                        }
                        
                        color = priority_colors.get(priority, priority_colors["MEDIUM"])
                        progress_pct = task["progress"]["percentage"]
                        
                        with st.expander(f"{color['icon']} **{task['title']}** ({progress_pct}%)", expanded=(priority in ["CRITICAL", "HIGH"])):
                            st.markdown(f"**{task['description']}**")
                            st.caption(f"👤 Zlecił: {task['assigned_by']} | ⏰ Deadline: {task['deadline']}")
                            
                            # Progress bar
                            current = task["progress"]["current"]
                            target = task["progress"]["target"]
                            
                            st.progress(progress_pct / 100)
                            st.caption(f"Postęp: {current}/{target}")
                            
                            # Reward preview
                            reward = task.get("reward", {})
                            reward_items = []
                            if reward.get("cash"):
                                reward_items.append(f"💰 {reward['cash']} PLN")
                            if reward.get("xp"):
                                reward_items.append(f"⭐ {reward['xp']} XP")
                            if reward.get("reputation"):
                                reward_items.append(f"❤️ +{reward['reputation']} rep")
                            
                            if reward_items:
                                st.success("🎁 Nagroda: " + " | ".join(reward_items))
                            
                            # Story intro
                            if task.get("story", {}).get("intro"):
                                with st.expander("📖 Historia zadania", expanded=False):
                                    st.markdown(task["story"]["intro"])
                
                # Show completed tasks (collapsed)
                if completed_tasks:
                    with st.expander(f"✅ Ukończone zadania ({len(completed_tasks)})", expanded=False):
                        for task in completed_tasks:
                            st.markdown(f"✅ **{task['title']}** - ukończono {task['completed_date']}")
                
                st.markdown("---")
            
            # =============================================================================
            # ZADANIA (ONBOARDING) - jako sekcja w Dashboard
            # =============================================================================
            
            with st.expander(f"📋 Zadania onboardingowe {tasks_badge}", expanded=(pending_tasks > 0)):
                # Trial period info
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                current_day = game_state.get("current_day", "Monday")
                current_week = game_state.get("current_week", 1)
                day_index = day_names.index(current_day) if current_day in day_names else 0
                is_trial = (current_week == 1 and day_index < 2)
            
                if is_trial:
                    st.info(f"""
                    🎓 **Witaj w okresie próbnym!** (Tydzień 1, Dzień {day_index + 1}/2)
                
                    Przez pierwsze 2 dni możesz swobodnie eksplorować grę bez ograniczeń energii.
                    Użyj tego czasu na zapoznanie się z interfejsem i ukończenie zadań onboardingowych.
                    """)
                else:
                    st.warning("""
                    ⚠️ **Okres próbny zakończony!**
                
                    Od dziś wizyty u klientów kosztują energię. Aby wykonywać wizyty, musisz najpierw ukończyć wszystkie zadania onboardingowe.
                    """)
            
                st.markdown("### 📝 Lista zadań")
            
                # Task completion tracking
                pending = get_pending_tasks_count(st.session_state)
            
                for task_id, task in ONBOARDING_TASKS.items():
                    task_status = get_task_status(st.session_state, task_id)
                    
                    # Skip completed tasks - they're shown in Historia realizacji zadań
                    if task_status["status"] == "completed":
                        continue
                
                    # Determine icon and color based on status
                    if task_status["status"] == "submitted":
                        status_icon = "⏳"
                        status_color = "#f59e0b"
                        button_text = "Sprawdź wynik"
                        button_disabled = False
                    else:
                        status_icon = "📝"
                        status_color = "#6b7280"
                        button_text = "Rozpocznij"
                        button_disabled = False
                
                    # Create expandable for each task
                    with st.expander(f"{status_icon} **{task['title']}**", expanded=(task_status["status"] != "completed" and pending <= 2)):
                        st.markdown(f"**Opis:** {task['description']}")
                        st.caption(f"⏱️ Deadline: {task.get('deadline', 'Brak')}")
                        st.caption(f"🎯 Wymagane do: {task.get('required_for', 'Ogólny postęp')}")
                    
                        # Show task-specific content based on type
                        if task_id == "task_company":
                            st.markdown("""
                            **Informacje do przeczytania:**
                            - 🏢 Firma: FreshLife
                            - 📦 Główne produkty: świeże owoce, warzywa, produkty ekologiczne
                            - 🎯 Misja: Dostawa świeżości prosto do biznesów
                            - 💡 USP: Dostawa w 24h, 100% świeżości gwarantowane
                            """)
                    
                        elif task_id == "task_territory":
                            # Show mini-map preview
                            territory_lat = game_state.get("territory_latitude", 52.0846)
                            territory_lon = game_state.get("territory_longitude", 21.0250)
                        
                            # Note: folium already imported at top of file
                        
                            mini_map = folium.Map(
                                location=[territory_lat, territory_lon],
                                zoom_start=12,
                                tiles="OpenStreetMap",
                                width=600,
                                height=300
                            )
                        
                            # Add base marker
                            folium.Marker(
                                [territory_lat, territory_lon],
                                popup="Twoja baza",
                                icon=folium.Icon(color="red", icon="home")
                            ).add_to(mini_map)
                        
                            # Add client markers (sample)
                            client_count = len([c for c in clients.values() if c.get("status") == "PROSPECT"])
                            folium.CircleMarker(
                                [territory_lat + 0.01, territory_lon + 0.01],
                                radius=5,
                                popup=f"{client_count} klientów w okolicy",
                                color="blue",
                                fill=True
                            ).add_to(mini_map)
                        
                            folium_static(mini_map)
                        
                            st.markdown(f"""
                            **Twoje terytorium:**
                            - 📍 Baza: {game_state.get('territory_name', 'Piaseczno')}
                            - 👥 Klienci: {len(clients)} punktów
                            - 🎯 Status: {status_summary.get("PROSPECT", 0)} prospektów, {status_summary.get("ACTIVE", 0)} aktywnych
                            """)
                    
                        elif task_id == "task_product":
                            st.markdown("""
                            **Przykładowe produkty FreshLife:**
                            - 🥗 Mixy sałat premium
                            - 🍎 Owoce sezonowe
                            - 🥕 Warzywa organiczne
                            - 🌿 Zioła świeże
                        
                            Pełny katalog znajdziesz w zakładce 'Produkty'
                            """)
                    
                        # Submission area
                        st.markdown("---")
                    
                        if task_status["status"] == "completed":
                            st.success(f"✅ **Zadanie ukończone!**")
                            st.info("� Zobacz szczegóły w 'Historia realizacji zadań' poniżej")
                    
                        elif task_status["status"] == "submitted":
                            # Show submission and allow re-edit
                            submission_text = task_status.get("submission", "")
                            
                            st.warning("⏳ **Zadanie złożone** - AI nie zaakceptowało jeszcze tej odpowiedzi")
                            
                            # Show previous submission
                            with st.expander("� Twoja poprzednia odpowiedź", expanded=False):
                                st.markdown(submission_text)
                            
                            # Re-evaluation button
                            col_check, col_resubmit = st.columns([1, 1])
                        
                            with col_check:
                                if st.button("🔍 Sprawdź ponownie AI", key=f"check_{task_id}", use_container_width=True):
                                    # AI evaluation
                                    with st.spinner("🤖 AI ocenia Twoje rozwiązanie..."):
                                        feedback, is_accepted = evaluate_task_with_ai(task_id, submission_text, task)
                                    
                                    if is_accepted:
                                        complete_task(st.session_state, task_id, feedback=feedback)
                                        
                                        # Update Company Reputation
                                        from utils.reputation_system import (
                                            calculate_company_reputation,
                                            calculate_overall_rating,
                                            get_tier
                                        )
                                        
                                        if "reputation" not in game_state:
                                            game_state["reputation"] = {
                                                "company": {"task_performance": 0},
                                                "overall_rating": 0,
                                                "tier": "Trainee"
                                            }
                                        
                                        if "task_performance" not in game_state["reputation"]["company"]:
                                            game_state["reputation"]["company"]["task_performance"] = 0
                                        
                                        game_state["reputation"]["company"]["task_performance"] = min(
                                            game_state["reputation"]["company"]["task_performance"] + 5,
                                            15
                                        )
                                        
                                        company_rep = calculate_company_reputation(game_state)
                                        game_state["reputation"]["company_reputation"] = company_rep
                                        
                                        overall = calculate_overall_rating(game_state, clients)
                                        game_state["reputation"]["overall_rating"] = overall
                                        
                                        tier = get_tier(overall)
                                        game_state["reputation"]["tier"] = tier
                                        
                                        # Persist updated reputation to database
                                        try:
                                            update_fmcg_game_state_sql(username, game_state, clients)
                                        except Exception as e:
                                            st.warning(f"⚠️ Nie udało się zapisać postępu: {e}")
                                        
                                        st.success("🎉 **Zadanie zaakceptowane!**")
                                        st.balloons()
                                        st.rerun()
                                    else:
                                        st.warning("⚠️ **Wymaga poprawek**")
                                        st.markdown(f"**Feedback:** {feedback}")
                                        st.info("Kliknij '🔄 Edytuj odpowiedź' aby poprawić")
                        
                            with col_resubmit:
                                if st.button("🔄 Edytuj odpowiedź", key=f"resub_{task_id}", use_container_width=True):
                                    # Reset task to allow editing
                                    if "completed_tasks" in st.session_state and task_id in st.session_state.completed_tasks:
                                        del st.session_state.completed_tasks[task_id]
                                    st.rerun()
                    
                        else:
                            # Input area for submission
                            user_answer = st.text_area(
                                "Twoja odpowiedź:",
                                placeholder="Napisz krótkie podsumowanie tego, czego się nauczyłeś...",
                                key=f"answer_{task_id}",
                                height=100
                            )
                        
                            if st.button(f"📤 Złóż zadanie", key=f"submit_{task_id}", type="primary", use_container_width=True):
                                if user_answer and len(user_answer) >= 10:
                                    # Submit task first
                                    submit_task(st.session_state, task_id, user_answer)
                                    
                                    # Immediate AI evaluation
                                    with st.spinner("🤖 AI ocenia Twoje rozwiązanie..."):
                                        feedback, is_accepted = evaluate_task_with_ai(task_id, user_answer, task)
                                    
                                    if is_accepted:
                                        # Complete task immediately
                                        complete_task(st.session_state, task_id, feedback=feedback)
                                        
                                        # Update Company Reputation - Task Performance component
                                        from utils.reputation_system import (
                                            calculate_company_reputation,
                                            calculate_overall_rating,
                                            get_tier
                                        )
                                        
                                        # Boost task_performance component by 5 points per completed task
                                        if "reputation" not in game_state:
                                            game_state["reputation"] = {
                                                "company": {"task_performance": 0},
                                                "overall_rating": 0,
                                                "tier": "Trainee"
                                            }
                                        
                                        if "task_performance" not in game_state["reputation"]["company"]:
                                            game_state["reputation"]["company"]["task_performance"] = 0
                                        
                                        # Add 5 points per completed onboarding task (max 15 for 3 tasks)
                                        game_state["reputation"]["company"]["task_performance"] = min(
                                            game_state["reputation"]["company"]["task_performance"] + 5,
                                            15  # Max 15 from onboarding tasks
                                        )
                                        
                                        # Recalculate company reputation and overall rating
                                        company_rep = calculate_company_reputation(game_state)
                                        game_state["reputation"]["company_reputation"] = company_rep
                                        
                                        overall = calculate_overall_rating(game_state, clients)
                                        game_state["reputation"]["overall_rating"] = overall
                                        
                                        tier = get_tier(overall)
                                        game_state["reputation"]["tier"] = tier
                                        
                                        # Persist updated reputation to database
                                        try:
                                            update_fmcg_game_state_sql(username, game_state, clients)
                                        except Exception as e:
                                            st.warning(f"⚠️ Nie udało się zapisać postępu: {e}")
                                        
                                        st.success("🎉 **Zadanie zaakceptowane!**")
                                        st.balloons()
                                        
                                        # Show reputation boost
                                        st.success(f"📈 **Company Reputation:** +5 Task Performance → Overall Rating: {overall:.1f}/100")
                                        
                                        # Show feedback from task assigner
                                        st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; border-radius: 12px; color: white; margin: 16px 0;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
    <div style='font-size: 16px; font-weight: 700; margin-bottom: 8px;'>💬 Feedback</div>
    <div style='font-size: 14px; line-height: 1.6; opacity: 0.95;'>{feedback}</div>
</div>
""", unsafe_allow_html=True)
                                        
                                        # Close button to refresh
                                        if st.button("✅ Zamknij i odśwież", key=f"close_{task_id}", type="primary", use_container_width=True):
                                            st.rerun()
                                    else:
                                        # Not accepted - reset to "not submitted" state so user can edit
                                        if "completed_tasks" in st.session_state and task_id in st.session_state.completed_tasks:
                                            del st.session_state.completed_tasks[task_id]
                                        
                                        # Show feedback
                                        st.warning("⚠️ **Wymaga poprawek**")
                                        
                                        st.markdown(f"""
<div style='background: #fef3c7; padding: 20px; border-radius: 12px; 
            border-left: 4px solid #f59e0b; margin: 16px 0;'>
    <div style='font-size: 16px; font-weight: 700; margin-bottom: 8px; color: #92400e;'>
        � Feedback
    </div>
    <div style='font-size: 14px; line-height: 1.6; color: #78350f;'>{feedback}</div>
</div>
""", unsafe_allow_html=True)
                                        
                                        st.info("💡 Przeczytaj feedback i popraw swoją odpowiedź powyżej. Następnie kliknij ponownie 'Złóż zadanie'.")
                                else:
                                    st.error("❌ Odpowiedź zbyt krótka (min. 10 znaków)")
            
                # Summary at bottom
                st.markdown("---")
                st.info(f"""
                💡 **Status:** {3 - pending}/3 zadań ukończonych
            
                Po ukończeniu wszystkich zadań będziesz gotowy do efektywnej pracy w terenie!
                """)
        
            # =============================================================================
            # HISTORIA REALIZACJI ZADAŃ
            # =============================================================================
            
            # Collect completed tasks history
            completed_tasks_history = []
            if "completed_tasks" in st.session_state:
                for task_id, task_data in st.session_state.completed_tasks.items():
                    if task_data.get("status") == "completed" and task_id in ONBOARDING_TASKS:
                        completed_tasks_history.append({
                            "task_id": task_id,
                            "title": ONBOARDING_TASKS[task_id]["title"],
                            "submission": task_data.get("submission", ""),
                            "feedback": task_data.get("feedback", ""),
                            "submitted_at": task_data.get("submitted_at", ""),
                            "completed_at": task_data.get("completed_at", "")
                        })
            
            if completed_tasks_history:
                with st.expander(f"📚 Historia realizacji zadań ({len(completed_tasks_history)})", expanded=False):
                    # Sort by completion date - newest first
                    sorted_tasks = sorted(
                        completed_tasks_history, 
                        key=lambda x: x.get('completed_at', ''), 
                        reverse=True
                    )
                    
                    for task_history in sorted_tasks:
                        # Each completed task in its own expander
                        with st.expander(f"✅ {task_history['title']}", expanded=False):
                            # Task description
                            task_description = ONBOARDING_TASKS[task_history['task_id']].get('description', '')
                            if task_description:
                                st.markdown("**📋 Treść zadania:**")
                                st.markdown(task_description)
                                st.markdown("---")
                            
                            # Timestamps
                            col_t1, col_t2 = st.columns(2)
                            with col_t1:
                                if task_history['submitted_at']:
                                    st.caption(f"📅 Złożono: {task_history['submitted_at'][:16]}")
                            with col_t2:
                                if task_history['completed_at']:
                                    st.caption(f"✅ Ukończono: {task_history['completed_at'][:16]}")
                            
                            st.markdown("---")
                            
                            # Submission
                            st.markdown("**📄 Twoja odpowiedź:**")
                            st.info(task_history['submission'])
                            
                            # Feedback
                            if task_history['feedback']:
                                st.markdown("**💬 Feedback:**")
                                st.success(task_history['feedback'])
        
            # =============================================================================
            # HISTORIA WIZYT - jako sekcja w Dashboard
            # =============================================================================
        
            with st.expander("📈 Historia Wizyt i Statystyki", expanded=False):
                # Get visit history
                visit_history = game_state.get("visit_history", [])
            
                if not visit_history:
                    st.info("📭 Brak historii wizyt. Wykonaj pierwszą wizytę aby zobaczyć statystyki!")
                else:
                    # Summary stats
                    col_v1, col_v2, col_v3 = st.columns(3)
                
                    with col_v1:
                        st.metric("📊 Wszystkie wizyty", len(visit_history))
                
                    with col_v2:
                        successful = sum(1 for v in visit_history if v.get("outcome") == "success")
                        st.metric("✅ Udane", successful)
                
                    with col_v3:
                        if len(visit_history) > 0:
                            success_rate = (successful / len(visit_history)) * 100
                            st.metric("📈 Win rate", f"{success_rate:.0f}%")
                
                    st.markdown("---")
                
                    # Recent visits (last 10)
                    st.markdown("### 🕒 Ostatnie wizyty")
                
                    for visit in reversed(visit_history[-10:]):
                        client_id = visit.get("client_id")
                        client = clients.get(client_id, {})
                        client_name = client.get("name", "Nieznany klient")
                    
                        outcome = visit.get("outcome", "unknown")
                        date = visit.get("date", "N/A")
                        notes = visit.get("notes", "Brak notatek")
                    
                        # Outcome icon
                        outcome_icon = "✅" if outcome == "success" else "❌" if outcome == "failed" else "⏸️"
                        outcome_color = "#10b981" if outcome == "success" else "#ef4444" if outcome == "failed" else "#6b7280"
                    
                        with st.container():
                            st.markdown(f"""
                            <div style='background: white; padding: 12px; border-radius: 8px; border-left: 4px solid {outcome_color}; margin-bottom: 8px;'>
                                <div style='font-weight: 600; margin-bottom: 4px;'>{outcome_icon} {client_name}</div>
                                <div style='font-size: 0.85rem; color: #64748b;'>📅 {date}</div>
                                <div style='font-size: 0.9rem; margin-top: 4px;'>{notes}</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                    if len(visit_history) > 10:
                        st.caption(f"Pokazano 10 z {len(visit_history)} wizyt")
    
        # =============================================================================
    # TAB: SPRZEDAŻ (nowa - konsolidacja: Klienci + Rozmowa + Produkty)
    # =============================================================================
    
    with tab_sales:
        # Sub-tabs dla różnych widoków sprzedaży
        sales_tab_map, sales_tab_prep, sales_tab_visit, sales_tab_products = st.tabs([
            "🗺️ Klienci & Trasa",
            "💼 Przygotowanie",
            "🤝 Wizyta",
            "📦 Produkty"
        ])
        
        # =========================================================================
        # SUB-TAB: MAPA & KLIENCI
        # =========================================================================
        
        with sales_tab_map:
            st.subheader("🗺️ Mapa Klientów")
            # Check if viewing client detail first (takes priority over list view)
            if st.session_state.get('show_client_detail', False):
                selected_client_id = st.session_state.get('selected_client_id')
            
                if selected_client_id and selected_client_id in clients:
                    # Get client data from new structure (SQL)
                    client_data = clients[selected_client_id]
                
                    # Use client_data as client_info (has all fields we need)
                    client_info = {
                        'name': client_data.get('name', selected_client_id),
                        'location': client_data.get('location', 'N/A'),
                        'owner': client_data.get('owner', 'N/A'),
                        'monthly_revenue': client_data.get('total_sales', 'N/A'),
                        'type': client_data.get('type', 'Sklep'),
                        'characteristics': client_data.get('characteristics', {})
                    }
                
                    render_client_detail_card(client_data, client_info)
                else:
                    st.error("❌ Błąd - klient nie istnieje")
                    st.session_state['show_client_detail'] = False
        
            else:
                # Client view based on scenario
                if is_heinz_scenario:
                    # =====================================================================
                    # HEINZ FOOD SERVICE - ENHANCED CLIENT VIEW
                    # =====================================================================
                
                    # =====================================================================
                    # SEKCJA 1: FILTRY I SORTOWANIE (na górze)
                    # =====================================================================
                    st.markdown("### 🎯 Filtry i sortowanie")
                    
                    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
                
                    with col_f1:
                        segment_filter = st.selectbox(
                            "🎯 Segment",
                            ["Wszystkie", "Premium", "Value", "Mixed"],
                            key="heinz_segment_filter"
                        )
                
                    with col_f2:
                        supplier_filter = st.selectbox(
                            "📦 Dostawca",
                            ["Wszyscy", "Kotlin", "Pudliszki", "Heinz", "No-name/Mix", "Brak"],
                            key="heinz_supplier_filter"
                        )
                
                    with col_f3:
                        type_filter = st.selectbox(
                            "🏪 Typ",
                            ["Wszystkie", "Burger/Street Food", "Kebab/Fast Food", "Stołówka/Bar", "Pizzeria/Casual", "Hotel", "Dystrybutor"],
                            key="heinz_type_filter"
                        )
                
                    with col_f4:
                        sort_by = st.selectbox(
                            "📊 Sortuj wg",
                            ["Dystans ↑", "Potencjał ↓", "Nazwa A-Z", "Ostatnia wizyta ↓", "Reputacja ↓"],
                            key="heinz_sort"
                        )
                
                    # Filter clients
                    filtered_clients = {}
                    for cid, client in clients.items():
                        # Segment filter
                        if segment_filter != "Wszystkie":
                            if client.get("segment", "").lower() != segment_filter.lower():
                                continue
                    
                        # Supplier filter
                        if supplier_filter != "Wszyscy":
                            current_supplier = client.get("current_supplier", "Brak")
                            if supplier_filter == "No-name/Mix":
                                if current_supplier not in ["Mix (Pudliszki + Kotlin)", "Brak stałego", "No-name 10kg wiadro (najtańszy)"]:
                                    continue
                            elif supplier_filter not in current_supplier:
                                continue
                    
                        # Type filter (simplified mapping)
                        if type_filter != "Wszystkie":
                            client_type = client.get("type", "")
                            type_mapping = {
                                "Burger/Street Food": ["burger_joint", "food_truck", "street_food"],
                                "Kebab/Fast Food": ["kebab", "fast_food_ethnic"],
                                "Stołówka/Bar": ["bar_mleczny", "canteen_school", "canteen_corporate"],
                                "Pizzeria/Casual": ["pizzeria", "pizza_chain", "casual_dining"],
                                "Hotel": ["hotel_3star", "hotel_4star"],
                                "Dystrybutor": ["distributor", "distributor_small", "cash_and_carry"]
                            }
                            if client_type not in type_mapping.get(type_filter, []):
                                continue
                    
                        filtered_clients[cid] = client
                
                    # Sort clients
                    sorted_clients_list = list(filtered_clients.items())
                    
                    if sort_by == "Dystans ↑":
                        sorted_clients_list.sort(key=lambda x: x[1].get("distance_from_base", 999))
                    elif sort_by == "Potencjał ↓":
                        sorted_clients_list.sort(key=lambda x: x[1].get("monthly_volume_kg", 0), reverse=True)
                    elif sort_by == "Nazwa A-Z":
                        sorted_clients_list.sort(key=lambda x: x[1].get("name", ""))
                    elif sort_by == "Ostatnia wizyta ↓":
                        # Sortuj po dniach od ostatniej wizyty (najwięcej dni = priorytet)
                        def get_days_since_visit(client):
                            last_visit_date = client.get("last_visit_date")
                            if last_visit_date:
                                try:
                                    if isinstance(last_visit_date, str):
                                        last_visit_dt = datetime.fromisoformat(last_visit_date)
                                    else:
                                        last_visit_dt = last_visit_date
                                    return (datetime.now() - last_visit_dt).days
                                except:
                                    return 999  # Brak daty = na koniec
                            return 999  # Nowy klient = na koniec
                        sorted_clients_list.sort(key=lambda x: get_days_since_visit(x[1]), reverse=True)
                    elif sort_by == "Reputacja ↓":
                        sorted_clients_list.sort(key=lambda x: x[1].get("reputation", 0), reverse=True)
                    
                    filtered_clients = dict(sorted_clients_list)
                
                    st.info(f"🔍 Znaleziono: **{len(filtered_clients)}** klientów")
                    
                    st.markdown("---")
                    
                    # =====================================================================
                    # TABS - MAPA | LISTA KLIENTÓW
                    # =====================================================================
                    view_tab_map, view_tab_table = st.tabs(["🗺️ Mapa", "📋 Lista klientów"])
                    
                    with view_tab_map:
                        st.markdown("**Legenda - ostatnia wizyta:**")
                        st.caption("🟢 0-3 dni  |  🟡 4-7 dni  |  🟠 8-14 dni  |  🔴 15+ dni  |  ⚪ Nowy klient  |  ⭐ W trasie")
                        
                        # Info about clickable map
                        st.info("💡 **Kliknij pin na mapie** aby dodać/usunąć klienta z trasy (max 6)")
                        
                        st.markdown("---")
                        
                        # Create Folium map centered on Dzięgielów (Lipowa 29)
                        base_lat = game_state.get("territory_latitude", 49.7271667)  # 49°43'37.8"N
                        base_lon = game_state.get("territory_longitude", 18.7025833)  # 18°42'09.3"E
                    
                        st.caption(f"🏢 Baza: ({base_lat:.6f}, {base_lon:.6f}) - Lipowa 29, Dzięgielów")
                    
                        m = folium.Map(
                            location=[base_lat, base_lon],
                            zoom_start=11,
                            tiles="OpenStreetMap"
                        )
                    
                        # Add base marker
                        folium.Marker(
                            [base_lat, base_lon],
                            popup=f"🏢 Baza Heinz - Dzięgielów<br>Lipowa 29, 43-445 Dzięgielów<br>({base_lat:.4f}, {base_lon:.4f})",
                            icon=folium.Icon(color="red", icon="home", prefix="fa"),
                            tooltip="Twoja baza (Lipowa 29, Dzięgielów)"
                        ).add_to(m)
                    
                        # Segment colors
                        segment_colors = {
                            "premium": "#7c3aed",  # Purple
                            "value": "#10b981",    # Green
                            "mixed": "#f59e0b",    # Orange
                            "distributor": "#ef4444"  # Red (special)
                        }
                    
                        # Add client markers
                        for client_id, client in filtered_clients.items():
                            lat = client.get("latitude", base_lat)
                            lon = client.get("longitude", base_lon)
                            name = client.get("name", client_id)
                            segment = client.get("segment", "mixed")
                            client_type = client.get("type", "")
                            distance = client.get("distance_from_base", 0)
                            potential_kg = client.get("monthly_volume_kg", 0)
                            current_supplier = client.get("current_supplier", "Brak")
                            recommended_products = client.get("recommended_products", [])
                            upsell_pot = client.get("upsell_potential", "medium")
                            
                            # Oblicz dni od ostatniej wizyty
                            last_visit_date = client.get("last_visit_date")
                            if last_visit_date:
                                try:
                                    if isinstance(last_visit_date, str):
                                        last_visit_dt = datetime.fromisoformat(last_visit_date)
                                    else:
                                        last_visit_dt = last_visit_date
                                    days_since_visit = (datetime.now() - last_visit_dt).days
                                except:
                                    days_since_visit = None
                            else:
                                days_since_visit = None
                            
                            # Kolor pinu bazujący na czasie ostatniej wizyty
                            pin_color_by_time = get_pin_color_by_days(days_since_visit)
                            color_emoji = get_color_emoji_by_days(days_since_visit)
                            
                            # Tekst dla tooltip
                            if days_since_visit is None:
                                visit_status = "Nowy klient"
                            else:
                                visit_status = f"{days_since_visit} dni temu"
                        
                            # Color by segment (dla tła w popup)
                            pin_color = segment_colors.get(segment, "#64748b")
                        
                            # Emoji by type
                            type_emojis = {
                                "burger_joint": "🍔", "food_truck": "🚚", "street_food": "🌭",
                                "kebab": "🌯", "fast_food_ethnic": "🥙",
                                "bar_mleczny": "🍽️", "canteen_school": "🏫", "canteen_corporate": "🏢",
                                "pizzeria": "🍕", "pizza_chain": "🍕", "casual_dining": "🍴",
                                "hotel_3star": "🏨", "hotel_4star": "🏨",
                                "distributor": "📦", "distributor_small": "📦", "cash_and_carry": "🏪"
                            }
                            type_emoji = type_emojis.get(client_type, "🏪")
                        
                            # Popup content (dodajemy info o ostatniej wizycie)
                            products_str = "<br>".join([f"• {p}" for p in recommended_products[:2]])
                            
                            # Check if client is in planned route
                            is_in_route = False
                            route_number = None
                            if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                                if client_id in st.session_state.planned_route:
                                    is_in_route = True
                                    route_number = st.session_state.planned_route.index(client_id) + 1
                            
                            # Route badge in popup
                            route_badge = ""
                            if is_in_route:
                                route_badge = f"<div style='background: #9333ea; color: white; padding: 6px 12px; border-radius: 6px; text-align: center; font-size: 12px; font-weight: 700; margin-bottom: 8px;'>⭐ W TRASIE - #{route_number}</div>"
                            
                            popup_html = f"""
                            <div style='min-width: 250px; font-family: system-ui;'>
                                <h3 style='margin: 0 0 8px 0; color: {pin_color};'>{type_emoji} {name}</h3>
                                {route_badge}
                                <div style='background: {pin_color}20; padding: 8px; border-radius: 6px; margin-bottom: 8px;'>
                                    <b>Segment:</b> {segment.upper()}<br>
                                    <b>Potencjał:</b> {potential_kg} kg/mies<br>
                                    <b>Dystans:</b> {distance:.1f} km<br>
                                    <b>{color_emoji} Ostatnia wizyta:</b> {visit_status}
                                </div>
                                <p style='margin: 4px 0; font-size: 13px;'><b>Obecnie:</b> {current_supplier}</p>
                                <p style='margin: 4px 0; font-size: 13px;'><b>Rekomendacja:</b><br>{products_str}</p>
                                <div style='background: {"#10b981" if upsell_pot in ["very_high", "guaranteed"] else "#f59e0b" if upsell_pot == "high" else "#94a3b8"}; color: white; padding: 4px 8px; border-radius: 4px; text-align: center; font-size: 12px; font-weight: 600; margin-top: 8px;'>
                                    Upsell: {upsell_pot.upper()}
                                </div>
                                <div style='margin-top: 8px; font-size: 11px; color: #64748b; font-style: italic; text-align: center;'>
                                    💡 Kliknij aby {'usunąć z trasy' if is_in_route else 'dodać do trasy'}
                                </div>
                            </div>
                            """
                        
                            # Tooltip HTML (pełna karta jak popup, ale bez interakcji)
                            tooltip_html = f"""
                            <div style='min-width: 250px; font-family: system-ui;'>
                                <h3 style='margin: 0 0 8px 0; color: {pin_color};'>{type_emoji} {name}</h3>
                                {route_badge}
                                <div style='background: {pin_color}20; padding: 8px; border-radius: 6px; margin-bottom: 8px;'>
                                    <b>Segment:</b> {segment.upper()}<br>
                                    <b>Potencjał:</b> {potential_kg} kg/mies<br>
                                    <b>Dystans:</b> {distance:.1f} km<br>
                                    <b>{color_emoji} Ostatnia wizyta:</b> {visit_status}
                                </div>
                                <p style='margin: 4px 0; font-size: 13px;'><b>Obecnie:</b> {current_supplier}</p>
                                <p style='margin: 4px 0; font-size: 13px;'><b>Rekomendacja:</b><br>{products_str}</p>
                                <div style='background: {"#10b981" if upsell_pot in ["very_high", "guaranteed"] else "#f59e0b" if upsell_pot == "high" else "#94a3b8"}; color: white; padding: 4px 8px; border-radius: 4px; text-align: center; font-size: 12px; font-weight: 600; margin-top: 8px;'>
                                    Upsell: {upsell_pot.upper()}
                                </div>
                            </div>
                            """
                        
                            # Custom marker - numbered for route or colored pin
                            if is_in_route:
                                # Numbered purple marker for route
                                folium.Marker(
                                    [lat, lon],
                                    popup=folium.Popup(popup_html, max_width=300),
                                    icon=folium.DivIcon(html=f"""
                                        <div style="
                                            background-color: #9333ea;
                                            color: white;
                                            border: 3px solid white;
                                            border-radius: 50%;
                                            width: 32px;
                                            height: 32px;
                                            display: flex;
                                            align-items: center;
                                            justify-content: center;
                                            font-weight: bold;
                                            font-size: 16px;
                                            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                                        ">{route_number}</div>
                                    """),
                                    tooltip=folium.Tooltip(tooltip_html, sticky=True)
                                ).add_to(m)
                            else:
                                # Regular colored pin by visit recency
                                folium.Marker(
                                    [lat, lon],
                                    popup=folium.Popup(popup_html, max_width=300),
                                    icon=folium.Icon(color=pin_color_by_time, icon="cutlery", prefix="fa"),
                                    tooltip=folium.Tooltip(tooltip_html, sticky=True)
                                ).add_to(m)
                    
                        # Draw route line if planned_route exists
                        if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                            # Ensure planned_route is a flat list of strings
                            if isinstance(st.session_state.planned_route, list):
                                # Flatten if nested and filter out non-strings
                                flat_route = []
                                for item in st.session_state.planned_route:
                                    if isinstance(item, str):
                                        flat_route.append(item)
                                    elif isinstance(item, list):
                                        flat_route.extend([x for x in item if isinstance(x, str)])
                                st.session_state.planned_route = flat_route
                            
                            # Get selected shops with locations
                            selected_shops = []
                            for cid in st.session_state.planned_route:
                                if isinstance(cid, str) and cid in filtered_clients:
                                    selected_shops.append({
                                        "client_id": cid,
                                        "lat": filtered_clients[cid].get("latitude", base_lat),
                                        "lng": filtered_clients[cid].get("longitude", base_lon)
                                    })
                        
                            # Get route geometry split (visits + return) using OSRM
                            if selected_shops:
                                route_split = get_route_geometry_split(
                                    {"lat": base_lat, "lng": base_lon},
                                    selected_shops,
                                    st.session_state.planned_route
                                )
                            
                                visits_geometry = route_split.get("visits", [])
                                return_geometry = route_split.get("return", [])
                            else:
                                visits_geometry = []
                                return_geometry = []
                        
                            # Fallback: proste linie jeśli OSRM nie działa
                            if not visits_geometry and st.session_state.planned_route:
                                visits_geometry = [[base_lat, base_lon]]
                                for client_id in st.session_state.planned_route:
                                    if isinstance(client_id, str) and client_id in filtered_clients:
                                        client = filtered_clients[client_id]
                                        visits_geometry.append([
                                            client.get("latitude", base_lat),
                                            client.get("longitude", base_lon)
                                        ])
                        
                            if not return_geometry and st.session_state.planned_route:
                                last_client_id = st.session_state.planned_route[-1]
                                if isinstance(last_client_id, str) and last_client_id in filtered_clients:
                                    last_client = filtered_clients[last_client_id]
                                    return_geometry = [
                                        [last_client.get("latitude", base_lat), last_client.get("longitude", base_lon)],
                                        [base_lat, base_lon]
                                    ]
                        
                            # Draw visits route (purple/blue)
                            if visits_geometry:
                                folium.PolyLine(
                                    visits_geometry,
                                    color='#9333ea',  # Purple for visits
                                    weight=5,
                                    opacity=0.8,
                                    popup="🗺️ Trasa wizyt"
                                ).add_to(m)
                        
                            # Draw return route (red)
                            if return_geometry:
                                folium.PolyLine(
                                    return_geometry,
                                    color='#ef4444',  # Red for return
                                    weight=5,
                                    opacity=0.7,
                                    dash_array='10, 5',  # Dashed line
                                    popup="🏠 Powrót do bazy"
                                ).add_to(m)
                    
                        # Display interactive map with click handling
                        map_data = st_folium(
                            m, 
                            width=900, 
                            height=500,
                            returned_objects=["last_object_clicked"],
                            key="heinz_map"
                        )
                        
                        # Handle map clicks - add/remove from route
                        if map_data and map_data.get("last_object_clicked"):
                            clicked = map_data["last_object_clicked"]
                            # Extract client_id from tooltip (format: "emoji name - text")
                            tooltip_text = clicked.get("tooltip", "")
                            
                            # Find matching client by coordinates
                            clicked_lat = clicked.get("lat")
                            clicked_lng = clicked.get("lng")
                            
                            if clicked_lat and clicked_lng:
                                # Find client with matching coordinates
                                for cid, client in filtered_clients.items():
                                    client_lat = client.get("latitude")
                                    client_lng = client.get("longitude")
                                    
                                    # Check if coordinates match (with small tolerance)
                                    if client_lat and client_lng:
                                        if abs(client_lat - clicked_lat) < 0.0001 and abs(client_lng - clicked_lng) < 0.0001:
                                            # Initialize planned_route if not exists
                                            if not hasattr(st.session_state, 'planned_route'):
                                                st.session_state.planned_route = []
                                            
                                            # Toggle client in route
                                            if cid in st.session_state.planned_route:
                                                st.session_state.planned_route.remove(cid)
                                                st.toast(f"🗑️ Usunięto {client.get('name')} z trasy", icon="ℹ️")
                                            else:
                                                if len(st.session_state.planned_route) < 6:
                                                    st.session_state.planned_route.append(cid)
                                                    st.toast(f"✅ Dodano {client.get('name')} do trasy (#{len(st.session_state.planned_route)})", icon="🎯")
                                                else:
                                                    st.toast("⚠️ Maksymalnie 6 klientów w trasie!", icon="⚠️")
                                            
                                            st.rerun()
                                            break
                        
                        # Show current route summary below map
                        if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                            st.markdown("---")
                            st.markdown("**📍 Aktualna trasa (kliknij na mapie aby edytować):**")
                            
                            route_clients = []
                            for i, cid in enumerate(st.session_state.planned_route):
                                if isinstance(cid, str) and cid in filtered_clients:
                                    client = filtered_clients[cid]
                                    route_clients.append(f"{i+1}. **{client.get('name')}** ({client.get('distance_from_base', 0):.1f} km)")
                            
                            if route_clients:
                                st.markdown(" → ".join(route_clients))
                                
                                # Calculate route characteristics
                                total_points = len(st.session_state.planned_route)
                                total_distance = 0
                                
                                # Sum distances from base for each client
                                for cid in st.session_state.planned_route:
                                    if isinstance(cid, str) and cid in filtered_clients:
                                        client = filtered_clients[cid]
                                        total_distance += client.get("distance_from_base", 0)
                                
                                # Add return distance (last client to base - approximate as same distance)
                                if st.session_state.planned_route and isinstance(st.session_state.planned_route[-1], str):
                                    last_client_id = st.session_state.planned_route[-1]
                                    if last_client_id in filtered_clients:
                                        total_distance += filtered_clients[last_client_id].get("distance_from_base", 0)
                                
                                # Estimate time (average 30 min per visit + 5 min per 10km travel)
                                visit_time = total_points * 30  # minutes
                                travel_time = (total_distance / 10) * 5  # minutes (5 min per 10km)
                                total_time = visit_time + travel_time
                                
                                # Convert to hours
                                total_hours = total_time / 60
                                
                                # Estimate energy (calories - rough estimate: 50 kcal per hour active work)
                                energy_kcal = total_hours * 50
                                
                                # Display route characteristics in nice card
                                st.markdown(f"""
                                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                            padding: 16px; border-radius: 12px; margin: 16px 0;'>
                                    <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;'>
                                        <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center;'>
                                            <div style='font-size: 28px; font-weight: bold; color: white;'>{total_points}</div>
                                            <div style='font-size: 12px; color: rgba(255,255,255,0.8);'>📍 Punktów</div>
                                        </div>
                                        <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center;'>
                                            <div style='font-size: 28px; font-weight: bold; color: white;'>{total_distance:.1f}</div>
                                            <div style='font-size: 12px; color: rgba(255,255,255,0.8);'>🚗 km</div>
                                        </div>
                                        <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center;'>
                                            <div style='font-size: 28px; font-weight: bold; color: white;'>{total_hours:.1f}</div>
                                            <div style='font-size: 12px; color: rgba(255,255,255,0.8);'>⏱️ godzin</div>
                                        </div>
                                        <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center;'>
                                            <div style='font-size: 28px; font-weight: bold; color: white;'>{energy_kcal:.0f}</div>
                                            <div style='font-size: 12px; color: rgba(255,255,255,0.8);'>🔥 kcal</div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col_clear, col_opt = st.columns(2)
                                with col_clear:
                                    if st.button("🗑️ Wyczyść trasę", key="clear_route_from_map"):
                                        st.session_state.planned_route = []
                                        st.rerun()
                                with col_opt:
                                    if len(st.session_state.planned_route) >= 2:
                                        if st.button("🚀 Optymalizuj (ALEX)", key="optimize_from_map"):
                                            base_location = {
                                                "lat": game_state.get("territory_latitude", 49.7271667),
                                                "lng": game_state.get("territory_longitude", 18.7025833)
                                            }
                                            selected_shops = []
                                            for cid in st.session_state.planned_route:
                                                if isinstance(cid, str) and cid in filtered_clients:
                                                    client = filtered_clients[cid]
                                                    selected_shops.append({
                                                        "client_id": cid,
                                                        "name": client.get("name", cid),
                                                        "lat": client.get("latitude", base_location["lat"]),
                                                        "lng": client.get("longitude", base_location["lng"])
                                                    })
                                            optimized_route, route_distance = optimize_route(base_location, selected_shops)
                                            st.session_state.planned_route = optimized_route
                                            st.success(f"✅ Trasa zoptymalizowana! Dystans: {route_distance:.1f} km")
                                            st.rerun()
                    
                        # Legend
                        st.markdown("""
                        <div style='background: #f8fafc; padding: 12px; border-radius: 8px; margin-top: 12px;'>
                            <b>Legenda:</b><br>
                            <span style='color: #7c3aed;'>🟣 Premium</span> • 
                            <span style='color: #10b981;'>🟢 Value</span> • 
                            <span style='color: #f59e0b;'>🟠 Mixed</span> • 
                            <span style='color: #ef4444;'>🔴 Baza</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                    with view_tab_table:
                        # Table view with detailed info in two columns
                        clients_list = list(filtered_clients.items())
                        
                        # Split into two columns
                        col1, col2 = st.columns(2)
                        
                        # Distribute clients evenly between columns
                        mid_point = len(clients_list) // 2 + len(clients_list) % 2
                        
                        for idx, (client_id, client) in enumerate(clients_list):
                            # Choose which column to use
                            current_col = col1 if idx < mid_point else col2
                            
                            with current_col:
                                name = client.get("name", client_id)
                                owner = client.get("owner", "N/A")
                                segment = client.get("segment", "mixed")
                                client_type = client.get("type", "")
                                distance = client.get("distance_from_base", 0)
                                potential_kg = client.get("monthly_volume_kg", 0)
                                current_supplier = client.get("current_supplier", "Brak")
                                personality = client.get("personality", "N/A")
                                upsell_pot = client.get("upsell_potential", "medium")
                                recommended_strategy = client.get("recommended_strategy", "")
                                
                                # Check if potential is discovered (Food category discovered)
                                discovered_info = client.get("discovered_info", {})
                                sales_capacity_discovered = discovered_info.get("sales_capacity_discovered", {})
                                is_potential_discovered = "Food" in sales_capacity_discovered
                                
                                # Oblicz dni od ostatniej wizyty
                                last_visit_date = client.get("last_visit_date")
                                if last_visit_date:
                                    try:
                                        if isinstance(last_visit_date, str):
                                            last_visit_dt = datetime.fromisoformat(last_visit_date)
                                        else:
                                            last_visit_dt = last_visit_date
                                        days_since_visit = (datetime.now() - last_visit_dt).days
                                    except:
                                        days_since_visit = None
                                else:
                                    days_since_visit = None
                                
                                # Emoji koloru dla ostatniej wizyty
                                color_emoji = get_color_emoji_by_days(days_since_visit)
                                if days_since_visit is None:
                                    visit_text = "Nowy klient"
                                else:
                                    visit_text = f"{days_since_visit} dni temu"
                            
                                # Segment badge color
                                segment_colors_badge = {
                                    "premium": "#7c3aed",
                                    "value": "#10b981",
                                    "mixed": "#f59e0b"
                                }
                                seg_color = segment_colors_badge.get(segment, "#64748b")
                            
                                # Upsell badge
                                upsell_colors = {
                                    "very_high": "#10b981", "guaranteed": "#10b981",
                                    "high": "#3b82f6", "medium": "#f59e0b",
                                    "low": "#94a3b8", "very_low": "#ef4444"
                                }
                                upsell_color = upsell_colors.get(upsell_pot, "#94a3b8")
                            
                                st.markdown(f"""
                                <div style='background: linear-gradient(135deg, {seg_color}15 0%, {seg_color}05 100%); 
                                            border-left: 4px solid {seg_color}; padding: 16px; border-radius: 12px; margin-bottom: 12px;'>
                                    <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                                        <div style='flex: 1;'>
                                            <div style='font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 4px;'>
                                                {name}
                                                <span style='background: {seg_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 8px;'>
                                                    {segment.upper()}
                                                </span>
                                            </div>
                                            <div style='font-size: 13px; color: #64748b; margin-bottom: 4px;'>
                                                {owner} • MBTI: {personality}
                                            </div>
                                            <div style='font-size: 13px; color: #64748b; margin-bottom: 8px;'>
                                                📍 {distance:.1f} km • {color_emoji} {visit_text}
                                            </div>
                                            <div style='display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px;'>
                                                <div style='background: #f1f5f9; padding: 6px 12px; border-radius: 6px; font-size: 12px;'>
                                                    📦 Obecnie: <b>{current_supplier}</b>
                                                </div>
                                                <div style='background: #f1f5f9; padding: 6px 12px; border-radius: 6px; font-size: 12px;'>
                                                    💰 Potencjał: <b>{"Nieznany" if not is_potential_discovered else f"{potential_kg} kg/mies"}</b>
                                                </div>
                                                <div style='background: {upsell_color}; color: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;'>
                                                    ⬆️ Upsell: {upsell_pot.upper()}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                                # Action button
                                if st.button("Szczegóły", key=f"visit_heinz_{client_id}", use_container_width=True):
                                    st.session_state['show_client_detail'] = True
                                    st.session_state['selected_client_id'] = client_id
                                    st.rerun()
                    
                    # =====================================================================
                    # SEKCJA 4: PLANOWANIE TRASY (na samym dole)
                    # =====================================================================
                    st.markdown("---")
                    st.markdown("### 🗺️ Planowanie trasy dziennej")
                    
                    with st.expander("📍 Wybierz klientów do odwiedzenia", expanded=False):
                        st.markdown("Wybierz klientów do odwiedzenia w jednej trasie (max 6):")
                    
                        # Multi-select clients for route
                        route_client_options = {
                            cid: f"{client.get('name', cid)} ({client.get('distance_from_base', 0):.1f} km, {client.get('segment', 'mixed').upper()})"
                            for cid, client in filtered_clients.items()
                        }
                    
                        selected_for_route = st.multiselect(
                            "Zaznacz klientów:",
                            options=list(route_client_options.keys()),
                            format_func=lambda x: route_client_options[x],
                            max_selections=6,
                            key="heinz_route_selection"
                        )
                    
                        # Show route characteristics if clients selected
                        if selected_for_route:
                            total_points = len(selected_for_route)
                            
                            # Calculate total distance (sum of distances + return)
                            base_lat = game_state.get("territory_latitude", 49.7271667)
                            base_lon = game_state.get("territory_longitude", 18.7025833)
                            
                            total_distance = 0
                            for cid in selected_for_route:
                                if isinstance(cid, str) and cid in filtered_clients:
                                    client = filtered_clients[cid]
                                    total_distance += client.get("distance_from_base", 0)
                            
                            # Add return distance (from last client back to base)
                            if selected_for_route:
                                last_cid = selected_for_route[-1]
                                if isinstance(last_cid, str) and last_cid in filtered_clients:
                                    last_client = filtered_clients[last_cid]
                                    total_distance += last_client.get("distance_from_base", 0)
                            
                            # Calculate time (30 min per visit + 5 min per 10 km)
                            visit_time = total_points * 30  # minutes
                            travel_time = (total_distance / 10) * 5  # 5 min per 10 km
                            total_time = visit_time + travel_time
                            total_hours = total_time / 60
                            
                            # Calculate energy (50 kcal per hour)
                            energy_kcal = total_hours * 50
                            
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        padding: 20px; border-radius: 10px; margin: 15px 0;
                                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                                <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;'>
                                    <div style='text-align: center; color: white;'>
                                        <div style='font-size: 32px; font-weight: bold; margin-bottom: 5px;'>{total_points}</div>
                                        <div style='font-size: 14px; opacity: 0.9;'>Punktów</div>
                                    </div>
                                    <div style='text-align: center; color: white;'>
                                        <div style='font-size: 32px; font-weight: bold; margin-bottom: 5px;'>{total_distance:.1f}</div>
                                        <div style='font-size: 14px; opacity: 0.9;'>km</div>
                                    </div>
                                    <div style='text-align: center; color: white;'>
                                        <div style='font-size: 32px; font-weight: bold; margin-bottom: 5px;'>{total_hours:.1f}</div>
                                        <div style='font-size: 14px; opacity: 0.9;'>godzin</div>
                                    </div>
                                    <div style='text-align: center; color: white;'>
                                        <div style='font-size: 32px; font-weight: bold; margin-bottom: 5px;'>{energy_kcal:.0f}</div>
                                        <div style='font-size: 14px; opacity: 0.9;'>kcal</div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                        if selected_for_route and len(selected_for_route) >= 2:
                            col_btn1, col_btn2 = st.columns(2)
                        
                            with col_btn1:
                                if st.button("🚀 Optymalizuj trasę (ALEX)", use_container_width=True):
                                    # Prepare data for optimization
                                    base_location = {
                                        "lat": game_state.get("territory_latitude", 49.7271667),
                                        "lng": game_state.get("territory_longitude", 18.7025833)
                                    }
                                
                                    selected_shops = []
                                    for cid in selected_for_route:
                                        if isinstance(cid, str) and cid in filtered_clients:
                                            client = filtered_clients[cid]
                                            selected_shops.append({
                                                "client_id": cid,
                                                "name": client.get("name", cid),
                                                "lat": client.get("latitude", base_location["lat"]),
                                                "lng": client.get("longitude", base_location["lng"])
                                            })
                                
                                    # Optimize route
                                    if selected_shops:
                                        optimized_route, route_distance = optimize_route(base_location, selected_shops)
                                    
                                        # Save to session state
                                        st.session_state.planned_route = optimized_route
                                        st.success(f"✅ Trasa zoptymalizowana ({route_distance:.1f} km)! Kolejność: {' → '.join([filtered_clients[cid]['name'] for cid in optimized_route if isinstance(cid, str) and cid in filtered_clients])}")
                                    else:
                                        st.error("Nie można zoptymalizować trasy - brak poprawnych klientów")
                                    st.rerun()
                        
                            with col_btn2:
                                if st.button("📍 Użyj mojej kolejności", use_container_width=True):
                                    # Use user's selection order
                                    st.session_state.planned_route = selected_for_route
                                    st.success(f"✅ Trasa zapisana! Kolejność: {' → '.join([filtered_clients[cid]['name'] for cid in selected_for_route])}")
                                    st.rerun()
                    
                        elif selected_for_route and len(selected_for_route) == 1:
                            st.warning("⚠️ Zaznacz co najmniej 2 klientów aby zaplanować trasę")
                    
                        # Show current planned route
                        if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                            st.markdown("---")
                            st.markdown("**📍 Aktualna trasa dzienna:**")
                        
                            route_distance = 0
                            base_lat = game_state.get("territory_latitude", 49.7271667)
                            base_lon = game_state.get("territory_longitude", 18.7025833)
                        
                            for i, cid in enumerate(st.session_state.planned_route):
                                if isinstance(cid, str) and cid in filtered_clients:
                                    client = filtered_clients[cid]
                                    st.markdown(f"{i+1}. **{client.get('name')}** ({client.get('distance_from_base', 0):.1f} km od bazy)")
                        
                            if st.button("🗑️ Wyczyść trasę", use_container_width=True):
                                st.session_state.planned_route = []
                                st.rerun()
            
                else:
                    # QUICK START / LIFETIME SCENARIO - Unified structure
                    st.subheader("🗺️ Mój Rejon - Klienci")
                    
                    # =====================================================================
                    # SEKCJA 1: FILTRY I SORTOWANIE
                    # =====================================================================
                    st.markdown("### 🎯 Filtry i sortowanie")
                    
                    col_f1, col_f2, col_f3 = st.columns(3)
                    
                    with col_f1:
                        status_filter = st.multiselect(
                            "Status klienta:",
                            options=['ACTIVE', 'PROSPECT', 'LOST'],
                            default=['ACTIVE', 'PROSPECT'],
                            format_func=lambda x: {
                                'ACTIVE': '✅ Aktywni',
                                'PROSPECT': '🎯 Potencjalni',
                                'LOST': '❌ Utraceni'
                            }[x],
                            key="lifetime_status_filter"
                        )
                    
                    with col_f2:
                        # Placeholder dla innych filtrów
                        st.caption("_Więcej filtrów wkrótce_")
                    
                    with col_f3:
                        sort_by_lifetime = st.selectbox(
                            "Sortuj wg:",
                            ["Dystans ↑", "Potencjał ↓", "Nazwa A-Z", "Reputacja ↓"],
                            key="lifetime_sort"
                        )
                    
                    # Filter and sort clients
                    filtered_clients_lifetime = {
                        cid: client for cid, client in clients.items()
                        if client.get("status", "PROSPECT").upper() in status_filter
                    }
                    
                    # Sort clients
                    sorted_clients_list_lifetime = list(filtered_clients_lifetime.items())
                    
                    if sort_by_lifetime == "Dystans ↑":
                        sorted_clients_list_lifetime.sort(key=lambda x: x[1].get("distance_from_base", x[1].get("distance_km", 999)))
                    elif sort_by_lifetime == "Potencjał ↓":
                        sorted_clients_list_lifetime.sort(key=lambda x: x[1].get("monthly_revenue_potential", 0), reverse=True)
                    elif sort_by_lifetime == "Nazwa A-Z":
                        sorted_clients_list_lifetime.sort(key=lambda x: x[1].get("name", ""))
                    elif sort_by_lifetime == "Reputacja ↓":
                        sorted_clients_list_lifetime.sort(key=lambda x: x[1].get("reputation", 0), reverse=True)
                    
                    filtered_clients_lifetime = dict(sorted_clients_list_lifetime)
                    
                    st.info(f"🔍 Znaleziono: **{len(filtered_clients_lifetime)}** klientów")
                    
                    st.markdown("---")
                    
                    # =====================================================================
                    # SEKCJA 2: LISTA KLIENTÓW (kompaktowa - 10 pierwszych)
                    # =====================================================================
                    st.markdown("### 📋 Lista klientów")
                    
                    for client_id, client_data in list(filtered_clients_lifetime.items())[:10]:
                        name = client_data.get('name', client_id)
                        location = client_data.get('location', 'N/A')
                        owner = client_data.get('owner', 'N/A')
                        reputation = client_data.get('reputation', 50)  # Wartość domyślna 50 (neutralna)
                        potential = client_data.get('monthly_revenue_potential', 0)
                        distance = client_data.get('distance_from_base', client_data.get('distance_km', 0))
                        status = client_data.get("status", "PROSPECT").upper()
                        
                        # Get reputation status
                        rep_status = get_reputation_status(reputation)
                        
                        # Status emoji
                        status_emoji = {"ACTIVE": "✅", "PROSPECT": "🎯", "LOST": "❌"}.get(status, "⚪")
                        
                        # Check if visit overdue
                        overdue_text = ""
                        if status == "ACTIVE" and is_visit_overdue(client_data):
                            days_overdue = (datetime.now() - datetime.fromisoformat(client_data.get('next_visit_due', datetime.now().isoformat()))).days
                            overdue_text = f"⚠️ {days_overdue}d overdue"
                        
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"{status_emoji} **{name}** • {distance:.1f}km • {potential:,}PLN/mc • {rep_status['emoji']} {reputation} {overdue_text}")
                        with col2:
                            if st.button("📞", key=f"visit_quick_lifetime_{client_id}", help="Odwiedź klienta"):
                                st.session_state['show_client_detail'] = True
                                st.session_state['selected_client_id'] = client_id
                                st.rerun()
                    
                    if len(filtered_clients_lifetime) > 10:
                        st.caption(f"... i {len(filtered_clients_lifetime) - 10} więcej klientów (zobacz w tabeli poniżej)")
                    
                    st.markdown("---")
                    
                    # =====================================================================
                    # SEKCJA 3: TABS - MAPA | TABELA
                    # =====================================================================
                    view_tab_map_lt, view_tab_table_lt = st.tabs(["🗺️ Mapa", "📋 Szczegóły (tabela)"])
                    
                    with view_tab_map_lt:
                        st.markdown("**Legenda - status klientów:**")
                        st.caption("🎯 Potencjalni  |  ✅ Aktywni  |  ❌ Utraceni  |  ⭐ W trasie")
                        
                        # Info about clickable map
                        st.info("💡 **Kliknij pin na mapie** aby dodać/usunąć klienta z trasy (max 6)")
                        
                        st.markdown("---")
                        
                        # Create Folium map centered on Piaseczno (centrum - Rynek)
                        base_lat = game_state.get("territory_latitude", 52.0748)
                        base_lon = game_state.get("territory_longitude", 21.0274)
                    
                        m = folium.Map(
                            location=[base_lat, base_lon],
                            zoom_start=12,
                            tiles="OpenStreetMap"
                        )
                    
                        # Add base marker
                        folium.Marker(
                            [base_lat, base_lon],
                            popup=f"🏢 Baza - Piaseczno (centrum)<br>({base_lat:.4f}, {base_lon:.4f})",
                            icon=folium.Icon(color="red", icon="home", prefix="fa"),
                            tooltip=f"Twoja baza (centrum Piaseczna)"
                        ).add_to(m)
                    
                        # Add client markers (only filtered)
                        for client_id, client in filtered_clients_lifetime.items():
                            lat = client.get("latitude", base_lat)
                            lon = client.get("longitude", base_lon)
                            status = client.get("status", "PROSPECT")
                            name = client.get("name", client_id)
                            client_type = client.get("type", "")
                            distance = client.get("distance_from_base", client.get("distance_km", 0))
                        
                            # Check if client is in planned route
                            is_in_route = False
                            route_number = None
                            if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                                if client_id in st.session_state.planned_route:
                                    is_in_route = True
                                    route_number = st.session_state.planned_route.index(client_id) + 1
                        
                            # Status colors
                            if is_in_route:
                                # Highlight clients in today's route
                                color = "purple"
                                icon = "star"
                            elif status == "PROSPECT":
                                color = "blue"
                                icon = "question"
                            elif status == "ACTIVE":
                                color = "green"
                                icon = "check"
                            else:  # LOST
                                color = "red"
                                icon = "times"
                        
                            # Popup content
                            popup_html = f"""
                            <div style='min-width: 200px;'>
                                <h4 style='margin: 0 0 8px 0;'>{name}</h4>
                                {'<p style="color: purple; font-weight: bold;">📍 W dzisiejszej trasie: #' + str(route_number) + '</p>' if is_in_route else ''}
                                <p style='margin: 4px 0;'><b>Typ:</b> {client_type}</p>
                                <p style='margin: 4px 0;'><b>Status:</b> {status}</p>
                                <p style='margin: 4px 0;'><b>Dystans:</b> {distance:.1f} km</p>
                            </div>
                            """
                        
                            # Custom icon with number for route
                            if is_in_route:
                                folium.Marker(
                                    [lat, lon],
                                    popup=folium.Popup(popup_html, max_width=300),
                                    icon=folium.DivIcon(html=f"""
                                        <div style="
                                            background-color: #9333ea;
                                            color: white;
                                            border: 3px solid white;
                                            border-radius: 50%;
                                            width: 32px;
                                            height: 32px;
                                            display: flex;
                                            align-items: center;
                                            justify-content: center;
                                            font-weight: bold;
                                        font-size: 16px;
                                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                                    ">{route_number}</div>
                                """),
                                tooltip=f"{name} - Wizyta #{route_number}"
                            ).add_to(m)
                        else:
                            folium.Marker(
                                [lat, lon],
                                popup=folium.Popup(popup_html, max_width=300),
                                icon=folium.Icon(color=color, icon=icon, prefix="fa"),
                                tooltip=f"{name} ({status})"
                            ).add_to(m)
                    
                    # Draw route line if planned
                    if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                        # Ensure planned_route is a flat list of strings
                        if isinstance(st.session_state.planned_route, list):
                            flat_route = []
                            for item in st.session_state.planned_route:
                                if isinstance(item, str):
                                    flat_route.append(item)
                                elif isinstance(item, list):
                                    flat_route.extend([x for x in item if isinstance(x, str)])
                            st.session_state.planned_route = flat_route
                        
                        # Get selected shops with locations
                        selected_shops = []
                        for cid in st.session_state.planned_route:
                            if isinstance(cid, str) and cid in clients:
                                if cid in filtered_clients_lifetime:
                                    lat = filtered_clients_lifetime[cid].get("latitude", base_lat)
                                    lng = filtered_clients_lifetime[cid].get("longitude", base_lon)
                                else:
                                    lat = clients[cid].get("latitude", base_lat)
                                    lng = clients[cid].get("longitude", base_lon)
                                
                                selected_shops.append({
                                    "client_id": cid,
                                    "lat": lat,
                                    "lng": lng
                                })
                    
                        # Pobierz geometrię trasy podzieloną na wizyt i powrót
                        if selected_shops:
                            route_split = get_route_geometry_split(
                                {"lat": base_lat, "lng": base_lon},
                                selected_shops,
                                st.session_state.planned_route
                            )
                        
                            visits_geometry = route_split.get("visits", [])
                            return_geometry = route_split.get("return", [])
                        else:
                            visits_geometry = []
                            return_geometry = []
                    
                        # Fallback: proste linie jeśli OSRM nie działa
                        if not visits_geometry and st.session_state.planned_route:
                            visits_geometry = [[base_lat, base_lon]]
                            for client_id in st.session_state.planned_route:
                                if isinstance(client_id, str) and client_id in clients:
                                    client = clients[client_id]
                                    visits_geometry.append([
                                        client.get("latitude", base_lat),
                                        client.get("longitude", base_lon)
                                    ])
                    
                        if not return_geometry and st.session_state.planned_route:
                            last_client_id = st.session_state.planned_route[-1]
                            if isinstance(last_client_id, str) and last_client_id in clients:
                                client = clients[last_client_id]
                                return_geometry = [
                                    [client.get("latitude", base_lat), client.get("longitude", base_lon)],
                                    [base_lat, base_lon]
                                ]
                    
                        route_color = "#9333ea" if getattr(st.session_state, 'route_optimized', False) else "#3b82f6"
                        route_label = "✨ Trasa zoptymalizowana" if getattr(st.session_state, 'route_optimized', False) else "📋 Twoja trasa"
                    
                        # Rysuj trasę wizyt (niebieska/fioletowa)
                        if visits_geometry and len(visits_geometry) > 1:
                            folium.PolyLine(
                                visits_geometry,
                                color=route_color,
                                weight=4,
                                opacity=0.8,
                                popup=f"{route_label} (wizyty)",
                                tooltip=f"{route_label} - wizyty po ulicach"
                            ).add_to(m)
                    
                        # Rysuj powrót do bazy (czerwona przerywana)
                        if return_geometry and len(return_geometry) > 1:
                            folium.PolyLine(
                                return_geometry,
                                color="#ef4444",  # Czerwony
                                weight=4,
                                opacity=0.9,
                                dash_array="10, 5",  # Przerywana linia
                                popup="🏠 Powrót do bazy",
                                tooltip="🏠 Powrót do bazy (koniec dnia)"
                            ).add_to(m)
                    
                    # Display interactive map with click handling
                    map_data_lt = st_folium(
                        m, 
                        width=800, 
                        height=400,
                        returned_objects=["last_object_clicked"],
                        key="lifetime_map"
                    )
                    
                    # Handle map clicks - add/remove from route
                    if map_data_lt and map_data_lt.get("last_object_clicked"):
                        clicked = map_data_lt["last_object_clicked"]
                        clicked_lat = clicked.get("lat")
                        clicked_lng = clicked.get("lng")
                        
                        if clicked_lat and clicked_lng:
                            # Find client with matching coordinates
                            for cid, client in filtered_clients_lifetime.items():
                                client_lat = client.get("latitude")
                                client_lng = client.get("longitude")
                                
                                # Check if coordinates match (with small tolerance)
                                if client_lat and client_lng:
                                    if abs(client_lat - clicked_lat) < 0.0001 and abs(client_lng - clicked_lng) < 0.0001:
                                        # Initialize planned_route if not exists
                                        if not hasattr(st.session_state, 'planned_route'):
                                            st.session_state.planned_route = []
                                        
                                        # Toggle client in route
                                        if cid in st.session_state.planned_route:
                                            st.session_state.planned_route.remove(cid)
                                            st.toast(f"🗑️ Usunięto {client.get('name')} z trasy", icon="ℹ️")
                                        else:
                                            if len(st.session_state.planned_route) < 6:
                                                st.session_state.planned_route.append(cid)
                                                st.toast(f"✅ Dodano {client.get('name')} do trasy (#{len(st.session_state.planned_route)})", icon="🎯")
                                            else:
                                                st.toast("⚠️ Maksymalnie 6 klientów w trasie!", icon="⚠️")
                                        
                                        st.rerun()
                                        break
                    
                    # Show current route summary below map
                    if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                        st.markdown("---")
                        st.markdown("**📍 Aktualna trasa (kliknij na mapie aby edytować):**")
                        
                        route_clients = []
                        for i, cid in enumerate(st.session_state.planned_route):
                            if isinstance(cid, str) and cid in clients:
                                client = clients[cid]
                                distance = client.get('distance_from_base', client.get('distance_km', 0))
                                route_clients.append(f"{i+1}. **{client.get('name')}** ({distance:.1f} km)")
                        
                        if route_clients:
                            st.markdown(" → ".join(route_clients))
                            
                            col_clear, col_opt = st.columns(2)
                            with col_clear:
                                if st.button("🗑️ Wyczyść trasę", key="clear_route_from_map_lt"):
                                    st.session_state.planned_route = []
                                    st.session_state.route_optimized = False
                                    st.rerun()
                            with col_opt:
                                if len(st.session_state.planned_route) >= 2:
                                    if st.button("🚀 Optymalizuj (ALEX)", key="optimize_from_map_lt"):
                                        base_location = {
                                            "lat": game_state.get("territory_latitude", 52.0748),
                                            "lng": game_state.get("territory_longitude", 21.0274)
                                        }
                                        selected_shops = []
                                        for cid in st.session_state.planned_route:
                                            if isinstance(cid, str) and cid in clients:
                                                client = clients[cid]
                                                selected_shops.append({
                                                    "client_id": cid,
                                                    "name": client.get("name", cid),
                                                    "lat": client.get("latitude", base_location["lat"]),
                                                    "lng": client.get("longitude", base_location["lng"])
                                                })
                                        optimized_route, route_distance = optimize_route(base_location, selected_shops)
                                        st.session_state.planned_route = optimized_route
                                        st.session_state.route_optimized = True
                                        st.success(f"✅ Trasa zoptymalizowana! Dystans: {route_distance:.1f} km")
                                        st.rerun()
                    
                    with view_tab_table_lt:
                        # Table view with detailed info
                        for client_id, client_data in filtered_clients_lifetime.items():
                            name = client_data.get('name', client_id)
                            location = client_data.get('location', 'N/A')
                            owner = client_data.get('owner', 'N/A')
                            reputation = client_data.get('reputation', 50)  # Wartość domyślna 50 (neutralna)
                            potential = client_data.get('monthly_revenue_potential', 0)
                            distance = client_data.get('distance_from_base', client_data.get('distance_km', 0))
                            status = client_data.get("status", "PROSPECT").upper()
                            
                            # Get reputation status
                            rep_status = get_reputation_status(reputation)
                            
                            # Check if visit overdue
                            overdue_badge = ""
                            if status == "ACTIVE" and is_visit_overdue(client_data):
                                days_overdue = (datetime.now() - datetime.fromisoformat(client_data.get('next_visit_due', datetime.now().isoformat()))).days
                                overdue_badge = f"<span style='background: #fef3c7; color: #d97706; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-left: 8px;'>⚠️ Overdue {days_overdue}d</span>"
                            
                            # Build color-coded card
                            potential_formatted = f"{potential:,}"
                            card_html = f"""<div style='background: linear-gradient(135deg, {rep_status['color']}10 0%, {rep_status['color']}05 100%); border-left: 4px solid {rep_status['color']}; padding: 16px; border-radius: 12px; margin-bottom: 12px;'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                <div style='flex: 1;'>
                    <div style='font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 4px;'>
                        {name} {overdue_badge}
                    </div>
                    <div style='font-size: 13px; color: #64748b; margin-bottom: 8px;'>
                        📍 {location} • 👤 {owner} • 📏 {distance:.1f} km • Status: {status}
                    </div>
                    <div style='display: flex; gap: 12px; align-items: center;'>
                        <div style='background: {rep_status['color']}; color: white; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600;'>
                            {rep_status['emoji']} {reputation} • {rep_status['label']}
                        </div>
                        <div style='color: #64748b; font-size: 13px;'>
                            💰 {potential_formatted} PLN/mc
                        </div>
                    </div>
                </div>
                </div>
            </div>"""
                            
                            st.markdown(card_html, unsafe_allow_html=True)
                            
                            # Action button
                            if st.button(f"📞 Odwiedź {name}", key=f"visit_lifetime_{client_id}", use_container_width=True):
                                st.session_state['show_client_detail'] = True
                                st.session_state['selected_client_id'] = client_id
                                st.rerun()
                    
                    # =====================================================================
                    # SEKCJA 4: PLANOWANIE TRASY (na samym dole)
                    # =====================================================================
                    st.markdown("---")
                    st.markdown("### 🗺️ Planowanie trasy dziennej")
                    
                    with st.expander("📍 Wybierz klientów do odwiedzenia", expanded=False):
                        st.markdown("Wybierz klientów do odwiedzenia w jednej trasie (max 6):")
                    
                        # Multi-select clients for route
                        route_client_options_lt = {
                            cid: f"{client.get('name', cid)} ({client.get('distance_from_base', client.get('distance_km', 0)):.1f} km)"
                            for cid, client in filtered_clients_lifetime.items()
                        }
                    
                        selected_for_route_lt = st.multiselect(
                            "Zaznacz klientów:",
                            options=list(route_client_options_lt.keys()),
                            format_func=lambda x: route_client_options_lt[x],
                            max_selections=6,
                            key="lifetime_route_selection"
                        )
                    
                        if selected_for_route_lt and len(selected_for_route_lt) >= 2:
                            col_btn1, col_btn2 = st.columns(2)
                        
                            with col_btn1:
                                if st.button("🚀 Optymalizuj trasę (ALEX)", use_container_width=True, key="lifetime_optimize_route"):
                                    # Prepare data for optimization
                                    base_location = {
                                        "lat": game_state.get("territory_latitude", 52.0748),
                                        "lng": game_state.get("territory_longitude", 21.0274)
                                    }
                                
                                    selected_shops = []
                                    for cid in selected_for_route_lt:
                                        if isinstance(cid, str) and cid in filtered_clients_lifetime:
                                            client = filtered_clients_lifetime[cid]
                                            selected_shops.append({
                                                "client_id": cid,
                                                "name": client.get("name", cid),
                                                "lat": client.get("latitude", base_location["lat"]),
                                                "lng": client.get("longitude", base_location["lng"])
                                            })
                                
                                    # Optimize route
                                    if selected_shops:
                                        optimized_route, route_distance = optimize_route(base_location, selected_shops)
                                    
                                        # Save to session state
                                        st.session_state.planned_route = optimized_route
                                        st.session_state.route_optimized = True
                                        st.success(f"✅ Trasa zoptymalizowana ({route_distance:.1f} km)! Kolejność: {' → '.join([filtered_clients_lifetime[cid]['name'] for cid in optimized_route if isinstance(cid, str) and cid in filtered_clients_lifetime])}")
                                    else:
                                        st.error("Nie można zoptymalizować trasy - brak poprawnych klientów")
                                    st.rerun()
                        
                            with col_btn2:
                                if st.button("📍 Użyj mojej kolejności", use_container_width=True, key="lifetime_manual_route"):
                                    # Use user's selection order - filter valid clients
                                    valid_route = [cid for cid in selected_for_route_lt if isinstance(cid, str) and cid in filtered_clients_lifetime]
                                    st.session_state.planned_route = valid_route
                                    st.session_state.route_optimized = False
                                    st.success(f"✅ Trasa zapisana! Kolejność: {' → '.join([filtered_clients_lifetime[cid]['name'] for cid in valid_route])}")
                                    st.rerun()
                    
                        elif selected_for_route_lt and len(selected_for_route_lt) == 1:
                            st.warning("⚠️ Zaznacz co najmniej 2 klientów aby zaplanować trasę")
                    
                        # Show current planned route
                        if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                            st.markdown("---")
                            st.markdown("**📍 Aktualna trasa dzienna:**")
                        
                            for i, cid in enumerate(st.session_state.planned_route):
                                if isinstance(cid, str) and cid in clients:
                                    client = clients[cid]
                                    distance = client.get('distance_from_base', client.get('distance_km', 0))
                                    st.markdown(f"{i+1}. **{client.get('name')}** ({distance:.1f} km od bazy)")
                        
                            if st.button("🗑️ Wyczyść trasę", use_container_width=True, key="lifetime_clear_route"):
                                st.session_state.planned_route = []
                                st.session_state.route_optimized = False
                                st.rerun()
    
            # =============================================================================
            # OLD TAB: PRODUKTY - TEMPORARILY DISABLED (code will be migrated to Sprzedaż/Katalog)
            # =============================================================================
            # OLD TAB: PRODUKTY - TEMPORARILY DISABLED (code migrated to Sprzedaż/Katalog)
            # =============================================================================
            # NOTE: This entire section is disabled - content moved to sales_tab_products
    
            if False:  # DISABLED CODE - TO BE MIGRATED
                # Using if False instead of with tab_products to avoid NameError
                pass  # Placeholder - code below will be migrated to sales_tab_products
        
            # =============================================================================
            # OLD TAB: ROZMOWA - TEMPORARILY DISABLED (code migrated to Sprzedaż/Wizyta)
            # =============================================================================
        
        with sales_tab_visit:
            st.subheader("🚗 Wykonaj Wizytę")
            
            # =================================================================
            # ONBOARDING TASKS CHECK - 2 days trial period
            # =================================================================
            
            current_week = game_state.get("current_week", 1)
            tasks_completed = all_tasks_completed(st.session_state)
            pending_tasks = get_pending_tasks_count(st.session_state)
            
            # Trial period: First 2 days (Mon-Tue of week 1)
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            current_day = game_state.get("current_day", "Monday")
            day_index = day_names.index(current_day) if current_day in day_names else 0
            
            is_trial_period = (current_week == 1 and day_index < 2)  # Mon=0, Tue=1
            visits_blocked = not is_trial_period and not tasks_completed
            
            # Show trial period warning
            if is_trial_period and not tasks_completed:
                st.warning(f"""
                ⏰ **Okres próbny: Dzień {day_index + 1}/2**
                
                Masz {2 - day_index} {'dni' if day_index == 0 else 'dzień'} na ukończenie zadań onboardingowych.
                
                📋 Status zadań: **{3 - pending_tasks}/3 ukończone**
                
                💡 Od środy wizyty będą zablokowane do czasu ukończenia wszystkich zadań.
                Przejdź do zakładki Dashboard > Zadania aby je wykonać.
                """)
            
            # Block visits after trial period
            if visits_blocked:
                st.error(f"""
                🚫 **Wizyty zablokowane**
                
                Musisz ukończyć wszystkie zadania onboardingowe przed rozpoczęciem wizyt.
                
                📋 **Nieukończone zadania:** {pending_tasks}/3
                
                💡 Przejdź do zakładki **Dashboard** > **Zadania** i wykonaj:
                - Segmentacja ABC terytorium
                - Plan tygodnia - Routing i klasteryzacja
                - Elevator Pitch - Przedstawienie firmy
                
                ⏱️ Okres próbny (Pn-Wt) zakończony. Czas na profesjonalne podejście!
                """)
                
                if st.button("📋 Przejdź do Dashboard", type="primary", key="goto_dashboard_from_visit"):
                    st.info("⬆️ Kliknij zakładkę **'📊 Dashboard'** powyżej i rozwiń sekcję 'Zadania'")
                
                # Don't show rest of visit UI if blocked
            elif energy_pct < 5:
                st.error("❌ Za mało energii! Zakończ dzień aby zregenerować energię.")
            else:
                # Show congratulations if tasks completed during trial
                if tasks_completed and is_trial_period:
                    st.success("""
                    🎉 **Świetna robota!** Ukończyłeś wszystkie zadania onboardingowe w okresie próbnym.
                    
                    Jesteś gotowy do profesjonalnych wizyt z dobrze zaplanowaną strategią! 🚀
                    """)
                
                # =================================================================
                # VISIT EXECUTION - Follow planned route
                # =================================================================
                
                # Check if route is planned
                if not hasattr(st.session_state, 'planned_route') or not st.session_state.planned_route:
                    st.warning("""
                    📍 **Brak zaplanowanej trasy**
                    
                    Przejdź do zakładki **"🗺️ Klienci & Trasa"** aby:
                    1. Wybrać klientów do odwiedzenia
                    2. Zaplanować optymalną trasę
                    3. Zatwierdzić plan wizyty
                    
                    Potem wróć tutaj aby wykonać wizyty według planu.
                    """)
                else:
                    # Get planned route
                    planned_route = st.session_state.planned_route
                    
                    # Track completed visits today
                    if 'completed_visits_today' not in st.session_state:
                        st.session_state.completed_visits_today = []
                    
                    # Find next client to visit
                    next_client_id = None
                    visit_index = 0
                    
                    for idx, client_id in enumerate(planned_route):
                        if client_id not in st.session_state.completed_visits_today:
                            next_client_id = client_id
                            visit_index = idx
                            break
                    
                    # Show route progress
                    total_visits = len(planned_route)
                    completed_count = len(st.session_state.completed_visits_today)
                    
                    st.markdown(f"""
                    ### 📋 Postęp wizyty: {completed_count}/{total_visits}
                    """)
                    
                    # Progress bar
                    progress = completed_count / total_visits if total_visits > 0 else 0
                    st.progress(progress)
                    
                    st.markdown("---")
                    
                    # Show route overview
                    with st.expander("🗺️ Cała trasa", expanded=False):
                        for idx, cid in enumerate(planned_route):
                            client = clients.get(cid, {})
                            status_icon = "✅" if cid in st.session_state.completed_visits_today else "⏳"
                            current_icon = "👉" if cid == next_client_id else ""
                            
                            st.markdown(f"{current_icon} **{idx + 1}.** {status_icon} {client.get('name', cid)}")
                    
                    st.markdown("---")
                    
                    # All visits completed?
                    if next_client_id is None:
                        st.success("""
                        🎉 **Wszystkie wizyty ukończone!**
                        
                        Wykonałeś wszystkie zaplanowane wizyty na dzisiaj.
                        
                        💡 Możesz:
                        - Zaplanować kolejne wizyty (zakładka Klienci & Trasa)
                        - Zakończyć dzień (przycisk "⏩ ZAKOŃCZ DZIEŃ" na dole strony)
                        """)
                        
                        if st.button("🔄 Wyczyść trasę i zaplanuj nowe wizyty", type="primary"):
                            st.session_state.planned_route = []
                            st.session_state.completed_visits_today = []
                            st.rerun()
                    else:
                        # Show current visit - get client data for panel
                        client = clients.get(next_client_id, {})
                        
                        # Prepare product list for notes
                        all_products = get_all_products()
                        products_list = [
                            {
                                "id": prod_id, 
                                "name": prod.get("name", "Nieznany"),
                                "sku": prod.get("sku", prod_id)
                            } 
                            for prod_id, prod in all_products.items()
                        ]
                        
                        # Prepare client list for notes
                        clients_list = [
                            {
                                "id": client_id,
                                "name": client.get("name", client_id)
                            }
                            for client_id, client in game_state.get("clients", {}).items()
                        ]
                        
                        # Show advanced AI visit panel (zawiera wszystko - nagłówek, info, przyciski, rozmowę, podsumowanie)
                        render_visit_panel_advanced(
                            next_client_id, 
                            clients, 
                            game_state, 
                            username,
                            available_products=products_list,
                            available_clients=clients_list
                        )
            
        # =================================================================
        # ROUTE PLANNING - Multi-select clients + optimization
        with sales_tab_prep:
            st.subheader("💼 Przygotowanie do Wizyt")
            
            st.info("""
            🚧 **Sekcja w budowie**
            
            Tutaj będą dostępne narzędzia Trade-Marketing:
            - 🎁 Planowanie promocji
            - 📊 Analiza konkurencji
            - 💰 Kalkulator marży
            - 📋 Materiały POS
            """)
            
            st.markdown("---")
            
            # =============================================================================
            # NOTATNIK - dostępny podczas przygotowania do wizyt
            # =============================================================================
            
            with st.expander("📝 Notatnik", expanded=False):
                st.markdown("""
                **Twoje notatki, pomysły i obserwacje**
                
                Zapisuj tutaj:
                - 📝 Pomysły na promocje
                - 💡 Obserwacje z rynku
                - 🎯 Plany działań
                - 📊 Analizy konkurencji
                """)
                
                # Get user data for notes
                from data.users_new import get_current_user_data
                from utils.user_helpers import get_user_sql_id
                user_data = get_current_user_data(username)
                
                if user_data and "user_id" in user_data:
                    # Get INTEGER user id from SQL (for notes foreign key)
                    sql_user_id = get_user_sql_id(username)
                    
                    if not sql_user_id:
                        st.warning(f"⚠️ Nie można załadować notatek - użytkownik '{username}' nie istnieje w bazie SQL")
                        st.caption("💡 Tylko użytkownicy z bazy SQL mogą używać notatnika. Skontaktuj się z administratorem.")
                    else:
                        # Prepare product list for notes
                        all_products = get_all_products()
                        products_list = [
                            {
                                "id": prod_id, 
                                "name": prod.get("name", "Nieznany"),
                                "sku": prod.get("sku", prod_id)
                            } 
                            for prod_id, prod in all_products.items()
                        ]
                        
                        # Prepare client list for notes
                        clients_list = [
                            {
                                "id": client_id,
                                "name": client.get("name", client_id)
                            }
                            for client_id, client in game_state.get("clients", {}).items()
                        ]
                        
                        # Render notes panel with unique key prefix and products/clients
                        render_notes_panel(
                            user_id=sql_user_id,  # INTEGER PRIMARY KEY z tabeli users
                            active_tab="product_card",
                            key_prefix="fmcg_sales_prep_notes",
                            available_products=products_list,
                            available_clients=clients_list
                        )
                else:
                    st.warning("⚠️ Nie można załadować notatek")
            
            st.markdown("---")
            st.markdown("💡 **Wskazówka**: Katalog produktów znajdziesz w zakładce **'📦 Produkty'**")
        
        # =========================================================================
        # SUB-TAB: PRODUKTY  
        # =========================================================================
        
        with sales_tab_products:
        
            # Dynamic header based on scenario
            if is_heinz_scenario:
                st.subheader("🍅 Portfolio Ketchupów Heinz")
                st.info("📋 **Scenariusz Heinz**: Koncentrujemy się wyłącznie na kategorii ketchupów (4 SKU)")
            else:
                st.subheader("📦 Katalog Produktów")
        
            # Filters (only show for non-Heinz scenarios)
            if not is_heinz_scenario:
                col_f1, col_f2, col_f3 = st.columns([2, 2, 3])
            
                with col_f1:
                    brand_filter = st.selectbox(
                        "Marka:",
                        ["Wszystkie", "FreshLife", "Konkurencja"]
                    )
            
                with col_f2:
                    categories = ["Wszystkie"] + list(set(
                        p["category"] for p in list(FRESHLIFE_PRODUCTS.values()) + list(COMPETITOR_PRODUCTS.values())
                    ))
                    category_filter = st.selectbox(
                        "Kategoria:",
                        categories
                    )
            
                with col_f3:
                    search_query = st.text_input(
                        "🔍 Szukaj produktu:",
                        placeholder="np. szampon, mleko, mydło..."
                    )
            
                st.markdown("---")
        
            # Get products based on scenario
            if is_heinz_scenario:
                # ONLY KETCHUPS for Heinz scenario
                heinz_ketchup_ids = [
                    "heinz_ketchup_classic",
                    "heinz_ketchup_hot",
                    "pudliszki_ketchup_lagodny",
                    "pudliszki_ketchup_ostry"
                ]
                all_products = {k: v for k, v in get_all_products().items() if k in heinz_ketchup_ids}
            else:
                # All products for other scenarios
                all_products = get_all_products()
        
            # Filter products (only for non-Heinz scenarios)
            if is_heinz_scenario:
                # All 4 ketchups are already filtered
                filtered_products = list(all_products.values())
            else:
                # Apply filters for full product catalog
                filtered_products = []
                for product in all_products.values():
                    # Brand filter
                    if brand_filter == "FreshLife" and product["brand"] != "FreshLife":
                        continue
                    elif brand_filter == "Konkurencja" and product["brand"] == "FreshLife":
                        continue
                
                    # Category filter
                    if category_filter != "Wszystkie" and product["category"] != category_filter:
                        continue
                
                    # Search filter
                    if search_query:
                        search_lower = search_query.lower()
                        if not (search_lower in product["name"].lower() or 
                               search_lower in product["brand"].lower() or
                               search_lower in product["category"].lower()):
                            continue
                
                    filtered_products.append(product)
        
            # Display count
            if is_heinz_scenario:
                st.success(f"🍅 **{len(filtered_products)} ketchupy** w portfolio Heinz")
            else:
                st.info(f"📊 Znaleziono **{len(filtered_products)}** produktów")
        
            # Display products in grid (2 columns)
            for i in range(0, len(filtered_products), 2):
                col1, col2 = st.columns(2)
            
                for idx, col in enumerate([col1, col2]):
                    if i + idx < len(filtered_products):
                        product = filtered_products[i + idx]
                    
                        with col:
                            # Get emoji based on category/subcategory
                            emoji_map = {
                                "Personal Care": {
                                    "Żele pod prysznic": "🚿",
                                    "Szampony": "💆",
                                    "Mydła": "🧼",
                                    "Dezodoranty": "💨",
                                    "Pasty do zębów": "🦷",
                                    "default": "🧴"
                                },
                                "Food": {
                                    "Mleko": "🥛",
                                    "Jogurty": "🥛",
                                    "Sery": "🧀",
                                    "Masło": "🧈",
                                    "Płatki śniadaniowe": "🥣",
                                    "Zupy instant": "🍜",
                                    "Ketchupy i sosy": "🍅",
                                    "Oleje spożywcze": "🫒",
                                    "default": "�"
                                },
                                "Home Care": {
                                    "Środki czystości": "🧽",
                                    "Płyny do mycia podłóg": "🧹",
                                    "Płyny do naczyń": "🍽️",
                                    "Proszki do prania": "🧺",
                                    "Odświeżacze powietrza": "🌸",
                                    "default": "🧽"
                                },
                                "Snacks": {
                                    "Chipsy": "🥔",
                                    "Ciastka": "🍪",
                                    "Czekolady": "🍫",
                                    "Orzechy i bakalie": "🥜",
                                    "Batony": "🍫",
                                    "default": "�"
                                },
                                "Beverages": {
                                    "Soki": "🧃",
                                    "Napoje gazowane": "🥤",
                                    "Woda": "💧",
                                    "Herbaty mrożone": "🍵",
                                    "Napoje energetyczne": "⚡",
                                    "default": "🥤"
                                }
                            }
                        
                            category = product.get("category", "")
                            subcategory = product.get("subcategory", "")
                        
                            if category in emoji_map:
                                product_emoji = emoji_map[category].get(subcategory, emoji_map[category]["default"])
                            else:
                                product_emoji = "📦"
                        
                            # Card styling
                            is_freshlife = product["brand"] == "FreshLife"
                            border_color = "#10b981" if is_freshlife else "#94a3b8"
                            bg_color = "#f0fdf4" if is_freshlife else "#f8fafc"
                        
                            # Popularity bar (with fallback for products without popularity field)
                            popularity = product.get("popularity", 50)
                            pop_color = "#10b981" if popularity >= 70 else "#f59e0b" if popularity >= 40 else "#ef4444"
                        
                            # Get margin and price with backward compatibility
                            margin_percent, margin_pln = _get_product_margin(product)
                            price = _get_product_price(product)
                        
                            # Use container for card
                            with st.container():
                                st.markdown(f"""
                                <div style="background: {bg_color}; padding: 20px; border-radius: 12px; border: 2px solid {border_color}; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 16px;">
                                    <div style="text-align: center; font-size: 48px; margin-bottom: 12px;">{product_emoji}</div>
                                    <div style="font-weight: 700; font-size: 16px; color: #1e293b; margin-bottom: 4px; text-align: center;">{product['name']}</div>
                                    <div style="font-size: 12px; color: #64748b; margin-bottom: 12px; text-align: center;">{product['brand']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                                # Metrics in white box
                                st.markdown(f"""
                                <div style="background: white; padding: 12px; border-radius: 8px; margin: -8px 0 12px 0;">
                                    <div style="margin-bottom: 8px;">
                                        <span style="color: #64748b; font-size: 13px;">Cena: </span>
                                        <span style="font-weight: 700; color: #1e293b; font-size: 14px;">{price:.2f} PLN</span>
                                    </div>
                                    <div style="margin-bottom: 8px;">
                                        <span style="color: #64748b; font-size: 13px;">Marża: </span>
                                        <span style="font-weight: 700; color: #10b981; font-size: 14px;">{margin_percent}%</span>
                                    </div>
                                    <div style="margin-top: 12px;">
                                        <div style="color: #64748b; font-size: 11px; margin-bottom: 4px;">Popularność:</div>
                                        <div style="background: #e2e8f0; border-radius: 4px; height: 8px; overflow: hidden;">
                                            <div style="background: {pop_color}; height: 100%; width: {popularity}%;"></div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                                st.markdown(f"""
                                <div style="text-align: center; padding: 8px; background: rgba(255,255,255,0.7); border-radius: 6px; font-size: 11px; color: #64748b; margin-bottom: 12px;">
                                    {product['category']}
                                </div>
                                """, unsafe_allow_html=True)
                        
                            # Details button (for all products, but especially useful for FreshLife)
                            if st.button(f"ℹ️ Szczegóły", key=f"details_{product['id']}", use_container_width=True):
                                st.session_state[f"show_product_details_{product['id']}"] = True
                        
                            # Show product details modal
                            if st.session_state.get(f"show_product_details_{product['id']}", False):
                                with st.expander("📦 Szczegóły produktu", expanded=True):
                                    _render_product_details(product, scenario_id)
                                
                                    if st.button("✖️ Zamknij", key=f"close_{product['id']}"):
                                        st.session_state[f"show_product_details_{product['id']}"] = False
                                        st.rerun()
                    # TODO: Przenieść kod z tab_products
    
            # =============================================================================
            # STARE ZAKŁADKI - DO USUNIĘCIA PO MIGRACJI
            # =============================================================================
    
            # Tymczasowo zostawiamy stare zakładki żeby gra działała
            # Będziemy stopniowo przenosić kod do nowych sub-tabów
    
            # TAB: HISTORIA (przeniesione do Dashboard jako expandable - można usunąć poniższy kod)
            if False:  # Wyłączone - kod już w Dashboard
                with st.container():
                    st.subheader("📈 Historia Wizyt i Statystyki")
        
                # Get visit history
                visit_history = game_state.get("visit_history", [])
        
                if not visit_history:
                    st.info("""
                    📭 **Brak historii wizyt**
            
                    Wykonaj swoją pierwszą wizytę aby zobaczyć statystyki!
                    """)
                else:
                    # Summary metrics
                    st.markdown("### 📊 Podsumowanie")
            
                    total_visits = len(visit_history)
                    total_sales = sum(v.get("order_value", 0) for v in visit_history)
                    total_margin = sum(v.get("order_margin", 0) for v in visit_history)
                    avg_order = total_sales / max(total_visits, 1)
            
                    # Count successful visits (quality >= 3)
                    successful_visits = sum(1 for v in visit_history if v.get("quality", 0) >= 3)
                    win_rate = (successful_visits / total_visits * 100) if total_visits > 0 else 0
            
                    col_h1, col_h2, col_h3, col_h4 = st.columns(4)
            
                    with col_h1:
                        st.metric("📞 Wszystkie wizyty", total_visits)
            
                    with col_h2:
                        st.metric("💰 Łączna sprzedaż", f"{total_sales:,} PLN")
            
                    with col_h3:
                        st.metric("📊 Średnie zamówienie", f"{avg_order:,.0f} PLN")
            
                    with col_h4:
                        st.metric("✅ Win Rate", f"{win_rate:.0f}%")
                        st.caption(f"{successful_visits}/{total_visits} wizyt (3⭐+)")
            
                    st.markdown("---")
            
                    # WEEKLY PERFORMANCE HISTORY
                    st.markdown("### 📅 Historia Tygodniowa")
            
                    weekly_history = game_state.get("weekly_history", [])
                    weekly_best = game_state.get("weekly_best_sales", 0)
                    current_streak = game_state.get("weekly_streak", 0)
            
                    if weekly_history:
                        # Show last 4 weeks
                        recent_weeks = weekly_history[-4:]
                
                        # Performance cards
                        week_cols = st.columns(len(recent_weeks))
                
                        for idx, week_data in enumerate(recent_weeks):
                            with week_cols[idx]:
                                week_num = week_data.get("week", idx + 1)
                                sales = week_data.get("sales", 0)
                                visits = week_data.get("visits", 0)
                                achieved = week_data.get("target_achieved", False)
                                target = week_data.get("target_sales", 8000)
                        
                                # Color based on achievement
                                if achieved:
                                    card_color = "#22c55e"
                                    card_emoji = "✅"
                                elif sales >= target * 0.75:
                                    card_color = "#eab308"
                                    card_emoji = "🥈"
                                else:
                                    card_color = "#ef4444"
                                    card_emoji = "📊"
                        
                                # Extract values
                                sales_fmt = f"{sales:,}"
                                card_color_grad1 = f"{card_color}15"
                                card_color_grad2 = f"{card_color}05"
                        
                                # Build card
                                week_card = f"""<div style="border: 2px solid {card_color}; border-radius: 8px; padding: 12px; background: linear-gradient(135deg, {card_color_grad1} 0%, {card_color_grad2} 100%); text-align: center; margin-bottom: 8px;">
    <div style="font-size: 24px; margin-bottom: 4px;">{card_emoji}</div>
    <div style="font-weight: 700; color: #1f2937; margin-bottom: 4px;">Tydzień {week_num}</div>
    <div style="font-size: 20px; font-weight: 700; color: {card_color};">{sales_fmt} PLN</div>
    <div style="font-size: 12px; color: #6b7280; margin-top: 4px;">{visits} wizyt</div>
    </div>"""
                                st.markdown(week_card, unsafe_allow_html=True)
                
                        # Stats summary
                        col_ws1, col_ws2, col_ws3 = st.columns(3)
                
                        with col_ws1:
                            st.metric("🏆 Najlepszy tydzień", f"{weekly_best:,} PLN")
                
                        with col_ws2:
                            total_weeks = len(weekly_history)
                            achieved_weeks = sum(1 for w in weekly_history if w.get("target_achieved", False))
                            achievement_rate = (achieved_weeks / total_weeks * 100) if total_weeks > 0 else 0
                            st.metric("✅ Osiągnięte cele", f"{achievement_rate:.0f}%")
                            st.caption(f"{achieved_weeks}/{total_weeks} tygodni")
                
                        with col_ws3:
                            st.metric("🔥 Aktualna seria", f"{current_streak}")
                            st.caption("tygodni z rzędu")
                    else:
                        st.info("📭 Brak historii tygodniowej. Zakończ pierwszy tydzień!")
            
                    st.markdown("---")
            
                    # Quality distribution
                    st.markdown("### ⭐ Jakość wizyt")
            
                    quality_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                    for visit in visit_history:
                        quality = visit.get("quality", 3)
                        quality_counts[quality] = quality_counts.get(quality, 0) + 1
            
                    col_q1, col_q2, col_q3, col_q4, col_q5 = st.columns(5)
            
                    quality_labels = {
                        1: ("1⭐", "❌", "#ef4444"),
                        2: ("2⭐", "⚠️", "#f97316"),
                        3: ("3⭐", "😐", "#eab308"),
                        4: ("4⭐", "😊", "#22c55e"),
                        5: ("5⭐", "🏆", "#3b82f6")
                    }
            
                    for idx, (col, quality) in enumerate(zip([col_q1, col_q2, col_q3, col_q4, col_q5], [1, 2, 3, 4, 5]), 1):
                        with col:
                            label, emoji, color = quality_labels[quality]
                            count = quality_counts[quality]
                            pct = (count / total_visits * 100) if total_visits > 0 else 0
                    
                            # Extract values
                            pct_fmt = f"{pct:.0f}"
                            color_bg = f"{color}15"
                    
                            st.markdown(f"""<div style='background: {color_bg}; border: 2px solid {color}; border-radius: 12px; padding: 16px; text-align: center;'>
    <div style='font-size: 32px; margin-bottom: 8px;'>{emoji}</div>
    <div style='font-size: 18px; font-weight: 700; color: {color};'>{count}</div>
    <div style='font-size: 12px; color: #64748b;'>{pct_fmt}%</div>
    <div style='font-size: 11px; color: #94a3b8; margin-top: 4px;'>{label}</div>
    </div>""", unsafe_allow_html=True)
            
                    st.markdown("---")
            
                    # Recent visits table
                    st.markdown("### 📜 Ostatnie wizyty")
            
                    # Show last 10 visits
                    recent_visits = sorted(visit_history, key=lambda v: v.get("date", ""), reverse=True)[:10]
            
                    for visit in recent_visits:
                        client_id = visit.get("client_id", "")
                        client_name = clients.get(client_id, {}).get("name", client_id)
                        date = visit.get("date", "N/A")
                        quality = visit.get("quality", 0)
                        order_value = visit.get("order_value", 0)
                        order_margin = visit.get("order_margin", 0)
                        impression = visit.get("customer_impression", "neutralne")
                
                        # Quality stars
                        stars = "⭐" * quality
                
                        # Impression color
                        impression_config = {
                            "pozytywne": ("😊", "#22c55e"),
                            "neutralne": ("😐", "#eab308"),
                            "negatywne": ("😞", "#ef4444")
                        }
                        impression_emoji, impression_color = impression_config.get(impression, ("😐", "#eab308"))
                
                        # Build visit card
                        visit_card_html = f"""<div style='background: white; border: 1px solid #e2e8f0; border-left: 4px solid {impression_color}; border-radius: 12px; padding: 16px; margin-bottom: 12px;'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                <div style='flex: 1;'>
                    <div style='font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 4px;'>
                        {client_name}
                    </div>
                    <div style='font-size: 13px; color: #64748b; margin-bottom: 8px;'>
                        📅 {date} • {stars} • {impression_emoji} {impression}
                    </div>
                    <div style='display: flex; gap: 16px; font-size: 13px;'>
                        <div>💰 <strong>{order_value:,} PLN</strong></div>
                        <div>📈 Marża: <strong>{order_margin:,} PLN</strong></div>
                    </div>
                </div>
                <div>
                    <button onclick="alert('Szczegóły wizyty - TODO')" style='background: #f1f5f9; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 12px; color: #64748b;'>
                        📋 Szczegóły
                    </button>
                </div>
            </div>
    </div>"""
                
                        st.markdown(visit_card_html, unsafe_allow_html=True)
            
                    if len(visit_history) > 10:
                        st.caption(f"Pokazano 10 z {len(visit_history)} wizyt")
    
            # =============================================================================
    # OLD TAB: ZADANIA - DISABLED (moved to Dashboard expandable section)
    # =============================================================================
    
    if False:  # Wyłączone - kod przeniesiony do Dashboard
            with st.container():  # Zmieniono z tab_tasks
                st.subheader("📋 Zadania onboardingowe")
        
            # Trial period info
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            current_day = game_state.get("current_day", "Monday")
            current_week = game_state.get("current_week", 1)
            day_index = day_names.index(current_day) if current_day in day_names else 0
            is_trial = (current_week == 1 and day_index < 2)
        
            if is_trial and not all_tasks_completed(st.session_state):
                st.info(f"""
                ⏰ **Okres próbny: Dzień {day_index + 1}/2**
            
                Masz {2 - day_index} {'dni' if day_index == 0 else 'dzień'} na ukończenie zadań.
                Od środy wizyty będą zablokowane do czasu ukończenia wszystkich zadań!
                """)
            elif not is_trial and not all_tasks_completed(st.session_state):
                st.error("""
                🚫 **Uwaga!** Wizyty są zablokowane do czasu ukończenia wszystkich zadań.
            
                Ukończ poniższe zadania aby móc kontynuować grę.
                """)
        
            # Wyświetl feedback z ostatniego AI evaluation (jeśli istnieje)
            if 'last_task_feedback' in st.session_state:
                feedback_data = st.session_state['last_task_feedback']
            
                if feedback_data['is_accepted']:
                    st.success("🎉 **Zadanie zaakceptowane przez AI!**")
                    st.balloons()
                else:
                    st.warning("⚠️ **AI wymaga poprawek**")
            
                # Pokaż feedback
                with st.expander("📝 **Feedback od AI**", expanded=True):
                    st.markdown(feedback_data['feedback'])
                    if not feedback_data['is_accepted']:
                        st.info("💡 Możesz edytować i wysłać ponownie w rozwiniętym zadaniu poniżej.")
            
                # Usuń z session_state żeby nie pokazywać ponownie
                del st.session_state['last_task_feedback']
        
            # Sprawdź czy wszystkie zadania ukończone
            if all_tasks_completed(st.session_state):
                st.success("🎉 **Gratulacje! Ukończyłeś wszystkie zadania onboardingowe!**")
                st.markdown("Możesz teraz swobodnie korzystać ze wszystkich funkcji gry.")
                st.markdown("---")
                st.info("💡 **Tip:** Wróć do artykułów w zakładce 📚 Inspiracje, jeśli potrzebujesz odświeżyć wiedzę.")
            else:
                pending = get_pending_tasks_count(st.session_state)
                st.info(f"📌 **Zadań do ukończenia: {pending}/3**")
                st.markdown("""
                Te zadania pomogą Ci rozpocząć grę z solidnym planem. Wykonaj je po kolei, 
                korzystając z materiałów edukacyjnych w zakładce **📚 Inspiracje**.
                """)
        
            st.markdown("---")
        
            # Wyświetl zadania w kolejności
            sorted_tasks = sorted(ONBOARDING_TASKS.values(), key=lambda x: x["order"])
        
            for task in sorted_tasks:
                task_id = task["id"]
                status = get_task_status(st.session_state, task_id)
            
                # Ikona statusu
                if status["status"] == "completed":
                    status_icon = "✅"
                    status_text = "Ukończone"
                    status_color = "#10b981"
                elif status["status"] == "submitted":
                    status_icon = "⏳"
                    status_text = "Wysłane - czeka na akceptację"
                    status_color = "#f59e0b"
                else:
                    status_icon = "⭕"
                    status_text = "Do wykonania"
                    status_color = "#94a3b8"
            
                # Expander dla zadania
                with st.expander(f"{status_icon} **{task['title']}** ({status_text})", 
                               expanded=(status["status"] == "not_started")):
                
                    # Opis zadania
                    st.markdown(task["description"])
                
                    # Link do artykułu
                    st.info(f"📖 **Materiał pomocny:** {task['required_article']}")
                
                    # Kryteria sukcesu
                    with st.expander("🎯 Kryteria oceny"):
                        for criterion in task["success_criteria"]:
                            st.markdown(f"- {criterion}")
                
                    st.markdown("---")
                
                    # Jeśli ukończone - pokaż feedback
                    if status["status"] == "completed":
                        st.success("✅ **Zadanie ukończone!**")
                        if status["feedback"]:
                            st.markdown(status["feedback"])
                
                    # Jeśli wysłane - pokaż submission i opcję ponownego wysłania
                    elif status["status"] == "submitted":
                        st.warning("⏳ **Zadanie wysłane. Poniżej możesz je edytować i wysłać ponownie.**")
                    
                        # Pokaż poprzednie zgłoszenie
                        with st.expander("📄 Twoje zgłoszenie"):
                            st.text(status["submission"])
                    
                        # Formularz do edycji
                        with st.form(f"edit_task_{task_id}"):
                            edited_submission = st.text_area(
                                "Edytuj zgłoszenie:",
                                value=status["submission"],
                                height=300,
                                placeholder=task["placeholder"]
                            )
                        
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                if st.form_submit_button("💾 Zapisz poprawki", use_container_width=True):
                                    submit_task(st.session_state, task_id, edited_submission)
                                    st.success("✅ Zapisano poprawki!")
                                    st.rerun()
                        
                            with col2:
                                if st.form_submit_button("✅ Wyślij do akceptacji", use_container_width=True):
                                    # Generuj feedback
                                    feedback = get_static_feedback(task_id, edited_submission)
                                
                                    # Sprawdź czy feedback jest pozytywny (zawiera ✅ na początku)
                                    if feedback.strip().startswith("✅"):
                                        complete_task(st.session_state, task_id, feedback)
                                        st.success("🎉 Zadanie zaakceptowane!")
                                    else:
                                        # Zapisz jako submitted ale nie complete
                                        submit_task(st.session_state, task_id, edited_submission)
                                        st.warning("⚠️ Zadanie wymaga poprawek. Zobacz feedback poniżej:")
                                        st.markdown(feedback)
                                
                                    st.rerun()
                
                    # Jeśli nie rozpoczęte - pokaż formularz
                    else:
                        with st.form(f"submit_task_{task_id}"):
                            submission_text = st.text_area(
                                "Twoja odpowiedź:",
                                height=300,
                                placeholder=task["placeholder"],
                                key=f"task_input_{task_id}"
                            )
                        
                            submitted = st.form_submit_button("📤 Wyślij zadanie", use_container_width=True)
                        
                            if submitted:
                                if not submission_text or len(submission_text.strip()) < 20:
                                    st.error("⚠️ Odpowiedź jest za krótka. Napisz co najmniej 20 znaków.")
                                else:
                                    # Zapisz submission PRZED AI evaluation
                                    submit_task(st.session_state, task_id, submission_text)
                                
                                    # AI Evaluation (używa Gemini 2.0 Flash)
                                    with st.spinner("🤖 AI analizuje Twoje zgłoszenie..."):
                                        feedback, is_accepted = evaluate_task_with_ai(
                                            task_id=task_id,
                                            submission_text=submission_text,
                                            task_data=task
                                        )
                                
                                    # Zapisz feedback do session_state żeby pokazać po rerun
                                    st.session_state['last_task_feedback'] = {
                                        'task_id': task_id,
                                        'feedback': feedback,
                                        'is_accepted': is_accepted
                                    }
                                
                                    # Handle decision
                                    if is_accepted:
                                        complete_task(st.session_state, task_id, feedback)
                                
                                    st.rerun()
        
            # Podsumowanie na końcu
            st.markdown("---")
            if all_tasks_completed(st.session_state):
                st.success("""
                ### 🎉 Świetna robota!
            
                Ukończyłeś wszystkie zadania onboardingowe. Teraz:
                - ✅ Masz plan terytorium (segmentacja ABC)
                - ✅ Znasz swoją trasówkę (routing)
                - ✅ Przygotowałeś elevator pitch
            
                **Możesz rozpocząć wizyty u klientów!** 🚀
                """)
            else:
                st.info(f"""
                💡 **Status:** {3 - pending}/3 zadań ukończonych
            
                Po ukończeniu wszystkich zadań będziesz gotowy do efektywnej pracy w terenie!
                """)
    
    # =============================================================================
    # OLD TAB: KLIENCI - TEMPORARILY DISABLED (code will be migrated to Sprzedaż/Mapa)
    # =============================================================================
    # NOTE: This entire section is disabled - content moved to sales_tab_map
    
    if False:  # DISABLED CODE - TO BE MIGRATED
        
            st.markdown("---")
            st.subheader("⏭️ Koniec Dnia")
    
            # Show urgent visits
            urgent_clients = get_clients_needing_visit(clients, urgent_threshold_days=10)
            if urgent_clients:
                st.warning(f"⚠️ Pilne wizyty: {len(urgent_clients)} klientów wymaga wizyty!")
                with st.expander("Zobacz listę pilnych wizyt"):
                    for client_id in urgent_clients:
                        client = clients[client_id]
                        st.write(f"- {client['name']} ({client.get('distance_from_base', 0):.1f} km)")
        
            if st.button("⏭️ Zakończ dzień", type="secondary"):
                with st.spinner("Przechodzenie do następnego dnia..."):
                    try:
                        # Calculate return to base cost if player is away
                        if game_state.get("current_location") is not None:
                            current_loc = game_state["current_location"]
                            base_loc = {
                                "lat": game_state.get("territory_latitude", 52.0846),
                                "lng": game_state.get("territory_longitude", 21.0250)
                            }
                        
                            return_distance = calculate_distance_between_points(
                                current_loc["lat"], current_loc["lng"],
                                base_loc["lat"], base_loc["lng"]
                            )
                        
                            return_energy = int(return_distance * 0.5)  # Return to base costs 50% less
                        
                            # Deduct return energy
                            game_state["energy"] = max(0, game_state.get("energy", 100) - return_energy)
                            game_state["total_distance_today"] = game_state.get("total_distance_today", 0) + return_distance
                        
                            st.info(f"🚗 Powrót do bazy: {return_distance:.1f} km (-{return_energy}% energii)")
                    
                        # Reset route tracking for next day
                        game_state["current_location"] = None
                        game_state["planned_visits_today"] = []
                        game_state["completed_visits_today"] = []
                        game_state["total_distance_today"] = 0.0
                        game_state["route_optimization_used"] = False
                    
                        # Clear session state route planning
                        if hasattr(st.session_state, 'planned_route'):
                            del st.session_state.planned_route
                        if hasattr(st.session_state, 'current_visit_idx'):
                            del st.session_state.current_visit_idx
                        if hasattr(st.session_state, 'route_optimized'):
                            del st.session_state.route_optimized
                    
                        # Advance day
                        updated_game_state, updated_clients = advance_day(game_state, clients)
                    
                        # Update references
                        game_state = updated_game_state
                        clients = updated_clients
                    
                        # Save to SQL and session state
                        update_fmcg_game_state_sql(username, game_state, clients)
                        st.session_state["fmcg_game_state"] = game_state
                        st.session_state["fmcg_clients"] = clients
                    
                        st.success(f"✅ Nowy dzień: {game_state['current_day']}")
                        st.info("⚡ Energia zregenerowana do 100%!")
                    
                        # WEEKLY SUMMARY - Display if new week started
                        if "last_week_summary" in game_state:
                            summary = game_state["last_week_summary"]
                        
                            # Determine medal/status
                            if summary["target_achieved"]:
                                medal_emoji = "🏆"
                                medal_color = "#22c55e"
                                status_msg = "GRATULACJE! Cel tygodniowy osiągnięty!"
                            elif summary["sales"] >= summary.get("target_sales", 8000) * 0.75:
                                medal_emoji = "🥈"
                                medal_color = "#eab308"
                                status_msg = "Blisko! Następnym razem uda się osiągnąć cel."
                            else:
                                medal_emoji = "📊"
                                medal_color = "#f97316"
                                status_msg = "Wyzwanie na następny tydzień: więcej wizyt!"
                        
                            # Extract all values
                            week_num = summary['week']
                            sales_value = summary['sales']
                            sales_fmt = f"{sales_value:,}"
                            target_sales = summary.get('target_sales', 8000)
                            target_sales_fmt = f"{target_sales:,}"
                            visits_value = summary['visits']
                            target_visits = summary.get('target_visits', 6)
                            streak_value = summary.get('streak', 0)
                            medal_color_grad1 = f"{medal_color}20"
                            medal_color_grad2 = f"{medal_color}05"
                        
                            summary_html = f"""<div style="border: 3px solid {medal_color}; border-radius: 16px; padding: 24px; background: linear-gradient(135deg, {medal_color_grad1} 0%, {medal_color_grad2} 100%); margin: 20px 0; text-align: center;">
    <h2 style="margin: 0 0 10px 0; color: #1f2937;">
    {medal_emoji} Podsumowanie Tygodnia {week_num}
    </h2>
    <div style="background: {medal_color}; color: white; padding: 12px 24px; border-radius: 24px; font-weight: 700; font-size: 18px; margin: 16px auto; display: inline-block;">
    {status_msg}
    </div>
    <div style="display: flex; justify-content: space-around; margin-top: 24px; flex-wrap: wrap; gap: 16px;">
    <div style="flex: 1; min-width: 150px;">
    <div style="font-size: 32px; font-weight: 700; color: {medal_color};">
    {sales_fmt} PLN
    </div>
    <div style="color: #6b7280; font-size: 14px; margin-top: 4px;">
    Sprzedaż (cel: {target_sales_fmt})
    </div>
    </div>
    <div style="flex: 1; min-width: 150px;">
    <div style="font-size: 32px; font-weight: 700; color: #6b7280;">
    {visits_value}
    </div>
    <div style="color: #6b7280; font-size: 14px; margin-top: 4px;">
    Wizyt (cel: {target_visits})
    </div>
    </div>
    <div style="flex: 1; min-width: 150px;">
    <div style="font-size: 32px; font-weight: 700; color: #3b82f6;">
    {streak_value}
    </div>
    <div style="color: #6b7280; font-size: 14px; margin-top: 4px;">
    🔥 Seria tygodni
    </div>
    </div>
    </div>
    </div>"""
                        
                            st.markdown(summary_html, unsafe_allow_html=True)
                        
                            # Clear summary after displaying
                            del game_state["last_week_summary"]
                            update_fmcg_game_state_sql(username, game_state, clients)
                    
                        # Rerun to refresh UI
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Błąd podczas przechodzenia do następnego dnia: {e}")
    
    # =============================================================================
    # TAB: NOTATNIK (Notes Panel)
    # =============================================================================
    
    # =============================================================================
    # TAB: NOTATNIK - PRZENIESIONY DO DASHBOARD → ZADANIA
    # =============================================================================
    # Notatnik został przeniesiony do Dashboard → Zadania & Rozwój (pełny notatnik)
    # Quick notes są dostępne w sidebarze (implementacja w main.py)
    
    # =============================================================================
    # TAB: HR & TEAM (Human Resources - Rozwój i Wsparcie)
    # =============================================================================
    
    with tab_hr:
        st.markdown("## 👥 HR - Rozwój i Wsparcie")
        st.markdown("Centrum rozwoju kariery, szkoleń i wsparcia w pracy Product Handlera")
        
        # HR Sub-tabs
        hr_tab_alex, hr_tab_career, hr_tab_mentor, hr_tab_training = st.tabs([
            "🤖 ALEX AI",
            "🎯 Ścieżka Kariery", 
            "🎓 Mentor", 
            "📚 Szkolenia"
        ])
        
        # =============================
        # HR TAB: ALEX AI ASSISTANT
        # =============================
        with hr_tab_alex:
            st.subheader("🤖 ALEX - Twój AI Sales Assistant")
            
            # Import ALEX functions
            from utils.fmcg_alex_training import (
                get_alex_stats,
                get_autopilot_penalty,
                get_points_to_next_level,
                ALEX_LEVELS,
                TRAINING_MODULES
            )
            
            # Get ALEX stats from game state
            alex_level = game_state.get("alex_level", 0)
            alex_training_points = game_state.get("alex_training_points", 0)
            alex_competencies = game_state.get("alex_competencies", {
                "planning": 0.0,
                "communication": 0.0,
                "analysis": 0.0,
                "relationship": 0.0,
                "negotiation": 0.0
            })
            autopilot_visits_count = game_state.get("autopilot_visits_count", 0)
            autopilot_visits_this_week = game_state.get("autopilot_visits_this_week", 0)
            autopilot_efficiency = game_state.get("autopilot_efficiency_avg", 0.0)
            
            alex_stats = get_alex_stats(alex_level)
            penalty = get_autopilot_penalty(alex_level, alex_competencies)
            points_needed, points_for_next = get_points_to_next_level(alex_training_points, alex_level)
            
            # ALEX Status Card
            points_text = "(MAX)" if alex_level >= 4 else f"(brakuje {points_needed})"
            progress_width = (alex_training_points / max(points_for_next, 1)) * 100
            
            alex_card_html = f"""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; border-radius: 16px; color: white; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3); margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;'>
            <div>
                <div style='font-size: 48px; margin-bottom: 8px;'>{alex_stats['emoji']}</div>
                <div style='font-size: 28px; font-weight: 700;'>ALEX</div>
                <div style='font-size: 16px; opacity: 0.9;'>AI Sales Assistant</div>
            </div>
            <div style='text-align: right;'>
                <div style='font-size: 14px; opacity: 0.8; margin-bottom: 4px;'>Poziom</div>
                <div style='font-size: 36px; font-weight: 700;'>{alex_level}/4</div>
                <div style='font-size: 14px; font-weight: 600;'>{alex_stats['name_pl']}</div>
            </div>
        </div>
        <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
            <div style='font-size: 12px; opacity: 0.9; margin-bottom: 6px;'>Punkty treningowe</div>
            <div style='background: rgba(255,255,255,0.2); border-radius: 6px; height: 12px; overflow: hidden;'>
                <div style='background: #10b981; height: 100%; width: {progress_width:.0f}%;'></div>
            </div>
            <div style='font-size: 11px; margin-top: 4px; opacity: 0.8;'>{alex_training_points} / {points_for_next} punktów {points_text}</div>
        </div>
    </div>"""
            
            st.markdown(alex_card_html, unsafe_allow_html=True)
            
            # ALEX Stats
            col_alex1, col_alex2, col_alex3, col_alex4 = st.columns(4)
            
            with col_alex1:
                st.metric("⚡ Kompetencja", f"{int(alex_stats['competence']*100)}%")
                st.caption(f"Efektywność vs manualna")
            
            with col_alex2:
                st.metric("⚠️ Penalty", f"{penalty:+.0f}%")
                st.caption(f"Wpływ na wyniki wizyt")
            
            with col_alex3:
                st.metric("📊 Limit wizyt/dzień", f"{alex_stats['visits_per_day']}")
                st.caption(f"Max autopilot capacity")
            
            with col_alex4:
                st.metric("🤖 Wizyt autopilota", f"{autopilot_visits_count}")
                st.caption(f"W tym tygodniu: {autopilot_visits_this_week}")
            
            # Competencies breakdown
            st.markdown("### 📚 Kompetencje ALEX")
            
            avg_competency = sum(alex_competencies.values()) / len(alex_competencies) if alex_competencies else 0
            
            st.markdown(f"""
            <div style='background: white; padding: 16px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 16px;'>
                <div style='margin-bottom: 8px;'>
                    <span style='font-weight: 600; color: #64748b;'>Średnie ukończenie modułów:</span>
                    <span style='font-weight: 700; color: #1e293b; font-size: 18px; margin-left: 8px;'>{avg_competency*100:.0f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            for module_id, module_data in TRAINING_MODULES.items():
                completion = alex_competencies.get(module_id, 0.0)
                completion_pct = int(completion * 100)
                
                # Color based on completion
                if completion_pct >= 80:
                    bar_color = "#10b981"
                elif completion_pct >= 50:
                    bar_color = "#f59e0b"
                else:
                    bar_color = "#ef4444"
                
                st.markdown(f"""
                <div style='background: white; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 8px;'>
                    <div style='font-weight: 600; color: #1e293b; margin-bottom: 6px;'>{module_data['name_pl']}</div>
                    <div style='background: #e2e8f0; border-radius: 4px; height: 8px; overflow: hidden;'>
                        <div style='background: {bar_color}; height: 100%; width: {completion_pct}%;'></div>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-top: 4px;'>
                        <span style='font-size: 11px; color: #64748b;'>{module_data['impact']}</span>
                        <span style='font-size: 11px; font-weight: 600; color: {bar_color};'>{completion_pct}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Training CTA
            st.markdown("---")
            
            if alex_level < 4:
                st.info(f"""
                💡 **Trenuj ALEX aby zwiększyć efektywność autopilota!**
                
                Ukończ quizy i case studies w zakładce **🤖 ALEX Training** aby:
                - 📈 Zwiększyć kompetencję ALEX (obecnie: {int(alex_stats['competence']*100)}%)
                - ⚠️ Zmniejszyć penalty na wyniki (obecnie: {penalty:+.0f}%)
                - 🔓 Odblokować więcej wizyt autopilota dziennie (obecnie: {alex_stats['visits_per_day']})
                - ⭐ Awansować ALEX na wyższy poziom
                
                **Do następnego poziomu:** {points_needed} punktów
                """)
            else:
                st.success(f"""
                🏆 **Gratulacje! ALEX osiągnął poziom MASTER!**
                
                Twój AI Sales Assistant jest w pełni wyszkolony:
                - ⚡ Kompetencja: {int(alex_stats['competence']*100)}%
                - ⚠️ Penalty: tylko {penalty:+.0f}%
                - 📊 Maksymalny limit wizyt: {alex_stats['visits_per_day']}/dzień
                
                Kontynuuj trening aby utrzymać kompetencje na najwyższym poziomie!
                """)
        
        # =============================
        # HR TAB: ŚCIEŻKA KARIERY  
        # =============================
        with hr_tab_career:
            st.markdown("### 🎯 Ścieżka Kariery w FMCG")
            
            # Career levels definition
            career_levels = [
                {"level": 1, "title": "Junior Sales Representative", "description": "Początkujący przedstawiciel handlowy", "requirements": "Brak wymagań", "emoji": "🌱", "color": "#4CAF50"},
                {"level": 2, "title": "Sales Representative", "description": "Doświadczony przedstawiciel handlowy", "requirements": "3 mies. doświadczenia<br>5 udanych negocjacji", "emoji": "💼", "color": "#2196F3"},
                {"level": 3, "title": "Senior Sales Representative", "description": "Starszy przedstawiciel handlowy", "requirements": "6 mies. doświadczenia<br>15 klientów, ocena 4.0", "emoji": "⭐", "color": "#FF9800"},
                {"level": 4, "title": "Key Account Manager", "description": "Menedżer kluczowych klientów", "requirements": "1 rok doświadczenia<br>25 klientów<br>Umowy długoterminowe", "emoji": "🔑", "color": "#9C27B0"},
                {"level": 5, "title": "Territory Manager", "description": "Menedżer terytorialny", "requirements": "1.5 roku<br>Zarządzanie 3+ osobami", "emoji": "🗺️", "color": "#FF5722"},
                {"level": 6, "title": "Regional Sales Manager", "description": "Regionalny menedżer sprzedaży", "requirements": "2 lata doświadczenia<br>Wyniki zespołu 120%", "emoji": "🏆", "color": "#795548"},
                {"level": 7, "title": "Area Sales Manager", "description": "Menedżer sprzedaży obszarowej", "requirements": "3 lata<br>Zarządzanie 5+ menedżerami", "emoji": "👑", "color": "#607D8B"},
                {"level": 8, "title": "Sales Director", "description": "Dyrektor sprzedaży", "requirements": "4 lata<br>Strategiczne planowanie", "emoji": "💎", "color": "#E91E63"},
                {"level": 9, "title": "Commercial Director", "description": "Dyrektor handlowy", "requirements": "5+ lat<br>Pełna odpowiedzialność", "emoji": "👨‍💼", "color": "#673AB7"}
            ]
            
            # Current level (get from game state or default to 1)
            current_level = game_state.get("career_level", 1)
            
            # Display current position as hero card
            st.markdown("#### 📊 Twoja Aktualna Pozycja")
            current_position = career_levels[current_level - 1]
            
            # Hero card with current position
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {current_position['color']}20, {current_position['color']}40);
                border: 2px solid {current_position['color']};
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <h2 style="color: {current_position['color']}; margin: 0;">
                    {current_position['emoji']} Poziom {current_position['level']}
                </h2>
                <h3 style="margin: 10px 0; color: #333;">
                    {current_position['title']}
                </h3>
                <p style="font-size: 16px; color: #666; margin: 0;">
                    {current_position['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            progress = (current_level - 1) / (len(career_levels) - 1) * 100
            st.markdown("#### 📈 Postęp Ogólny")
            st.progress(progress / 100)
            st.markdown(f"<div style='text-align: center; color: #666;'>Ukończono {current_level} z {len(career_levels)} poziomów ({progress:.1f}%)</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("#### 🚀 Kompletna Ścieżka Kariery")
            
            # Display career path in cards - 3 columns
            for i in range(0, len(career_levels), 3):
                cols = st.columns(3)
                
                for j, col in enumerate(cols):
                    if i + j < len(career_levels):
                        level = career_levels[i + j]
                        level_num = level['level']
                        
                        with col:
                            # Determine card status and style
                            if level_num < current_level:
                                # Completed
                                status = "✅ UKOŃCZONY"
                                border_color = "#4CAF50"
                                bg_gradient = "linear-gradient(135deg, #4CAF5020, #4CAF5040)"
                                opacity = "1"
                            elif level_num == current_level:
                                # Current
                                status = "🎯 AKTUALNY"
                                border_color = level['color']
                                bg_gradient = f"linear-gradient(135deg, {level['color']}30, {level['color']}50)"
                                opacity = "1"
                            else:
                                # Locked
                                status = "🔒 ZABLOKOWANY"
                                border_color = "#CCCCCC"
                                bg_gradient = "linear-gradient(135deg, #f5f5f5, #e0e0e0)"
                                opacity = "0.7"
                            
                            # Card HTML
                            card_html = f"""
                            <div style="
                                background: {bg_gradient};
                                border: 2px solid {border_color};
                                border-radius: 12px;
                                padding: 15px;
                                margin: 5px 0;
                                height: 320px;
                                opacity: {opacity};
                                transition: transform 0.2s;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                display: flex;
                                flex-direction: column;
                            ">
                                <div style="text-align: center; flex-grow: 1;">
                                    <div style="font-size: 2em; margin-bottom: 5px;">
                                        {level['emoji']}
                                    </div>
                                    <div style="
                                        background: {border_color};
                                        color: white;
                                        padding: 2px 8px;
                                        border-radius: 10px;
                                        font-size: 12px;
                                        font-weight: bold;
                                        margin-bottom: 8px;
                                        display: inline-block;
                                    ">
                                        {status}
                                    </div>
                                    <h4 style="
                                        color: {border_color};
                                        margin: 8px 0;
                                        font-size: 14px;
                                        line-height: 1.2;
                                    ">
                                        Poziom {level['level']}
                                    </h4>
                                    <h5 style="
                                        color: #333;
                                        margin: 5px 0;
                                        font-size: 12px;
                                        font-weight: bold;
                                        line-height: 1.2;
                                        height: 32px;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                    ">
                                        {level['title']}
                                    </h5>
                                    <p style="
                                        color: #666;
                                        font-size: 11px;
                                        margin: 8px 0;
                                        line-height: 1.3;
                                        height: 30px;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                    ">
                                        {level['description']}
                                    </p>
                                </div>
                                <div style="
                                    background: rgba(255,255,255,0.9);
                                    padding: 8px;
                                    border-radius: 8px;
                                    margin-top: auto;
                                    min-height: 60px;
                                ">
                                    <strong style="font-size: 11px; color: #333;">Wymagania:</strong><br>
                                    <div style="font-size: 10px; color: #666; line-height: 1.4; margin-top: 4px;">
                                        {level['requirements']}
                                    </div>
                                </div>
                            </div>
                            """
                            
                            st.markdown(card_html, unsafe_allow_html=True)
            
            # Benefits section with modern styling
            st.markdown("---")
            st.markdown("#### 🎁 Korzyści z Awansu")
            
            benefits = {
                1: ["Podstawowe narzędzia sprzedażowe", "Dostęp do katalogu produktów"],
                2: ["Zwiększony limit negocjacji", "Dostęp do historii klientów"],
                3: ["Narzędzia analityczne", "Specjalne rabaty dla klientów"],
                4: ["Zarządzanie kluczowymi klientami", "Dostęp do ekskluzywnych produktów"],
                5: ["Narzędzia zarządzania zespołem", "Budżet marketingowy"],
                6: ["Analityka regionalna", "Planowanie strategiczne"],
                7: ["Zarządzanie wieloma regionami", "Dostęp do danych rynkowych"],
                8: ["Strategia sprzedaży", "Budżet na rozwój produktów"],
                9: ["Pełne uprawnienia komercyjne", "Strategia biznesowa firmy"]
            }
            
            # Display benefits in a nice format
            benefit_cols = st.columns(3)
            for i, level in enumerate(range(1, current_level + 1)):
                if level in benefits:
                    with benefit_cols[i % 3]:
                        level_info = career_levels[level - 1]
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, {level_info['color']}20, {level_info['color']}30);
                            border-left: 4px solid {level_info['color']};
                            padding: 10px;
                            margin: 5px 0;
                            border-radius: 5px;
                        ">
                            <strong style="color: {level_info['color']};">
                                {level_info['emoji']} Poziom {level}
                            </strong><br>
                            <small>
                                {'<br>'.join([f"• {benefit}" for benefit in benefits[level]])}
                            </small>
                        </div>
                        """, unsafe_allow_html=True)
        
        # =============================
        # HR TAB: MENTOR (istniejąca funkcjonalność)
        # =============================
        with hr_tab_mentor:
            st.markdown("### 🎓 Mentor - Twój Doradca Sprzedażowy")
            
            # Initialize mentor state
            if "mentor_questions_today" not in game_state:
                game_state["mentor_questions_today"] = 0
            if "mentor_last_reset_day" not in game_state:
                game_state["mentor_last_reset_day"] = game_state.get("current_day", "Monday")
            if "mentor_conversation_history" not in game_state:
                game_state["mentor_conversation_history"] = []
            
            # Reset daily limit and clear history when day changes
            if game_state.get("mentor_last_reset_day") != game_state.get("current_day"):
                game_state["mentor_questions_today"] = 0
                game_state["mentor_last_reset_day"] = game_state.get("current_day", "Monday")
                game_state["mentor_conversation_history"] = []  # Clear history from previous day
            
            # Header with limits
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; 
                            border-radius: 10px; 
                            color: white; 
                            margin-bottom: 20px;">
                    <h3 style="margin: 0;">📞 Telefon do Mentora</h3>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Twój osobisty doradca - ekspert od sprzedaży FMCG</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                questions_left = 2 - game_state.get("mentor_questions_today", 0)
                if questions_left > 0:
                    st.success(f"✅ Pozostało pytań: **{questions_left}/2**")
                else:
                    st.error("❌ Limit wyczerpany")
            
            st.markdown("---")
            
            # Display conversation history from today
            mentor_history = game_state.get("mentor_conversation_history", [])
            
            if mentor_history:
                st.markdown("### 📝 Twoje rozmowy z Mentorem (dzisiaj)")
                st.caption("💡 Możesz wracać do tych porad w ciągu całego dnia. Historie zerują się każdego dnia.")
                
                for idx, entry in enumerate(reversed(mentor_history), 1):
                    with st.expander(f"🗨️ Pytanie #{len(mentor_history) - idx + 1}: {entry.get('question', '')[:80]}...", expanded=(idx == 1)):
                        # Question
                        st.markdown(f"**Twoje pytanie:**")
                        st.info(entry.get('question', ''))
                        
                        # Context if provided
                        if entry.get('client_name') or entry.get('product_name'):
                            st.markdown("**Kontekst:**")
                            context_items = []
                            if entry.get('client_name'):
                                context_items.append(f"👤 Klient: {entry['client_name']}")
                            if entry.get('product_name'):
                                context_items.append(f"📦 Produkt: {entry['product_name']}")
                            st.caption(" | ".join(context_items))
                        
                        # Answer
                        st.markdown("**Rada Mentora:**")
                        st.markdown(f"""
                        <div style="background: #f0fdf4; 
                                    padding: 20px; 
                                    border-radius: 10px; 
                                    border-left: 4px solid #10b981;
                                    margin: 15px 0;">
                            {entry.get('answer', '')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Copy button helper
                        st.caption("💡 Tip: Zaznacz tekst i skopiuj (Ctrl+C) żeby użyć w rozmowie z klientem!")
                
                st.markdown("---")
            
            # Info box
            st.info("""
            💡 **Jak to działa?**
            - Możesz zadać **2 pytania dziennie** (limit resetuje się każdego dnia)
            - Mentor pomoże Ci z **konkretnymi klientami, produktami i sytuacjami sprzedażowymi**
            - Pytaj o strategie rozmowy, argumenty sprzedażowe, obsługę obiekcji
            
            ⚠️ **Wskazówka:** Zadawaj konkretne pytania! Im bardziej szczegółowe, tym lepsze porady.
            """)
            
            # Check if can ask
            if game_state.get("mentor_questions_today", 0) >= 2:
                st.warning("📵 **Mentor niedostępny dzisiaj.** Zadzwoń jutro - odświeży się limit pytań!")
                st.markdown("---")
                st.markdown("### 💼 Przykładowe pytania na przyszłość:")
                st.markdown("""
                - "Jak przekonać Pana Kowalskiego do zamówienia naszego BodyWash? Ma już Dove."
                - "Jakie argumenty użyć jeśli sklep mówi że nie ma miejsca na półce?"
                - "Co powiedzieć klientowi który się boi że produkt się nie sprzeda?"
                - "Jak zbudować relację ze sklepem na początku współpracy?"
                """)
            else:
                # Question input
                st.markdown("### 📝 Zadaj pytanie Mentorowi:")
                
                # Context helpers
                with st.expander("🎯 Sugestie tematów (kliknij aby rozwinąć)"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **Klienci i relacje:**
                        - Jak zacząć rozmowę z nowym klientem?
                        - Jak zbudować zaufanie?
                        - Co robić gdy klient jest zimny/obojętny?
                        """)
                    with col2:
                        st.markdown("""
                        **Produkty i argumenty:**
                        - Jakie argumenty dla konkretnego produktu?
                        - Jak porównać się z konkurencją?
                        - Co mówić o cenie i marży?
                        """)
                
                # Question form
                user_question = st.text_area(
                    "Twoje pytanie:",
                    placeholder="Np. 'Jak przekonać sklep osiedlowy do zamówienia naszego BodyWash Natural? Mają już Dove i mówią że nie potrzebują więcej produktów.'",
                    height=100,
                    key="mentor_question_input"
                )
                
                # Optional context
                with st.expander("➕ Dodaj kontekst (opcjonalnie)"):
                    selected_client_name = st.selectbox(
                        "Dotyczy klienta:",
                        ["Nie dotyczy konkretnego klienta"] + [c.get("name", "Unknown") for c in clients.values()],
                        key="mentor_client_context"
                    )
                    
                    # Get product list from FRESHLIFE_PRODUCTS (player's company products)
                    product_names = [p.get("name", "Unknown") for p in FRESHLIFE_PRODUCTS.values()]
                    
                    selected_product = st.selectbox(
                    "Dotyczy produktu:",
                    ["Nie dotyczy konkretnego produktu"] + product_names,
                    key="mentor_product_context"
                )
            
            # Submit button
            if st.button("📞 Zadzwoń do Mentora", type="primary", use_container_width=True):
                if not user_question or len(user_question.strip()) < 10:
                    st.error("⚠️ Pytanie jest za krótkie. Opisz swoją sytuację dokładniej (min. 10 znaków).")
                else:
                    with st.spinner("☎️ Mentor analizuje Twoją sytuację..."):
                        try:
                            # Build context for AI
                            context_parts = []
                            
                            # Add client context
                            if selected_client_name != "Nie dotyczy konkretnego klienta":
                                # clients is a dict, iterate through values
                                client = next((c for c in clients.values() if c.get("name") == selected_client_name), None)
                                if client:
                                    context_parts.append(f"""
                                    **Klient:** {client.get('name')}
                                    - Typ: {client.get('client_type', 'Unknown')}
                                    - Status: {client.get('status', 'Unknown')}
                                    - Reputacja: {client.get('reputation', 0)}/100
                                    """)
                            
                            # Add product context
                            if selected_product != "Nie dotyczy konkretnego produktu":
                                # FRESHLIFE_PRODUCTS is a dict with player's company products
                                product = next((p for p in FRESHLIFE_PRODUCTS.values() if p.get("name") == selected_product), None)
                                if product:
                                    margin_pct, margin_pln = _get_product_margin(product)
                                    price = _get_product_price(product)
                                    context_parts.append(f"""
                                    **Produkt:** {product.get('name')}
                                    - Cena detaliczna: {price} zł
                                    - Marża dla sklepu: {margin_pct}% ({margin_pln:.2f} zł)
                                    - Kategoria: {product.get('category', 'Unknown')}
                                    """)
                            
                            # Build full prompt
                            system_prompt = """Jesteś doświadczonym mentorem sprzedaży FMCG (Fast-Moving Consumer Goods) w Polsce. 
                            Pomagasz handlowcom w sprzedaży produktów do małych sklepów osiedlowych.
                            
                            Twoje odpowiedzi powinny być:
                            - Praktyczne i konkretne
                            - Oparte na realnych technikach sprzedaży B2B
                            - Dostosowane do polskiego rynku
                            - Zawierać przykładowe frazy do użycia
                            - Krótkie (200-400 słów)
                            
                            Pamiętaj o specyfice kanału tradycyjnego:
                            - Decyzje podejmuje właściciel/rodzina
                            - Ważna jest marża w PLN (nie %), rotacja produktu
                            - Ograniczone miejsce na półce
                            - Kapitał obrotowy jest ograniczony
                            - Relacje są kluczowe"""
                            
                            context = "\n\n".join(context_parts) if context_parts else "Brak dodatkowego kontekstu."
                            
                            user_prompt = f"""
                            Kontekst sytuacji:
                            {context}
                            
                            Pytanie handlowca:
                            {user_question}
                            
                            Udziel konkretnej porady. Jeśli możesz, podaj przykładowe frazy/argumenty które może użyć.
                            """
                            
                            # Call AI (Gemini)
                            import google.generativeai as genai
                            from utils.fmcg_tasks import get_gemini_api_key
                            
                            api_key = get_gemini_api_key()
                            if api_key:
                                genai.configure(api_key=api_key)
                                model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
                                
                                response = model.generate_content(
                                    [system_prompt, user_prompt],
                                    generation_config=genai.GenerationConfig(
                                        temperature=0.7,
                                        max_output_tokens=800,
                                    )
                                )
                                
                                mentor_response = response.text
                                
                                # Save to conversation history
                                if "mentor_conversation_history" not in game_state:
                                    game_state["mentor_conversation_history"] = []
                                
                                game_state["mentor_conversation_history"].append({
                                    "question": user_question,
                                    "answer": mentor_response,
                                    "client_name": selected_client_name if selected_client_name != "Nie dotyczy konkretnego klienta" else None,
                                    "product_name": selected_product if selected_product != "Nie dotyczy konkretnego produktu" else None,
                                    "timestamp": game_state.get("current_day", "Unknown")
                                })
                                
                                # Increment question count
                                game_state["mentor_questions_today"] = game_state.get("mentor_questions_today", 0) + 1
                                update_fmcg_game_state_sql(username, game_state, clients)
                                st.session_state["fmcg_game_state"] = game_state
                                
                                # Display response
                                st.success("✅ **Mentor odpowiada:**")
                                st.markdown(f"""
                                <div style="background: #f0fdf4; 
                                            padding: 20px; 
                                            border-radius: 10px; 
                                            border-left: 4px solid #10b981;
                                            margin: 15px 0;">
                                    {mentor_response}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Copy instruction
                                st.info("💡 **Tip:** Przewiń do góry aby zobaczyć wszystkie rozmowy z dzisiaj. Możesz kopiować fragmenty porad do użycia w rozmowach!")
                                
                                # Rerun to show in history
                                if st.button("🔄 Pokaż w historii rozmów", type="secondary", use_container_width=True):
                                    st.rerun()
                                
                                # Update remaining questions
                                remaining = 2 - game_state.get("mentor_questions_today", 0)
                                if remaining > 0:
                                    st.info(f"💡 Pozostało pytań dzisiaj: **{remaining}/2**")
                                else:
                                    st.warning("📵 To było Twoje ostatnie pytanie na dzisiaj. Mentor będzie dostępny jutro!")
                                
                                # Feedback
                                st.markdown("---")
                                st.markdown("**Czy ta rada była pomocna?**")
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("👍 Pomocna"):
                                        st.success("Dziękujemy za feedback!")
                                with col2:
                                    if st.button("👎 Nie bardzo"):
                                        st.info("Spróbuj zadać pytanie bardziej szczegółowo lub z dodatkowym kontekstem.")
                            
                            else:
                                st.error("❌ Brak klucza API Google Gemini. Skontaktuj się z administratorem.")
                        
                        except Exception as e:
                            st.error(f"❌ Błąd podczas łączenia z Mentorem: {e}")
                            st.info("Spróbuj ponownie za chwilę.")
    
    # =============================================================================
    # HR TAB: SZKOLENIA (przeniesiena z Inspiracji)
    # =============================================================================
    
        # =============================
        # HR TAB: SZKOLENIA
        # =============================
        with hr_tab_training:
            st.markdown("### 📚 Akademia Handlowca FMCG")
            st.markdown("Kompleksowe szkolenia z wszystkich aspektów sprzedaży w kanale tradycyjnym")
        
            # Training categories - NOWA STRUKTURA
            training_categories = st.tabs([
                "🗺️ Planowanie i Routing",
                "💬 Rozmowy i Relacje",
                "📦 Portfolio Produktowe",
                "🏪 Kanały Dystrybucji",
                "🎨 Trade Marketing",
                "📊 Analityka Biznesowa"
            ])
        
            # =============================
            # TAB 1: PLANOWANIE I ROUTING
            # =============================
            with training_categories[0]:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: white; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">🗺️ Planowanie i Routing</h2>
                    <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                        Segmentacja ABC, optymalizacja trasy, strategia prospectingowa
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Lekcja: Planowanie terytorium sprzedażowego (Lokalny HTML)
                with st.expander("📚 Lekcja: Planowanie terytorium sprzedażowego - Od analizy do pierwszej wizyty", expanded=False):
                    # Wczytaj i wyświetl lokalny plik HTML
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "PLANOWANIE_TERYTORIUM_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        # Wyświetl HTML w iframe przez components.html
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                        st.info("💡 Upewnij się, że plik PLANOWANIE_TERYTORIUM_INTERACTIVE.html znajduje się w folderze docs/")
               
            # =============================
            # TAB 2: ROZMOWY I RELACJE
            # =============================
            with training_categories[1]:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: white; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(240, 147, 251, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">💬 Rozmowy i Relacje</h2>
                    <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                        Sondowanie potrzeb, budowanie zaufania, techniki negocjacyjne
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Lekcja: Sondowanie potrzeb klienta
                with st.expander("🎯 Lekcja: Sondowanie potrzeb klienta - Sztuka zadawania właściwych pytań", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "SONDOWANIE_POTRZEB_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        # Wyświetl HTML w iframe przez components.html
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                        st.info("💡 Upewnij się, że plik SONDOWANIE_POTRZEB_INTERACTIVE.html znajduje się w folderze docs/")
            
            # =============================
            # TAB 3: PORTFOLIO PRODUKTOWE
            # =============================
            with training_categories[2]:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: #1e293b; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(168, 237, 234, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">📦 Portfolio Produktowe</h2>
                    <p style="font-size: 1.1rem; opacity: 0.85; margin: 0;">
                        Znajomość produktów, kategorii FMCG, argumentacja sprzedażowa
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center; border: 2px dashed #dee2e6; margin-top: 20px;">
                    <div style="font-size: 3rem; margin-bottom: 15px;">📦</div>
                    <h3 style="color: #6c757d; margin-bottom: 10px;">Materiały w przygotowaniu</h3>
                    <p style="color: #6c757d;">Wkrótce znajdziesz tutaj:</p>
                    <ul style="color: #adb5bd; font-size: 0.9rem; text-align: left; max-width: 500px; margin: 20px auto;">
                        <li>Kategorie FMCG (Personal Care, Food, Beverages...)</li>
                        <li>USP produktów FreshLife</li>
                        <li>Argumenty value vs premium</li>
                        <li>Cross-selling i up-selling</li>
                        <li>Konkurencja - Dove, Nivea, L'Oreal</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # =============================
            # TAB 4: KANAŁY DYSTRYBUCJI
            # =============================
            with training_categories[3]:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: white; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(79, 172, 254, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">🏪 Kanały Dystrybucji</h2>
                    <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                        Traditional Trade, Modern Trade, modele dystrybucji, ekonomika sklepu
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Lekcja: Kanał Tradycyjny
                with st.expander("🏪 Lekcja: Kanał Tradycyjny - Charakterystyka i Modele Dystrybucji", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "KANAL_TRADYCYJNY_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        # Wyświetl HTML w iframe przez components.html
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                        st.info("💡 Upewnij się, że plik KANAL_TRADYCYJNY_INTERACTIVE.html znajduje się w folderze docs/")
            
            # =============================
            # TAB 5: TRADE MARKETING
            # =============================
            with training_categories[4]:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: white; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(250, 112, 154, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">🎨 Trade Marketing</h2>
                    <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                        Merchandising, materiały POS, promocje, visual merchandising, visibility w sklepie
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Lekcja 1: Trade Marketing - Podstawy + Merchandising + POS
                with st.expander("📚 Lekcja 1: Trade Marketing - Podstawy, Merchandising i Materiały POS", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "TRADE_MARKETING_PART1_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                        st.info("💡 Upewnij się, że plik TRADE_MARKETING_PART1_INTERACTIVE.html znajduje się w folderze docs/")
                
                # Lekcja 2A: Trade Marketing - Promocje
                with st.expander("🎪 Lekcja 2A: Trade Marketing - Planowanie i Realizacja Promocji", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "TRADE_MARKETING_PART2A_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                        st.info("💡 Upewnij się, że plik TRADE_MARKETING_PART2A_INTERACTIVE.html znajduje się w folderze docs/")
                
                # Lekcja 2B: Trade Marketing - Visual Merchandising
                with st.expander("🎨 Lekcja 2B: Trade Marketing - Visual Merchandising i Psychologia Kolorów", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "TRADE_MARKETING_PART2B_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                        st.info("💡 Upewnij się, że plik TRADE_MARKETING_PART2B_INTERACTIVE.html znajduje się w folderze docs/")
                
                # Lekcja 2C: Trade Marketing - Zwiększanie Visibility
                with st.expander("🚀 Lekcja 2C: Trade Marketing - Zwiększanie Visibility i Special Placements", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "TRADE_MARKETING_PART2C_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                        st.info("💡 Upewnij się, że plik TRADE_MARKETING_PART2C_INTERACTIVE.html znajduje się w folderze docs/")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # NAGŁÓWEK: Ekonomia talerza
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: white; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(245, 87, 108, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">🍽️ Ekonomia talerza</h2>
                    <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                        Jak gastronomia liczy pieniądze - Food Cost, struktura kosztów, koszt porcji
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Lekcja: Ekonomia talerza
                with st.expander("📊 Lekcja: Ekonomia talerza - Jak gastronomia liczy pieniądze", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "EKONOMIA_TALERZA_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # NAGŁÓWEK: Narzędzia ekonomiczne
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: white; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(118, 75, 162, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">🧮 Narzędzia ekonomiczne</h2>
                    <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                        Interaktywne kalkulatory: Food Cost, porównywanie produktów, monitoring cen
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Lekcja: Narzędzia ekonomiczne
                with st.expander("🔧 Lekcja: Narzędzia ekonomiczne - Kalkulatory dla handlowców", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "NARZEDZIA_EKONOMICZNE_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # NAGŁÓWEK: Dwie marki, jeden zysk
                st.markdown("""
                <div style="background: linear-gradient(135deg, #dc2626 0%, #f59e0b 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: white; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(220, 38, 38, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">🎯 Dwie marki, jeden zysk</h2>
                    <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                        Jak sprzedawać ekonomicznie Heinz i Pudliszki - Smart Portfolio
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Lekcja: Dwie marki, jeden zysk
                with st.expander("🔴🟡 Lekcja: Dwie marki, jeden zysk - Heinz i Pudliszki", expanded=False):
                    import os
                    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                            "docs", "DWIE_MARKI_JEDEN_ZYSK_INTERACTIVE.html")
                    
                    if os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        components.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ Nie znaleziono pliku lekcji: {html_path}")
            
            # =============================
            # TAB 6: ANALITYKA BIZNESOWA
            # =============================
            with training_categories[5]:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); 
                            padding: 30px; 
                            border-radius: 15px; 
                            color: white; 
                            margin-bottom: 20px;
                            box-shadow: 0 8px 24px rgba(48, 207, 208, 0.3);">
                    <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">📊 Analityka Biznesowa</h2>
                    <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                        KPI, dashboardy, analiza sprzedaży, forecasting, reporting
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center; border: 2px dashed #dee2e6; margin-top: 20px;">
                    <div style="font-size: 3rem; margin-bottom: 15px;">📊</div>
                    <h3 style="color: #6c757d; margin-bottom: 10px;">Materiały w przygotowaniu</h3>
                    <p style="color: #6c757d;">Wkrótce znajdziesz tutaj:</p>
                    <ul style="color: #adb5bd; font-size: 0.9rem; text-align: left; max-width: 500px; margin: 20px auto;">
                        <li>KPI handlowca (sell-in, sell-out, distribution)</li>
                        <li>Analiza trendów sprzedażowych</li>
                        <li>Forecasting i planowanie zamówień</li>
                        <li>Reporting dla managera</li>
                        <li>Data-driven decision making</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    # =============================================================================
    # TAB: INSTRUKCJA
    # =============================================================================
    
    with tab_instructions:
        st.markdown("# 📖 Instrukcja Gry - Heinz Food Service")
        
        # Hero banner
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; margin-bottom: 30px; text-align: center;'>
            <h2 style='color: white; margin: 0;'>🎮 Witaj w Heinz Food Service Challenge!</h2>
            <p style='color: #e0e7ff; font-size: 18px; margin-top: 10px;'>
                Symulacja sprzedaży produktów premium dla gastronomii
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Start Guide
        st.markdown("### 🚀 Szybki Start")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: #f0f9ff; padding: 20px; border-radius: 12px; border-left: 4px solid #3b82f6;'>
                <h4 style='color: #1e40af; margin-top: 0;'>1️⃣ Rozpocznij od Onboardingu</h4>
                <p style='color: #1e3a8a; font-size: 14px;'>
                    Wykonaj 3 zadania wprowadzające w zakładce <strong>Dashboard → Zadania</strong>. 
                    Otrzymasz feedback od AI i pierwsze punkty reputacji.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #f0fdf4; padding: 20px; border-radius: 12px; border-left: 4px solid #22c55e;'>
                <h4 style='color: #15803d; margin-top: 0;'>2️⃣ Planuj Wizyty</h4>
                <p style='color: #14532d; font-size: 14px;'>
                    Przejdź do <strong>Sprzedaż → Wizyty Handlowe</strong>. Wybieraj klientów strategicznie 
                    i buduj relacje przez regularny kontakt.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: #fef3c7; padding: 20px; border-radius: 12px; border-left: 4px solid #f59e0b;'>
                <h4 style='color: #92400e; margin-top: 0;'>3️⃣ Rozwijaj Zespół</h4>
                <p style='color: #78350f; font-size: 14px;'>
                    W <strong>HR & Team → Wiedza Produktowa</strong> ucz się o produktach Heinz i Pudliszki. 
                    Zdobywaj certyfikaty i odblokuj nowe możliwości.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Główne mechaniki gry
        st.markdown("### 🎯 Główne Mechaniki Gry")
        
        with st.expander("📊 **System Reputacji** - Twój Główny Cel", expanded=True):
            st.markdown("""
            **Overall Rating** to Twój główny wskaźnik sukcesu, obliczany jako:
            
            - **60% Client Reputation** (średnia reputacja u wszystkich klientów)
            - **40% Company Reputation** składająca się z:
              - 30% Task Performance (wykonanie zadań)
              - 40% Sales Performance (wyniki sprzedaży)
              - 30% Professionalism (profesjonalizm w działaniu)
            
            **Tiery reputacji:**
            - 🥉 **Bronze** (0-25): Początkujący
            - 🥈 **Silver** (25-50): Rozwijający się
            - 🥇 **Gold** (50-75): Profesjonalista
            - 💎 **Platinum** (75-90): Ekspert
            - 👑 **Diamond** (90+): Mistrz sprzedaży
            
            **Jak podnosić reputację?**
            - Wykonuj zadania i otrzymuj pozytywny feedback
            - Prowadź udane wizyty handlowe (ocena 4-5⭐)
            - Podpisuj kontrakty i realizuj dostawy na czas
            - Utrzymuj profesjonalizm (unikaj wizyt <3⭐)
            """)
        
        with st.expander("🎓 **Zadania Onboardingowe** - Twój Start", expanded=False):
            st.markdown("""
            **3 zadania wprowadzające oceniane przez AI:**
            
            1. **🎤 Elevator Pitch** - Przedstawienie firmy Heinz Food Service
               - Struktura: Kim jesteś → Co robicie → Wartość → Social proof → Pytanie
               - AI oceni: długość, USP, konkretność, pytanie na koniec
            
            2. **❓ Pytania do Klienta** - Przygotowanie 3-4 pytań otwartych
               - Cel: zrozumieć potrzeby, poznać obecne rozwiązania
               - AI oceni: czy pytania są otwarte, konkretne, nastawione na klienta
            
            3. **💬 Obsługa Obiekcji** - Odpowiedź na "Mam już Heinz, po co mi Pudliszki?"
               - Struktura: Akceptacja → Uzupełnienie → Korzyść → Przykład → Pytanie
               - AI oceni: kompletność argumentacji, konkretne przykłady, profesjonalizm
            
            **Feedback od AI:**
            - Natychmiastowa ocena Twojej odpowiedzi
            - Konkretne wskazówki co poprawić
            - Możliwość ponownego wysłania przy odrzuceniu
            """)
        
        with st.expander("🤝 **Wizyty Handlowe** - Serce Gry", expanded=False):
            st.markdown("""
            **Proces wizyty:**
            
            1. **Wybór Klienta** - Zobacz listę restauracji z kategoryzacją:
               - 🏆 **Premium** (fine dining, hotele) - wysokie marże, wymagający
               - 🍔 **Casual** (burger bary, bistro) - średnie wolumeny, elastyczni
               - 🌮 **Quick Service** (food trucki, fast food) - szybkie obroty, cena
            
            2. **Cele Wizyty** - Wybierz 1-2 cele:
               - Budowanie relacji
               - Prezentacja produktów
               - Negocjacje kontraktu
               - Wsparcie merchandising
            
            3. **Notatki & Discovery** - Zapisuj informacje o kliencie:
               - Profil kuchni i gości
               - Obecni dostawcy i wyzwania
               - Potencjał i plany rozwoju
            
            4. **Ocena Wizyty** - System gwiazdkowy (1-5⭐):
               - 5⭐ = +3 reputacja u klienta
               - 4⭐ = +2 reputacja
               - 3⭐ = +1 reputacja
               - <3⭐ = -5 professionalism (Company Rep)
            
            **Wskazówki:**
            - Regularność > jednorazowe akcje (odwiedzaj co 2-4 tygodnie)
            - Dostosuj produkty do typu kuchni
            - Buduj relację przed próbą sprzedaży
            """)
        
        with st.expander("📦 **Portfolio Produktów** - Co Sprzedajesz", expanded=False):
            st.markdown("""
            **Heinz** - Marka premium dla gastronomii:
            - **Heinz Tomato Ketchup** - ikona jakości, rozpoznawalność międzynarodowa
            - **Heinz BBQ Sauce** - różne warianty (Classic, Smoky, Honey)
            - **Heinz Mayonnaise** - kremowa konsystencja, stabilna jakość
            - Idealny dla: burgery, steaki, kuchnia amerykańska/międzynarodowa
            
            **Pudliszki** - Tradycja i polski smak:
            - **Pudliszki Ketchup Łagodny** - klasyczny polski smak
            - **Pudliszki Musztarda** - różne rodzaje (Sarepska, Dijon)
            - **Pudliszki Chrzan** - autentyczny, ostry
            - Idealny dla: polska kuchnia, pierogi, żeberka, schabowe
            
            **Strategie sprzedaży:**
            - **Complementary, nie konkurencja** - Heinz i Pudliszki uzupełniają się
            - **Segmentacja menu** - premium burger = Heinz, tradycyjny obiad = Pudliszki
            - **Portfolio approach** - sprzedawaj rozwiązania, nie produkty
            """)
        
        with st.expander("👥 **Rozwój & Wiedza** - Nauka w Grze", expanded=False):
            st.markdown("""
            **Artykuły Wiedzy (HR & Team → Wiedza Produktowa):**
            
            - **🗺️ Planowanie Terytorium** - segmentacja ABC, routing, klasteryzacja
            - **🔥 Heinz - Historia Marki** - 150 lat tradycji, wartości, positioning
            - **🇵🇱 Pudliszki - Polski Smak** - lokalna marka, autentyczność
            
            **System uczenia:**
            - Quiz po przeczytaniu artykułu
            - Certyfikat po zaliczeniu (70%+)
            - Odblokowanie nowych funkcji
            
            **Rozwój handlowca:**
            - Zdobywaj XP przez zadania i wizyty
            - Awansuj w tierach reputacji
            - Odblokuj zaawansowane strategie sprzedaży
            """)
        
        with st.expander("💰 **Ekonomia Gry** - Waluty i Nagrody", expanded=False):
            st.markdown("""
            **Waluty w grze:**
            
            - **XP (Experience Points)** - ogólny poziom doświadczenia
            - **Unlock Tokens** - odblokowują nowe funkcje/produkty
            - **Company Credits** - waluta do rozwoju (przyszła funkcja)
            - **Reputation Points** - główny wskaźnik sukcesu
            
            **Źródła nagród:**
            - Wykonane zadania: XP + Tokens + Reputacja
            - Udane wizyty: Reputacja u klienta + XP
            - Zaliczone quizy: Certyfikaty + XP
            - Kontrakty (coming soon): Credits + Sales Performance
            
            **Progresja:**
            - Bronze → Silver: wykonaj onboarding, zrób 5 wizyt
            - Silver → Gold: podpisz pierwsze kontrakty, zbuduj portfolio
            - Gold → Platinum: maksymalizuj reputację, zarządzaj wieloma klientami
            """)
        
        st.markdown("---")
        
        # Wskazówki strategiczne
        st.markdown("### 💡 Wskazówki Strategiczne")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
            **✅ DO:**
            - ✅ Zacznij od zadań onboardingowych
            - ✅ Czytaj artykuły przed wizytami
            - ✅ Rób notatki o każdym kliencie
            - ✅ Odwiedzaj regularnie (co 2-4 tygodnie)
            - ✅ Dopasuj produkty do typu kuchni
            - ✅ Buduj relację przed sprzedażą
            - ✅ Używaj Heinz + Pudliszki jako portfolio
            - ✅ Zapisuj feedback z wizyt
            """)
        
        with col_b:
            st.markdown("""
            **❌ DON'T:**
            - ❌ Nie ignoruj reputacji u klientów
            - ❌ Nie sprzedawaj bez zrozumienia potrzeb
            - ❌ Nie traktuj Heinz i Pudliszki jako konkurencji
            - ❌ Nie zaniedbuj profesjonalizmu (<3⭐ boli!)
            - ❌ Nie rób wizyt "na ślepo" bez przygotowania
            - ❌ Nie obiecuj jeśli nie możesz dostarczyć
            - ❌ Nie rezygnuj po jednej nieudanej wizycie
            - ❌ Nie pomijaj onboardingu - to fundament!
            """)
        
        st.markdown("---")
        
        # FAQ
        st.markdown("### ❓ Najczęstsze Pytania (FAQ)")
        
        with st.expander("Jak podnieść Overall Rating?"):
            st.markdown("""
            **Overall Rating = (Client Rep × 60%) + (Company Rep × 40%)**
            
            **Podniesienie Client Reputation:**
            - Rób wizyty 4-5⭐ (quality matters!)
            - Odwiedzaj regularnie (częstotliwość liczy się)
            - Rozwiązuj problemy klientów
            - Dostarczaj wartość, nie tylko sprzedawaj
            
            **Podniesienie Company Reputation:**
            - **Task Performance**: wykonuj zadania i dostawaj feedback ACCEPT
            - **Sales Performance**: podpisuj kontrakty, realizuj dostawy (coming soon)
            - **Professionalism**: unikaj wizyt <3⭐ (każda to -5 punktów!)
            """)
        
        with st.expander("Co jeśli zadanie zostanie odrzucone przez AI?"):
            st.markdown("""
            **Nie ma problemu - możesz poprawić!**
            
            1. Przeczytaj uważnie feedback od AI
            2. Zobacz co konkretnie wymaga poprawy
            3. Edytuj swoją odpowiedź
            4. Kliknij "Sprawdź ponownie AI"
            5. Otrzymasz nową ocenę
            
            **Pamiętaj:**
            - AI ocenia według kryteriów sukcesu z zadania
            - Feedback jest konstruktywny - mówi CO i DLACZEGO
            - Możesz próbować wielokrotnie
            - Odrzucenie ≠ porażka, to szansa na naukę!
            """)
        
        with st.expander("Jak często powinienem odwiedzać klientów?"):
            st.markdown("""
            **Złota zasada: 2-4 tygodnie między wizytami**
            
            **Premium Clients:**
            - Co 2 tygodnie w fazie budowania relacji
            - Co 3-4 tygodnie po podpisaniu kontraktu
            - Więcej przy problemach/nowych produktach
            
            **Casual & Quick Service:**
            - Co 3-4 tygodnie standardowo
            - Co miesiąc w fazie maintenance
            
            **Wskaźniki:**
            - Jeśli reputacja u klienta <50: zwiększ częstotliwość
            - Jeśli >80: możesz wydłużyć cykl
            - Obserwuj "ostatnia wizyta" w liście klientów
            """)
        
        with st.expander("Czym różni się Heinz od Pudliszek?"):
            st.markdown("""
            **Heinz** - Premium, międzynarodowy:
            - **Positioning**: jakość światowej klasy, rozpoznawalność
            - **Cena**: wyższa (premium)
            - **Idealny dla**: kuchnia amerykańska, burgery, steaki, hotele
            - **Target**: goście międzynarodowi, menu premium
            - **Argumenty**: brand recognition, consistent quality, 150 lat tradycji
            
            **Pudliszki** - Tradycja, polski smak:
            - **Positioning**: autentyczny polski smak, lokalność
            - **Cena**: niższa (accessible)
            - **Idealny dla**: polska kuchnia, pierogi, żeberka, schabowe
            - **Target**: polscy goście, menu tradycyjne/dnia
            - **Argumenty**: lokalny smak, autentyczność, dopasowanie do polskich dań
            
            **Strategia PORTFOLIO:**
            Nie "albo/albo", tylko "both/and"! Klient z obiema markami może:
            - Segmentować menu (premium vs casual)
            - Dopasować do profilu gościa (zagraniczny vs polski)
            - Różnicować cenowo (fine dining vs daily lunch)
            """)
        
        st.markdown("---")
        
        # Call to Action
        st.markdown("""
        <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 25px; border-radius: 12px; text-align: center; margin-top: 30px;'>
            <h3 style='color: white; margin: 0;'>🚀 Gotowy do Startu?</h3>
            <p style='color: #d1fae5; font-size: 16px; margin: 15px 0;'>
                Przejdź do zakładki <strong>Dashboard</strong> i rozpocznij od zadań onboardingowych!
            </p>
            <p style='color: #a7f3d0; font-size: 14px; margin: 0;'>
                Powodzenia w budowaniu kariery w Heinz Food Service! 💪
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # =============================================================================
    # TAB: USTAWIENIA
    # =============================================================================
    
    with tab_settings:
        st.subheader("⚙️ Ustawienia Gry")
        
        st.markdown("---")
        
        # Get scenario name
        scenario_id = game_state.get("scenario_id", st.session_state.get("fmcg_scenario", "quick_start"))
        scenario_names = {
            "quick_start": "Quick Start - Piaseczno",
            "heinz_food_service": "Heinz Food Service - Dzięgielów",
            "lifetime": "Lifetime Mode"
        }
        scenario_name = scenario_names.get(scenario_id, scenario_id)
        
        # Current game info
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.metric("📅 Scenariusz", scenario_name)
        
        with col_info2:
            current_week = game_state.get("current_week", 1)
            total_weeks = game_state.get("total_weeks", 8)
            st.metric("📆 Tydzień", f"{current_week}/{total_weeks}")
        
        with col_info3:
            clients_active = game_state.get("clients_active", 0)
            st.metric("👥 Aktywni klienci", clients_active)
        
        st.markdown("---")
        
        # Reset game section
        st.markdown("### 🔄 Reset Gry")
        
        st.warning("""
        ⚠️ **Uwaga!** Resetowanie gry spowoduje:
        - Usunięcie całego postępu w bieżącej grze
        - Powrót do ekranu wyboru scenariusza
        - Utratę wszystkich danych (sprzedaż, klienci, zadania, HR)
        
        **Ta operacja jest nieodwracalna!**
        """)
        
        # Two-step confirmation
        if 'confirm_reset' not in st.session_state:
            st.session_state.confirm_reset = False
        
        col_reset1, col_reset2 = st.columns([1, 1])
        
        with col_reset1:
            if not st.session_state.confirm_reset:
                if st.button("🔄 Chcę zresetować grę", type="primary", use_container_width=True):
                    st.session_state.confirm_reset = True
                    st.rerun()
            else:
                if st.button("❌ Anuluj", use_container_width=True):
                    st.session_state.confirm_reset = False
                    st.rerun()
        
        with col_reset2:
            if st.session_state.confirm_reset:
                if st.button("✅ TAK, RESETUJ GRĘ", type="secondary", use_container_width=True):
                    # Clear all FMCG game state
                    keys_to_clear = [
                        'fmcg_game_state',
                        'fmcg_clients',
                        'fmcg_conversation_history',
                        'fmcg_notes',
                        'fmcg_sales_history',
                        'fmcg_visit_history',
                        'fmcg_scenario',
                        'fmcg_scenario_name',
                        'fmcg_game_initialized',  # KEY: Reset initialization flag
                        'show_client_detail',
                        'selected_client_id',
                        'planned_route',
                        'confirm_reset',
                        # Onboarding tasks
                        'task_company_complete',
                        'task_territory_complete', 
                        'task_product_complete',
                        # HR state
                        'alex_level',
                        'alex_competencies',
                        'career_level',
                        'career_xp',
                        # Other
                        'current_conversation_client'
                    ]
                    
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    # Clear SQL database as well
                    try:
                        # Delete game state from SQL by saving empty/null state
                        import sqlite3
                        conn = sqlite3.connect('business_games.db')
                        cursor = conn.cursor()
                        cursor.execute('DELETE FROM fmcg_game_state WHERE username = ?', (username,))
                        cursor.execute('DELETE FROM fmcg_clients WHERE username = ?', (username,))
                        conn.commit()
                        conn.close()
                    except Exception:
                        # Silently ignore SQL errors (tables may not exist yet)
                        pass
                    
                st.success("✅ Gra została zresetowana! Przekierowuję do wyboru scenariusza...")
                st.balloons()
                # Wait 2 seconds before rerun
                time.sleep(2)
                st.rerun()
        
        st.markdown("---")
        
        # Game settings
        st.markdown("### 🎮 Ustawienia Rozgrywki")
        
        # Energy settings (optional - can be hidden for non-dev users)
        with st.expander("⚡ Zarządzanie energią (tylko dla testów)", expanded=False):
            current_energy = game_state.get("energy", 100)
            max_energy = game_state.get("max_energy", 100)
            
            st.info(f"Aktualna energia: **{current_energy}/{max_energy}**")
            
            new_energy = st.slider(
                "Ustaw energię:",
                min_value=0,
                max_value=max_energy,
                value=current_energy,
                step=5,
                key="energy_slider"
            )
            
            if st.button("💾 Zapisz energię", use_container_width=True):
                game_state["energy"] = new_energy
                update_fmcg_game_state_sql(st.session_state.username, game_state)
                st.success(f"✅ Energia ustawiona na {new_energy}")
                st.rerun()
        
        # Time controls
        with st.expander("📅 Kontrola czasu (tylko dla testów)", expanded=False):
            st.info(f"**Tydzień:** {game_state.get('current_week', 1)}/{game_state.get('total_weeks', 8)}")
            st.info(f"**Dzień:** {game_state.get('current_day', 'Monday')}")
            
            if st.button("⏭️ Następny dzień", use_container_width=True):
                # Simple day advance (without full end_day logic)
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                current_day = game_state.get("current_day", "Monday")
                current_week = game_state.get("current_week", 1)
                
                if current_day in days:
                    day_idx = days.index(current_day)
                    if day_idx < len(days) - 1:
                        game_state["current_day"] = days[day_idx + 1]
                    else:
                        # Next week
                        game_state["current_day"] = "Monday"
                        game_state["current_week"] = current_week + 1
                
                game_state["energy"] = game_state.get("max_energy", 100)
                update_fmcg_game_state_sql(st.session_state.username, game_state)
                st.success("✅ Przeszedłeś do kolejnego dnia")
                st.rerun()
        
        st.markdown("---")
        
        # Export/Import (future feature)
        st.markdown("### 💾 Backup i Eksport")
        st.info("🚧 Funkcja eksportu i importu gry będzie dostępna w przyszłych wersjach")
        
        # Display scenario info
        st.markdown("---")
        st.markdown("### ℹ️ Informacje o Scenariuszu")
        
        scenario_info = {
            "Scenariusz": scenario_name,
            "Firma": game_state.get("company_name", "N/A"),
            "Baza": f"{game_state.get('territory_name', 'N/A')} ({game_state.get('territory_latitude', 0):.4f}, {game_state.get('territory_longitude', 0):.4f})",
            "Promień": f"{game_state.get('radius_km', 15)} km",
            "Liczba klientów": len(clients),
            "Czas trwania": f"{game_state.get('total_weeks', 8)} tygodni",
            "Cel sprzedażowy": f"{game_state.get('sales_target', 0):,} PLN"
        }
        
        for key, value in scenario_info.items():
            st.markdown(f"**{key}:** {value}")
        
        # SCENARIO OBJECTIVES DETAILS
        st.markdown("---")
        st.markdown("### 🎯 Cele Scenariusza - Szczegóły")
        
        if is_heinz_scenario:
            st.markdown("**📋 Heinz Food Service Challenge - 3 Kluczowe Cele**")
            st.markdown("")
            
            # Objective 1: Numeric Distribution
            with st.expander("🎯 **CEL 1: Dystrybucja Numeryczna - 15/25 punktów (60%)**", expanded=False):
                st.markdown("""
                **Nagroda:** 💰 3,000 PLN  
                **Priorytet:** 🔴 CRITICAL
                
                **Opis:**  
                Zdobądź co najmniej **15 aktywnych punktów sprzedaży** z 25 dostępnych w regionie Dzięgielów. 
                To oznacza 60% dystrybucji numerycznej portfolio Heinz (Heinz Premium + Pudliszki Value).
                
                **Jak to osiągnąć:**
                - ✅ Podpisz umowy z 15 różnymi lokalami Food Service
                - ✅ Każdy aktywny klient liczy się jako 1 punkt dystrybucji
                - ✅ Nieważne czy kupują Heinz, Pudliszki, czy obie marki
                
                **Strategia:**
                - Zacznij od **Easy Wins** (klienci już znający markę)
                - Przejmuj klientów od konkurencji (szczególnie Kotlin)
                - Wykorzystaj portfolio play: Pudliszki dla budżetowych, Heinz dla premium
                
                **Wskaźnik sukcesu:**  
                Liczba aktywnych klientów ≥ 15 → ✅ Cel osiągnięty
                """)
            
            # Objective 2: Monthly Sales
            with st.expander("💰 **CEL 2: Sprzedaż Miesięczna - 15,000 PLN**", expanded=False):
                st.markdown("""
                **Nagroda:** 💰 2,500 PLN  
                **Priorytet:** 🟠 HIGH
                
                **Opis:**  
                Osiągnij łączną sprzedaż na poziomie **15,000 PLN** w skali miesiąca. 
                Liczy się suma przychodów z obu marek: Heinz Premium + Pudliszki Value.
                
                **Jak to osiągnąć:**
                - 📦 Sprzedawaj regularnie do aktywnych klientów
                - 📈 Zwiększaj wielkość zamówień (volume play)
                - ⭐ Mix produktów: Heinz (wyższa marża) + Pudliszki (wyższy wolumen)
                
                **Przykładowa ścieżka do 15,000 PLN:**
                - 10 klientów × 1,500 PLN/miesiąc = 15,000 PLN
                - LUB: 6 premium (Heinz, ~2,000 PLN) + 8 value (Pudliszki, ~750 PLN) = 18,000 PLN
                
                **Strategia:**
                - Priorytetyzuj klientów z wysokim **potencjałem** (kg/mies)
                - Dystrybutorzy = duże wolumeny (100+ kg/mies)
                - Upselluj: jeśli klient kupuje Pudliszki, zaproponuj Heinz na menu premium
                
                **Wskaźnik sukcesu:**  
                Suma sprzedaży miesięcznej ≥ 15,000 PLN → ✅ Cel osiągnięty
                """)
            
            # Objective 3: Beat Kotlin
            with st.expander("🥊 **CEL 3: Przejęcia z Kotlin - 6 wygranych**", expanded=False):
                st.markdown("""
                **Nagroda:** 💰 1,500 PLN  
                **Priorytet:** 🟡 MEDIUM
                
                **Opis:**  
                Przejmij **co najmniej 6 klientów** od konkurencji - marki **Kotlin**. 
                Kotlin ma obecnie 8 klientów w Twoim regionie - Twój cel to zdobyć 6 z nich.
                
                **Jak to osiągnąć:**
                - 🔍 Zidentyfikuj klientów używających Kotlin (oznaczeni w bazie)
                - 💬 Użyj technik sprzedażowych: FOZ, Kompensacja, Perspektywizacja
                - 🎯 Pokaż przewagę: jakość Heinz vs Kotlin, polska marka Pudliszki
                
                **Klienci Kotlin (8 total - cel: 6 wins):**
                1. Burger Station (price sensitive - target: Pudliszki)
                2. Hot Dog Heaven (brand matters - target: Heinz)
                3. Kebab King (volume play - target: Pudliszki)
                4. Kebab Express (delivery issues - EASY WIN)
                5. Burger Craft (mix suppliers - chce uprościć)
                6. Bar Mleczny Smaczek (no-name currently)
                7. Stołówka Zakładowa (kontrakt wygasa)
                8. Pizza House (niespójna jakość - EASY WIN)
                
                **Strategia:**
                - Start od najłatwiejszych: Kebab Express (problemy z dostawami), Pizza House (jakość)
                - Nie musisz sprzedawać Heinz - **Pudliszki też się liczy!**
                - Argument: "Kotlin to marka niszowa, Pudliszki/Heinz = узнаваемость"
                
                **Wskaźnik sukcesu:**  
                Liczba przejętych klientów od Kotlin ≥ 6 → ✅ Cel osiągnięty
                """)
            
            st.info("💡 **Tip:** Wszystkie 3 cele są niezależne - możesz je realizować równolegle. Priorytetyzuj według nagród i Twojego stylu gry!")
        
        else:
            # Standard scenarios (Quick Start, Lifetime)
            st.markdown("**🚀 Podstawowe Cele - Quick Start / Lifetime**")
            st.markdown("")
            
            with st.expander("🎯 **CEL 1: Aktywni Klienci - 10 punktów**", expanded=False):
                st.markdown("""
                **Opis:** Zdobądź co najmniej 10 aktywnych klientów w swoim portfolio.
                
                **Jak to osiągnąć:**
                - Odwiedzaj prospectów i przekonuj ich do współpracy
                - Używaj różnych technik sprzedażowych
                - Dbaj o relacje z klientami (reputation)
                """)
            
            with st.expander("📦 **CEL 2: Dywersyfikacja Produktowa - 15 różnych produktów**", expanded=False):
                st.markdown("""
                **Opis:** Sprzedaj co najmniej 15 różnych produktów ze swojego portfolio.
                
                **Jak to osiągnąć:**
                - Oferuj różnorodne produkty różnym klientom
                - Dostosuj ofertę do potrzeb segmentu
                - Cross-selling i upselling
                """)
            
            with st.expander("⭐ **CEL 3: Satysfakcja Klientów - Średnia reputacja +50**", expanded=False):
                st.markdown("""
                **Opis:** Utrzymaj średnią reputację na poziomie +50 punktów wśród aktywnych klientów.
                
                **Jak to osiągnąć:**
                - Regularnie odwiedzaj klientów
                - Dotrzymuj obietnic
                - Rozwiązuj problemy szybko i skutecznie
                """)

    
    # =============================================================================
    # DEBUG INFO (collapsible)
    # =============================================================================
    
    with st.expander("🔧 Debug Info"):
        st.json({
            "game_state": {
                "energy": game_state.get("energy"),
                "current_day": game_state.get("current_day"),
                "current_week": game_state.get("current_week"),
                "monthly_sales": game_state.get("monthly_sales"),
                "clients_prospect": game_state.get("clients_prospect"),
                "clients_active": game_state.get("clients_active"),
                "clients_lost": game_state.get("clients_lost")
            },
            "clients_count": len(clients),
            "status_summary": status_summary
        })
