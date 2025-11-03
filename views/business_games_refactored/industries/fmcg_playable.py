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
from streamlit_folium import st_folium
import html
import os
import base64

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


def _render_product_details(product: Dict):
    """
    Renderuje szczegółowy widok produktu ze storytellingiem i argumentami
    
    Args:
        product: Dict z danymi produktu (z FRESHLIFE_PRODUCTS lub COMPETITOR_PRODUCTS)
    """
    is_freshlife = product.get("brand") == "FreshLife"
    
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
    scenario_titles = {
        "quick_start": "🚀 Quick Start - Piaseczno Territory",
        "heinz_food_service": "🍅 Heinz Food Service Challenge - Dzięgielów",
        "lifetime": "♾️ Lifetime Mode - Unlimited"
    }
    
    st.title("🛒 FMCG Sales Simulator")
    st.caption(scenario_titles.get(scenario_id, "Junior Sales Representative"))
    
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
    # DASHBOARD - TOP METRICS
    # =============================================================================
    
    st.markdown("---")
    st.subheader("📊 Dashboard")
    
    # Energy bar
    energy_pct = game_state.get("energy", 100)
    energy_color = "#10b981" if energy_pct > 50 else "#f59e0b" if energy_pct > 25 else "#ef4444"
    
    st.markdown(f"""
    <div style='background: white; padding: 16px; border-radius: 12px; border-left: 4px solid {energy_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 16px;'>
        <div style='color: #64748b; font-size: 14px; font-weight: 600; margin-bottom: 8px;'>⚡ ENERGIA</div>
        <div style='background: #e2e8f0; border-radius: 8px; height: 24px; overflow: hidden; position: relative;'>
            <div style='background: {energy_color}; height: 100%; width: {energy_pct}%; transition: width 0.3s;'></div>
            <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #1e293b; font-size: 14px;'>{energy_pct}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    status_summary = get_client_status_summary(clients)
    
    with col1:
        st.metric("🔓 PROSPECT", status_summary.get("PROSPECT", 0))
    
    with col2:
        st.metric("✅ ACTIVE", status_summary.get("ACTIVE", 0))
    
    with col3:
        st.metric("❌ LOST", status_summary.get("LOST", 0))
    
    with col4:
        st.metric("💰 Sprzedaż", f"{game_state.get('monthly_sales', 0):,} PLN")
    
    # Day & Week info
    col_day, col_week, col_tasks = st.columns(3)
    
    with col_day:
        current_day = game_state.get("current_day", "Monday")
        day_emoji = {"Monday": "1️⃣", "Tuesday": "2️⃣", "Wednesday": "3️⃣", "Thursday": "4️⃣", "Friday": "5️⃣"}
        st.info(f"{day_emoji.get(current_day, '📅')} Dzień: **{current_day}**")
    
    with col_week:
        current_week = game_state.get("current_week", 1)
        visits_this_week = game_state.get("visits_this_week", 0)
        st.info(f"📅 Tydzień: **{current_week}** | Wizyty: **{visits_this_week}**")
    
    with col_tasks:
        tasks_completed_count = 3 - get_pending_tasks_count(st.session_state)
        all_done = all_tasks_completed(st.session_state)
        
        if all_done:
            st.success(f"✅ Zadania: **3/3** ukończone")
        else:
            # Check if in trial period
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            current_day = game_state.get("current_day", "Monday")
            day_index = day_names.index(current_day) if current_day in day_names else 0
            is_trial = (current_week == 1 and day_index < 2)
            
            if is_trial:
                st.warning(f"⏰ Zadania: **{tasks_completed_count}/3** (Trial: dzień {day_index + 1}/2)")
            else:
                st.error(f"❗ Zadania: **{tasks_completed_count}/3** (Wymagane do wizyt!)")
    
    # =============================================================================
    # TABS NAVIGATION (REFACTORED - 5 głównych zakładek)
    # =============================================================================
    
    st.markdown("---")
    
    # Liczba zadań do wykonania
    pending_tasks = get_pending_tasks_count(st.session_state)
    tasks_badge = f" ({pending_tasks})" if pending_tasks > 0 else ""
    
    tab_dashboard, tab_sales, tab_hr, tab_settings = st.tabs([
        f"📊 Dashboard{tasks_badge}",
        "🎯 Sprzedaż",
        "👥 HR & Team",
        "⚙️ Ustawienia"
    ])
    
    # =============================================================================
    # TAB: DASHBOARD
    # =============================================================================
    
    with tab_dashboard:
        st.subheader("📈 Podsumowanie Tygodnia")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric(
                "🎯 Cel sprzedażowy",
                f"{game_state.get('monthly_sales', 0):,} PLN",
                delta=f"{game_state.get('monthly_sales', 0) - 50000:,} PLN" if game_state.get('monthly_sales', 0) < 50000 else "Cel osiągnięty! 🎉"
            )
        
        with col_m2:
            avg_order = game_state.get('monthly_sales', 0) / max(visits_this_week, 1)
            st.metric(
                "💰 Średnie zamówienie",
                f"{avg_order:,.0f} PLN"
            )
        
        with col_m3:
            st.metric(
                "📞 Wizyty w tym tygodniu",
                visits_this_week
            )
        
        st.markdown("---")
        
        # Client status breakdown
        st.subheader("👥 Status Klientów")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            st.info(f"""
            **🔓 PROSPECT**  
            {status_summary.get('PROSPECT', 0)} klientów
            
            _Potencjalni klienci do pozyskania_
            """)
        
        with col_s2:
            st.success(f"""
            **✅ ACTIVE**  
            {status_summary.get('ACTIVE', 0)} klientów
            
            _Aktywni klienci kupujący regularnie_
            """)
        
        with col_s3:
            st.error(f"""
            **❌ LOST**  
            {status_summary.get('LOST', 0)} klientów
            
            _Klienci, którzy przestali kupować_
            """)
        
        # =============================================================================
        # REPUTATION ALERTS - Critical clients at risk
        # =============================================================================
        
        st.markdown("---")
        
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
        st.subheader("🎯 Cele Tygodniowe")
        
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
        
        st.markdown("---")
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
        
        # =============================================================================
        # ALEX AI ASSISTANT STATUS
        # =============================================================================
        
        st.markdown("---")
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
        
        # =============================================================================
        # ZADANIA (ONBOARDING) - jako sekcja w Dashboard
        # =============================================================================
        
        st.markdown("---")
        
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
                
                # Determine icon and color based on status
                if task_status["status"] == "completed":
                    status_icon = "✅"
                    status_color = "#10b981"
                    button_text = "Ukończone"
                    button_disabled = True
                elif task_status["status"] == "submitted":
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
                        
                        if task_status.get("feedback"):
                            st.info(f"💬 Feedback: {task_status['feedback']}")
                    
                    elif task_status["status"] == "submitted":
                        st.warning("⏳ Zadanie złożone, oczekuje na weryfikację...")
                        
                        col_check, col_resubmit = st.columns([1, 1])
                        
                        with col_check:
                            if st.button("🔍 Sprawdź wynik", key=f"check_{task_id}", use_container_width=True):
                                # Simulate evaluation
                                feedback = get_static_feedback(task_id)
                                complete_task(st.session_state, task_id, feedback=feedback)
                                st.rerun()
                        
                        with col_resubmit:
                            if st.button("🔄 Złóż ponownie", key=f"resub_{task_id}", use_container_width=True):
                                st.session_state[f"{task_id}_submitted"] = False
                                st.rerun()
                    
                    else:
                        # Input area for submission
                        user_answer = st.text_area(
                            "Twoja odpowiedź:",
                            placeholder="Napisz krótkie podsumowanie tego, czego się nauczyłeś...",
                            key=f"answer_{task_id}",
                            height=100
                        )
                        
                        col_submit, col_skip = st.columns([2, 1])
                        
                        with col_submit:
                            if st.button(f"📤 Złóż zadanie", key=f"submit_{task_id}", type="primary", use_container_width=True):
                                if user_answer and len(user_answer) >= 10:
                                    submit_task(st.session_state, task_id, user_answer)
                                    st.success("✅ Zadanie złożone!")
                                    st.rerun()
                                else:
                                    st.error("❌ Odpowiedź zbyt krótka (min. 10 znaków)")
                        
                        with col_skip:
                            if st.button("⏭️ Pomiń", key=f"skip_{task_id}", use_container_width=True):
                                st.info("💡 Możesz wrócić do tego zadania później")
            
            # Summary at bottom
            st.markdown("---")
            st.info(f"""
            💡 **Status:** {3 - pending}/3 zadań ukończonych
            
            Po ukończeniu wszystkich zadań będziesz gotowy do efektywnej pracy w terenie!
            """)
        
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
        # NOTES PANEL IN DASHBOARD
        # =============================================================================
        
        st.markdown("---")
        st.subheader("📝 Notatnik")
        
        # Get user data for notes
        from data.users_new import get_current_user_data
        user_data = get_current_user_data(username)
        
        if user_data and "user_id" in user_data:
            # Render notes panel with unique key prefix
            render_notes_panel(
                user_id=user_data["user_id"],
                active_tab="product_card",
                key_prefix="fmcg_dashboard"
            )
        else:
            st.warning("⚠️ Nie można załadować notatek")
    
    # =============================================================================
    # TAB: SPRZEDAŻ (nowa - konsolidacja: Klienci + Rozmowa + Produkty)
    # =============================================================================
    
    with tab_sales:
        # Sub-tabs dla różnych widoków sprzedaży
        sales_tab_map, sales_tab_visit, sales_tab_products = st.tabs([
            "�️ Mapa & Klienci",
            "💬 Wizyta u klienta",
            "📦 Katalog produktów"
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
                # Check scenario - Heinz scenario has enhanced client view
                scenario_id = game_state.get("scenario_id", "").lower()
                is_heinz_scenario = "heinz" in scenario_id
            
                if is_heinz_scenario:
                    # =====================================================================
                    # HEINZ FOOD SERVICE - ENHANCED CLIENT VIEW
                    # =====================================================================
                    st.subheader("🍅 Heinz Food Service - Portfolio Klientów")
                    st.caption(f"25 punktów Food Service w regionie Dzięgielów • {len(clients)} total")
                
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
                    # SEKCJA 2: LISTA KLIENTÓW (kompaktowa)
                    # =====================================================================
                    st.markdown("### 📋 Lista klientów")
                    
                    for client_id, client in list(filtered_clients.items())[:10]:  # Pokazuj tylko pierwsze 10
                        name = client.get("name", client_id)
                        segment = client.get("segment", "mixed")
                        distance = client.get("distance_from_base", 0)
                        potential_kg = client.get("monthly_volume_kg", 0)
                        
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
                        
                        color_emoji = get_color_emoji_by_days(days_since_visit)
                        visit_text = f"{days_since_visit} dni" if days_since_visit is not None else "Nowy"
                        
                        # Segment emoji
                        segment_emoji = {"premium": "💜", "value": "💚", "mixed": "🧡"}.get(segment, "⚪")
                        
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"{segment_emoji} **{name}** • {distance:.1f}km • {potential_kg}kg/mies • {color_emoji} {visit_text}")
                        with col2:
                            if st.button("📞", key=f"visit_quick_{client_id}", help="Odwiedź klienta"):
                                st.session_state['show_client_detail'] = True
                                st.session_state['selected_client_id'] = client_id
                                st.rerun()
                    
                    if len(filtered_clients) > 10:
                        st.caption(f"... i {len(filtered_clients) - 10} więcej klientów (zobacz w tabeli poniżej)")
                    
                    st.markdown("---")
                    
                    # =====================================================================
                    # SEKCJA 3: TABS - MAPA | TABELA
                    # =====================================================================
                    view_tab_map, view_tab_table = st.tabs(["🗺️ Mapa", "📋 Szczegóły (tabela)"])
                    
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
                                    tooltip=f"⭐ #{route_number} - {name}"
                                ).add_to(m)
                            else:
                                # Regular colored pin by visit recency
                                folium.Marker(
                                    [lat, lon],
                                    popup=folium.Popup(popup_html, max_width=300),
                                    icon=folium.Icon(color=pin_color_by_time, icon="cutlery", prefix="fa"),
                                    tooltip=f"{color_emoji} {name} - {visit_status}"
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
                        # Table view with detailed info
                        for client_id, client in filtered_clients.items():
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
                                        <div style='font-size: 13px; color: #64748b; margin-bottom: 8px;'>
                                            👤 {owner} • 📍 {distance:.1f} km • {color_emoji} {visit_text} • 💼 MBTI: {personality}
                                        </div>
                                        <div style='display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px;'>
                                            <div style='background: #f1f5f9; padding: 6px 12px; border-radius: 6px; font-size: 12px;'>
                                                📦 Obecnie: <b>{current_supplier}</b>
                                            </div>
                                            <div style='background: #f1f5f9; padding: 6px 12px; border-radius: 6px; font-size: 12px;'>
                                                💰 Potencjał: <b>{potential_kg} kg/mies</b>
                                            </div>
                                            <div style='background: {upsell_color}; color: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;'>
                                                ⬆️ Upsell: {upsell_pot.upper()}
                                            </div>
                                        </div>
                                        <div style='margin-top: 8px; font-size: 12px; color: #64748b; font-style: italic;'>
                                            💡 Strategia: {recommended_strategy}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                            # Action button
                            if st.button(f"📞 Odwiedź {name}", key=f"visit_heinz_{client_id}", use_container_width=True):
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
                        reputation = client_data.get('reputation', 0)
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
                            reputation = client_data.get('reputation', 0)
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
                
                # Rest of visit code continues (full conversation, route planning, etc.)
        # Show congratulations if tasks completed during trial
        if tasks_completed and is_trial_period:
            st.success("""
            🎉 **Świetna robota!** Ukończyłeś wszystkie zadania onboardingowe w okresie próbnym.
                
            Jesteś gotowy do profesjonalnych wizyt z dobrze zaplanowaną strategią! 🚀
            """)
            
        # =================================================================
        # ROUTE PLANNING - Multi-select clients + optimization
        # =================================================================
            
        st.subheader("🗺️ Planowanie trasy")
            
        # Prepare client list with locations
        client_options = []
        for client_id, client in clients.items():
            client_options.append({
                "client_id": client_id,
                "name": client.get('name', client_id),
                "status": client.get('status', 'prospect'),
                "lat": client.get("latitude", 0),
                "lng": client.get("longitude", 0),
                "distance_from_base": client.get("distance_from_base", 0)
            })
            
        # Base location (territory center)
        base_location = {
            "lat": game_state.get("territory_latitude", 52.0846),
            "lng": game_state.get("territory_longitude", 21.0250)
        }
            
        # Multi-select clients
        selected_client_ids = st.multiselect(
            "Wybierz klientów do odwiedzenia dzisiaj (max 6):",
            options=[c["client_id"] for c in client_options],
            format_func=lambda x: next(
                f"{c['name']} ({c['status']}) - {c['distance_from_base']:.1f} km od bazy"
                for c in client_options if c['client_id'] == x
            ),
            max_selections=6,
            key="selected_clients_for_route"
        )
            
        if selected_client_ids:
            st.info(f"✅ Wybrano: {len(selected_client_ids)} klientów")
                
            # Get selected shops with locations
            selected_shops = [c for c in client_options if c["client_id"] in selected_client_ids]
                
            # =================================================================
            # ALEX ROUTE SUGGESTION
            # =================================================================
                
            st.markdown("---")
            st.subheader("🤖 Sugestia ALEX")
                
            # Import ALEX route planning
            from utils.fmcg_alex_training import suggest_route_with_alex, get_alex_stats
                
            # Get ALEX stats
            alex_level = game_state.get("alex_level", 0)
            alex_competencies = game_state.get("alex_competencies", {
                "planning": 0.0,
                "communication": 0.0,
                "analysis": 0.0,
                "relationship": 0.0,
                "negotiation": 0.0
            })
                
            alex_stats = get_alex_stats(alex_level)
                
            # Get ALEX suggestion
            alex_suggestion = suggest_route_with_alex(
                base_location=base_location,
                selected_shops=selected_shops,
                alex_level=alex_level,
                competencies=alex_competencies,
                clients_data=clients
            )
                
            # Calculate manual route (order of selection)
            manual_distance = calculate_route_distance(
                base_location,
                selected_shops,
                selected_client_ids
            )
            manual_energy = int(manual_distance * 1.0 + len(selected_client_ids) * 15)
                
            # Show ALEX suggestion card
            confidence_pct = alex_suggestion['confidence'] * 100
            savings_dist = alex_suggestion['savings_vs_manual']['distance_km']
            savings_time = alex_suggestion['savings_vs_manual']['time_minutes']
            savings_energy = alex_suggestion['savings_vs_manual']['energy_percent']
                
            alex_route_card_html = f"""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;'>
    <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
    <div style='font-size: 36px;'>{alex_stats['emoji']}</div>
    <div>
        <div style='font-size: 18px; font-weight: 700;'>ALEX {alex_stats['name_pl']}</div>
        <div style='font-size: 13px; opacity: 0.9;'>Pewność sugestii: {confidence_pct:.0f}%</div>
    </div>
    </div>
    <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; text-align: center;'>
        <div>
            <div style='font-size: 11px; opacity: 0.8;'>Dystans</div>
            <div style='font-size: 20px; font-weight: 700;'>{alex_suggestion['distance_km']} km</div>
        </div>
        <div>
            <div style='font-size: 11px; opacity: 0.8;'>Czas</div>
            <div style='font-size: 20px; font-weight: 700;'>{alex_suggestion['time_minutes']} min</div>
        </div>
        <div>
            <div style='font-size: 11px; opacity: 0.8;'>Energia</div>
            <div style='font-size: 20px; font-weight: 700;'>~{alex_suggestion['energy_cost']}%</div>
        </div>
    </div>
    </div>
    <div style='background: rgba(16, 185, 129, 0.2); padding: 10px; border-radius: 6px; border-left: 3px solid #10b981;'>
    <div style='font-size: 12px; font-weight: 600; margin-bottom: 4px;'>💡 Oszczędności vs Twoja kolejność:</div>
    <div style='font-size: 13px;'>
        📏 {savings_dist:.1f} km | 
        ⏱️ {savings_time} min | 
        ⚡ ~{savings_energy}% energii
    </div>
    </div>
</div>"""
                
            st.markdown(alex_route_card_html, unsafe_allow_html=True)
                
            # Show alerts if any
            if alex_suggestion['alerts']:
                for alert in alex_suggestion['alerts']:
                    st.warning(alert)
                
            # Show reasoning in expander
            with st.expander("💭 Dlaczego ALEX sugeruje tę kolejność?", expanded=False):
                st.markdown(alex_suggestion['reasoning'])
                
            # Show comparison: Manual vs ALEX
            st.markdown("---")
            st.markdown("### 📊 Porównanie tras")
                
            col_manual, col_alex = st.columns(2)
                
            with col_manual:
                st.markdown("**📋 Twoja kolejność**")
                st.caption("(porządek wyboru)")
                for idx, client_id in enumerate(selected_client_ids, 1):
                    shop = next(c for c in selected_shops if c["client_id"] == client_id)
                    st.markdown(f"{idx}. {shop['name']}")
                    
                st.metric("📏 Dystans", f"{manual_distance:.1f} km")
                st.metric("⚡ Energia", f"~{manual_energy}%")
                
            with col_alex:
                st.markdown(f"**🤖 Sugestia ALEX** {alex_stats['emoji']}")
                st.caption(f"({alex_stats['name_pl']} - {alex_suggestion['confidence']*100:.0f}% pewności)")
                for idx, client_id in enumerate(alex_suggestion['suggested_order'], 1):
                    shop = next((c for c in selected_shops if c["client_id"] == client_id), None)
                    if shop:
                        st.markdown(f"{idx}. {shop['name']}")
                    
                st.metric("📏 Dystans", f"{alex_suggestion['distance_km']} km")
                st.metric("⚡ Energia", f"~{alex_suggestion['energy_cost']}%")
                    
                if alex_suggestion['distance_km'] < manual_distance:
                    savings = manual_distance - alex_suggestion['distance_km']
                    st.success(f"💡 -{savings:.1f} km")
                
            # Choose route
            st.markdown("---")
            st.markdown("### 🎯 Wybierz trasę")
                
            col_choice1, col_choice2 = st.columns(2)
                
            with col_choice1:
                if st.button("📋 Użyj mojej kolejności", use_container_width=True):
                    st.session_state.planned_route = selected_client_ids
                    st.session_state.route_optimized = False
                    st.session_state.used_alex_suggestion = False
                    st.success("✅ Zaplanowano trasę w Twojej kolejności")
                    st.rerun()
                
            with col_choice2:
                if st.button(f"🤖 Użyj sugestii ALEX {alex_stats['emoji']}", use_container_width=True, type="primary"):
                    st.session_state.planned_route = alex_suggestion['suggested_order']
                    st.session_state.route_optimized = True
                    st.session_state.used_alex_suggestion = True
                    st.session_state.alex_route_confidence = alex_suggestion['confidence']
                    st.success(f"✅ ALEX {alex_stats['name_pl']} zaplanował trasę!")
                    st.rerun()
            
        # =================================================================
        # EXECUTE PLANNED VISITS
        # =================================================================
            
        if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
            st.markdown("---")
            st.subheader("🚗 Wykonaj wizyty")
            
            # Flatten planned_route to ensure it contains only strings
            if isinstance(st.session_state.planned_route, list):
                flat_route = []
                for item in st.session_state.planned_route:
                    if isinstance(item, str):
                        flat_route.append(item)
                    elif isinstance(item, list):
                        flat_route.extend([x for x in item if isinstance(x, str)])
                st.session_state.planned_route = flat_route
                
            planned_route = st.session_state.planned_route
            current_visit_idx = getattr(st.session_state, 'current_visit_idx', 0)
                
            if current_visit_idx >= len(planned_route):
                st.success("🎉 Wszystkie zaplanowane wizyty wykonane!")
                    
                if st.button("🔄 Zaplanuj nową trasę"):
                    del st.session_state.planned_route
                    del st.session_state.current_visit_idx
                    st.rerun()
            else:
                # Show progress
                st.progress(current_visit_idx / len(planned_route), text=f"Wizyta {current_visit_idx + 1} / {len(planned_route)}")
                    
                # Current visit - validate it's a string
                route_client_id = planned_route[current_visit_idx]
                if not isinstance(route_client_id, str):
                    st.error(f"❌ Błąd: nieprawidłowe ID klienta w trasie (pozycja {current_visit_idx})")
                    if st.button("🗑️ Wyczyść trasę i zacznij od nowa"):
                        st.session_state.planned_route = []
                        if hasattr(st.session_state, 'current_visit_idx'):
                            del st.session_state.current_visit_idx
                        st.rerun()
                    st.stop()
                
                if route_client_id not in clients:
                    st.error(f"❌ Błąd: klient {route_client_id} nie istnieje")
                    if st.button("🗑️ Wyczyść trasę i zacznij od nowa"):
                        st.session_state.planned_route = []
                        if hasattr(st.session_state, 'current_visit_idx'):
                            del st.session_state.current_visit_idx
                        st.rerun()
                    st.stop()
                
                selected_client = clients[route_client_id]
                selected_client_id = route_client_id  # Set for use in conversation code
                    
                st.info(f"📍 Obecnie: **{selected_client['name']}** (wizyta {current_visit_idx + 1}/{len(planned_route)})")
                    
                # Calculate distance from current location
                current_location = game_state.get("current_location")
                if current_location is None:
                    # First visit - from base
                    distance = selected_client.get("distance_from_base", 0)
                else:
                    # From previous visit
                    distance = calculate_distance_between_points(
                        current_location["lat"], current_location["lng"],
                        selected_client.get("latitude", 0), selected_client.get("longitude", 0)
                    )
                    
                travel_time = calculate_travel_time(distance)
                visit_duration = 45  # Default
                energy_cost = calculate_visit_energy_cost(distance, visit_duration)
                    
                col_preview1, col_preview2, col_preview3 = st.columns(3)
                    
                with col_preview1:
                    st.metric("🚗 Dojazd", f"{travel_time} min")
                    
                with col_preview2:
                    st.metric("⏱️ Wizyta", f"{visit_duration} min")
                    
                with col_preview3:
                    st.metric("⚡ Koszt energii", f"{energy_cost}%")
            
            # =================================================================
            # AUTOPILOT OPTION
            # =================================================================
                
            st.markdown("---")
            st.subheader("🤖 Opcja Autopilota ALEX")
                
            # Import ALEX functions
            from utils.fmcg_alex_training import (
                get_alex_stats,
                get_autopilot_penalty,
                get_autopilot_capacity,
                simulate_autopilot_visit,
                ALEX_LEVELS
            )
                
            # Get ALEX stats
            alex_level = game_state.get("alex_level", 0)
            alex_training_points = game_state.get("alex_training_points", 0)
            alex_competencies = game_state.get("alex_competencies", {
                "planning": 0.0,
                "communication": 0.0,
                "analysis": 0.0,
                "relationship": 0.0,
                "negotiation": 0.0
            })
            autopilot_visits_this_week = game_state.get("autopilot_visits_this_week", 0)
                
            alex_stats = get_alex_stats(alex_level)
            penalty = get_autopilot_penalty(alex_level, alex_competencies)
            capacity = get_autopilot_capacity(alex_level, visits_this_week)
                
            # Show ALEX status
            with st.expander(f"ℹ️ Status ALEX: {alex_stats['emoji']} {alex_stats['name_pl']}", expanded=False):
                col_a1, col_a2, col_a3 = st.columns(3)
                    
                with col_a1:
                    st.metric("🎓 Poziom", f"{alex_level}/4")
                    st.caption(f"{alex_stats['name_pl']}")
                    
                with col_a2:
                    st.metric("⚡ Kompetencja", f"{int(alex_stats['competence']*100)}%")
                    st.caption(f"Penalty: {penalty:+.0f}%")
                    
                with col_a3:
                    st.metric("📊 Limit wizyt/dzień", f"{alex_stats['visits_per_day']}")
                    st.caption(f"Max/tydzień: {capacity['max_autopilot_per_week']}")
                    
                st.info(f"""
                💡 **Co to jest Autopilot ALEX?**
                    
                ALEX to Twój AI Sales Assistant, który może wykonywać rutynowe wizyty za Ciebie.
                    
                **Zalety:**
                - ⏱️ Oszczędność czasu (30 min vs 45-60 min)
                - 🔄 Możliwość skupienia się na trudniejszych klientach
                - 📈 Więcej wizyt dziennie
                    
                **Wady:**
                - ⚠️ Penalty na wyniki: {penalty:+.0f}% (mniejsze zamówienia, wolniejszy wzrost reputacji)
                - 🚫 Brak odkryć o kliencie (autopilot nie prowadzi pogłębionej rozmowy)
                - 📊 Limit: max {capacity['max_autopilot_per_week']} wizyt/tydzień (50% wszystkich)
                    
                **💡 Tip:** Trenuj ALEX w zakładce "🤖 ALEX Training" aby zmniejszyć penalty!
                """)
                
            # Check if autopilot available
            can_use_autopilot = autopilot_visits_this_week < capacity['max_autopilot_per_week']
                
            if not can_use_autopilot:
                st.warning(f"""
                🚫 **Limit autopilota wyczerpany w tym tygodniu**
                    
                Wykorzystałeś: {autopilot_visits_this_week}/{capacity['max_autopilot_per_week']} wizyt autopilota.
                Musisz wykonać tę wizytę manualnie.
                """)
                use_autopilot = False
            else:
                # Checkbox dla autopilota
                use_autopilot = st.checkbox(
                    f"🤖 Użyj autopilota ALEX ({autopilot_visits_this_week}/{capacity['max_autopilot_per_week']} wykorzystanych)",
                    value=False,
                    help=f"ALEX wykona wizytę za Ciebie. Penalty: {penalty:+.0f}%, Oszczędność czasu: ~15-30 min"
                )
                    
                if use_autopilot:
                    st.info(f"""
                    🤖 **Autopilot aktywny**
                        
                    ALEX {alex_stats['emoji']} ({alex_stats['name_pl']}) wykona wizytę w {selected_client['name']}.
                        
                    **Przewidywane wyniki:**
                    - 📦 Zamówienie: ~{int(selected_client.get('potential_monthly', 1000) / 4 * (1 + penalty/100))} PLN (penalty: {penalty:+.0f}%)
                    - ⭐ Reputacja: +{max(1, int(5 * (1 + penalty/100)))}
                    - ⏱️ Czas: 30 min (oszczędność: ~20 min)
                    - ⚡ Energia: ~25%
                        
                    Kliknij przycisk poniżej aby ALEX rozpoczął wizytę.
                    """)
            
            # =================================================================
            # AI CONVERSATION INTERFACE
            # =================================================================
            
            st.markdown("---")
                
            # Show different interface based on autopilot choice
            if use_autopilot:
                st.subheader("🤖 ALEX wykonuje wizytę...")
                    
            if st.button("▶️ Rozpocznij wizytę autopilota", type="primary"):
                with st.spinner(f"🤖 ALEX odwiedza {selected_client['name']}..."):
                    time.sleep(2)  # Symulacja wizyty
                        
                    # Symuluj wizytę
                    autopilot_result = simulate_autopilot_visit(
                        client_data=selected_client,
                        player_stats={"level": game_state.get("level", 1)},
                        alex_level=alex_level,
                        competencies=alex_competencies
                    )
                        
                    # Update client data
                    selected_client["reputation"] = selected_client.get("reputation", 0) + autopilot_result["reputation_change"]
                    selected_client["total_sales"] = selected_client.get("total_sales", 0) + autopilot_result["order_value"]
                    selected_client["last_visit_date"] = datetime.now().isoformat()
                    selected_client["visits_count"] = selected_client.get("visits_count", 0) + 1
                        
                    # Promote to ACTIVE if was PROSPECT
                    if selected_client.get("status", "PROSPECT") == "PROSPECT":
                        selected_client["status"] = "ACTIVE"
                        selected_client["status_since"] = datetime.now().isoformat()
                        
                    # Update game state
                    game_state["energy"] -= autopilot_result["energy_cost"]
                    game_state["monthly_sales"] = game_state.get("monthly_sales", 0) + autopilot_result["order_value"]
                    game_state["weekly_actual_sales"] = game_state.get("weekly_actual_sales", 0) + autopilot_result["order_value"]
                    game_state["monthly_actual_sales"] = game_state.get("monthly_actual_sales", 0) + autopilot_result["order_value"]
                    game_state["visits_this_week"] += 1
                    game_state["autopilot_visits_count"] = game_state.get("autopilot_visits_count", 0) + 1
                    game_state["autopilot_visits_this_week"] = autopilot_visits_this_week + 1
                        
                    # Update current location
                    game_state["current_location"] = {
                        "lat": selected_client.get("latitude", 0),
                        "lng": selected_client.get("longitude", 0)
                    }
                        
                    # Save to database (function imported at top of file)
                    update_fmcg_game_state_sql(username, game_state, clients)
                        
                    # Move to next visit
                    st.session_state.current_visit_idx = current_visit_idx + 1
                        
                    # Show results
                    st.success("✅ Wizyta autopilota zakończona!")
                    st.markdown(autopilot_result["summary"])
                        
                    # Show comparison
                    st.markdown("---")
                    st.markdown("### 📊 Porównanie z wizytą manualną")
                        
                    col_comp1, col_comp2 = st.columns(2)
                        
                    with col_comp1:
                        st.markdown("**🤖 Autopilot (ALEX)**")
                        st.metric("📦 Zamówienie", f"{autopilot_result['order_value']} PLN")
                        st.metric("⭐ Reputacja", f"+{autopilot_result['reputation_change']}")
                        st.metric("⏱️ Czas", "30 min")
                        st.metric("⚡ Energia", f"-{autopilot_result['energy_cost']}%")
                        
                    with col_comp2:
                        manual_order = int(selected_client.get('potential_monthly', 1000) / 4)
                        manual_rep = 5
                        st.markdown("**👤 Wizyta manualna (szacunkowo)**")
                        st.metric("📦 Zamówienie", f"~{manual_order} PLN")
                        st.metric("⭐ Reputacja", f"+{manual_rep}")
                        st.metric("⏱️ Czas", "45-60 min")
                        st.metric("⚡ Energia", f"-{energy_cost}%")
                        
                    time.sleep(3)
                    st.rerun()
                
            else:
                # Manual visit - normal AI conversation
                st.subheader("💬 Rozmowa z klientem")
                
                # Show conversation history if exists
                from utils.fmcg_mechanics import get_client_conversation_history
            
                try:
                    history = get_client_conversation_history(
                        username=username,
                        client_id=selected_client_id,
                        limit=3
                    )
                except Exception as e:
                    print(f"Error loading history: {e}")
                    history = []
            
                if history:
                    with st.expander(f"📜 Historia wizyt ({len(history)} ostatnich)", expanded=False):
                        for idx, visit in enumerate(history, 1):
                            st.markdown(f"""
                            **Wizyta #{idx}** ({visit['date']})  
                            ⭐ Jakość: {visit['quality']}/5 | 💰 Zamówienie: {visit['order_value']} PLN  
                            📝 {visit['summary']}
                            """)
                        
                            if visit.get('key_points'):
                                st.markdown("**Kluczowe ustalenia:**")
                                for point in visit['key_points']:
                                    st.markdown(f"- {point}")
                            
                            # Show order details if available
                            if visit.get('order_items'):
                                st.markdown("**📦 Zamówione produkty:**")
                                for item in visit['order_items']:
                                    st.markdown(f"- {item['name']} ({item['brand']}) × {item['quantity']} = {item['value']:.2f} PLN")
                                if visit.get('order_margin'):
                                    st.markdown(f"_💵 Marża: {visit['order_margin']:.2f} PLN_")
                            
                            # Show tools used
                            if visit.get('tools_used'):
                                tool_names = {
                                    'gratis': '🎁 Gratis/próbki',
                                    'rabat': '💰 Rabat',
                                    'pos_material': '📄 Materiały POS (ulotki, plakaty)',
                                    'promocja': '🎯 Promocja',
                                    'free_delivery': '🚚 Darmowa dostawa'
                                }
                                tools_desc = [tool_names.get(tool, tool) for tool in visit['tools_used']]
                                st.markdown(f"**🛠️ Użyte narzędzia:** {', '.join(tools_desc)}")
                            
                            # Show manager feedback if available
                            if visit.get('manager_feedback'):
                                st.markdown("---")
                                st.markdown("**👔 Feedback menedżerski (FUKO):**")
                                for area_idx, area_feedback in enumerate(visit['manager_feedback'], 1):
                                    with st.expander(f"Obszar {area_idx}: {area_feedback['area']}"):
                                        st.markdown(f"**Fakty:** {area_feedback['fakty']}")
                                        st.markdown(f"**Ustosunkowanie:** {area_feedback['ustosunkowanie']}")
                                        st.markdown(f"**Konsekwencje:** {area_feedback['konsekwencje']}")
                                        st.markdown(f"**Oczekiwania:** {area_feedback['oczekiwania']}")
                            
                            # Show conversation transcript if available
                            if visit.get('conversation_transcript'):
                                st.markdown("---")
                                with st.expander("💬 Transkrypcja rozmowy"):
                                    st.markdown("_Pełny zapis rozmowy - możesz wykorzystać do analizy lub konsultacji z mentorem_")
                                    st.markdown("")
                                    for msg_idx, msg in enumerate(visit['conversation_transcript'], 1):
                                        role_emoji = "🙋‍♂️" if msg['role'] == "Ja" else "👤"
                                        msg_role = msg['role']
                                        msg_content = html.escape(msg['content'])
                                        bg_color = "#e3f2fd" if msg_role == "Ja" else "#f5f5f5"
                                        
                                        st.markdown(f"""
                                        <div style='background: {bg_color}; 
                                                    padding: 12px; border-radius: 8px; margin: 8px 0;'>
                                            <b>{role_emoji} {msg_role}:</b><br>
                                            {msg_content}
                                        </div>
                                        """, unsafe_allow_html=True)
                        
                            if idx < len(history):
                                st.markdown("---")
            
                # =================================================================
                # COACHING ON-THE-JOB OPTION
                # =================================================================
            
                # Check if manager coaching available this week
                current_week = game_state.get("current_week", 1)
                coaching_visits_this_week = game_state.get("coaching_visits_this_week", 0)
                    
                # First week: 2 coaching visits allowed
                max_coaching_visits = 2 if current_week == 1 else 0
                    
                coaching_available = coaching_visits_this_week < max_coaching_visits
                    
                if coaching_available:
                    with_manager = st.checkbox(
                    f"🎓 Wizyta rozwojowa z menedżerem ({coaching_visits_this_week}/{max_coaching_visits} wykorzystanych w tym tygodniu)",
                    value=False,
                        help="Menedżer będzie obserwował wizytę i udzieli feedbacku rozwojowego w formule FUKO"
                    )
                else:
                    with_manager = False
                    if current_week == 1:
                        st.info(f"ℹ️ Wykorzystałeś już wszystkie wizyty rozwojowe w tym tygodniu ({max_coaching_visits}/{max_coaching_visits})")
            
                st.markdown("---")
            
                # Initialize conversation state for this client
                conv_key = f"fmcg_conv_{selected_client_id}"
                if conv_key not in st.session_state:
                    st.session_state[conv_key] = {
                        "messages": [],
                        "started": False,
                        "finished": False
                    }
            
                conversation_state = st.session_state[conv_key]                # Start conversation button
            if not conversation_state["started"]:
                if st.button("🚀 Rozpocznij rozmowę", type="primary"):
                    # Load conversation history for this client
                    from utils.fmcg_mechanics import get_client_conversation_history
                    
                    conversation_history = get_client_conversation_history(
                        username=username,
                        client_id=selected_client_id,
                        limit=5
                    )
                    
                    conversation_state["started"] = True
                    conversation_state["messages"] = []
                    conversation_state["finished"] = False
                    conversation_state["history"] = conversation_history  # Store for AI
                    conversation_state["with_manager"] = with_manager  # Store coaching flag
                    
                    # Add welcome message from AI
                    from utils.fmcg_ai_conversation import conduct_fmcg_conversation
                    
                    welcome_msg = f"Dzień dobry! Witam w {selected_client['name']}."
                    conversation_state["messages"].append({
                        "role": "assistant",
                        "content": welcome_msg,
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
            
            # Display conversation
            if conversation_state["started"] and not conversation_state["finished"]:
                    
                # Show manager observation notice
                if conversation_state.get("with_manager"):
                    st.info("👔 **Wizyta rozwojowa:** Twój menedżer obserwuje rozmowę i przygotuje feedback rozwojowy.")
                    
                # Show messages
                for msg in conversation_state["messages"]:
                    # Escape HTML to prevent injection
                    safe_content = html.escape(msg['content'])
                    
                    if msg["role"] == "player":
                        st.markdown(f"""
                        <div style='background: #e3f2fd; padding: 12px; border-radius: 8px; margin: 8px 0;'>
                            <b>🧑 Ty:</b> {safe_content}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='background: #f5f5f5; padding: 12px; border-radius: 8px; margin: 8px 0;'>
                            <b>👤 {selected_client.get('owner', 'Właściciel')}:</b> {safe_content}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Player input with audio option
                st.markdown("### 💬 Twoja odpowiedź:")
                    
                # Initialize session state for transcription
                transcription_key = f"fmcg_transcription_{selected_client_id}"
                if transcription_key not in st.session_state:
                    st.session_state[transcription_key] = ""
                    
                transcription_version_key = f"fmcg_transcription_version_{selected_client_id}"
                if transcription_version_key not in st.session_state:
                    st.session_state[transcription_version_key] = 0
                    
                last_audio_hash_key = f"fmcg_audio_hash_{selected_client_id}"
                if last_audio_hash_key not in st.session_state:
                    st.session_state[last_audio_hash_key] = None
                    
                # Audio input first (to process before text_area renders)
                audio_data = st.audio_input(
                    "🎤 Nagraj audio (opcjonalnie):",
                    key=f"fmcg_audio_{selected_client_id}"
                )
                    
                # Process audio if available
                if audio_data is not None:
                    try:
                        import hashlib
                        import speech_recognition as sr
                        import tempfile
                        from pydub import AudioSegment
                    except ImportError:
                        st.warning("⚠️ Moduły rozpoznawania mowy nie są zainstalowane. Funkcja audio niedostępna.")
                        audio_data = None
                    
                if audio_data is not None:
                    # Check if this is new audio
                    audio_bytes = audio_data.getvalue()
                    current_audio_hash = hashlib.md5(audio_bytes).hexdigest()
                        
                    if current_audio_hash != st.session_state[last_audio_hash_key]:
                        # New audio - process it!
                        st.session_state[last_audio_hash_key] = current_audio_hash
                            
                        with st.spinner("🤖 Rozpoznaję mowę i dodaję interpunkcję..."):
                            try:
                                # Save audio to temp file
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                                    tmp_file.write(audio_bytes)
                                    tmp_path = tmp_file.name
                                    
                                wav_path = None
                                try:
                                    # Convert to WAV
                                    audio = AudioSegment.from_file(tmp_path)
                                    wav_path = tmp_path.replace(".wav", "_converted.wav")
                                    audio.export(wav_path, format="wav")
                                        
                                    # Recognize speech
                                    recognizer = sr.Recognizer()
                                    with sr.AudioFile(wav_path) as source:
                                        audio_data_sr = recognizer.record(source)
                                        transcription = recognizer.recognize_google(audio_data_sr, language="pl-PL")
                                        
                                    # Add punctuation with Gemini
                                    try:
                                        import google.generativeai as genai
                                            
                                        api_key = st.secrets["API_KEYS"]["gemini"]
                                        genai.configure(api_key=api_key)
                                            
                                        model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
                                        prompt = f"""Dodaj interpunkcję (kropki, przecinki, pytajniki, wykrzykniki) do poniższego tekstu.
Nie zmieniaj słów, tylko dodaj znaki interpunkcyjne. Zachowaj strukturę i podział na zdania.
Zwróć tylko poprawiony tekst, bez dodatkowych komentarzy.

Tekst do poprawy:
{transcription}"""
                                            
                                        response = model.generate_content(prompt)
                                        transcription = response.text.strip()
                                    except:
                                        pass  # Use basic transcription if Gemini fails
                                        
                                    # Append to existing text - check current text_area value
                                    text_area_key = f"player_input_{selected_client_id}_v{st.session_state[transcription_version_key]}"
                                    existing_text = st.session_state.get(text_area_key, st.session_state.get(transcription_key, ""))
                                        
                                    if existing_text.strip():
                                        st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
                                    else:
                                        st.session_state[transcription_key] = transcription
                                        
                                    # Increment version to force text_area refresh
                                    st.session_state[transcription_version_key] += 1
                                        
                                    st.success("✅ Transkrypcja zakończona!")
                                    st.rerun()
                                    
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
                    
                # Text area with versioned key (refreshes after transcription)
                current_text = st.session_state.get(transcription_key, "")
                text_area_key = f"player_input_{selected_client_id}_v{st.session_state[transcription_version_key]}"
                    
                # Callback to save text_area value to transcription_key
                def save_text():
                    st.session_state[transcription_key] = st.session_state[text_area_key]
                    
                player_message = st.text_area(
                    "Napisz lub nagraj swoją wypowiedź:",
                    value=current_text,
                    height=100,
                    placeholder="Napisz co chcesz powiedzieć klientowi lub nagraj audio powyżej...",
                    key=text_area_key,
                    on_change=save_text
                )
                    
                # Sync transcription_key with current text_area value
                st.session_state[transcription_key] = player_message
                
                col_send, col_finish = st.columns([3, 1])
                
                with col_send:
                    if st.button("📤 Wyślij wiadomość", disabled=not player_message):
                        if player_message:
                            from utils.fmcg_ai_conversation import conduct_fmcg_conversation
                            
                            # Add player message
                            conversation_state["messages"].append({
                                "role": "player",
                                "content": player_message,
                                "timestamp": datetime.now().isoformat()
                            })
                            
                            # Get AI response
                            with st.spinner(f"{selected_client.get('owner', 'Klient')} zastanawia się..."):
                                ai_response, metadata = conduct_fmcg_conversation(
                                    client=selected_client,
                                    player_message=player_message,
                                    conversation_history=conversation_state.get("history", []),
                                    current_messages=conversation_state["messages"]
                                )
                            
                            # Add AI response
                            conversation_state["messages"].append({
                                "role": "assistant",
                                "content": ai_response,
                                "timestamp": datetime.now().isoformat(),
                                "metadata": metadata
                            })
                            
                            # Clear the text area for next message
                            st.session_state[transcription_key] = ""
                            st.session_state[transcription_version_key] += 1
                            
                            st.rerun()
                
                with col_finish:
                    if st.button("✅ Zakończ rozmowę"):
                        conversation_state["finished"] = True
                        st.rerun()
                    
                st.markdown("---")
                    
                # =================================================================
                # NOTES PANEL (below message input - during conversation)
                # =================================================================
                    
                # Initialize visit notes in session state
                if 'visit_notes' not in st.session_state:
                    st.session_state.visit_notes = {}
                
                client_id = st.session_state.get('selected_visit_client')
                client_name = selected_client.get('name', 'Klient')
                
                # Panel notatek z poprzednich wizyt
                with st.expander(f"📝 Notatki: {client_name}", expanded=False):
                    st.caption("Zapisuj ważne informacje podczas rozmowy")
                    
                    # Pokaż poprzednie notatki jeśli istnieją
                    if client_id in st.session_state.visit_notes and st.session_state.visit_notes[client_id].get('previous'):
                        prev_notes = st.session_state.visit_notes[client_id]['previous']
                        prev_date = st.session_state.visit_notes[client_id].get('previous_date', 'poprzednia wizyta')
                        
                        st.info(f"""
**📖 Ostatnia wizyta ({prev_date}):**

{prev_notes}
                        """)
                        st.markdown("---")
                    
                    # Textarea dla bieżących notatek
                    current_notes = st.session_state.visit_notes.get(client_id, {}).get('current', '')
                    
                    notes_text = st.text_area(
                        "Notatki z tej wizyty",
                        value=current_notes,
                        height=150,
                        placeholder="""💡 Zapisuj ważne info:
- Kluczowe informacje z rozmowy
- Obiekcje klienta i Twoje odpowiedzi
- Uzgodnienia (cena, dostawa, warunki)
- Co pamiętać na następną wizytę
- Preferencje właściciela""",
                        key=f"visit_notes_{client_id}"
                    )
                    
                    col_notes1, col_notes2 = st.columns(2)
                    
                    with col_notes1:
                        if st.button("💾 Zapisz notatki", use_container_width=True, key=f"save_notes_{client_id}"):
                            # Zapisz notatki
                            if client_id not in st.session_state.visit_notes:
                                st.session_state.visit_notes[client_id] = {}
                            
                            st.session_state.visit_notes[client_id]['current'] = notes_text
                            st.session_state.visit_notes[client_id]['saved_at'] = datetime.now().strftime("%d.%m.%Y %H:%M")
                            st.success("✅ Notatki zapisane!")
                    
                    with col_notes2:
                        if st.button("📖 Załaduj poprzednie", use_container_width=True, key=f"load_notes_{client_id}"):
                            if client_id in st.session_state.visit_notes and st.session_state.visit_notes[client_id].get('previous'):
                                st.session_state.visit_notes[client_id]['current'] = st.session_state.visit_notes[client_id]['previous']
                                st.rerun()
                            else:
                                st.warning("Brak poprzednich notatek dla tego klienta")
            
            # Conversation finished - evaluate and execute visit
            if conversation_state["finished"]:
                st.success("✅ Rozmowa zakończona!")
                
                # Evaluate conversation
                from utils.fmcg_ai_conversation import evaluate_conversation_quality
                
                with st.spinner("Ocenianie rozmowy..."):
                    evaluation = evaluate_conversation_quality(
                        conversation_messages=conversation_state["messages"],
                        client=selected_client
                    )
                
                # Show evaluation
                st.markdown("### 📊 Ocena rozmowy")
                
                col_eval1, col_eval2, col_eval3 = st.columns(3)
                
                with col_eval1:
                    quality_stars = "⭐" * evaluation["quality"]
                    st.metric("Jakość", quality_stars)
                
                with col_eval2:
                    order_emoji = "✅" if evaluation["order_likely"] else "❌"
                    st.metric("Zamówienie", f"{order_emoji} {evaluation['order_value']} PLN")
                
                with col_eval3:
                    rep_emoji = "📈" if evaluation["reputation_change"] > 0 else "📉" if evaluation["reputation_change"] < 0 else "➡️"
                    st.metric("Reputacja", f"{rep_emoji} {evaluation['reputation_change']:+d}")
                
                st.info(f"**Feedback:** {evaluation['feedback']}")
                
                # =================================================================
                # MANAGER FEEDBACK (FUKO) - if coaching visit
                # =================================================================
                
                manager_feedback = None
                if conversation_state.get("with_manager"):
                    st.markdown("---")
                    st.markdown("### 👔 Feedback menedżerski")
                        
                    with st.spinner("Menedżer przygotowuje feedback rozwojowy..."):
                        from utils.fmcg_ai_conversation import generate_manager_feedback_fuko
                            
                        manager_feedback = generate_manager_feedback_fuko(
                            conversation_messages=conversation_state["messages"],
                            client=selected_client,
                            evaluation=evaluation
                        )
                        
                    if manager_feedback:
                        for idx, area in enumerate(manager_feedback, 1):
                            with st.expander(f"📋 Obszar {idx}: {area['area']}", expanded=True):
                                st.markdown(f"""
                                **F - Fakty:**  
                                {area['fakty']}
                                    
                                **U - Ustosunkowanie:**  
                                {area['ustosunkowanie']}
                                    
                                **K - Konsekwencje:**  
                                {area['konsekwencje']}
                                    
                                **O - Oczekiwania:**  
                                {area['oczekiwania']}
                                """)
                
                # =================================================================
                # ORDER SYSTEM - Product Selection
                # =================================================================
                
                st.markdown("---")
                st.markdown("### � Zamówienie - Wybierz produkty")
                
                # Initialize order state
                order_key = f"order_{selected_client_id}"
                if order_key not in st.session_state:
                    st.session_state[order_key] = {}
                
                # Tabs: FreshLife vs Konkurencja
                tab_fl, tab_comp = st.tabs(["🌿 FreshLife (Twoje produkty)", "🏪 Konkurencja"])
                
                total_value = 0
                total_margin = 0
                order_items = []
                
                with tab_fl:
                    st.caption("Wyższa marża! 💰")
                        
                    # Import order realism functions
                    from utils.fmcg_order_realism import (
                        calculate_realistic_order_quantity,
                        validate_order_quantity,
                        get_category_display_name
                    )
                        
                    # Check if this is first order for this client
                    is_first_order = selected_client.get("status") == "PROSPECT"
                        
                    # Get discovered capacity info
                    discovered_info = selected_client.get('discovered_info', {})
                    sales_capacity_discovered = discovered_info.get('sales_capacity_discovered', {})
                        
                    # Group by category
                    fl_by_category = {}
                    for prod_id, prod in CURRENT_PRODUCTS.items():
                        cat = prod["category"]
                        if cat not in fl_by_category:
                            fl_by_category[cat] = []
                        fl_by_category[cat].append((prod_id, prod))
                        
                    for category, products in fl_by_category.items():
                        # Sprawdź czy kategoria odkryta
                        is_capacity_discovered = category in sales_capacity_discovered
                            
                        # Calculate recommended quantity for this category
                        first_product = products[0][1] if products else None
                        if first_product:
                            recommended_qty = calculate_realistic_order_quantity(
                                selected_client, 
                                first_product, 
                                weeks_to_cover=2,
                                is_first_order=is_first_order
                            )
                                
                            category_display = get_category_display_name(category)
                            sales_capacity = selected_client.get('sales_capacity', {})
                            capacity_info = sales_capacity.get(category, {})
                                
                            # Expander label - różny w zależności od odkrycia
                            if is_capacity_discovered:
                                expander_label = f"✅ {category_display} ({len(products)} produktów) - 💡 Sugerowane: {recommended_qty} szt/produkt"
                            else:
                                expander_label = f"🔒 {category_display} ({len(products)} produktów) - możliwości zakupowe nieznane"
                        else:
                            expander_label = f"📦 {category} ({len(products)} produktów)"
                            
                        with st.expander(expander_label):
                            # Show category capacity info TYLKO jeśli odkryte
                            if is_capacity_discovered and first_product and capacity_info:
                                discovered_capacity = sales_capacity_discovered[category]
                                st.success(f"""
✅ **Poznałeś możliwości zakupowe dla {category_display}:**
- Sprzedaż tygodniowa: ~{discovered_capacity.get('weekly_sales_volume', 100)} szt (cała kategoria)
- Miejsce na półce: {discovered_capacity.get('shelf_space_facings', 10)} pozycji
- 💡 Typowe zamówienie na 1 produkt: **{recommended_qty} szt** (2 tygodnie)
{"- 🎯 Dla pierwszego zamówienia: ostrożnie, mniej na test!" if is_first_order else ""}
                                """)
                            elif not is_capacity_discovered:
                                # Nieodkryte - pokazuj komunikat
                                st.info(f"""
🔒 **Możliwości zakupowe dla {category_display} nieznane**

💡 **Jak odkryć:**
- Odwiedź sklep kilka razy (~4 wizyty)
- Buduj reputację (wyższa reputacja → klient chętniej dzieli się informacjami)
- Podczas rozmowy klient może naturalnie wspomnieć o sprzedaży

⚠️ **Możesz próbować składać zamówienia**, ale:
- Nie znasz realistycznych ilości
- Klient może odrzucić zbyt duże propozycje
- Ryzykujesz obniżenie reputacji proponując kosmiczne kwoty
                                """)
                                
                            for prod_id, prod in products:
                                col_info, col_qty, col_validation = st.columns([3, 1, 1])
                                    
                                with col_info:
                                    # Get margin and price with backward compatibility
                                    margin_percent, margin_pln = _get_product_margin(prod)
                                    price = _get_product_price(prod)
                                    st.markdown(f"""
                                    **{prod['name']}**  
                                    💰 {price:.2f} PLN | 📊 Marża: {margin_percent}% ({margin_pln:.2f} PLN)  
                                    📈 Popularność: {prod.get('popularity', 50)}%
                                    """)
                                    
                                with col_qty:
                                    qty = st.number_input(
                                        "Ilość",
                                        min_value=0,
                                        max_value=200,
                                        value=st.session_state[order_key].get(prod_id, 0),
                                        step=6,  # Step by 6 (standard packing)
                                        key=f"qty_{prod_id}",
                                        label_visibility="collapsed"
                                    )
                                    st.session_state[order_key][prod_id] = qty
                                    
                                with col_validation:
                                    # Validate quantity if > 0
                                    if qty > 0:
                                        validation = validate_order_quantity(
                                            selected_client,
                                            prod,
                                            qty,
                                            is_first_order=is_first_order
                                        )
                                            
                                        if validation['realism_level'] == 'perfect':
                                            st.success(f"✅ {validation['feedback_for_player']}")
                                        elif validation['realism_level'] == 'acceptable':
                                            st.info(f"✅ {validation['feedback_for_player']}")
                                        elif validation['realism_level'] == 'too_high':
                                            st.warning(f"⚠️ {validation['feedback_for_player']}")
                                        elif validation['realism_level'] in ['too_low', 'unrealistic']:
                                            st.error(f"❌ {validation['feedback_for_player']}")
                                        
                                    if qty > 0:
                                        price = _get_product_price(prod)
                                        item_value = qty * price
                                        item_margin = qty * margin_pln
                                        total_value += item_value
                                        total_margin += item_margin
                                        order_items.append({
                                            "product_id": prod_id,
                                            "name": prod['name'],
                                            "brand": "FreshLife",
                                            "quantity": qty,
                                            "price_unit": price,
                                            "value": item_value,
                                            "margin": item_margin,
                                            "margin_percent": margin_percent
                                        })
                    
                with tab_comp:
                    st.caption("Produkty konkurencji - niższa marża")
                        
                    # Group by category
                    comp_by_category = {}
                    for prod_id, prod in CURRENT_COMPETITOR_PRODUCTS.items():
                        cat = prod["category"]
                        if cat not in comp_by_category:
                            comp_by_category[cat] = []
                        comp_by_category[cat].append((prod_id, prod))
                        
                    for category, products in comp_by_category.items():
                        with st.expander(f"📦 {category} ({len(products)} produktów)"):
                            for prod_id, prod in products:
                                col_info, col_qty = st.columns([3, 1])
                                    
                                with col_info:
                                    # Get margin and price with backward compatibility
                                    margin_percent, margin_pln = _get_product_margin(prod)
                                    price = _get_product_price(prod)
                                    st.markdown(f"""
                                    **{prod['name']}** ({prod['brand']})  
                                    💰 {price:.2f} PLN | 📊 Marża: {margin_percent}% ({margin_pln:.2f} PLN)  
                                    📈 Popularność: {prod.get('popularity', 50)}%
                                    """)
                                    
                                with col_qty:
                                    qty = st.number_input(
                                        "Ilość",
                                        min_value=0,
                                        max_value=100,
                                        value=st.session_state[order_key].get(prod_id, 0),
                                        step=1,
                                        key=f"qty_{prod_id}",
                                        label_visibility="collapsed"
                                    )
                                    st.session_state[order_key][prod_id] = qty
                                        
                                    if qty > 0:
                                        price = _get_product_price(prod)
                                        item_value = qty * price
                                        item_margin = qty * margin_pln
                                        total_value += item_value
                                        total_margin += item_margin
                                        order_items.append({
                                            "product_id": prod_id,
                                            "name": prod['name'],
                                            "brand": prod['brand'],
                                            "quantity": qty,
                                            "price_unit": price,
                                            "value": item_value,
                                            "margin": item_margin,
                                            "margin_percent": margin_percent
                                        })
                
                # Order summary
                st.markdown("---")
                st.markdown("### 📋 Podsumowanie zamówienia")
                
                if order_items:
                    col_sum1, col_sum2, col_sum3 = st.columns(3)
                        
                    with col_sum1:
                        st.metric("💰 Wartość zamówienia", f"{total_value:.2f} PLN")
                        
                    with col_sum2:
                        st.metric("💵 Twoja marża", f"{total_margin:.2f} PLN")
                        
                    with col_sum3:
                        margin_pct = (total_margin / total_value * 100) if total_value > 0 else 0
                        st.metric("📊 Średnia marża", f"{margin_pct:.1f}%")
                        
                    # Show items
                    with st.expander(f"📦 Szczegóły zamówienia ({len(order_items)} pozycji)"):
                        for item in order_items:
                            st.markdown(f"""
                            - **{item['name']}** ({item['brand']}) × {item['quantity']} = {item['value']:.2f} PLN  
                              _Marża: {item['margin']:.2f} PLN ({item['margin_percent']}%)_
                            """)
                else:
                    st.warning("⚠️ Brak produktów w zamówieniu")
                
                # =================================================================
                # FINALIZATION
                # =================================================================
                
                st.markdown("---")
                st.markdown("### 💰 Finalizacja wizyty")
                
                col_order, col_tools = st.columns(2)
                
                with col_order:
                    # Use calculated total_value as default, but allow manual override
                    order_value = st.number_input(
                        "Wartość zamówienia (PLN)",
                        min_value=0,
                        max_value=50000,
                        value=int(total_value) if total_value > 0 else evaluation["order_value"],
                        step=100,
                        help="Wyliczona z produktów lub dostosuj ręcznie"
                    )
                
                with col_tools:
                    tools_options = ["gratis", "rabat", "pos_material", "promocja", "free_delivery"]
                    tools_used = st.multiselect(
                        "Narzędzia trade marketing użyte",
                        options=tools_options,
                        default=[]
                    )
                
                # Tasks
                tasks_completed = st.number_input(
                    "Zadania wykonane podczas wizyty",
                    min_value=0,
                    max_value=5,
                    value=0
                )
                
                # Execute visit button
                if st.button("💾 Zapisz wizytę", type="primary"):
                    if energy_cost > energy_pct:
                        st.error(f"❌ Za mało energii! Potrzebujesz {energy_cost}%, masz {energy_pct}%")
                    else:
                        with st.spinner("Zapisywanie wizyty..."):
                            try:
                                # Generate conversation summary for history
                                from utils.fmcg_ai_conversation import generate_conversation_summary
                                
                                summary_data = generate_conversation_summary(
                                    conversation_messages=conversation_state["messages"],
                                    client=selected_client,
                                    evaluation=evaluation
                                )
                                
                                # Execute visit with AI evaluation quality
                                updated_client, updated_game_state, visit_record = execute_visit_placeholder(
                                    client=selected_client,
                                    game_state=game_state,
                                    conversation_quality=evaluation["quality"],
                                    order_value=order_value,
                                    tasks_completed=tasks_completed,
                                    tools_used=tools_used
                                )
                                
                                # Add summary to visit record
                                visit_record["conversation_summary"] = summary_data["summary"]
                                visit_record["key_points"] = summary_data["key_points"]
                                
                                # =================================================================
                                # RECORD VISIT - Update visits_history and events_timeline
                                # =================================================================
                                reputation_change = record_visit(
                                    client_data=updated_client,
                                    visit_quality=evaluation["quality"],
                                    notes=summary_data["summary"]
                                )
                                
                                # Update references
                                clients[selected_client_id] = updated_client
                                game_state = updated_game_state
                                
                                # Add visit to history in game_state
                                if "visit_history" not in game_state:
                                    game_state["visit_history"] = []
                                
                                # Build conversation transcript for review
                                conversation_transcript = []
                                for msg in conversation_state["messages"]:
                                    role_label = "Ja" if msg["role"] == "player" else selected_client.get("owner", "Klient")
                                    conversation_transcript.append({
                                        "role": role_label,
                                        "content": msg["content"],
                                        "timestamp": msg.get("timestamp", "")
                                    })
                                
                                game_state["visit_history"].append({
                                    "client_id": selected_client_id,
                                    "date": datetime.now().strftime("%Y-%m-%d"),
                                    "topic": "rozmowa handlowa" + (" (wizyta rozwojowa)" if conversation_state.get("with_manager") else ""),
                                    "agreements": "; ".join(summary_data["key_points"]) if summary_data["key_points"] else summary_data["summary"],
                                    "next_steps": "Kontynuacja współpracy" if order_value > 0 else "Do uzgodnienia",
                                    "customer_impression": "pozytywne" if evaluation["quality"] >= 4 else "neutralne" if evaluation["quality"] >= 3 else "negatywne",
                                    "quality": evaluation["quality"],
                                    "order_value": order_value,
                                    "order_margin": total_margin,
                                    "order_items": order_items,
                                    "tools_used": tools_used,
                                    "manager_feedback": manager_feedback if conversation_state.get("with_manager") else None,
                                    "summary": summary_data["summary"],
                                    "key_points": summary_data["key_points"],
                                    "conversation_transcript": conversation_transcript
                                })
                                    
                                # =================================================================
                                # SAVE VISIT NOTES - Move current to previous
                                # =================================================================
                                if selected_client_id in st.session_state.visit_notes:
                                    current_notes = st.session_state.visit_notes[selected_client_id].get('current', '')
                                    if current_notes:
                                        # Przenieś bieżące notatki do poprzednich
                                        st.session_state.visit_notes[selected_client_id]['previous'] = current_notes
                                        st.session_state.visit_notes[selected_client_id]['previous_date'] = datetime.now().strftime("%d.%m.%Y %H:%M")
                                        # Wyczyść bieżące
                                        st.session_state.visit_notes[selected_client_id]['current'] = ''
                                
                                # Update coaching visits counter if this was a coaching visit
                                if conversation_state.get("with_manager"):
                                    game_state["coaching_visits_this_week"] = game_state.get("coaching_visits_this_week", 0) + 1
                                
                                # =================================================================
                                # CLIENT DISCOVERY - Extract new information from conversation
                                # =================================================================
                                from utils.fmcg_ai_conversation import extract_client_discoveries, calculate_knowledge_level, extract_sales_capacity_discovery
                                from utils.fmcg_order_realism import calculate_market_share
                                    
                                # Get current discovered info
                                current_discovered_info = updated_client.get("discovered_info", {})
                                knowledge_level_before = updated_client.get("knowledge_level", 0)
                                    
                                # Extract new discoveries from conversation
                                discovery_result = extract_client_discoveries(
                                    conversation_history=conversation_state["messages"],
                                    client_name=selected_client.get("name", "Klient"),
                                    client_current_info=current_discovered_info
                                )
                                    
                                # =================================================================
                                # SALES CAPACITY DISCOVERY - Extract capacity info from conversation
                                # =================================================================
                                    
                                # Build conversation transcript for AI
                                conversation_transcript = "\n\n".join([
                                    f"{'GRACZ' if msg['role'] == 'user' else 'KLIENT'}: {msg['content']}"
                                    for msg in conversation_state["messages"]
                                ])
                                    
                                # Get current discovered capacity
                                current_sales_capacity_discovered = current_discovered_info.get("sales_capacity_discovered", {})
                                    
                                # Extract new capacity discoveries
                                capacity_discoveries = extract_sales_capacity_discovery(
                                    conversation_transcript=conversation_transcript,
                                    client=updated_client,
                                    current_discovered=current_sales_capacity_discovered
                                )
                                    
                                # If new capacity discoveries found → update and recalculate market share
                                capacity_discovery_toasts = []
                                if capacity_discoveries:
                                    # Update discovered_info with new capacity
                                    if "sales_capacity_discovered" not in current_discovered_info:
                                        current_discovered_info["sales_capacity_discovered"] = {}
                                        
                                    for category, capacity_data in capacity_discoveries.items():
                                        current_discovered_info["sales_capacity_discovered"][category] = capacity_data
                                            
                                        # Prepare toast message
                                        weekly_vol = capacity_data.get('weekly_sales_volume', 0)
                                        capacity_discovery_toasts.append(f"✨ Odkryto: {category} (~{weekly_vol} szt/tydz.)")
                                        
                                    # Recalculate market share for discovered categories
                                    if "market_share_by_category" not in current_discovered_info:
                                        current_discovered_info["market_share_by_category"] = {}
                                        
                                    for category in capacity_discoveries.keys():
                                        # Calculate market share for this category
                                        market_share_data = calculate_market_share(updated_client, category)
                                        current_discovered_info["market_share_by_category"][category] = market_share_data
                                        
                                    # Update client
                                    updated_client["discovered_info"] = current_discovered_info
                                    
                                # Store capacity discoveries for display
                                st.session_state["capacity_discoveries"] = capacity_discovery_toasts if capacity_discovery_toasts else None
                                    
                                # Update discovered info
                                new_discoveries = discovery_result.get("discovered", {})
                                discovery_notes_new = discovery_result.get("notes", [])
                                    
                                if new_discoveries:
                                    # Merge new discoveries with existing
                                    if not current_discovered_info:
                                        current_discovered_info = {}
                                        
                                    for field, value in new_discoveries.items():
                                        current_discovered_info[field] = value
                                        
                                    updated_client["discovered_info"] = current_discovered_info
                                        
                                    # Add discovery notes
                                    if "discovery_notes" not in updated_client:
                                        updated_client["discovery_notes"] = []
                                        
                                    for note in discovery_notes_new:
                                        updated_client["discovery_notes"].append({
                                            "visit_date": datetime.now().isoformat(),
                                            "note_text": note.get("value", ""),
                                            "discovered_fields": [note.get("field", "")],
                                            "context": note.get("context", "")
                                        })
                                        
                                    # Recalculate knowledge level
                                    knowledge_level_after = calculate_knowledge_level(current_discovered_info)
                                    updated_client["knowledge_level"] = knowledge_level_after
                                        
                                    # Store in session for displaying later
                                    st.session_state["latest_discoveries"] = {
                                        "new_fields": list(new_discoveries.keys()),
                                        "notes": discovery_notes_new,
                                        "knowledge_before": knowledge_level_before,
                                        "knowledge_after": knowledge_level_after,
                                        "discoveries_count": len(new_discoveries)
                                    }
                                else:
                                    st.session_state["latest_discoveries"] = None
                                    
                                # Update client in dict
                                clients[selected_client_id] = updated_client
                                
                                # Save visit to SQL with summary (optional, dla user z SQL)
                                from utils.fmcg_mechanics import save_fmcg_visit_to_sql
                                save_fmcg_visit_to_sql(username, visit_record, game_state)
                                
                                # Save to SQL and session state
                                update_fmcg_game_state_sql(username, game_state, clients)
                                st.session_state["fmcg_game_state"] = game_state
                                st.session_state["fmcg_clients"] = clients
                                
                                # Clear conversation and order
                                if conv_key in st.session_state:
                                    del st.session_state[conv_key]
                                if order_key in st.session_state:
                                    del st.session_state[order_key]
                                
                                # Show results
                                st.success("✅ Wizyta zapisana!")
                                    
                                # Show reputation change as toast for significant changes
                                if abs(reputation_change) >= 10:
                                    rep_toast_icon = "🎉" if reputation_change > 0 else "⚠️"
                                    st.toast(f"{rep_toast_icon} Reputacja: {reputation_change:+d} punktów!", icon=rep_toast_icon)
                                    
                                # Show capacity discoveries (toast-like notifications)
                                capacity_discoveries_msgs = st.session_state.get("capacity_discoveries")
                                if capacity_discoveries_msgs:
                                    for msg in capacity_discoveries_msgs:
                                        st.toast(msg, icon="✨")
                                    # Clear after showing
                                    st.session_state["capacity_discoveries"] = None
                                
                                col_res1, col_res2, col_res3 = st.columns(3)
                                
                                with col_res1:
                                    old_status = selected_client.get("status", "PROSPECT")
                                    new_status = updated_client.get("status", "PROSPECT")
                                    if old_status != new_status:
                                        st.info(f"📈 Status: {old_status} → **{new_status}**")
                                    else:
                                        st.info(f"Status: {new_status}")
                                
                                with col_res2:
                                    # Show reputation change from record_visit with enhanced visual feedback
                                    old_rep = selected_client.get("reputation", 0)
                                    new_rep = updated_client.get("reputation", 0)
                                    rep_emoji = "📈" if reputation_change > 0 else "📉" if reputation_change < 0 else "➡️"
                                        
                                    # Color-coded based on change
                                    if reputation_change > 0:
                                        st.success(f"{rep_emoji} **Reputacja:** {old_rep} → {new_rep} ({reputation_change:+d})")
                                    elif reputation_change < 0:
                                        st.error(f"{rep_emoji} **Reputacja:** {old_rep} → {new_rep} ({reputation_change:+d})")
                                    else:
                                        st.info(f"{rep_emoji} **Reputacja:** {new_rep} (bez zmian)")
                                        
                                    # Show reputation status label
                                    rep_status = get_reputation_status(new_rep)
                                    st.caption(f"{rep_status['emoji']} {rep_status['label']}")
                                
                                with col_res3:
                                    st.info(f"⚡ Energia: {game_state['energy']}%")
                                
                                # Show visit details
                                st.markdown("---")
                                st.markdown("### 📊 Podsumowanie wizyty")
                                    
                                col_details1, col_details2 = st.columns(2)
                                    
                                with col_details1:
                                    quality_stars = "⭐" * evaluation["quality"]
                                    st.markdown(f"**Jakość rozmowy:** {quality_stars} ({evaluation['quality']}/5)")
                                        
                                    # Check if visit was recorded in history
                                    visits_count = len(updated_client.get("visits_history", []))
                                    st.markdown(f"**Łączna liczba wizyt:** {visits_count}")
                                        
                                    # Show current reputation
                                    current_rep = updated_client.get("reputation", 0)
                                    rep_status = get_reputation_status(current_rep)
                                    st.markdown(f"**Aktualna reputacja:** {rep_status['emoji']} {current_rep} ({rep_status['label']})")
                                    
                                with col_details2:
                                    if order_value > 0:
                                        st.markdown(f"**💰 Wartość zamówienia:** {order_value:,} PLN")
                                        if total_margin > 0:
                                            st.markdown(f"**💵 Twoja marża:** {total_margin:,.2f} PLN")
                                        
                                    # Show next visit reminder
                                    if updated_client.get("next_visit_due"):
                                        next_visit = updated_client["next_visit_due"]
                                        st.markdown(f"**📅 Następna wizyta:** {next_visit}")
                                    
                                # =================================================================
                                # SHOW CLIENT DISCOVERIES
                                # =================================================================
                                    
                                latest_discoveries = st.session_state.get("latest_discoveries")
                                    
                                if latest_discoveries and latest_discoveries["discoveries_count"] > 0:
                                    st.markdown("---")
                                        
                                    # Knowledge level change
                                    knowledge_before = latest_discoveries["knowledge_before"]
                                    knowledge_after = latest_discoveries["knowledge_after"]
                                        
                                    stars_before = "⭐" * knowledge_before + "☆" * (5 - knowledge_before)
                                    stars_after = "⭐" * knowledge_after + "☆" * (5 - knowledge_after)
                                        
                                    # Success header with animation
                                    st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #10b98115 0%, #10b98105 100%); 
                                                padding: 20px; border-radius: 12px; border-left: 6px solid #10b981; 
                                                margin: 16px 0;'>
                                        <div style='font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 12px;'>
                                            🎉 Nowe odkrycia o kliencie!
                                        </div>
                                        <div style='font-size: 16px; color: #64748b; margin-bottom: 8px;'>
                                            Podczas rozmowy odkryłeś {latest_discoveries["discoveries_count"]} 
                                            {'nową informację' if latest_discoveries["discoveries_count"] == 1 else 'nowe informacje'} 
                                            o kliencie.
                                        </div>
                                        <div style='font-size: 18px; margin-top: 12px;'>
                                            Poziom znajomości: {stars_before} → {stars_after}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                        
                                    # Show discovered details
                                    with st.expander("🔍 Co odkryłeś?", expanded=True):
                                        for note in latest_discoveries["notes"]:
                                            field_name = note.get("field", "")
                                            value = note.get("value", "")
                                            context = note.get("context", "")
                                                
                                            # Field label mapping
                                            field_labels = {
                                                "personality_description": "👤 Charakterystyka właściciela",
                                                "decision_priorities": "⚖️ Priorytety decyzyjne",
                                                "main_customers": "🎯 Główni klienci sklepu",
                                                "customer_demographics": "📊 Demografia klientów",
                                                "competing_brands": "🛒 Marki konkurencji",
                                                "shelf_space_constraints": "📦 Ograniczenia półki",
                                                "pain_points": "💡 Problemy/Bolesności",
                                                "business_goals": "🎯 Cele biznesowe",
                                                "typical_order_value": "💰 Typowe zamówienie",
                                                "preferred_frequency": "📅 Preferowana częstotliwość",
                                                "payment_terms": "💳 Warunki płatności",
                                                "delivery_preferences": "🚚 Preferencje dostaw",
                                                "best_selling_categories": "📈 Najlepiej sprzedające się",
                                                "seasonal_patterns": "🌞 Wzorce sezonowe",
                                                "trust_level": "🤝 Poziom zaufania",
                                                "preferred_communication": "💬 Preferowana komunikacja"
                                            }
                                                
                                            label = field_labels.get(field_name, field_name)
                                                
                                            st.markdown(f"""
                                            <div style='background: #f1f5f9; padding: 16px; border-radius: 8px; 
                                                        margin-bottom: 12px; border-left: 3px solid #6366f1;'>
                                                <div style='font-weight: 600; color: #1e293b; margin-bottom: 8px;'>
                                                    {label}
                                                </div>
                                                <div style='font-size: 14px; color: #1e293b; margin-bottom: 8px;'>
                                                    ✅ {value}
                                                </div>
                                                {f'<div style="font-size: 12px; color: #64748b; font-style: italic;">💬 "{context}"</div>' if context else ''}
                                            </div>
                                            """, unsafe_allow_html=True)
                                            
                                        # Tips for next visit
                                        if knowledge_after < 5:
                                            st.info(f"""
                                            💡 **Wskazówka:** Odkryłeś {_count_discovered_fields(updated_client.get('discovered_info', {}))}/16 pól. 
                                            Podczas następnej wizyty zadawaj więcej pytań otwartych, aby poznać klienta jeszcze lepiej!
                                            """)
                                    
                                elif latest_discoveries is not None:
                                    # No new discoveries
                                    st.markdown("---")
                                    st.info("ℹ️ Brak nowych odkryć podczas tej wizyty. Spróbuj zadawać więcej pytań otwartych o biznes klienta.")
                                    
                                # =================================================================
                                # CONTRACT SIGNING - If PROSPECT and quality >= 4
                                # =================================================================
                                    
                                if updated_client.get("status") == "PROSPECT" and evaluation["quality"] >= 4:
                                    st.markdown("---")
                                    st.success("🎉 Świetna rozmowa! Klient gotowy do podpisania kontraktu!")
                                        
                                    with st.expander("📝 Podpisz kontrakt - wybierz produkty do portfolio", expanded=True):
                                        st.caption("Wybierz co najmniej 1 produkt, który będzie w stałym asortymencie klienta")
                                            
                                        # Group products by category
                                        fl_by_category = {}
                                        for prod_id, prod in FRESHLIFE_PRODUCTS.items():
                                            cat = prod["category"]
                                            if cat not in fl_by_category:
                                                fl_by_category[cat] = []
                                            fl_by_category[cat].append((prod_id, prod))
                                            
                                        # Multi-select by category
                                        selected_product_ids = []
                                            
                                        for category, products in fl_by_category.items():
                                            st.markdown(f"**{category}**")
                                                
                                            for prod_id, prod in products:
                                                col_prod, col_check = st.columns([4, 1])
                                                    
                                                with col_prod:
                                                    # Get margin and price with backward compatibility
                                                    margin_percent, _ = _get_product_margin(prod)
                                                    price = _get_product_price(prod)
                                                    popularity = prod.get('popularity', 50)
                                                    st.markdown(f"""
                                                    **{prod['name']}**  
                                                    💰 {price:.2f} PLN | 📊 Marża: {margin_percent}% | 📈 Pop: {popularity}%
                                                    """)
                                                    
                                                with col_check:
                                                    if st.checkbox("Dodaj", key=f"contract_{prod_id}", label_visibility="collapsed"):
                                                        selected_product_ids.append(prod_id)
                                                
                                            st.markdown("---")
                                            
                                        # Contract signing button
                                        if len(selected_product_ids) > 0:
                                            st.markdown(f"**Wybrane produkty:** {len(selected_product_ids)}")
                                                
                                            if st.button("✍️ PODPISZ KONTRAKT", type="primary", use_container_width=True):
                                                with st.spinner("Podpisywanie kontraktu..."):
                                                    # Sign contract
                                                    sign_contract(updated_client, selected_product_ids)
                                                        
                                                    # Update in clients dict
                                                    clients[selected_client_id] = updated_client
                                                        
                                                    # Save to SQL
                                                    update_fmcg_game_state_sql(username, game_state, clients)
                                                    st.session_state["fmcg_game_state"] = game_state
                                                    st.session_state["fmcg_clients"] = clients
                                                        
                                                    # Show success
                                                    st.balloons()
                                                    st.success(f"🎉 Kontrakt podpisany! Status: PROSPECT → ACTIVE")
                                                    st.success(f"📈 Bonus reputacji: +20 (nowa: {updated_client['reputation']})")
                                                    st.success(f"📦 Produkty w portfolio: {len(selected_product_ids)}")
                                                        
                                                    # Wait and rerun
                                                    time.sleep(3)
                                                    st.rerun()
                                        else:
                                            st.warning("⚠️ Wybierz co najmniej 1 produkt do kontraktu")
                                    
                                # Button to view client card
                                if st.button("📋 Zobacz kartę klienta", type="secondary"):
                                    st.session_state['show_client_detail'] = True
                                    st.session_state['selected_client_id'] = selected_client_id
                                    st.rerun()
                                
                                if order_value > 0:
                                    st.balloons()
                                
                                # Update current location (route tracking)
                                game_state["current_location"] = {
                                    "lat": selected_client.get("latitude", 0),
                                    "lng": selected_client.get("longitude", 0)
                                }
                                    
                                # Move to next visit in planned route
                                if hasattr(st.session_state, 'planned_route'):
                                    if not hasattr(st.session_state, 'current_visit_idx'):
                                        st.session_state.current_visit_idx = 0
                                    st.session_state.current_visit_idx += 1
                                    
                                # Save updated game state
                                update_fmcg_game_state_sql(username, game_state, clients)
                                st.session_state["fmcg_game_state"] = game_state
                                
                                # Show continue button instead of auto-rerun
                                st.markdown("---")
                                if st.button("✅ Kontynuuj do kolejnej wizyty", type="primary", use_container_width=True):
                                    st.rerun()
                                
                            except Exception as e:
                                import traceback
                                st.error(f"❌ Błąd podczas wizyty: {e}")
                                st.error(f"Typ błędu: {type(e).__name__}")
                                st.code(traceback.format_exc())
                                print(f"❌ BŁĄD PODCZAS WIZYTY:")
                                print(traceback.format_exc())
            
            # Manual mode fallback (if conversation not started)
            if not conversation_state["started"]:
                st.markdown("---")
                st.caption("💡 **Tryb manualny:** Jeśli AI jest niedostępne, możesz użyć trybu manual:")
                
                with st.expander("📝 Tryb manualny (bez AI)"):
                    col_quality, col_order = st.columns(2)
                    
                    with col_quality:
                        conversation_quality = st.slider(
                            "Jakość rozmowy (1-5⭐)",
                            min_value=1,
                            max_value=5,
                            value=3,
                            help="Tryb manualny - bez AI"
                        )
                    
                    with col_order:
                        manual_order_value = st.number_input(
                            "Wartość zamówienia (PLN)",
                            min_value=0,
                            max_value=10000,
                            value=0,
                            step=100,
                            key="manual_order"
                        )
                    
                    # Tasks and tools
                    col_tasks, col_tools = st.columns(2)
                    
                    with col_tasks:
                        manual_tasks = st.number_input(
                            "Zadania wykonane",
                            min_value=0,
                            max_value=5,
                            value=0,
                            key="manual_tasks"
                        )
                    
                    with col_tools:
                        tools_options = ["gratis", "rabat", "pos_material", "promocja", "free_delivery"]
                        manual_tools = st.multiselect(
                            "Narzędzia trade marketing",
                            options=tools_options,
                            default=[],
                            key="manual_tools"
                        )
                    
                    # Execute manual visit
                    if st.button("🚀 Wykonaj wizytę (manual)", type="secondary"):
                        if energy_cost > energy_pct:
                            st.error(f"❌ Za mało energii! Potrzebujesz {energy_cost}%, masz {energy_pct}%")
                        else:
                            with st.spinner("Wykonywanie wizyty..."):
                                try:
                                    # Execute visit
                                    updated_client, updated_game_state, visit_record = execute_visit_placeholder(
                                        client=selected_client,
                                        game_state=game_state,
                                        conversation_quality=conversation_quality,
                                        order_value=manual_order_value,
                                        tasks_completed=manual_tasks,
                                        tools_used=manual_tools
                                    )
                                    
                                    # Update references
                                    clients[selected_client_id] = updated_client
                                    game_state = updated_game_state
                                    
                                    # Save to SQL and session state
                                    update_fmcg_game_state_sql(username, game_state, clients)
                                    st.session_state["fmcg_game_state"] = game_state
                                    st.session_state["fmcg_clients"] = clients
                                    
                                    # Show results
                                    st.success("✅ Wizyta wykonana!")
                                    
                                    col_res1, col_res2, col_res3 = st.columns(3)
                                    
                                    with col_res1:
                                        old_status = selected_client.get("status", "PROSPECT")
                                        new_status = updated_client.get("status", "PROSPECT")
                                        if old_status != new_status:
                                            st.info(f"📈 Status: {old_status} → **{new_status}**")
                                        else:
                                            st.info(f"Status: {new_status}")
                                    
                                    with col_res2:
                                        rep_change = visit_record.get("reputation_change", 0)
                                        rep_emoji = "📈" if rep_change > 0 else "📉" if rep_change < 0 else "➡️"
                                        st.info(f"{rep_emoji} Reputacja: {rep_change:+d}")
                                    
                                    with col_res3:
                                        st.info(f"⚡ Energia: {game_state['energy']}%")
                                    
                                    if manual_order_value > 0:
                                        st.balloons()
                                        st.success(f"🎉 Zamówienie: {manual_order_value:,} PLN!")
                                    
                                    # Rerun to refresh UI
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Błąd podczas wizyty: {e}")
        
    # =============================================================================
    # DAY ADVANCEMENT
    # =============================================================================
        
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
    
        
        # =========================================================================
        # SUB-TAB: KATALOG PRODUKTÓW
        # =========================================================================
        
        with sales_tab_products:
            st.subheader("📦 Katalog Produktów")
        # Check if Heinz scenario
        is_heinz_scenario = "heinz" in scenario_id.lower()
        
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
        
        # Display products in grid (3 columns)
        for i in range(0, len(filtered_products), 3):
            col1, col2, col3 = st.columns(3)
            
            for idx, col in enumerate([col1, col2, col3]):
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
                                _render_product_details(product)
                                
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
    # TAB: HR & TEAM (Human Resources - Rozwój i Wsparcie)
    # =============================================================================
    
    with tab_hr:
        st.markdown("## 👥 HR - Rozwój i Wsparcie")
        st.markdown("Centrum rozwoju kariery, szkoleń i wsparcia w pracy Product Handlera")
        
        # HR Sub-tabs
        hr_tab_career, hr_tab_mentor, hr_tab_training = st.tabs([
            "🎯 Ścieżka Kariery", 
            "🎓 Mentor", 
            "📚 Szkolenia"
        ])
        
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
                            api_key = st.secrets.get("GOOGLE_API_KEY")
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
            st.markdown("### 📚 Szkolenia i Materiały Edukacyjne")
            st.markdown("Rozwijaj swoje umiejętności sprzedażowe dzięki specjalistycznym materiałom")
            
            # Training categories
            training_categories = st.tabs([
                "🗺️ Planowanie", 
                "💬 Rozmowy sprzedażowe", 
                "🏪 Merchandising",
                "📊 Analityka"
            ])
            
            # PLANOWANIE TRAINING
            with training_categories[0]:
                st.markdown("#### 🗺️ Planowanie Terytorium Sprzedażowego")
                
                with st.expander("**Planowanie terytorium - od analizy do pierwszej wizyty**", expanded=False):
                    # Elegancki preview
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 30px; 
                                border-radius: 15px; 
                                color: white; 
                                margin-bottom: 20px;
                                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);">
                        <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">🗺️ Zacznij od planu!</h2>
                        <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                            Segmentacja ABC, routing, strategia prospectingowa i przygotowanie do pierwszej wizyty
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Highlights
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("""
                        <div style="background: #d1fae5; padding: 15px; border-radius: 10px; border-left: 4px solid #10b981;">
                            <div style="font-size: 2rem; margin-bottom: 5px;">🔤</div>
                            <strong>Segmentacja ABC</strong><br>
                            <span style="color: #64748b; font-size: 0.9rem;">20% klientów = 80% przychodów</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div style="background: #dbeafe; padding: 15px; border-radius: 10px; border-left: 4px solid #3b82f6;">
                            <div style="font-size: 2rem; margin-bottom: 5px;">🚀</div>
                            <strong>Quick Wins First</strong><br>
                            <span style="color: #64748b; font-size: 0.9rem;">Od kogo zacząć? B→C→A</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("""
                        <div style="background: #ffedd5; padding: 15px; border-radius: 10px; border-left: 4px solid #f97316;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">🗺️</div>
                    <strong>Routing + Klasteryzacja</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Oszczędź 100 km dziennie!</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Wyświetl HTML
            html_path = os.path.join("docs", "PLANOWANIE_TERYTORIUM_INTERACTIVE.html")
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                components.html(html_content, height=800, scrolling=True)
            else:
                st.error("⚠️ Plik HTML nie został znaleziony.")
        
        st.markdown("---")
        
        # Artykuł 1: Kanał Tradycyjny
        with st.expander("🏪 **Kanał Tradycyjny - Charakterystyka i Modele Dystrybucji**", expanded=False):
            # Elegancki preview w stylu karty
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 30px; 
                        border-radius: 15px; 
                        color: white; 
                        margin-bottom: 20px;
                        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);">
                <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">📚 Kompleksowy przewodnik po kanale tradycyjnym</h2>
                <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                    Dowiedz się wszystkiego o sprzedaży FMCG w małych sklepach osiedlowych
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Highlights w kartach
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div style="background: #f0fdf4; padding: 15px; border-radius: 10px; border-left: 4px solid #10b981;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">🔄</div>
                    <strong>4 Modele Dystrybucji</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Od bezpośredniej do Cash & Carry</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: #eff6ff; padding: 15px; border-radius: 10px; border-left: 4px solid #3b82f6;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">💰</div>
                    <strong>Ekonomika Sklepu</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Marża, rotacja, kapitał obrotowy</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background: #fef3c7; padding: 15px; border-radius: 10px; border-left: 4px solid #f59e0b;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">💬</div>
                    <strong>Argumenty + Obiekcje</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Gotowe odpowiedzi na wyzwania</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Wyświetl HTML bezpośrednio
            html_path = os.path.join("docs", "KANAL_TRADYCYJNY_INTERACTIVE.html")
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                # Wyświetl HTML w komponencie (scrollable)
                components.html(html_content, height=800, scrolling=True)
            else:
                st.error("⚠️ Plik HTML nie został znaleziony.")
        
        # Artykuł 2: Sondowanie potrzeb klienta
        with st.expander("🎯 **Sondowanie potrzeb klienta - sztuka zadawania właściwych pytań**", expanded=False):
            # Elegancki preview
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 30px; 
                        border-radius: 15px; 
                        color: white; 
                        margin-bottom: 20px;
                        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);">
                <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">🎯 Kompetencje > Reputacja</h2>
                <p style="font-size: 1.1rem; opacity: 0.95; margin: 0;">
                    Odkryj jak profesjonalne pytania odblokowują capacity nawet przy reputacji 0
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Highlights
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div style="background: #fef3c7; padding: 15px; border-radius: 10px; border-left: 4px solid #f59e0b;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">❓</div>
                    <strong>5 Technik Sondowania</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Od pytań otwartych do capacity questions</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: #f0fdf4; padding: 15px; border-radius: 10px; border-left: 4px solid #10b981;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">🔄</div>
                    <strong>SPIN Selling</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Sprawdzona metodyka 4 pytań</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background: #eff6ff; padding: 15px; border-radius: 10px; border-left: 4px solid #3b82f6;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">💬</div>
                    <strong>Przykładowa Rozmowa</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">7 kroków od kontaktu do zamknięcia</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Wyświetl HTML bezpośrednio (jak w pierwszym artykule)
            html_path = os.path.join("docs", "SONDOWANIE_POTRZEB_INTERACTIVE.html")
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                # Wyświetl HTML w komponencie (scrollable)
                components.html(html_content, height=800, scrolling=True)
            else:
                st.error("⚠️ Plik HTML nie został znaleziony.")
        
        # Placeholder na kolejne artykuły
        st.markdown("---")
        st.info("💡 **Więcej artykułów wkrótce!** Pracujemy nad materiałami dotyczącymi merchandisingu, negocjacji i budowania relacji z klientami.")
        
    
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
