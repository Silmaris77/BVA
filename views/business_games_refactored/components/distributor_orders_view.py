"""
Distributor Orders View - Pull-Through Orders Display
=====================================================

Wyświetla zamówienia pull-through od przekonanych klientów.
Gracz może śledzić efekty swojej pracy conviction.
"""

import streamlit as st
from typing import Dict, List
from datetime import datetime, timedelta


def render_distributor_orders_modal(
    game_state: Dict,
    distributor_name: str = "Orbico",
    days_back: int = 7
) -> None:
    """
    Wyświetla modal z zamówieniami pull-through dla danego dystrybutora.
    
    Args:
        game_state: Stan gry
        distributor_name: Nazwa dystrybutora
        days_back: Ile dni wstecz pokazać zamówienia
    """
    st.markdown(f"### 📦 Zamówienia Pull-Through - {distributor_name}")
    st.caption(f"Ostatnie {days_back} dni")
    
    # Pobierz dystrybutora
    distributors = game_state.get('distributors', {})
    
    if distributor_name not in distributors:
        st.warning(f"⚠️ Dystrybutor **{distributor_name}** nie ma jeszcze żadnych zamówień.")
        st.info("💡 Przekonaj klientów do produktów Heinz, a za kilka dni zobaczysz tutaj ich zamówienia!")
        return
    
    distributor = distributors[distributor_name]
    orders = distributor.get('orders_received', [])
    
    # Filtruj tylko pull-through z ostatnich N dni
    current_date_str = game_state.get('current_game_date', datetime.now().strftime("%Y-%m-%d"))
    current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    cutoff_date = current_date - timedelta(days=days_back)
    
    pull_through_orders = [
        o for o in orders 
        if o.get('source') == 'pull_through' 
        and datetime.strptime(o.get('order_date', '2000-01-01'), "%Y-%m-%d") >= cutoff_date
    ]
    
    if not pull_through_orders:
        st.info(f"""
        📭 **Brak zamówień pull-through w ostatnich {days_back} dniach**
        
        💡 Aby zobaczyć zamówienia:
        1. Przekonaj klienta do produktu Heinz (100% progress)
        2. Kliknij "⏭️ Następny dzień" (1-3 razy)
        3. Klient zadzwoni do dystrybutora
        4. Zamówienie pojawi się tutaj!
        """)
        return
    
    # Statystyki
    total_orders = len(pull_through_orders)
    total_quantity = sum(o.get('quantity', 0) for o in pull_through_orders)
    new_orders = sum(1 for o in pull_through_orders if o.get('status') == 'new')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Zamówienia", total_orders)
    with col2:
        st.metric("📊 Łączna ilość", f"{total_quantity} szt.")
    with col3:
        st.metric("🆕 Nowe", new_orders, delta=f"+{new_orders}" if new_orders > 0 else None)
    
    st.markdown("---")
    
    # Lista zamówień (od najnowszych)
    sorted_orders = sorted(
        pull_through_orders, 
        key=lambda x: x.get('order_date', ''), 
        reverse=True
    )
    
    for order in sorted_orders:
        order_id = order.get('order_id', 'N/A')
        client_name = order.get('client_name', 'Nieznany')
        product_id = order.get('product_id', 'N/A')
        quantity = order.get('quantity', 0)
        order_date = order.get('order_date', 'N/A')
        convinced_on = order.get('convinced_on', 'N/A')
        delay_days = order.get('delay_days', 0)
        status = order.get('status', 'new')
        
        # Ikona statusu
        status_icons = {
            'new': '🆕',
            'viewed': '👁️',
            'fulfilled': '✅'
        }
        status_icon = status_icons.get(status, '📦')
        
        # Kolor obramowania
        status_colors = {
            'new': '#10b981',
            'viewed': '#3b82f6',
            'fulfilled': '#6b7280'
        }
        border_color = status_colors.get(status, '#d1d5db')
        
        with st.expander(f"{status_icon} **{client_name}** - {product_id} ({quantity} szt.) - {order_date}", expanded=(status == 'new')):
            col_info, col_action = st.columns([3, 1])
            
            with col_info:
                st.markdown(f"""
                <div style='background: #f8fafc; padding: 12px; border-radius: 6px; border-left: 4px solid {border_color};'>
                    <div style='margin-bottom: 8px;'>
                        <strong style='color: #1e293b;'>🏢 Klient:</strong> {client_name}
                    </div>
                    <div style='margin-bottom: 8px;'>
                        <strong style='color: #1e293b;'>📦 Produkt:</strong> {product_id}
                    </div>
                    <div style='margin-bottom: 8px;'>
                        <strong style='color: #1e293b;'>📊 Ilość:</strong> {quantity} szt.
                    </div>
                    <div style='margin-bottom: 8px;'>
                        <strong style='color: #1e293b;'>📅 Data zamówienia:</strong> {order_date}
                    </div>
                    <div style='margin-bottom: 8px;'>
                        <strong style='color: #1e293b;'>🎯 Przekonany:</strong> {convinced_on} ({delay_days} dni temu)
                    </div>
                    <div style='padding: 8px; background: #dcfce7; border-radius: 4px; margin-top: 8px;'>
                        <strong style='color: #065f46;'>💡 Pull-Through Effect!</strong><br>
                        <span style='color: #047857; font-size: 13px;'>
                            To efekt Twojej pracy - klient sam zadzwonił do dystrybutora.
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_action:
                if status == 'new':
                    if st.button("✅ Oznacz jako przejrzane", key=f"mark_{order_id}"):
                        # Oznacz jako viewed
                        order['status'] = 'viewed'
                        order['viewed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.success("Oznaczono!")
                        st.rerun()
                elif status == 'viewed':
                    st.caption("👁️ Przejrzane")
                else:
                    st.caption("✅ Zrealizowane")
    
    st.markdown("---")
    
    # Podsumowanie pull-through
    st.markdown("### 📈 Analiza Pull-Through")
    
    # Grupowanie po klientach
    clients_ordering = {}
    for order in pull_through_orders:
        client_id = order.get('client_id')
        client_name = order.get('client_name')
        if client_id:
            if client_id not in clients_ordering:
                clients_ordering[client_id] = {
                    'name': client_name,
                    'orders': 0,
                    'total_quantity': 0
                }
            clients_ordering[client_id]['orders'] += 1
            clients_ordering[client_id]['total_quantity'] += order.get('quantity', 0)
    
    if clients_ordering:
        st.markdown("**🏆 Najlepsi klienci pull-through:**")
        
        # Sortuj po ilości zamówień
        top_clients = sorted(
            clients_ordering.items(),
            key=lambda x: x[1]['total_quantity'],
            reverse=True
        )[:5]
        
        for client_id, data in top_clients:
            st.markdown(f"""
            <div style='background: white; padding: 8px 12px; border-radius: 6px; margin-bottom: 4px; border-left: 3px solid #10b981;'>
                <strong>{data['name']}</strong> - {data['orders']} zamówień ({data['total_quantity']} szt.)
            </div>
            """, unsafe_allow_html=True)
    
    # Grupowanie po produktach
    products_ordered = {}
    for order in pull_through_orders:
        product_id = order.get('product_id')
        if product_id:
            if product_id not in products_ordered:
                products_ordered[product_id] = 0
            products_ordered[product_id] += order.get('quantity', 0)
    
    if products_ordered:
        st.markdown("**📦 Najpopularniejsze produkty:**")
        
        top_products = sorted(
            products_ordered.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for product_id, quantity in top_products:
            st.markdown(f"""
            <div style='background: white; padding: 8px 12px; border-radius: 6px; margin-bottom: 4px; border-left: 3px solid #3b82f6;'>
                <strong>{product_id}</strong> - {quantity} szt.
            </div>
            """, unsafe_allow_html=True)


def get_pull_through_badge_count(game_state: Dict, distributor_name: str = "Orbico") -> int:
    """
    Zwraca liczbę nowych (nieprzejrzanych) zamówień pull-through.
    
    Returns:
        Liczba nowych zamówień
    """
    distributors = game_state.get('distributors', {})
    
    if distributor_name not in distributors:
        return 0
    
    orders = distributors[distributor_name].get('orders_received', [])
    
    new_count = sum(
        1 for o in orders 
        if o.get('source') == 'pull_through' and o.get('status') == 'new'
    )
    
    return new_count
