"""
Delayed Orders Processor - Background Time-Based Processing
===========================================================

Ten moduł przetwarza pending orders w tle, symulując telefony klientów do dystrybutorów.
Wywoływany automatycznie przy zmianie dnia w grze.
"""

from datetime import datetime
from typing import Dict, List, Tuple
from utils.delayed_orders import check_pending_orders


def process_daily_delayed_orders(
    game_state: Dict,
    current_game_date: str
) -> Tuple[Dict, List[Dict]]:
    """
    Przetwarza wszystkie pending orders dla aktualnej daty gry.
    
    Args:
        game_state: Stan gry gracza
        current_game_date: Aktualna data w grze (YYYY-MM-DD)
        
    Returns:
        Tuple[updated_game_state, notifications]
        - updated_game_state: Zaktualizowany game_state z nowymi zamówieniami
        - notifications: Lista powiadomień do wyświetlenia graczowi
    """
    notifications = []
    
    # Pobierz klientów
    clients = game_state.get('clients', {})
    
    # Sprawdź każdego klienta
    for client_id, client_data in clients.items():
        conviction_data = client_data.get('conviction_data', {})
        
        # Sprawdź każdy produkt
        for product_id, product_conv in conviction_data.items():
            pending_orders = product_conv.get('pending_orders', [])
            
            if not pending_orders:
                continue
            
            # Sprawdź pending orders dla tego produktu
            updated_pending, new_orders = check_pending_orders(
                pending_orders,
                current_game_date
            )
            
            # Zaktualizuj pending orders
            product_conv['pending_orders'] = updated_pending
            
            # Przetwórz nowe zamówienia
            for order in new_orders:
                # Dodaj zamówienie do dystrybutora
                distributor_name = order.get('distributor_name', 'Orbico')
                
                # Inicjalizuj strukturę dystrybutorów jeśli nie istnieje
                if 'distributors' not in game_state:
                    game_state['distributors'] = {}
                
                if distributor_name not in game_state['distributors']:
                    game_state['distributors'][distributor_name] = {
                        'name': distributor_name,
                        'orders_received': [],
                        'inventory': {}
                    }
                
                # Dodaj zamówienie do listy dystrybutora
                if 'orders_received' not in game_state['distributors'][distributor_name]:
                    game_state['distributors'][distributor_name]['orders_received'] = []
                
                game_state['distributors'][distributor_name]['orders_received'].append({
                    'order_id': f"PTO_{client_id}_{product_id}_{current_game_date}",
                    'source': 'pull_through',
                    'client_id': order['client_id'],
                    'client_name': order['client_name'],
                    'product_id': order['product_id'],
                    'quantity': order['quantity'],
                    'order_date': current_game_date,
                    'convinced_on': order['convinced_on'],
                    'delay_days': order['delay_days'],
                    'status': 'new'  # new, viewed, fulfilled
                })
                
                # Utwórz notyfikację
                notification = {
                    'type': 'pull_through_order',
                    'title': '🎯 Pull-Through Effect!',
                    'message': f"""**{order['client_name']}** właśnie złożył zamówienie przez dystrybutora **{distributor_name}**!

📦 **Produkt:** {order['product_id']}  
📊 **Ilość:** {order['quantity']} szt.  
📅 **Przekonany:** {order['convinced_on']} ({order['delay_days']} dni temu)  
✅ **Zamówienie:** {current_game_date}

To efekt Twojej wcześniejszej pracy conviction! Sprawdź kartę dystrybutora.
""",
                    'client_id': order['client_id'],
                    'product_id': order['product_id'],
                    'date': current_game_date,
                    'priority': 'high'
                }
                notifications.append(notification)
    
    # Zaktualizuj ostatni dzień przetwarzania
    game_state['last_delayed_orders_check'] = current_game_date
    
    return game_state, notifications


def get_pull_through_notifications(game_state: Dict) -> List[Dict]:
    """
    Pobiera nieprzeczytane notyfikacje pull-through.
    
    Returns:
        Lista notyfikacji do wyświetlenia
    """
    # Dla przyszłej implementacji - system notyfikacji
    # Na razie zwracamy puste
    return []


def mark_distributor_order_as_viewed(
    game_state: Dict,
    distributor_name: str,
    order_id: str
) -> Dict:
    """
    Oznacza zamówienie dystrybutora jako przejrzane.
    
    Returns:
        Zaktualizowany game_state
    """
    if 'distributors' not in game_state:
        return game_state
    
    if distributor_name not in game_state['distributors']:
        return game_state
    
    orders = game_state['distributors'][distributor_name].get('orders_received', [])
    
    for order in orders:
        if order.get('order_id') == order_id:
            order['status'] = 'viewed'
            order['viewed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return game_state


def get_new_pull_through_count(game_state: Dict) -> int:
    """
    Zwraca liczbę nowych (nieprzejrzanych) zamówień pull-through.
    
    Returns:
        Liczba nowych zamówień
    """
    count = 0
    
    distributors = game_state.get('distributors', {})
    for dist_name, dist_data in distributors.items():
        orders = dist_data.get('orders_received', [])
        count += sum(1 for o in orders if o.get('source') == 'pull_through' and o.get('status') == 'new')
    
    return count


def simulate_distributor_inventory_deduction(
    game_state: Dict,
    distributor_name: str,
    product_id: str,
    quantity: int
) -> Tuple[Dict, bool, str]:
    """
    Symuluje odjęcie produktu z inwentarza dystrybutora po zamówieniu klienta.
    
    Returns:
        Tuple[updated_game_state, success, message]
    """
    if 'distributors' not in game_state:
        return game_state, False, "Brak dystrybutorów w systemie"
    
    if distributor_name not in game_state['distributors']:
        return game_state, False, f"Dystrybutor {distributor_name} nie istnieje"
    
    inventory = game_state['distributors'][distributor_name].get('inventory', {})
    
    if product_id not in inventory:
        return game_state, False, f"Dystrybutor nie ma {product_id} w magazynie (0 szt.)"
    
    available = inventory[product_id].get('quantity', 0)
    
    if available < quantity:
        if available > 0:
            # Częściowa realizacja
            inventory[product_id]['quantity'] = 0
            msg = f"⚠️ Częściowa realizacja: dystrybutor miał tylko {available}/{quantity} szt."
            return game_state, True, msg
        else:
            return game_state, False, f"❌ Brak towaru - dystrybutor ma 0 szt."
    
    # Pełna realizacja
    inventory[product_id]['quantity'] -= quantity
    msg = f"✅ Zamówienie zrealizowane: -{quantity} szt. (pozostało: {inventory[product_id]['quantity']})"
    
    return game_state, True, msg
