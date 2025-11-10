"""
Heinz Conviction KPIs - Dashboard Metrics
==========================================

Oblicza i wyświetla KPI dla mechaniki conviction (Heinz scenario).
"""

from typing import Dict, List, Tuple
from datetime import datetime


def calculate_conviction_kpis(clients: Dict) -> Dict:
    """
    Oblicza KPI conviction dla wszystkich klientów.
    
    Returns:
        Dict z metrykami:
        - active_convictions: Liczba klientów z conviction w toku (1-99%)
        - won_clients: Liczba klientów przekonanych (100%)
        - total_attempts: Łączna liczba prób conviction
        - avg_progress: Średni progress conviction
        - conviction_rate: % przekonanych z tych, którzy mają jakikolwiek progress
        - products_in_progress: Liczba produktów w trakcie conviction
        - products_won: Liczba przekonanych produktów
        - avg_conviction_time_days: Średni czas od startu do WON (w dniach)
        - stage_distribution: Dict z liczbą klientów w każdym etapie
    """
    active_convictions = 0
    won_clients = 0
    total_attempts = 0
    total_progress = 0
    products_in_progress = 0
    products_won = 0
    conviction_times = []
    
    stage_distribution = {
        'discovery': 0,
        'pitch': 0,
        'convince': 0,
        'won': 0
    }
    
    clients_with_conviction = 0
    
    for client_id, client_data in clients.items():
        conviction_data = client_data.get('conviction_data', {})
        
        if not conviction_data:
            continue
        
        for product_id, product_conv in conviction_data.items():
            stage = product_conv.get('stage', 'discovery')
            progress = product_conv.get('progress', 0)
            conversation_history = product_conv.get('conversation_history', [])
            
            # Zlicz produkty
            if progress > 0:
                products_in_progress += 1
                total_progress += progress
            
            if progress >= 100 or stage == 'won':
                products_won += 1
                
                # Oblicz czas conviction (jeśli są dane)
                if 'started_date' in product_conv and conversation_history:
                    try:
                        started = datetime.strptime(product_conv['started_date'], "%Y-%m-%d")
                        # Znajdź datę WON (ostatnia konwersacja)
                        last_conv = conversation_history[-1]
                        won_date = datetime.strptime(last_conv['date'], "%Y-%m-%d")
                        days_to_convince = (won_date - started).days
                        conviction_times.append(days_to_convince)
                    except:
                        pass
            
            # Zlicz próby
            total_attempts += len(conversation_history)
            
            # Stage distribution
            stage_distribution[stage] = stage_distribution.get(stage, 0) + 1
        
        # Sprawdź status klienta
        if conviction_data:
            clients_with_conviction += 1
            
            # Czy klient ma przynajmniej 1 produkt WON?
            has_won = any(
                p.get('progress', 0) >= 100 or p.get('stage') == 'won' 
                for p in conviction_data.values()
            )
            
            # Czy klient ma produkty w toku (nie WON)?
            has_active = any(
                0 < p.get('progress', 0) < 100 and p.get('stage') != 'won'
                for p in conviction_data.values()
            )
            
            if has_won:
                won_clients += 1
            
            if has_active:
                active_convictions += 1
    
    # Oblicz średnie
    avg_progress = (total_progress / products_in_progress) if products_in_progress > 0 else 0
    conviction_rate = (products_won / products_in_progress * 100) if products_in_progress > 0 else 0
    avg_conviction_time = sum(conviction_times) / len(conviction_times) if conviction_times else 0
    
    return {
        'active_convictions': active_convictions,
        'won_clients': won_clients,
        'total_attempts': total_attempts,
        'avg_progress': avg_progress,
        'conviction_rate': conviction_rate,
        'products_in_progress': products_in_progress,
        'products_won': products_won,
        'avg_conviction_time_days': avg_conviction_time,
        'stage_distribution': stage_distribution,
        'clients_with_conviction': clients_with_conviction
    }


def calculate_pull_through_kpis(game_state: Dict) -> Dict:
    """
    Oblicza KPI pull-through (zamówienia dystrybutorów).
    
    Returns:
        Dict z metrykami:
        - pending_orders: Liczba oczekujących zamówień
        - completed_orders: Liczba zrealizowanych zamówień
        - cancelled_orders: Liczba anulowanych
        - pull_through_rate: % zrealizowanych z wszystkich (pending + completed + cancelled)
        - total_quantity_ordered: Łączna ilość zamówiona (szt.)
        - avg_delay_days: Średni czas od conviction do zamówienia
    """
    pending = 0
    completed = 0
    cancelled = 0
    total_quantity = 0
    delay_days_list = []
    
    # Sprawdź pending_orders w conviction_data klientów
    clients = game_state.get('clients', {})
    for client_id, client_data in clients.items():
        conviction_data = client_data.get('conviction_data', {})
        
        for product_id, product_conv in conviction_data.items():
            pending_orders = product_conv.get('pending_orders', [])
            
            for order in pending_orders:
                status = order.get('status', 'pending')
                
                if status == 'pending':
                    pending += 1
                elif status == 'ordered':
                    completed += 1
                    total_quantity += order.get('quantity', 0)
                    delay_days_list.append(order.get('delay_days', 0))
                elif status == 'cancelled':
                    cancelled += 1
    
    # Sprawdź też distributors.orders_received
    distributors = game_state.get('distributors', {})
    for dist_name, dist_data in distributors.items():
        orders = dist_data.get('orders_received', [])
        
        for order in orders:
            if order.get('source') == 'pull_through':
                # Te są już completed (znalazły się w systemie dystrybutora)
                if order.get('delay_days') not in delay_days_list:  # Unikaj duplikatów
                    delay_days_list.append(order.get('delay_days', 0))
    
    total_all = pending + completed + cancelled
    pull_through_rate = (completed / total_all * 100) if total_all > 0 else 0
    avg_delay = sum(delay_days_list) / len(delay_days_list) if delay_days_list else 0
    
    return {
        'pending_orders': pending,
        'completed_orders': completed,
        'cancelled_orders': cancelled,
        'pull_through_rate': pull_through_rate,
        'total_quantity_ordered': total_quantity,
        'avg_delay_days': avg_delay,
        'total_orders': total_all
    }


