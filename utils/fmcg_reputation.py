"""
🌟 FMCG Reputation System
System zarządzania reputacją u klientów FMCG
"""

from datetime import datetime, timedelta
from typing import Dict, Optional


# Definicje zmian reputacji dla różnych eventów
REPUTATION_CHANGES = {
    # POZYTYWNE
    "regular_visit_on_time": +5,
    "visit_excellent_5stars": +10,
    "task_completed": +3,
    "promotion_delivered": +5,
    "cross_sell_success": +15,
    "exceeded_sales_plan": +10,
    "on_time_delivery": +2,
    "problem_resolved_quickly": +8,
    
    # NEGATYWNE
    "visit_late_1_7days": -3,
    "visit_late_8_14days": -7,
    "visit_late_15plus": -15,
    "no_visit_30days": -20,
    "visit_poor_1_2stars": -10,
    "visit_poor_3stars": -5,
    "product_unavailable": -8,
    "delivery_late": -5,
    "complaint_unresolved": -12,
    "competitor_won_listing": -20,
    "price_increase_rejected": -10
}


def update_client_reputation(
    client_data: Dict,
    event_type: str,
    custom_change: Optional[int] = None,
    description: Optional[str] = None,
    related_products: Optional[list] = None
) -> int:
    """
    Aktualizuje reputację klienta na podstawie wydarzenia
    
    Args:
        client_data: Dict z danymi klienta (modyfikowany in-place)
        event_type: Typ wydarzenia (klucz z REPUTATION_CHANGES)
        custom_change: Opcjonalna niestandardowa zmiana (nadpisuje standardową)
        description: Opis wydarzenia (opcjonalny)
        related_products: Lista ID produktów związanych z eventem
    
    Returns:
        reputation_change: Wartość zmiany reputacji
    """
    
    # Ensure client has 'status' field (backward compatibility)
    if "status" not in client_data:
        client_data["status"] = "PROSPECT"
    
    # Oblicz zmianę
    change = custom_change if custom_change is not None else REPUTATION_CHANGES.get(event_type, 0)
    
    # Zastosuj zmianę (0-100, start: 50 neutral)
    old_rep = client_data.get("reputation", 50)
    new_rep = max(0, min(100, old_rep + change))
    client_data["reputation"] = new_rep
    
    # Przygotuj opis
    if not description:
        description = get_default_event_description(event_type, change)
    
    # Dodaj event do timeline
    event_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": event_type,
        "description": description,
        "reputation_change": change,
        "reputation_after": new_rep,
        "related_products": related_products or []
    }
    
    client_data.setdefault("events_timeline", []).append(event_entry)
    
    # Sprawdź czy klient został LOST
    if new_rep <= -50 and client_data.get("status") == "ACTIVE":
        client_data["status"] = "LOST"
        client_data["lost_date"] = datetime.now().isoformat()
        client_data["lost_reason"] = "reputation_too_low"
        
        # Dodaj event "lost"
        client_data["events_timeline"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "lost",
            "description": f"❌ Klient utracony - reputacja zbyt niska ({new_rep})",
            "reputation_change": 0,
            "reputation_after": new_rep,
            "related_products": []
        })
    
    return change


def get_default_event_description(event_type: str, change: int) -> str:
    """Generuje domyślny opis dla typu wydarzenia"""
    
    descriptions = {
        "regular_visit_on_time": "✅ Wizyta w terminie",
        "visit_excellent_5stars": "⭐⭐⭐⭐⭐ Wizyta oceniona 5/5 - doskonała!",
        "task_completed": "✅ Wykonano zadanie dodatkowe",
        "promotion_delivered": "🎁 Dostarczona promocja",
        "cross_sell_success": "🆕 Sprzedaż krzyżowa - nowy produkt",
        "exceeded_sales_plan": "📊 Przekroczono plan sprzedaży",
        "on_time_delivery": "🚚 Dostawa na czas",
        "problem_resolved_quickly": "🔧 Szybko rozwiązano problem",
        
        "visit_late_1_7days": "⏰ Wizyta spóźniona (1-7 dni)",
        "visit_late_8_14days": "⚠️ Wizyta mocno spóźniona (8-14 dni)",
        "visit_late_15plus": "❌ Wizyta bardzo spóźniona (15+ dni)",
        "no_visit_30days": "💀 Brak wizyty przez 30+ dni",
        "visit_poor_1_2stars": "⭐⭐ Wizyta słabo oceniona (1-2/5)",
        "visit_poor_3stars": "⭐⭐⭐ Wizyta średnio oceniona (3/5)",
        "product_unavailable": "📦 Brak produktu na półce",
        "delivery_late": "🚚 Opóźniona dostawa",
        "complaint_unresolved": "😡 Nierozwiązana reklamacja",
        "competitor_won_listing": "💔 Konkurencja wygrała listing",
        "price_increase_rejected": "💰 Odrzucona podwyżka cen"
    }
    
    base_desc = descriptions.get(event_type, f"Wydarzenie: {event_type}")
    return f"{base_desc} ({change:+d} rep)"


