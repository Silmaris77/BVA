"""
🛒 FMCG Playable Game UI
Minimal playable interface for FMCG sales simulation
Uses fmcg_mechanics.py backend
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Optional
import time
import folium
from streamlit_folium import folium_static
import html

# Import FMCG mechanics
from utils.fmcg_mechanics import (
    execute_visit_placeholder,
    advance_day,
    update_fmcg_game_state_sql,
    load_fmcg_game_state_sql,
    get_client_status_summary,
    get_clients_needing_visit,
    calculate_visit_energy_cost,
    calculate_travel_time
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
from utils.fmcg_products import (
    get_product_info,
    suggest_cross_sell_products,
    get_portfolio_summary,
    FRESHLIFE_PRODUCTS as FRESHLIFE_PRODUCTS_NEW
)

# Import client detail card component
from views.business_games_refactored.components.client_detail_card import render_client_detail_card


def show_fmcg_playable_game(username: str):
    """
    Main FMCG playable game interface
    
    Components:
    1. Dashboard (energy, stats, day/week)
    2. Client map (Folium with status colors)
    3. Visit interface (client select, quality slider, order input)
    4. Day advancement button
    """
    
    st.title("🛒 FMCG Sales Simulator")
    st.caption("Junior Sales Representative - Piaseczno Territory")
    
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
    
    # Try to load existing game
    loaded_data = load_fmcg_game_state_sql(username)
    
    if loaded_data:
        game_state, clients = loaded_data
        st.success("✅ Gra wczytana")
    else:
        # Check if we should initialize
        if "fmcg_game_initialized" not in st.session_state:
            st.session_state["fmcg_game_initialized"] = False
        
        # Initialize new game
        if not st.session_state["fmcg_game_initialized"]:
            if st.button("🎮 Start New Game", type="primary"):
                with st.spinner("Inicjalizacja gry..."):
                    game_data = initialize_fmcg_game_new(username)
                    game_state = game_data["fmcg_state"]
                    clients = game_state.get("clients", {})
                    
                    # Save initial state
                    save_success = update_fmcg_game_state_sql(username, game_state, clients)
                    
                    if save_success:
                        st.success("✅ Nowa gra utworzona!")
                        st.session_state["fmcg_game_initialized"] = True
                        st.session_state["fmcg_game_state"] = game_state
                        st.session_state["fmcg_clients"] = clients
                        st.rerun()
                    else:
                        st.error("❌ Błąd zapisu gry")
                        return
            else:
                st.info("👆 Kliknij przycisk aby rozpocząć nową grę")
                return
        else:
            # Load from session state
            game_state = st.session_state.get("fmcg_game_state")
            clients = st.session_state.get("fmcg_clients")
            
            if not game_state or not clients:
                st.error("❌ Błąd wczytywania gry z sesji")
                st.session_state["fmcg_game_initialized"] = False
                st.rerun()
                return
    
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
    col_day, col_week = st.columns(2)
    
    with col_day:
        current_day = game_state.get("current_day", "Monday")
        day_emoji = {"Monday": "1️⃣", "Tuesday": "2️⃣", "Wednesday": "3️⃣", "Thursday": "4️⃣", "Friday": "5️⃣"}
        st.info(f"{day_emoji.get(current_day, '📅')} Dzień: **{current_day}**")
    
    with col_week:
        current_week = game_state.get("current_week", 1)
        visits_this_week = game_state.get("visits_this_week", 0)
        st.info(f"📅 Tydzień: **{current_week}** | Wizyty: **{visits_this_week}**")
    
    # =============================================================================
    # TABS NAVIGATION
    # =============================================================================
    
    st.markdown("---")
    
    tab_dashboard, tab_clients, tab_products, tab_conversation = st.tabs([
        "📊 Dashboard", 
        "🗺️ Klienci", 
        "📦 Produkty", 
        "💬 Rozmowa"
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
    # TAB: KLIENCI (MAP)
    # =============================================================================
    
    with tab_clients:
        # Check if viewing client detail
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
            # Show clients list and map
            st.subheader("🗺️ Moja Rejon - Klienci")
            
            # Clients list with detail buttons
            st.markdown("### 👥 Lista Klientów")
            
            # Group by status (case insensitive)
            for status_key in ["ACTIVE", "PROSPECT", "LOST"]:
                # Convert client status to uppercase for comparison
                status_clients = [cid for cid, c in clients.items() if c.get("status", "prospect").upper() == status_key]
                
                if status_clients:
                    status_config = {
                        "PROSPECT": {"icon": "🎯", "color": "#3b82f6", "label": "Potencjalni"},
                        "ACTIVE": {"icon": "✅", "color": "#10b981", "label": "Aktywni"},
                        "LOST": {"icon": "❌", "color": "#ef4444", "label": "Utraceni"}
                    }
                    
                    cfg = status_config[status_key]
                    
                    with st.expander(f"{cfg['icon']} {cfg['label']} ({len(status_clients)})", expanded=(status_key=="ACTIVE")):
                        for client_id in status_clients:
                            client_data = clients[client_id]
                            
                            # Use client_data directly (SQL has all info)
                            name = client_data.get('name', client_id)
                            location = client_data.get('location', 'N/A')
                            reputation = client_data.get('reputation', 0)
                            
                            col_info, col_btn = st.columns([4, 1])
                            
                            with col_info:
                                # Get reputation status (consistent with detail card)
                                rep_status = get_reputation_status(reputation)
                                
                                st.markdown(f"**{name}** • {location} • {rep_status['emoji']} {reputation}")
                            
                            with col_btn:
                                if st.button("📋 Szczegóły", key=f"detail_{client_id}"):
                                    st.session_state['show_client_detail'] = True
                                    st.session_state['selected_client_id'] = client_id
                                    st.rerun()
                            
                            st.markdown("<div style='margin: 8px 0; border-bottom: 1px solid #e2e8f0;'></div>", 
                                       unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🗺️ Mapa")
            
            # Create Folium map centered on Piaseczno (only when not showing detail)
            base_lat = game_state.get("territory_latitude", 52.0846)
            base_lon = game_state.get("territory_longitude", 21.0250)
            
            m = folium.Map(
                location=[base_lat, base_lon],
                zoom_start=12,
                tiles="OpenStreetMap"
            )
            
            # Add base marker
            folium.Marker(
                [base_lat, base_lon],
                popup="🏢 Baza - Piaseczno",
                icon=folium.Icon(color="black", icon="home", prefix="fa"),
                tooltip="Twoja baza"
            ).add_to(m)
            
            # Add client markers
            for client_id, client in clients.items():
                lat = client.get("latitude", base_lat)
                lon = client.get("longitude", base_lon)
                status = client.get("status", "PROSPECT")
                name = client.get("name", client_id)
                client_type = client.get("type", "")
                distance = client.get("distance_from_base", 0)
                
                # Status colors
                if status == "PROSPECT":
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
                    <p style='margin: 4px 0;'><b>Typ:</b> {client_type}</p>
                    <p style='margin: 4px 0;'><b>Status:</b> {status}</p>
                    <p style='margin: 4px 0;'><b>Dystans:</b> {distance:.1f} km</p>
                </div>
                """
                
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color=color, icon=icon, prefix="fa"),
                    tooltip=f"{name} ({status})"
                ).add_to(m)
            
            # Display map
            folium_static(m, width=800, height=400)
    
    # =============================================================================
    # TAB: PRODUKTY
    # =============================================================================
    
    with tab_products:
        st.subheader("📦 Katalog Produktów")
        
        # Filters
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
        
        # Get all products
        all_products = get_all_products()
        
        # Filter products
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
                        
                        # Popularity bar
                        pop_color = "#10b981" if product["popularity"] >= 70 else "#f59e0b" if product["popularity"] >= 40 else "#ef4444"
                        
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
                                    <span style="font-weight: 700; color: #1e293b; font-size: 14px;">{product['price_retail']:.2f} PLN</span>
                                </div>
                                <div style="margin-bottom: 8px;">
                                    <span style="color: #64748b; font-size: 13px;">Marża: </span>
                                    <span style="font-weight: 700; color: #10b981; font-size: 14px;">{product['margin_percent']}%</span>
                                </div>
                                <div style="margin-top: 12px;">
                                    <div style="color: #64748b; font-size: 11px; margin-bottom: 4px;">Popularność:</div>
                                    <div style="background: #e2e8f0; border-radius: 4px; height: 8px; overflow: hidden;">
                                        <div style="background: {pop_color}; height: 100%; width: {product['popularity']}%;"></div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div style="text-align: center; padding: 8px; background: rgba(255,255,255,0.7); border-radius: 6px; font-size: 11px; color: #64748b; margin-bottom: 12px;">
                                {product['category']}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Compare button for FreshLife products
                        if is_freshlife:
                            if st.button(f"🔍 Porównaj z konkurencją", key=f"compare_{product['id']}"):
                                # Find competitors in same category
                                competitor_ids = get_competitors_for_product(product['id'])
                                comparison = compare_products(product['id'], competitor_ids)
                                
                                if comparison:
                                    st.markdown("---")
                                    st.markdown("**Produkty konkurencji:**")
                                    
                                    for comp in comparison['competitors'][:2]:
                                        st.markdown(f"""
                                        - **{comp['name']}** ({comp['brand']}) - {comp['price_retail']:.2f} PLN  
                                          Marża: {comp['margin_percent']}% | Popularność: {comp['popularity']}%
                                        """)
    
    # =============================================================================
    # TAB: ROZMOWA (VISIT INTERFACE)
    # =============================================================================
    
    with tab_conversation:
        st.subheader("🚗 Wykonaj Wizytę")
        
        # Check if player has energy
        if energy_pct < 5:
            st.error("❌ Za mało energii! Zakończ dzień aby zregenerować energię.")
        else:
            # Client selection
            available_clients = {
                client_id: f"{client['name']} ({client['status']}) - {client.get('distance_from_base', 0):.1f} km"
                for client_id, client in clients.items()
            }
        
            if not available_clients:
                st.warning("Brak klientów w bazie")
            else:
                selected_client_id = st.selectbox(
                    "Wybierz klienta do odwiedzenia:",
                    options=list(available_clients.keys()),
                    format_func=lambda x: available_clients[x]
                )
            
                selected_client = clients[selected_client_id]
            
                # Show visit cost preview
                distance = selected_client.get("distance_from_base", 0)
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
                # AI CONVERSATION INTERFACE
                # =================================================================
            
                st.markdown("---")
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
            
                conversation_state = st.session_state[conv_key]
            
                # Start conversation button
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
                        import hashlib
                        import speech_recognition as sr
                        import tempfile
                        import os
                        from pydub import AudioSegment
                        
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
                        
                        # Group by category
                        fl_by_category = {}
                        for prod_id, prod in FRESHLIFE_PRODUCTS.items():
                            cat = prod["category"]
                            if cat not in fl_by_category:
                                fl_by_category[cat] = []
                            fl_by_category[cat].append((prod_id, prod))
                        
                        for category, products in fl_by_category.items():
                            with st.expander(f"📦 {category} ({len(products)} produktów)"):
                                for prod_id, prod in products:
                                    col_info, col_qty = st.columns([3, 1])
                                    
                                    with col_info:
                                        margin_profit = prod['price_retail'] - prod['price_wholesale']
                                        st.markdown(f"""
                                        **{prod['name']}**  
                                        💰 {prod['price_retail']:.2f} PLN | 📊 Marża: {prod['margin_percent']}% ({margin_profit:.2f} PLN)  
                                        📈 Popularność: {prod['popularity']}%
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
                                            item_value = qty * prod['price_retail']
                                            item_margin = qty * margin_profit
                                            total_value += item_value
                                            total_margin += item_margin
                                            order_items.append({
                                                "product_id": prod_id,
                                                "name": prod['name'],
                                                "brand": "FreshLife",
                                                "quantity": qty,
                                                "price_unit": prod['price_retail'],
                                                "value": item_value,
                                                "margin": item_margin,
                                                "margin_percent": prod['margin_percent']
                                            })
                    
                    with tab_comp:
                        st.caption("Produkty konkurencji - niższa marża")
                        
                        # Group by category
                        comp_by_category = {}
                        for prod_id, prod in COMPETITOR_PRODUCTS.items():
                            cat = prod["category"]
                            if cat not in comp_by_category:
                                comp_by_category[cat] = []
                            comp_by_category[cat].append((prod_id, prod))
                        
                        for category, products in comp_by_category.items():
                            with st.expander(f"📦 {category} ({len(products)} produktów)"):
                                for prod_id, prod in products:
                                    col_info, col_qty = st.columns([3, 1])
                                    
                                    with col_info:
                                        margin_profit = prod['price_retail'] - prod['price_wholesale']
                                        st.markdown(f"""
                                        **{prod['name']}** ({prod['brand']})  
                                        💰 {prod['price_retail']:.2f} PLN | 📊 Marża: {prod['margin_percent']}% ({margin_profit:.2f} PLN)  
                                        📈 Popularność: {prod['popularity']}%
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
                                            item_value = qty * prod['price_retail']
                                            item_margin = qty * margin_profit
                                            total_value += item_value
                                            total_margin += item_margin
                                            order_items.append({
                                                "product_id": prod_id,
                                                "name": prod['name'],
                                                "brand": prod['brand'],
                                                "quantity": qty,
                                                "price_unit": prod['price_retail'],
                                                "value": item_value,
                                                "margin": item_margin,
                                                "margin_percent": prod['margin_percent']
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
                                    
                                    # Update coaching visits counter if this was a coaching visit
                                    if conversation_state.get("with_manager"):
                                        game_state["coaching_visits_this_week"] = game_state.get("coaching_visits_this_week", 0) + 1
                                
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
                                
                                    col_res1, col_res2, col_res3 = st.columns(3)
                                
                                    with col_res1:
                                        old_status = selected_client.get("status", "PROSPECT")
                                        new_status = updated_client.get("status", "PROSPECT")
                                        if old_status != new_status:
                                            st.info(f"📈 Status: {old_status} → **{new_status}**")
                                        else:
                                            st.info(f"Status: {new_status}")
                                
                                    with col_res2:
                                        # Show reputation change from record_visit
                                        rep_emoji = "📈" if reputation_change > 0 else "📉" if reputation_change < 0 else "➡️"
                                        st.info(f"{rep_emoji} Reputacja: {reputation_change:+d}")
                                
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
                                    # CONTRACT SIGNING - If PROSPECT and quality >= 4
                                    # =================================================================
                                    
                                    if updated_client.get("status") == "prospect" and evaluation["quality"] >= 4:
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
                                                        st.markdown(f"""
                                                        **{prod['name']}**  
                                                        💰 {prod['price_retail']:.2f} PLN | 📊 Marża: {prod['margin_percent']}% | 📈 Pop: {prod['popularity']}%
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
                                
                                    # Wait a moment then rerun
                                    import time
                                    time.sleep(2)
                                    st.rerun()
                                
                                except Exception as e:
                                    st.error(f"❌ Błąd podczas wizyty: {e}")
            
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
                
                # Rerun to refresh UI
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Błąd podczas przechodzenia do następnego dnia: {e}")
    
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