def render_conviction_kpis_widget(clients: Dict, game_state: Dict = None) -> None:
    """
    Renderuje widget z KPI conviction dla Dashboard.
    """
    import streamlit as st
    
    kpis = calculate_conviction_kpis(clients)
    
    st.markdown("### 🎯 Conviction Performance (Heinz)")
    
    # Główne metryki
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔄 Active Convictions",
            kpis['active_convictions'],
            help="Klienci z conviction w toku (1-99% progress)"
        )
    
    with col2:
        st.metric(
            "✅ Won Clients",
            kpis['won_clients'],
            help="Klienci przekonani (100% progress)"
        )
    
    with col3:
        st.metric(
            "📈 Conviction Rate",
            f"{kpis['conviction_rate']:.0f}%",
            help="% przekonanych produktów z wszystkich w toku"
        )
    
    with col4:
        st.metric(
            "⏱️ Avg Time to Won",
            f"{kpis['avg_conviction_time_days']:.1f} dni",
            help="Średni czas od pierwszej konwersacji do WON"
        )
    
    # Dodatkowe metryki
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            "📦 Products in Progress",
            kpis['products_in_progress']
        )
    
    with col6:
        st.metric(
            "🎁 Products Won",
            kpis['products_won']
        )
    
    with col7:
        st.metric(
            "💬 Total Attempts",
            kpis['total_attempts']
        )
    
    with col8:
        st.metric(
            "📊 Avg Progress",
            f"{kpis['avg_progress']:.0f}%"
        )
    
    # Stage Distribution
    st.markdown("**📊 Stage Distribution:**")
    
    dist = kpis['stage_distribution']
    stage_col1, stage_col2, stage_col3, stage_col4 = st.columns(4)
    
    with stage_col1:
        st.markdown(f"""
        <div style='background: #eff6ff; padding: 12px; border-radius: 8px; text-align: center; border-left: 4px solid #3b82f6;'>
            <div style='font-size: 24px; font-weight: 600; color: #1e40af;'>{dist.get('discovery', 0)}</div>
            <div style='font-size: 12px; color: #60a5fa; font-weight: 600;'>🔍 DISCOVERY</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stage_col2:
        st.markdown(f"""
        <div style='background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center; border-left: 4px solid #f59e0b;'>
            <div style='font-size: 24px; font-weight: 600; color: #92400e;'>{dist.get('pitch', 0)}</div>
            <div style='font-size: 12px; color: #f59e0b; font-weight: 600;'>💼 PITCH</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stage_col3:
        st.markdown(f"""
        <div style='background: #fce7f3; padding: 12px; border-radius: 8px; text-align: center; border-left: 4px solid #ec4899;'>
            <div style='font-size: 24px; font-weight: 600; color: #9f1239;'>{dist.get('convince', 0)}</div>
            <div style='font-size: 12px; color: #ec4899; font-weight: 600;'>🎯 CONVINCE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stage_col4:
        st.markdown(f"""
        <div style='background: #dcfce7; padding: 12px; border-radius: 8px; text-align: center; border-left: 4px solid #10b981;'>
            <div style='font-size: 24px; font-weight: 600; color: #065f46;'>{dist.get('won', 0)}</div>
            <div style='font-size: 12px; color: #10b981; font-weight: 600;'>🏆 WON</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Pull-Through KPIs (jeśli game_state dostępne)
    if game_state:
        st.markdown("---")
        st.markdown("### 📦 Pull-Through Performance")
        
        pt_kpis = calculate_pull_through_kpis(game_state)
        
        pt_col1, pt_col2, pt_col3, pt_col4 = st.columns(4)
        
        with pt_col1:
            st.metric(
                "⏳ Pending Orders",
                pt_kpis['pending_orders'],
                help="Oczekujące zamówienia (klient zadzwoni za 1-3 dni)"
            )
        
        with pt_col2:
            st.metric(
                "✅ Completed Orders",
                pt_kpis['completed_orders'],
                help="Zrealizowane zamówienia przez dystrybutorów"
            )
        
        with pt_col3:
            st.metric(
                "📈 Pull-Through Rate",
                f"{pt_kpis['pull_through_rate']:.0f}%",
                help="% zrealizowanych z wszystkich zamówień"
            )
        
        with pt_col4:
            st.metric(
                "⏱️ Avg Delay",
                f"{pt_kpis['avg_delay_days']:.1f} dni",
                help="Średni czas od conviction do zamówienia"
            )