def record_visit(client_data: Dict, visit_quality: int, notes: str = "") -> int:
    """
    Rejestruje wizytę u klienta i aktualizuje reputację
    
    Args:
        client_data: Dane klienta
        visit_quality: Ocena wizyty 1-5 (np. z AI evaluation)
        notes: Notatki z wizyty
    
    Returns:
        reputation_change: Zmiana reputacji
    """
    
    from datetime import datetime, timedelta
    
    # Ensure client has 'status' field (backward compatibility)
    if "status" not in client_data:
        client_data["status"] = "PROSPECT"
    
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    # Określ typ wydarzenia na podstawie jakości i terminowości
    event_type = None
    
    # Sprawdź czy wizyta była spóźniona
    next_visit_due = client_data.get("next_visit_due")
    if next_visit_due and client_data.get("status") == "ACTIVE":
        due_dt = datetime.fromisoformat(next_visit_due)
        days_late = (now - due_dt).days
        
        if days_late > 15:
            event_type = "visit_late_15plus"
        elif days_late > 7:
            event_type = "visit_late_8_14days"
        elif days_late > 0:
            event_type = "visit_late_1_7days"
        else:
            # Na czas - sprawdź jakość
            if visit_quality >= 5:
                event_type = "visit_excellent_5stars"
            else:
                event_type = "regular_visit_on_time"
    else:
        # Prospect lub brak next_visit_due
        if visit_quality >= 5:
            event_type = "visit_excellent_5stars"
        elif visit_quality <= 2:
            event_type = "visit_poor_1_2stars"
        elif visit_quality == 3:
            event_type = "visit_poor_3stars"
        else:
            event_type = "regular_visit_on_time"
    
    # Update reputacji
    desc = f"Wizyta u klienta"
    if notes:
        desc += f" - {notes}"
    
    change = update_client_reputation(
        client_data,
        event_type,
        description=desc
    )
    
    # Add to visits_history
    if "visits_history" not in client_data:
        client_data["visits_history"] = []
    
    # Ensure client has 'reputation' field (even PROSPECT can have it)
    if "reputation" not in client_data:
        client_data["reputation"] = 0
    
    client_data["visits_history"].append({
        "date": today,
        "quality": visit_quality,
        "notes": notes,
        "reputation_change": change,
        "reputation_after": client_data["reputation"]
    })
    
    # Update last_visit_date i next_visit_due
    client_data["last_visit_date"] = now.isoformat()
    
    frequency = client_data.get("visit_frequency_required", 14)
    next_dt = now + timedelta(days=frequency)
    client_data["next_visit_due"] = next_dt.strftime("%Y-%m-%d")
    
    # Jeśli to była pierwsza wizyta i prospect, dodaj event "first_visit"
    if client_data.get("status") == "PROSPECT" and not client_data.get("contract_start_date"):
        # Ensure events_timeline exists
        if "events_timeline" not in client_data:
            client_data["events_timeline"] = []
        
        client_data["events_timeline"].append({
            "date": today,
            "type": "first_visit",
            "description": "🎯 Pierwsza wizyta u klienta",
            "reputation_change": 0,
            "reputation_after": client_data["reputation"],
            "related_products": []
        })
    
    return change


def sign_contract(client_data: Dict, products: list) -> None:
    """
    Podpisuje kontrakt z klientem (PROSPECT → ACTIVE)
    
    Args:
        client_data: Dane klienta (modyfikowany in-place)
        products: Lista ID produktów w kontrakcie
    """
    
    # Ensure client has 'status' field (backward compatibility)
    if "status" not in client_data:
        client_data["status"] = "PROSPECT"
    
    if client_data.get("status") != "PROSPECT":
        return  # Już aktywny lub lost
    
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    # Zmień status
    client_data["status"] = "ACTIVE"
    client_data["contract_start_date"] = today
    
    # Initialize reputation if not exists (should start at 50 for new ACTIVE)
    if "reputation" not in client_data:
        client_data["reputation"] = 50
    
    # Renewal za rok
    renewal_date = (now + timedelta(days=365)).strftime("%Y-%m-%d")
    client_data["contract_renewal_date"] = renewal_date
    
    # Dodaj produkty do portfolio
    from utils.fmcg_client_helpers import add_product_to_portfolio
    for product_id in products:
        add_product_to_portfolio(client_data, product_id, initial_volume=50)
    
    # Update reputacji za podpisanie kontraktu
    update_client_reputation(
        client_data,
        "cross_sell_success",  # +15
        description=f"📝 Podpisano pierwszy kontrakt - {len(products)} produktów",
        related_products=products
    )
    
    # Dodaj specjalny event
    client_data["events_timeline"].append({
        "date": today,
        "type": "contract_signed",
        "description": f"✅ Podpisano kontrakt! Produkty: {', '.join(products)}",
        "reputation_change": +20,
        "reputation_after": client_data["reputation"],
        "related_products": products
    })
    
    client_data["reputation"] = min(100, client_data.get("reputation", 0) + 20)


def check_overdue_visits(clients_dict: Dict) -> list:
    """
    Sprawdza wszystkich aktywnych klientów pod kątem spóźnionych wizyt
    
    Args:
        clients_dict: Dictionary wszystkich klientów
    
    Returns:
        Lista tupli (client_id, days_overdue, client_data)
    """
    
    from datetime import datetime
    
    overdue = []
    now = datetime.now()
    
    for client_id, client_data in clients_dict.items():
        if client_data.get("status") != "ACTIVE":
            continue
        
        next_visit = client_data.get("next_visit_due")
        if not next_visit:
            continue
        
        due_dt = datetime.fromisoformat(next_visit)
        
        if now > due_dt:
            days_late = (now - due_dt).days
            overdue.append((client_id, days_late, client_data))
    
    # Sortuj po liczbie dni spóźnienia (malejąco)
    overdue.sort(key=lambda x: x[1], reverse=True)
    
    return overdue
