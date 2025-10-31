"""
🎴 FMCG Client Detail Card Component
Rozszerzony widok klienta z reputacją, portfolio i timeline
"""

import streamlit as st
from typing import Dict, Optional
from datetime import datetime
from utils.fmcg_client_helpers import get_reputation_status, is_visit_overdue
from utils.fmcg_products import get_product_info, get_portfolio_summary, suggest_cross_sell_products


def _count_discovered_fields(discovered_info: Dict) -> int:
    """Liczy ile pól zostało odkrytych (nie None, nie puste)"""
    if not discovered_info:
        return 0
    
    count = 0
    for value in discovered_info.values():
        if value is not None and value != "" and value != []:
            count += 1
    return count


def _render_discovery_field(value: Optional[str], placeholder: str):
    """Renderuje pojedyncze pole discovery (odkryte lub do ustalenia)"""
    if value:
        st.markdown(f"✅ {value}")
    else:
        st.markdown(f"❓ *{placeholder} - do ustalenia podczas wizyty*")


def render_client_detail_card(client_data: Dict, client_info: Dict):
    """
    Renderuje rozszerzoną kartę klienta z:
    - Reputation gauge
    - Products portfolio
    - Events timeline
    - Visit tracker
    
    Args:
        client_data: Dict z danymi klienta (z nowej struktury)
        client_info: Dict z database info (name, location, etc.)
    """
    
    client_id = client_data.get("id", "unknown")
    
    # =============================================================================
    # HEADER
    # =============================================================================
    
    status = client_data.get("status", "prospect")
    status_config = {
        "prospect": {"color": "#3b82f6", "icon": "🎯", "label": "PROSPECT"},
        "active": {"color": "#10b981", "icon": "✅", "label": "ACTIVE"},
        "lost": {"color": "#ef4444", "icon": "❌", "label": "LOST"}
    }
    
    st_conf = status_config.get(status, status_config["prospect"])
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {st_conf['color']}15 0%, {st_conf['color']}05 100%); 
                padding: 24px; border-radius: 16px; border-left: 6px solid {st_conf['color']}; 
                margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <div style='font-size: 28px; font-weight: 700; color: #1e293b; margin-bottom: 8px;'>
                    {client_info.get('name', 'Klient')}
                </div>
                <div style='color: #64748b; font-size: 14px;'>
                    📍 {client_info.get('location', 'N/A')} • 
                    👤 {client_info.get('owner', 'N/A')} • 
                    💰 {client_info.get('monthly_revenue', 'N/A')}
                </div>
            </div>
            <div style='background: {st_conf['color']}; color: white; padding: 12px 20px; 
                        border-radius: 12px; font-weight: 700; font-size: 14px;'>
                {st_conf['icon']} {st_conf['label']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # REPUTATION GAUGE
    # =============================================================================
    
    st.markdown("### 🌟 Reputacja")
    
    reputation = client_data.get("reputation", 0)
    rep_status = get_reputation_status(reputation)
    
    # Info card with color
    col_label, col_value = st.columns([3, 1])
    with col_label:
        st.markdown(f"**{rep_status['emoji']} {rep_status['label']}**")
    with col_value:
        st.markdown(f"<div style='font-size: 24px; font-weight: 700; color: {rep_status['color']}; text-align: right;'>{reputation}</div>", unsafe_allow_html=True)
    
    # Custom colored progress bar
    progress_html = f"""
    <div style='width: 100%; background: #e2e8f0; border-radius: 8px; height: 24px; overflow: hidden; margin: 16px 0;'>
        <div style='background: {rep_status['color']}; height: 100%; width: {rep_status['progress']}%; transition: width 0.5s ease;'></div>
    </div>
    <div style='color: #64748b; font-size: 13px; text-align: center; margin-bottom: 24px;'>
        {rep_status['description']}
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # =============================================================================
    # MARKET SHARE & SALES CAPACITY DISCOVERY
    # =============================================================================
    
    st.markdown("### 📊 Możliwości zakupowe i Market Share")
    
    size_sqm = client_data.get("size_sqm", 80)
    discovered_info = client_data.get("discovered_info", {})
    sales_capacity_discovered = discovered_info.get("sales_capacity_discovered", {})
    market_share_by_category = discovered_info.get("market_share_by_category", {})
    
    # Policz ile kategorii odkryte
    all_categories = ["Personal Care", "Food", "Home Care", "Snacks", "Beverages"]
    discovered_count = len(sales_capacity_discovered)
    undiscovered_count = 5 - discovered_count
    
    from utils.fmcg_order_realism import get_segment_name, get_category_display_name, calculate_market_share
    
    segment_name = get_segment_name(size_sqm)
    st.info(f"**{segment_name}** ({size_sqm} m²)")
    
    # Pokazuj challenge - ile nieodkrytych
    if undiscovered_count > 0:
        st.warning(f"� **Nieodkryte: {undiscovered_count} kategorii**")
        st.caption("💡 Poznaj klienta lepiej podczas wizyt, aby odkryć możliwości zakupowe i zwiększyć market share!")
    else:
        st.success("✅ **Wszystkie kategorie odkryte!**")
    
    # Wyświetl każdą kategorię
    for category in all_categories:
        category_display = get_category_display_name(category)
        is_discovered = category in sales_capacity_discovered
        
        with st.expander(
            f"{'✅' if is_discovered else '🔒'} {category_display}" + 
            (f" - Market Share: {market_share_by_category.get(category, {}).get('player_share', 0)}%" if is_discovered else " (nieodkryte)"),
            expanded=is_discovered
        ):
            if is_discovered:
                # Pokazuj capacity info
                capacity_info = sales_capacity_discovered[category]
                weekly_vol = capacity_info.get('weekly_sales_volume', 0)
                facings = capacity_info.get('shelf_space_facings', 0)
                max_per_sku = capacity_info.get('max_order_per_sku', 0)
                rotation_days = capacity_info.get('rotation_days', 14)
                discovered_date = capacity_info.get('discovered_date', 'nieznana data')
                
                st.markdown(f"""
**📦 Możliwości zakupowe:**
- 📈 Sprzedaż tygodniowa (cała kategoria): **~{weekly_vol} szt**
- 🏪 Miejsce na półce: **{facings} pozycji** (facings)
- 📦 Typowe zamówienie (2 tygodnie): **{max_per_sku // 2}-{max_per_sku} szt/produkt**
- 🔄 Rotacja: **{rotation_days} dni**

*Odkryto: {discovered_date[:10]}*
                """)
                
                st.markdown("---")
                
                # Oblicz i pokazuj market share
                market_data = calculate_market_share(client_data, category)
                
                player_share = market_data.get('player_share', 0)
                competitor_share = market_data.get('competitor_share', 100)
                player_volume = market_data.get('player_volume_weekly', 0)
                total_volume = market_data.get('total_volume_weekly', 0)
                trend = market_data.get('trend', 'stable')
                trend_pct = market_data.get('trend_percentage', 0)
                
                # Trend emoji
                trend_emoji = {
                    "growing": "↗️",
                    "declining": "↘️",
                    "stable": "➡️"
                }.get(trend, "➡️")
                
                trend_color = {
                    "growing": "#10b981",
                    "declining": "#ef4444",
                    "stable": "#6b7280"
                }.get(trend, "#6b7280")
                
                st.markdown(f"**📈 Market Share:**")
                
                # Metric z trendem
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label="Twój udział",
                        value=f"{player_share}%",
                        delta=f"{trend_pct:+.0f}% vs miesiąc temu" if trend_pct != 0 else "bez zmian"
                    )
                with col2:
                    st.metric(
                        label="Konkurencja",
                        value=f"{competitor_share}%"
                    )
                
                # Progress bar
                progress_html = f"""
<div style='margin: 12px 0;'>
    <div style='width: 100%; background: #e5e7eb; border-radius: 8px; height: 28px; overflow: hidden; position: relative;'>
        <div style='background: #3b82f6; height: 100%; width: {player_share}%; transition: width 0.5s ease; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 12px;'>
            {player_share}%
        </div>
        <div style='position: absolute; top: 0; left: {player_share}%; right: 0; height: 100%; background: #dc2626; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 12px;'>
            {competitor_share}% (konkurencja)
        </div>
    </div>
    <div style='margin-top: 8px; color: {trend_color}; font-size: 13px; font-weight: 500;'>
        {trend_emoji} Trend: {trend.upper()} ({trend_pct:+.0f}%)
    </div>
    <div style='margin-top: 4px; color: #6b7280; font-size: 12px;'>
        Twoja sprzedaż: {player_volume} szt/tydz. z {total_volume} szt całkowitej sprzedaży
    </div>
</div>
                """
                st.markdown(progress_html, unsafe_allow_html=True)
                
                # Wykres historii (jeśli jest)
                history = market_data.get('history', [])
                if len(history) >= 2:
                    st.markdown("**📊 Historia Market Share:**")
                    
                    import pandas as pd
                    
                    # Przygotuj dane dla wykresu
                    chart_data = pd.DataFrame(history)
                    chart_data['month'] = pd.to_datetime(chart_data['month'])
                    chart_data = chart_data.set_index('month')
                    chart_data = chart_data.rename(columns={'player_share': 'Twój udział (%)'})
                    
                    # Dodaj konkurencję
                    chart_data['Konkurencja (%)'] = 100 - chart_data['Twój udział (%)']
                    
                    st.line_chart(chart_data[['Twój udział (%)', 'Konkurencja (%)']])
                
            else:
                # Nieodkryte
                st.info("🔒 **Możliwości zakupowe nieznane**")
                st.caption("Odwiedź sklep kilka razy (~4 wizyty), aby poznać potencjał klienta w tej kategorii.")
                
                # Pokazuj wykres market share OD RAZU (punkt startu 0%)
                st.markdown("**📈 Market Share: 0%**")
                st.caption("Nie sprzedajesz jeszcze produktów w tej kategorii")
                
                # Progress bar na 0%
                progress_html = """
<div style='margin: 12px 0;'>
    <div style='width: 100%; background: #dc2626; border-radius: 8px; height: 28px; overflow: hidden; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 12px;'>
        100% (konkurencja)
    </div>
    <div style='margin-top: 8px; color: #6b7280; font-size: 13px;'>
        ➡️ Trend: BRAK DANYCH
    </div>
</div>
                """
                st.markdown(progress_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =============================================================================
    # VISIT TRACKER
    # =============================================================================
    
    st.markdown("### 📅 Wizyty")
    
    last_visit = client_data.get("last_visit_date")
    next_visit = client_data.get("next_visit_due")
    
    col_last, col_next = st.columns(2)
    
    with col_last:
        if last_visit:
            visit_dt = datetime.fromisoformat(last_visit)
            days_ago = (datetime.now() - visit_dt).days
            st.info(f"🕐 Ostatnia wizyta: **{days_ago} dni temu**")
        else:
            st.warning("⚠️ Brak historii wizyt")
    
    with col_next:
        if next_visit and status == "active":
            overdue, days = is_visit_overdue(client_data)
            if overdue:
                st.error(f"🚨 Spóźnienie: **{days} dni**")
            else:
                st.success(f"✅ Następna wizyta: **{next_visit}**")
        elif status == "prospect":
            st.info("🎯 Prospect - umów pierwszą wizytę!")
        else:
            st.caption("—")
    
    # =============================================================================
    # CLIENT DISCOVERY PROFILE
    # =============================================================================
    
    st.markdown("### 🔍 Profil Klienta")
    
    # Get discovered info and knowledge level
    discovered_info = client_data.get("discovered_info", {})
    knowledge_level = client_data.get("knowledge_level", 0)
    
    # Knowledge level display
    stars_full = "⭐" * knowledge_level
    stars_empty = "☆" * (5 - knowledge_level)
    
    knowledge_labels = {
        0: "Nieznajomy",
        1: "Nieznajomy",
        2: "Powierzchowny",
        3: "Dobry",
        4: "Bardzo dobry",
        5: "Ekspert"
    }
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #6366f115 0%, #6366f105 100%); 
                padding: 16px; border-radius: 12px; margin-bottom: 16px;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <div style='font-size: 18px; font-weight: 600; color: #1e293b;'>
                    Poziom znajomości: {knowledge_labels.get(knowledge_level, 'Nieznajomy')}
                </div>
                <div style='font-size: 24px; margin-top: 4px;'>
                    {stars_full}{stars_empty}
                </div>
            </div>
            <div style='font-size: 14px; color: #64748b;'>
                {_count_discovered_fields(discovered_info)}/16 pól odkrytych
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Discovered fields
    with st.expander("📋 Szczegóły profilu", expanded=(knowledge_level >= 2)):
        col1, col2 = st.columns(2)
        
        with col1:
            # Personality & Decision Making
            st.markdown("**👤 Charakterystyka właściciela**")
            _render_discovery_field(
                discovered_info.get("personality_description"),
                "Osobowość, styl podejmowania decyzji"
            )
            
            st.markdown("**⚖️ Priorytety decyzyjne**")
            priorities = discovered_info.get("decision_priorities")
            if priorities:
                st.markdown(f"✅ {', '.join(priorities)}")
            else:
                st.markdown("❓ *Do ustalenia podczas wizyty*")
            
            # Customer Base
            st.markdown("**🎯 Główni klienci sklepu**")
            _render_discovery_field(
                discovered_info.get("main_customers"),
                "Demografia, potrzeby"
            )
            
            st.markdown("**📊 Najlepiej sprzedające się kategorie**")
            categories = discovered_info.get("best_selling_categories")
            if categories:
                st.markdown(f"✅ {', '.join(categories)}")
            else:
                st.markdown("❓ *Do ustalenia*")
        
        with col2:
            # Competition
            st.markdown("**🛒 Obecnie sprzedawane marki**")
            brands = discovered_info.get("competing_brands")
            if brands:
                st.markdown(f"✅ {', '.join(brands)}")
            else:
                st.markdown("❓ *Do ustalenia*")
            
            # Business Needs
            st.markdown("**💡 Potrzeby/Bolesności**")
            pain_points = discovered_info.get("pain_points")
            if pain_points:
                for pain in pain_points:
                    st.markdown(f"• {pain}")
            else:
                st.markdown("❓ *Do ustalenia*")
            
            # Ordering Patterns
            st.markdown("**💰 Typowe zamówienie**")
            _render_discovery_field(
                discovered_info.get("typical_order_value"),
                "Wartość zamówienia"
            )
            
            st.markdown("**📅 Preferowana częstotliwość**")
            _render_discovery_field(
                discovered_info.get("preferred_frequency"),
                "Jak często zamawia"
            )
    
    # Discovery tips (only if knowledge level < 3)
    if knowledge_level < 3:
        with st.expander("💡 Wskazówki - jak odkryć więcej?"):
            tips = [
                "Zadawaj pytania otwarte: 'Jakie kategorie produktów najlepiej się sprzedają w Pana sklepie?'",
                "Słuchaj aktywnie - klient często sam dzieli się informacjami",
                "Pytaj o konkurencję: 'Jakie marki ma Pan obecnie na półce?'",
                "Identyfikuj problemy: 'Z jakimi wyzwaniami boryka się Pan w zarządzaniu asortymentem?'",
                "Poznaj klientów sklepu: 'Kto najczęściej robi u Pana zakupy?'"
            ]
            
            for tip in tips:
                st.markdown(f"🎯 {tip}")
    
    # Discovery notes history
    discovery_notes = client_data.get("discovery_notes", [])
    if discovery_notes:
        with st.expander(f"📝 Historia odkryć ({len(discovery_notes)})"):
            # Show recent notes (max 5)
            recent_notes = sorted(
                discovery_notes, 
                key=lambda x: x.get('visit_date', ''), 
                reverse=True
            )[:5]
            
            for note in recent_notes:
                visit_date = note.get('visit_date', 'N/A')[:10]
                note_text = note.get('note_text', '')
                discovered_fields = note.get('discovered_fields', [])
                
                st.markdown(f"""
                <div style='background: #f1f5f9; padding: 12px; border-radius: 8px; 
                            margin-bottom: 8px; border-left: 3px solid #6366f1;'>
                    <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>
                        📅 {visit_date}
                    </div>
                    <div style='font-size: 14px; color: #1e293b; margin-bottom: 4px;'>
                        {note_text}
                    </div>
                    <div style='font-size: 12px; color: #6366f1;'>
                        🔍 Odkryto: {', '.join(discovered_fields)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # =============================================================================
    # PRODUCTS PORTFOLIO
    # =============================================================================
    
    st.markdown("### 📦 Portfolio Produktów")
    
    portfolio = client_data.get("products_portfolio", [])
    
    if portfolio:
        summary = get_portfolio_summary(client_data)
        
        # Summary cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Produkty", summary['total_products'])
        with col2:
            st.metric("Wartość/mies.", f"{summary['total_value']:,.0f} PLN")
        with col3:
            if summary['top_product']:
                st.metric("Top produkt", summary['top_product'][:20])
        
        # Products table
        st.markdown("**Szczegóły:**")
        
        for entry in portfolio:
            product_id = entry.get("product_id")
            product_info = get_product_info(product_id)
            
            if product_info:
                col_prod, col_vol, col_share = st.columns([3, 1, 1])
                
                with col_prod:
                    st.markdown(f"**{product_info['name']}**")
                    st.caption(f"{product_info['category']} • {product_info['brand']}")
                
                with col_vol:
                    st.markdown(f"📊 **{entry.get('volume', 0)}** szt/mies")
                
                with col_share:
                    market_share = entry.get('market_share', 0)
                    st.markdown(f"📈 **{market_share}%** market")
                
                st.markdown("<div style='margin: 8px 0; border-bottom: 1px solid #e2e8f0;'></div>", 
                           unsafe_allow_html=True)
    else:
        st.info("📭 Brak produktów w portfolio - podpisz pierwszy kontrakt!")
    
    # Cross-sell suggestions (only for ACTIVE clients)
    if status == "active" and len(portfolio) < 5:
        with st.expander("💡 Sugestie Cross-Sell"):
            suggestions = suggest_cross_sell_products(client_data, max_suggestions=3)
            
            if suggestions:
                for sugg in suggestions:
                    prod = sugg['product']
                    priority_colors = {"high": "#10b981", "medium": "#f59e0b", "low": "#64748b"}
                    color = priority_colors.get(sugg['priority'], "#64748b")
                    
                    st.markdown(f"""
                    <div style='background: {color}10; padding: 12px; border-radius: 8px; 
                                border-left: 4px solid {color}; margin-bottom: 8px;'>
                        <div style='font-weight: 600; color: #1e293b; margin-bottom: 4px;'>
                            {prod['name']}
                        </div>
                        <div style='font-size: 13px; color: #64748b; margin-bottom: 8px;'>
                            {sugg['reason']}
                        </div>
                        <div style='font-size: 12px; color: {color}; font-weight: 600;'>
                            💰 Margin: {prod['margin_percent']:.1f}% • 
                            📦 Expected volume: {sugg['expected_volume']} szt/mies
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # TODO: Add button to add product
                    # if st.button(f"➕ Dodaj {prod['name']}", key=f"add_{prod['id']}"):
                    #     add_product_to_portfolio(client_data, prod['id'], initial_volume=sugg['expected_volume'])
            else:
                st.caption("Brak sugestii cross-sell w tym momencie")
    
    # =============================================================================
    # EVENTS TIMELINE
    # =============================================================================
    
    st.markdown("### 📜 Historia Wydarzeń")
    
    timeline = client_data.get("events_timeline", [])
    
    if timeline:
        # Show last 10 events
        recent_events = sorted(timeline, key=lambda x: x.get('date', ''), reverse=True)[:10]
        
        for event in recent_events:
            date = event.get('date', 'N/A')[:10]  # YYYY-MM-DD only
            event_type = event.get('type', 'unknown')
            desc = event.get('description', 'Wydarzenie')
            rep_change = event.get('reputation_change', 0)
            
            # Icon based on event type
            icons = {
                'first_visit': '🎯',
                'contract_signed': '📝',
                'visit': '👔',
                'cross_sell': '🆕',
                'volume_change': '📊',
                'product_removed': '❌',
                'lost': '💀',
                'regular_visit_on_time': '✅',
                'visit_excellent_5stars': '⭐',
                'visit_late_1_7days': '⏰',
                'visit_late_8_14days': '⚠️',
                'visit_late_15plus': '🚨'
            }
            icon = icons.get(event_type, '📌')
            
            # Color based on reputation change
            if rep_change > 0:
                color = "#10b981"
                change_text = f"+{rep_change}"
            elif rep_change < 0:
                color = "#ef4444"
                change_text = f"{rep_change}"
            else:
                color = "#64748b"
                change_text = "—"
            
            st.markdown(f"""
            <div style='background: white; padding: 12px 16px; border-radius: 8px; 
                        border-left: 3px solid {color}; margin-bottom: 8px; 
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div style='flex: 1;'>
                        <div style='font-size: 13px; color: #64748b; margin-bottom: 4px;'>
                            {icon} {date}
                        </div>
                        <div style='font-size: 14px; color: #1e293b;'>
                            {desc}
                        </div>
                    </div>
                    <div style='font-size: 16px; font-weight: 700; color: {color}; margin-left: 16px;'>
                        {change_text}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 Brak historii - rozpocznij współpracę z klientem!")
    
    # Back button
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    if st.button("⬅️ Powrót do listy klientów", type="secondary", use_container_width=True):
        st.session_state['show_client_detail'] = False
        st.rerun()
