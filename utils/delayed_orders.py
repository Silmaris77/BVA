"""
Delayed Orders System for Heinz Food Service Scenario
======================================================

W modelu "Through Distributor", po przekonaniu klienta (progress=100%),
restauracja NIE składa zamówienia natychmiast przez gracza.
Zamiast tego:
1. Klient jest oznaczony jako "convinced" 
2. Za 1-3 dni klient SAM dzwoni do dystrybutora (Orbico)
3. Zamówienie pojawia się w systemie dystrybutora
4. Gracz dostaje powiadomienie o "pull-through" efekcie

Ten moduł zarządza symulacją opóźnionych zamówień.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


def create_pending_order(
    client_id: str,
    client_name: str,
    product_id: str,
    date_convinced: str,
    distributor_name: str = "Orbico"
) -> Dict:
    """
    Tworzy pending order po przekonaniu klienta.
    
    Args:
        client_id: ID klienta (np. "rest_005")
        client_name: Nazwa restauracji
        product_id: ID produktu Heinz
        date_convinced: Data przekonania (YYYY-MM-DD)
        distributor_name: Nazwa dystrybutora
        
    Returns:
        Dict z danymi pending order
    """
    # Losuj delay 1-3 dni (weighted: 40% 1 dzień, 40% 2 dni, 20% 3 dni)
    delay_days = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
    
    convinced_date = datetime.strptime(date_convinced, "%Y-%m-%d")
    expected_order_date = convinced_date + timedelta(days=delay_days)
    
    # Losuj ilość (realistyczne zamówienie testowe)
    # Małe restauracje: 1-2 opakowania, średnie: 2-4, duże: 4-6
    quantity = random.choices([1, 2, 3, 4, 5, 6], weights=[20, 30, 25, 15, 7, 3])[0]
    
    return {
        "client_id": client_id,
        "client_name": client_name,
        "product_id": product_id,
        "distributor_name": distributor_name,
        "date_convinced": date_convinced,
        "expected_order_date": expected_order_date.strftime("%Y-%m-%d"),
        "delay_days": delay_days,
        "quantity": quantity,
        "status": "pending",  # pending, ordered, cancelled
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def check_pending_orders(
    pending_orders: List[Dict],
    current_date: str
) -> Tuple[List[Dict], List[Dict]]:
    """
    Sprawdza pending orders i konwertuje te, których czas nadszedł.
    
    Args:
        pending_orders: Lista pending orders
        current_date: Aktualna data gry (YYYY-MM-DD)
        
    Returns:
        Tuple[updated_pending_orders, new_orders]
        - updated_pending_orders: Lista z zaktualizowanymi statusami
        - new_orders: Lista zamówień do dodania do dystrybutora
    """
    current = datetime.strptime(current_date, "%Y-%m-%d")
    updated_pending = []
    new_orders = []
    
    for order in pending_orders:
        if order["status"] != "pending":
            updated_pending.append(order)
            continue
            
        expected = datetime.strptime(order["expected_order_date"], "%Y-%m-%d")
        
        # Jeśli czas nadszedł (lub minął)
        if current >= expected:
            # 90% szans na złożenie zamówienia, 10% na anulowanie
            if random.random() < 0.9:
                order["status"] = "ordered"
                order["ordered_at"] = current_date
                
                # Utwórz zamówienie dla dystrybutora
                new_order = {
                    "source": "pull_through",  # Oznaczenie, że to efekt conviction
                    "client_id": order["client_id"],
                    "client_name": order["client_name"],
                    "product_id": order["product_id"],
                    "quantity": order["quantity"],
                    "order_date": current_date,
                    "convinced_on": order["date_convinced"],
                    "delay_days": order["delay_days"]
                }
                new_orders.append(new_order)
            else:
                order["status"] = "cancelled"
                order["cancelled_at"] = current_date
                order["cancel_reason"] = random.choice([
                    "Zmiana menu",
                    "Problemy budżetowe",
                    "Konkurencyjna oferta",
                    "Opóźnienie decyzji"
                ])
        
        updated_pending.append(order)
    
    return updated_pending, new_orders


def get_pending_orders_summary(pending_orders: List[Dict]) -> Dict:
    """
    Zwraca podsumowanie pending orders.
    
    Returns:
        Dict z statystykami
    """
    total = len(pending_orders)
    pending = sum(1 for o in pending_orders if o["status"] == "pending")
    ordered = sum(1 for o in pending_orders if o["status"] == "ordered")
    cancelled = sum(1 for o in pending_orders if o["status"] == "cancelled")
    
    return {
        "total": total,
        "pending": pending,
        "ordered": ordered,
        "cancelled": cancelled,
        "conversion_rate": (ordered / total * 100) if total > 0 else 0
    }


def add_pending_order_to_conviction_data(
    conviction_data: Dict,
    product_id: str,
    current_date: str,
    distributor_name: str = "Orbico"
) -> Dict:
    """
    Dodaje pending order do conviction_data klienta.
    
    Args:
        conviction_data: Dict conviction_data klienta
        product_id: ID produktu
        current_date: Aktualna data gry
        distributor_name: Nazwa dystrybutora
        
    Returns:
        Zaktualizowany conviction_data
    """
    if product_id not in conviction_data:
        return conviction_data
    
    product_conv = conviction_data[product_id]
    
    # Inicjalizuj pending_orders jeśli nie istnieje
    if "pending_orders" not in product_conv:
        product_conv["pending_orders"] = []
    
    # Nie dodawaj jeśli już jest pending order dla tego produktu
    existing_pending = [
        o for o in product_conv["pending_orders"] 
        if o["status"] == "pending"
    ]
    if existing_pending:
        return conviction_data
    
    # Tworz pending order (wymaga client_id i client_name z zewnątrz)
    # Ta funkcja tylko aktualizuje strukturę, właściwe tworzenie w visit_panel
    
    return conviction_data


def format_pending_order_notification(order: Dict) -> str:
    """
    Formatuje powiadomienie o nowym zamówieniu z pull-through.
    
    Returns:
        Sformatowany tekst powiadomienia
    """
    msg = f"""
