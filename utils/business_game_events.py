"""
Business Game Events - System zdarzeń losowych
Obsługa losowania, walidacji i aplikacji efektów zdarzeń
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from data.random_events import RANDOM_EVENTS, EVENT_TYPE_WEIGHTS, RARITY_WEIGHTS


def check_event_conditions(event_data: Dict, bg_data: Dict) -> bool:
    """Sprawdza czy zdarzenie może wystąpić (warunki spełnione)"""
    conditions = event_data.get("conditions", {})
    
    # Min kontrakty
    if "min_contracts" in conditions:
        if bg_data["stats"]["contracts_completed"] < conditions["min_contracts"]:
            return False
    
    # Min reputacja
    if "min_reputation" in conditions:
        if bg_data["firm"]["reputation"] < conditions["min_reputation"]:
            return False
    
    # Min średnia ocena
    if "min_avg_rating" in conditions:
        if bg_data["stats"]["avg_rating"] < conditions["min_avg_rating"]:
            return False
    
    # Min monety
    if "min_coins" in conditions:
        # Pobierz coins z user_data (przekazane osobno)
        if conditions["min_coins"] > 0:  # Wymaga sprawdzenia w wyższej funkcji
            pass
    
    # Czy ma pracowników
    if conditions.get("has_employees", False):
        if len(bg_data["employees"]) == 0:
            return False
    
    # Czy ma aktywne kontrakty
    if conditions.get("has_active_contracts", False):
        if len(bg_data["contracts"]["active"]) == 0:
            return False
    
    # Czy ma dostępne kontrakty w puli
    if "min_available_contracts" in conditions:
        if len(bg_data["contracts"]["available_pool"]) < conditions["min_available_contracts"]:
            return False
    
    # Czy ostatni kontrakt miał niską ocenę (dla bad_review)
    if conditions.get("has_low_rated_contract", False):
        completed = bg_data["contracts"]["completed"]
        if completed:
            last_contract = completed[-1]
            if last_contract.get("rating", 5) > 2:
                return False
        else:
            return False
    
    return True


def get_random_event(bg_data: Dict, user_coins: int) -> Optional[Tuple[str, Dict]]:
    """Losuje zdarzenie spełniające warunki"""
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
    
    # Zbierz dostępne zdarzenia
    available_events = []
    
    for event_id, event_data in RANDOM_EVENTS.items():
        # Sprawdź warunki
        if check_event_conditions(event_data, bg_data):
            # Dodatkowe sprawdzenie min_coins (wymaga user_coins)
            conditions = event_data.get("conditions", {})
            if "min_coins" in conditions:
                if user_coins < conditions["min_coins"]:
                    continue
            
            available_events.append((event_id, event_data))
    
    if not available_events:
        return None
    
    # Losuj według typu (pozytywne/neutralne/negatywne)
    type_choice = random.choices(
        ["positive", "neutral", "negative"],
        weights=[EVENT_TYPE_WEIGHTS["positive"], EVENT_TYPE_WEIGHTS["neutral"], EVENT_TYPE_WEIGHTS["negative"]]
    )[0]
    
    # Filtruj po typie
    events_by_type = [(eid, edata) for eid, edata in available_events if edata["type"] == type_choice]
    
    if not events_by_type:
        # Fallback - losuj z wszystkich dostępnych
        events_by_type = available_events
    
    # Losuj według rzadkości
    rarities = [edata["rarity"] for _, edata in events_by_type]
    weights = [RARITY_WEIGHTS.get(r, 50) for r in rarities]
    
    chosen = random.choices(events_by_type, weights=weights)[0]
    
    return chosen


def should_trigger_event(bg_data: Dict) -> bool:
    """Sprawdza czy zdarzenie powinno wystąpić (cooldown, szansa)"""
    
    now = datetime.now()
    
    # Inicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
    
    # Sprawdź cooldown (24h)
    last_roll = bg_data["events"].get("last_roll")
    if last_roll:
        last_dt = datetime.strptime(last_roll, "%Y-%m-%d %H:%M:%S")
        if now - last_dt < timedelta(hours=24):
            return False
    
    # 20% szansa na zdarzenie
    if random.random() > 0.2:
        bg_data["events"]["last_roll"] = now.strftime("%Y-%m-%d %H:%M:%S")
        return False
    
    return True


def apply_event_effects(event_id: str, event_data: Dict, choice_idx: Optional[int], user_data: Dict) -> Dict:
    """Aplikuje efekty zdarzenia do user_data"""
    
    bg_data = user_data["business_game"]
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
    
    # Wybierz efekty (dla neutralnych z wyborem lub bezpośrednio)
    if event_data["type"] == "neutral" and "choices" in event_data:
        if choice_idx is None:
            raise ValueError("Neutral event requires choice_idx")
        effects = event_data["choices"][choice_idx]["effects"]
        choice_text = event_data["choices"][choice_idx]["text"]
    else:
        effects = event_data["effects"]
        choice_text = None
    
    if effects is None:
        effects = {}
    
    # Zmienna do śledzenia dotknięcia kontraktu
    affected_contract_title = None
    
    # Aplikuj efekty
    # Monety
    if "coins" in effects:
        user_data["degencoins"] = user_data.get("degencoins", 0) + effects["coins"]
    
    # Reputacja
    if "reputation" in effects:
        bg_data["firm"]["reputation"] += effects["reputation"]
    
    # Bonus do następnego kontraktu
    if "next_contract_bonus" in effects:
        bg_data["events"].setdefault("active_effects", []).append({
            "type": "next_contract_bonus",
            "multiplier": effects["next_contract_bonus"],
            "expires": None
        })
    
    # Boost pojemności
    if "capacity_boost" in effects:
        expiry = datetime.now() + timedelta(days=effects.get("duration_days", 1))
        bg_data["events"]["active_effects"].append({
            "type": "capacity_boost",
            "value": effects["capacity_boost"],
            "expires": expiry.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Penalty pojemności
    if "capacity_penalty" in effects:
        expiry = datetime.now() + timedelta(days=effects.get("duration_days", 1))
        bg_data["events"]["active_effects"].append({
            "type": "capacity_penalty",
            "value": effects["capacity_penalty"],
            "expires": expiry.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Przedłużenie deadline dla aktywnych kontraktów
    affected_contracts_extended = []
    if "deadline_extension" in effects:
        for contract in bg_data["contracts"]["active"]:
            old_deadline = datetime.strptime(contract["deadline"], "%Y-%m-%d %H:%M:%S")
            new_deadline = old_deadline + timedelta(days=effects["deadline_extension"])
            contract["deadline"] = new_deadline.strftime("%Y-%m-%d %H:%M:%S")
            
            # Zaznacz kontrakt jako dotknięty pozytywnie
            contract["affected_by_event"] = {
                "type": "deadline_extension",
                "event_title": event_data["title"],
                "days_added": effects["deadline_extension"]
            }
            
            affected_contracts_extended.append(contract["tytul"])
    
    # Skrócenie deadline
    affected_contract_title = None
    if "deadline_reduction" in effects:
        if bg_data["contracts"]["active"]:
            # Losowy aktywny kontrakt
            contract = random.choice(bg_data["contracts"]["active"])
            old_deadline = datetime.strptime(contract["deadline"], "%Y-%m-%d %H:%M:%S")
            new_deadline = old_deadline + timedelta(days=effects["deadline_reduction"])  # Ujemna wartość
            contract["deadline"] = new_deadline.strftime("%Y-%m-%d %H:%M:%S")
            
            # Zaznacz kontrakt jako dotknięty zdarzeniem
            contract["affected_by_event"] = {
                "type": "deadline_reduction",
                "event_title": event_data["title"],
                "days_reduced": abs(effects["deadline_reduction"])
            }
            
            affected_contract_title = contract["tytul"]
    
    # Usuń kontrakt z puli
    if effects.get("remove_contract_from_pool"):
        if bg_data["contracts"]["available_pool"]:
            bg_data["contracts"]["available_pool"].pop(random.randint(0, len(bg_data["contracts"]["available_pool"]) - 1))
    
    # Zapisz zdarzenie w historii
    event_entry = {
        "event_id": event_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": event_data["title"],
        "emoji": event_data["emoji"],
        "type": event_data["type"],
        "description": event_data["description"],
        "choice": choice_text,
        "effects": effects
    }
    
    # Dodaj informację o dotkniętym kontrakcie (jeśli dotyczy)
    if affected_contract_title:
        event_entry["affected_contract"] = affected_contract_title
    
    # Dodaj informację o przedłużonych kontraktach
    if affected_contracts_extended:
        event_entry["affected_contracts_extended"] = affected_contracts_extended
    
    bg_data["events"]["history"].append(event_entry)
    
    # Aktualizuj last_roll
    bg_data["events"]["last_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return user_data


def get_latest_event(bg_data: Dict) -> Optional[Dict]:
    """Pobiera najnowsze zdarzenie z historii"""
    if "events" not in bg_data or not bg_data["events"].get("history"):
        return None
    
    return bg_data["events"]["history"][-1]


def get_active_effects(bg_data: Dict) -> list:
    """Pobiera aktywne efekty (nie wygasłe)"""
    if "events" not in bg_data:
        return []
    
    now = datetime.now()
    active = []
    
    for effect in bg_data["events"].get("active_effects", []):
        if effect.get("expires"):
            expires_dt = datetime.strptime(effect["expires"], "%Y-%m-%d %H:%M:%S")
            if now < expires_dt:
                active.append(effect)
        else:
            # Bez expiry (np. next_contract_bonus - jednorazowy)
            active.append(effect)
    
    return active


def clean_expired_effects(bg_data: Dict) -> None:
    """Usuwa wygasłe efekty"""
    if "events" not in bg_data:
        return
    
    now = datetime.now()
    active_effects = []
    
    for effect in bg_data["events"].get("active_effects", []):
        if effect.get("expires"):
            expires_dt = datetime.strptime(effect["expires"], "%Y-%m-%d %H:%M:%S")
            if now < expires_dt:
                active_effects.append(effect)
        else:
            # Bez expiry - zachowaj
            active_effects.append(effect)
    
    bg_data["events"]["active_effects"] = active_effects
