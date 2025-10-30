"""
🎴 FMCG Client Management - Helpers
Funkcje do zarządzania rozszerzoną strukturą danych klientów FMCG
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


def create_new_client_entry(client_id: str, status: str = "prospect") -> Dict:
    """
    Tworzy nowy wpis klienta z pełną rozszerzoną strukturą
    
    Args:
        client_id: ID klienta z bazy (np. "trad_001")
        status: Status początkowy (prospect/active/lost)
    
    Returns:
        Dict z pełną strukturą klienta
    """
    return {
        "id": client_id,
        "status": status,
        
        # Reputacja i wizyty
        "reputation": 0,  # -100 do +100
        "last_visit_date": None,
        "visit_frequency_required": 14,  # dni
        "next_visit_due": None,
        
        # Produkty u klienta
        "products_portfolio": [],
        
        # Metryki biznesowe
        "monthly_value": 0,
        "contract_start_date": None,
        "contract_renewal_date": None,
        "market_share_vs_competition": 0,
        "satisfaction_score": 3,  # 1-5
        
        # Timeline
        "events_timeline": [],
        
        # Conversations (kompatybilność wsteczna)
        "conversations": []
    }


def migrate_fmcg_customers_to_new_structure(bg_data: Dict) -> Tuple[Dict, int]:
    """
    Migruje starą strukturę FMCG customers do nowej z rozszerzonymi danymi
    
    Args:
        bg_data: business_games["fmcg"] dict
    
    Returns:
        (bg_data, migrated_count): Zaktualizowane dane + liczba zmigrowanych
    """
    
    if "customers" not in bg_data:
        # Brak struktury customers - utwórz pustą nową
        bg_data["customers"] = {"clients": {}}
        return bg_data, 0
    
    old_customers = bg_data["customers"]
    
    # Sprawdź czy już jest nowa struktura
    if "clients" in old_customers and isinstance(old_customers["clients"], dict):
        # Już nowa struktura - nie migruj
        return user_data, 0
    
    # MIGRACJA: Stara struktura → Nowa
    new_clients = {}
    migrated_count = 0
    
    # Migruj prospects
    for client_id in old_customers.get("prospects", []):
        new_clients[client_id] = create_new_client_entry(client_id, status="prospect")
        
        # Przenieś conversations jeśli były
        old_conversations = bg_data.get("conversations", {}).get(client_id, [])
        if old_conversations:
            new_clients[client_id]["conversations"] = old_conversations
            
            # Dodaj event "first_visit" jeśli były conversations
            first_conv_date = old_conversations[0].get("date", datetime.now().isoformat())
            new_clients[client_id]["events_timeline"].append({
                "date": first_conv_date.split(" ")[0] if " " in first_conv_date else first_conv_date,
                "type": "first_visit",
                "description": "Pierwsza wizyta - rozmowa z klientem",
                "reputation_change": 0,
                "related_products": []
            })
        
        migrated_count += 1
    
    # Migruj active_clients
    for client_id in old_customers.get("active_clients", []):
        new_clients[client_id] = create_new_client_entry(client_id, status="active")
        
        # Przenieś conversations
        old_conversations = bg_data.get("conversations", {}).get(client_id, [])
        if old_conversations:
            new_clients[client_id]["conversations"] = old_conversations
            
            # Dodaj events z conversations
            for conv in old_conversations:
                conv_date = conv.get("date", datetime.now().isoformat())
                new_clients[client_id]["events_timeline"].append({
                    "date": conv_date.split(" ")[0] if " " in conv_date else conv_date,
                    "type": "regular_visit",
                    "description": "Wizyta u klienta - rozmowa",
                    "reputation_change": 0,
                    "related_products": []
                })
        
        migrated_count += 1
    
    # Migruj lost_clients
    for client_id in old_customers.get("lost_clients", []):
        new_clients[client_id] = create_new_client_entry(client_id, status="lost")
        new_clients[client_id]["lost_date"] = datetime.now().isoformat()
        new_clients[client_id]["lost_reason"] = "unknown"
        migrated_count += 1
    
    # Zamień starą strukturę na nową
    bg_data["customers"] = {"clients": new_clients}
    
    # Usuń stare pole conversations (przeniesione do clients)
    if "conversations" in bg_data:
        del bg_data["conversations"]
    
    return bg_data, migrated_count


def get_client_by_id(clients_dict: Dict, client_id: str) -> Optional[Dict]:
    """
    Pobiera dane klienta po ID
    
    Args:
        clients_dict: Dictionary wszystkich klientów (bg_data["customers"]["clients"])
        client_id: ID klienta
    
    Returns:
        Dict z danymi klienta lub None
    """
    return clients_dict.get(client_id)


def get_clients_by_status(clients_dict: Dict, status: str) -> List[Dict]:
    """
    Pobiera listę klientów o danym statusie
    
    Args:
        clients_dict: Dictionary wszystkich klientów
        status: Status do filtrowania (prospect/active/lost)
    
    Returns:
        Lista klientów
    """
    return [
        client for client in clients_dict.values()
        if client.get("status") == status
    ]


def calculate_next_visit_due(last_visit_date: str, frequency_days: int) -> str:
    """
    Oblicza datę następnej wymaganej wizyty
    
    Args:
        last_visit_date: ISO datetime ostatniej wizyty
        frequency_days: Częstotliwość wizyt w dniach
    
    Returns:
        ISO date następnej wizyty
    """
    if not last_visit_date:
        return datetime.now().isoformat()
    
    last_dt = datetime.fromisoformat(last_visit_date.split(" ")[0])
    next_dt = last_dt + timedelta(days=frequency_days)
    return next_dt.strftime("%Y-%m-%d")


def is_visit_overdue(client_data: Dict) -> Tuple[bool, int]:
    """
    Sprawdza czy wizyta jest spóźniona
    
    Args:
        client_data: Dane klienta
    
    Returns:
        (is_overdue: bool, days_overdue: int)
    """
    if client_data["status"] != "active":
        return False, 0
    
    next_visit = client_data.get("next_visit_due")
    if not next_visit:
        return False, 0
    
    next_dt = datetime.fromisoformat(next_visit)
    now = datetime.now()
    
    if now > next_dt:
        days_overdue = (now - next_dt).days
        return True, days_overdue
    
    return False, 0


def add_product_to_portfolio(client_data: Dict, product_id: str, initial_volume: int = 50) -> None:
    """
    Dodaje produkt do portfolio klienta (cross-sell)
    
    Args:
        client_data: Dane klienta (modyfikowane in-place)
        product_id: ID produktu (np. "pc_shampoo_fresh")
        initial_volume: Początkowy volume miesięczny
    """
    
    # Sprawdź czy produkt już istnieje
    existing = next(
        (p for p in client_data["products_portfolio"] if p["product_id"] == product_id),
        None
    )
    
    if existing:
        return  # Już jest
    
    # Dodaj nowy produkt
    client_data["products_portfolio"].append({
        "product_id": product_id,
        "date_listed": datetime.now().strftime("%Y-%m-%d"),
        "volume_monthly": initial_volume,  # Changed from monthly_volume
        "market_share_category": 20,  # Domyślnie 20%
        "shelf_placement": "eye_level",
        "facing_count": 2,
        "stock_days": 14
    })
    
    # Update monthly_value (załóżmy średnio 15 PLN za sztukę)
    avg_price_per_unit = 15
    client_data["monthly_value"] = sum(
        p.get("volume_monthly", 0) * avg_price_per_unit  # Changed from monthly_volume
        for p in client_data["products_portfolio"]
    )
    
    # Dodaj event
    client_data["events_timeline"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": "cross_sell",
        "description": f"Dodano nowy produkt: {product_id}",
        "reputation_change": +15,
        "related_products": [product_id]
    })
    
    # Update reputacji za cross-sell
    client_data["reputation"] = min(100, client_data.get("reputation", 0) + 15)


def get_reputation_status(reputation: int) -> Dict:
    """
    Zwraca status reputacji z kolorami i emoji
    
    Args:
        reputation: Wartość reputacji (-100 do +100)
    
    Returns:
        Dict z label, color, emoji, progress (0-1)
    """
    if reputation <= -50:
        return {
            "label": "LOST",
            "color": "#ef4444",
            "emoji": "💀",
            "progress": (reputation + 100) / 2,  # 0% to 25%
            "description": "Klient utracony - krytyczna reputacja"
        }
    elif reputation < 0:
        return {
            "label": "AT RISK",
            "color": "#f97316",
            "emoji": "⚠️",
            "progress": (reputation + 100) / 2,  # 25% to 50%
            "description": "Zagrożenie utratą klienta"
        }
    elif reputation < 50:
        return {
            "label": "NEUTRAL",
            "color": "#eab308",
            "emoji": "😐",
            "progress": (reputation + 100) / 2,  # 50% to <75%
            "description": "Neutralna relacja - potencjał wzrostu"
        }
    elif reputation < 80:
        return {
            "label": "GOOD",
            "color": "#22c55e",
            "emoji": "😊",
            "progress": (reputation + 100) / 2,  # 75% to <90%
            "description": "Dobra współpraca"
        }
    else:
        return {
            "label": "CHAMPION",
            "color": "#3b82f6",
            "emoji": "🏆",
            "progress": (reputation + 100) / 2,  # 90% to 100%
            "description": "Klient-ambasador marki!"
        }
