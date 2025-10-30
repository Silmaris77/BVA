"""
🎴 FMCG Client Detail Card Component
Rozszerzony widok klienta z reputacją, portfolio i timeline
"""

import streamlit as st
from typing import Dict
from datetime import datetime
from utils.fmcg_client_helpers import get_reputation_status, is_visit_overdue
from utils.fmcg_products import get_product_info, get_portfolio_summary, suggest_cross_sell_products


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