🎯 **Pull-Through Effect!**

**{order['client_name']}** właśnie złożył zamówienie przez dystrybutora **{order.get('distributor_name', 'Orbico')}**!

📦 **Produkt:** {order['product_id']}  
📊 **Ilość:** {order['quantity']} szt.  
📅 **Przekonany:** {order['convinced_on']} ({order['delay_days']} dni temu)  
✅ **Zamówienie:** {order['order_date']}

To efekt Twojej wcześniejszej pracy conviction! Klient zadzwonił bezpośrednio do dystrybutora.
"""
    return msg.strip()


def simulate_order_placement(
    pending_order: Dict,
    distributor_inventory: Dict,
    current_date: str
) -> Tuple[bool, str, Optional[Dict]]:
    """
    Symuluje złożenie zamówienia przez klienta do dystrybutora.
    
    Args:
        pending_order: Dane pending order
        distributor_inventory: Inwentarz dystrybutora
        current_date: Aktualna data
        
    Returns:
        Tuple[success, message, order_details]
        - success: Czy zamówienie się powiodło
        - message: Komunikat dla gracza
        - order_details: Szczegóły zamówienia (jeśli success=True)
    """
    product_id = pending_order["product_id"]
    quantity = pending_order["quantity"]
    
    # Sprawdź dostępność u dystrybutora
    if product_id not in distributor_inventory:
        return False, f"Dystrybutor nie ma {product_id} w ofercie.", None
    
    available = distributor_inventory[product_id].get("quantity", 0)
    
    if available < quantity:
        # Częściowa realizacja lub anulowanie
        if available > 0:
            # Częściowa realizacja
            order_details = {
                **pending_order,
                "quantity_ordered": available,
                "quantity_requested": quantity,
                "status": "partially_filled",
                "order_date": current_date
            }
            msg = f"""
⚠️ **Częściowa realizacja zamówienia**

{pending_order['client_name']} zamówił {quantity} szt. {product_id}, 
ale dystrybutor miał tylko {available} szt. w magazynie.

Zamówienie zrealizowane częściowo. Możesz uzupełnić zapasy dystrybutora.
"""
            return True, msg.strip(), order_details
        else:
            # Brak towaru - zamówienie anulowane
            msg = f"""
❌ **Zamówienie anulowane**

{pending_order['client_name']} chciał zamówić {product_id}, 
ale dystrybutor **nie ma towaru w magazynie**.

To stracona szansa! Upewnij się, że Twoi dystrybutorzy mają wystarczające zapasy.
"""
            return False, msg.strip(), None
    
    # Pełna realizacja
    order_details = {
        **pending_order,
        "quantity_ordered": quantity,
        "status": "filled",
        "order_date": current_date
    }
    
    msg = format_pending_order_notification({
        **pending_order,
        "order_date": current_date
    })
    
    return True, msg, order_details


def get_pull_through_stats(conviction_data: Dict) -> Dict:
    """
    Oblicza statystyki pull-through dla wszystkich produktów klienta.
    
    Returns:
        Dict ze statystykami
    """
    total_convinced = 0
    total_orders = 0
    total_pending = 0
    total_cancelled = 0
    
    for product_id, data in conviction_data.items():
        if data.get("stage") == "won":
            total_convinced += 1
        
        pending_orders = data.get("pending_orders", [])
        for order in pending_orders:
            if order["status"] == "ordered":
                total_orders += 1
            elif order["status"] == "pending":
                total_pending += 1
            elif order["status"] == "cancelled":
                total_cancelled += 1
    
    return {
        "convinced_products": total_convinced,
        "orders_placed": total_orders,
        "orders_pending": total_pending,
        "orders_cancelled": total_cancelled,
        "pull_through_rate": (total_orders / total_convinced * 100) if total_convinced > 0 else 0
    }
