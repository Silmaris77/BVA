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


def apply_event_effects(event_id: str, event_data: Dict, choice_idx: Optional[int], user_data: Dict, industry_id: str = "consulting") -> Dict:
    """Aplikuje efekty zdarzenia do user_data
    
    Args:
        event_id: ID wydarzenia
        event_data: Dane wydarzenia
        choice_idx: Indeks wyboru (dla neutralnych eventów)
        user_data: Dane użytkownika
        industry_id: ID branży (domyślnie consulting)
    """
    
    # Pobierz dane gry z backward compatibility
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        bg_data = user_data["business_games"][industry_id]
    elif "business_game" in user_data:
        bg_data = user_data["business_game"]
    else:
        # Jeśli nie ma gry, nie możemy aplikować efektów
        return user_data
    
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
        coins_amount = effects["coins"]
        user_data["degencoins"] = user_data.get("degencoins", 0) + coins_amount
        
        # WAŻNE: Rejestruj transakcję w historii finansowej
        bg_data["history"]["transactions"].append({
            "type": "event_reward" if coins_amount > 0 else "event_cost",
            "amount": coins_amount,
            "event_id": event_id,
            "event_title": event_data["title"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Aktualizuj statystyki
        if coins_amount > 0:
            bg_data["stats"]["total_revenue"] += coins_amount
        else:
            bg_data["stats"]["total_costs"] += abs(coins_amount)
    
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
        
        # Jeśli jest boost_count, dodaj aktywny efekt na przyszłe kontrakty
        if "boost_count" in effects:
            bg_data["events"]["active_effects"].append({
                "type": "deadline_boost",
                "days": effects["deadline_extension"],
                "remaining_contracts": effects["boost_count"],
                "expires": None  # Nie wygasa na czas, tylko po użyciu
            })
    
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
    
    # Modyfikuj aktywny kontrakt (renegocjacja)
    if effects.get("modify_active_contract"):
        if bg_data["contracts"]["active"]:
            # Wybierz losowy aktywny kontrakt
            contract = random.choice(bg_data["contracts"]["active"])
            
            # Zmień nagrodę (jeśli określono)
            if "reward_multiplier" in effects:
                multiplier = effects["reward_multiplier"]
                contract["nagroda_base"] = int(contract["nagroda_base"] * multiplier)
                contract["nagroda_4star"] = int(contract.get("nagroda_4star", contract["nagroda_base"]) * multiplier)
                contract["nagroda_5star"] = int(contract["nagroda_5star"] * multiplier)
            
            # Dodaj czas (jeśli określono)
            if "time_bonus" in effects:
                old_deadline = datetime.strptime(contract["deadline"], "%Y-%m-%d %H:%M:%S")
                new_deadline = old_deadline + timedelta(days=effects["time_bonus"])
                contract["deadline"] = new_deadline.strftime("%Y-%m-%d %H:%M:%S")
            
            # Zaznacz kontrakt jako zmodyfikowany
            contract["affected_by_event"] = {
                "type": "renegotiation",
                "event_title": event_data["title"],
                "reward_multiplier": effects.get("reward_multiplier", 1.0),
                "time_bonus": effects.get("time_bonus", 0)
            }
            
            affected_contract_title = contract["tytul"]
    
    # Dodaj ryzykowny kontrakt (risky_offer)
    if effects.get("add_risky_contract"):
        # Wybierz losowy kontrakt z puli jako bazę
        if bg_data["contracts"]["available_pool"]:
            base_contract = random.choice(bg_data["contracts"]["available_pool"]).copy()
            
            # Zmodyfikuj: trudność max (5), podwójna nagroda, unikalny ID
            base_contract["id"] = f"RISKY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            base_contract["tytul"] = f"🎰 RYZYKO: {base_contract['tytul']}"
            base_contract["trudnosc"] = 5
            base_contract["nagroda_base"] = base_contract["nagroda_base"] * 2
            base_contract["nagroda_4star"] = base_contract.get("nagroda_4star", base_contract["nagroda_base"]) * 2
            base_contract["nagroda_5star"] = base_contract["nagroda_5star"] * 2
            base_contract["emoji"] = "🎰"
            
            # Dodaj do puli dostępnych kontraktów
            bg_data["contracts"]["available_pool"].append(base_contract)
            
            affected_contract_title = base_contract["tytul"]
    
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
    
    # Zapisz dane gry z powrotem do odpowiedniej struktury
    if "business_games" not in user_data:
        user_data["business_games"] = {}
    user_data["business_games"][industry_id] = bg_data
    
    # Backward compatibility - zapisz też w starej strukturze jeśli była używana
    if "business_game" in user_data and industry_id == "consulting":
        user_data["business_game"] = bg_data
    
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


def auto_trigger_event_on_action(action_type: str, user_data: Dict, industry_id: str = "consulting") -> Tuple[Optional[str], Optional[Dict], Dict]:
    """
    Automatyczne triggerowanie wydarzenia przy określonych akcjach
    
    Args:
        action_type: "login", "accept_contract", "submit_solution"
        user_data: Pełne dane użytkownika
        industry_id: ID branży (domyślnie consulting)
        
    Returns:
        (event_id, event_data, updated_user_data) lub (None, None, user_data)
        Jeśli event wymaga wyboru - zwraca event_data, jeśli nie - aplikuje i zwraca None
    """
    # Pobierz dane gry z backward compatibility
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        bg_data = user_data["business_games"][industry_id]
    elif "business_game" in user_data:
        bg_data = user_data["business_game"]
    else:
        # Jeśli nie ma gry, nie możemy triggerować eventów
        return None, None, user_data
    
    # Sprawdź czy powinno się wydarzenie wystąpić
    if not should_trigger_event(bg_data):
        return None, None, user_data
    
    # Losuj wydarzenie
    event_result = get_random_event(bg_data, user_data.get("degencoins", 0))
    
    if not event_result:
        # Brak wydarzenia (80% przypadków lub brak spełnionych warunków)
        bg_data["events"]["last_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return None, None, user_data
    
    event_id, event_data = event_result
    
    # NEGATYWNE - aplikuj automatycznie
    if event_data["type"] == "negative":
        user_data = apply_event_effects(event_id, event_data, None, user_data, industry_id)
        # Zwróć None - nie wymaga UI reaction (toast wyświetli się w widoku)
        return event_id, event_data, user_data
    
    # POZYTYWNE - dodaj do pending z TTL 24h
    elif event_data["type"] == "positive":
        add_pending_positive_event(bg_data, event_id, event_data, hours=24)
        # Zapisz dane gry
        if "business_games" not in user_data:
            user_data["business_games"] = {}
        user_data["business_games"][industry_id] = bg_data
        if "business_game" in user_data and industry_id == "consulting":
            user_data["business_game"] = bg_data
        return event_id, event_data, user_data
    
    # NEUTRALNE (wybory) - ZWRÓĆ do UI (wymaga blocking modal)
    elif event_data["type"] == "neutral":
        return event_id, event_data, user_data
    
    return None, None, user_data


def add_pending_positive_event(bg_data: Dict, event_id: str, event_data: Dict, hours: int = 24) -> None:
    """Dodaje pozytywne wydarzenie do listy oczekujących (z TTL)"""
    if "events" not in bg_data:
        bg_data["events"] = {"history": [], "last_roll": None, "active_effects": [], "pending_positive": []}
    
    if "pending_positive" not in bg_data["events"]:
        bg_data["events"]["pending_positive"] = []
    
    expires = datetime.now() + timedelta(hours=hours)
    
    bg_data["events"]["pending_positive"].append({
        "event_id": event_id,
        "event_data": event_data,
        "triggered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires": expires.strftime("%Y-%m-%d %H:%M:%S")
    })


def get_pending_positive_events(bg_data: Dict) -> list:
    """Pobiera listę nieodebranych pozytywnych wydarzeń (nie wygasłych)"""
    if "events" not in bg_data or "pending_positive" not in bg_data["events"]:
        return []
    
    now = datetime.now()
    valid_events = []
    
    for pending in bg_data["events"]["pending_positive"]:
        expires_dt = datetime.strptime(pending["expires"], "%Y-%m-%d %H:%M:%S")
        if now < expires_dt:
            valid_events.append(pending)
    
    return valid_events


def claim_positive_event(event_id: str, user_data: Dict, industry_id: str = "consulting") -> Dict:
    """Odbiera (claim) pozytywne wydarzenie i aplikuje efekty
    
    Args:
        event_id: ID wydarzenia
        user_data: Dane użytkownika
        industry_id: ID branży (domyślnie consulting)
    """
    # Pobierz dane gry z backward compatibility
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        bg_data = user_data["business_games"][industry_id]
    elif "business_game" in user_data:
        bg_data = user_data["business_game"]
    else:
        # Jeśli nie ma gry, zwróć bez zmian
        return user_data
    
    if "events" not in bg_data or "pending_positive" not in bg_data["events"]:
        return user_data
    
    # Znajdź wydarzenie
    pending = next(
        (e for e in bg_data["events"]["pending_positive"] if e["event_id"] == event_id),
        None
    )
    
    if not pending:
        return user_data
    
    # Aplikuj efekty
    user_data = apply_event_effects(event_id, pending["event_data"], None, user_data, industry_id)
    
    # Usuń z pending
    bg_data["events"]["pending_positive"] = [
        e for e in bg_data["events"]["pending_positive"] if e["event_id"] != event_id
    ]
    
    # Zapisz dane gry
    if "business_games" not in user_data:
        user_data["business_games"] = {}
    user_data["business_games"][industry_id] = bg_data
    if "business_game" in user_data and industry_id == "consulting":
        user_data["business_game"] = bg_data
    
    return user_data


def clean_expired_positive_events(bg_data: Dict) -> int:
    """Usuwa wygasłe pozytywne wydarzenia (zwraca liczbę przepadłych)"""
    if "events" not in bg_data or "pending_positive" not in bg_data["events"]:
        return 0
    
    now = datetime.now()
    original_count = len(bg_data["events"]["pending_positive"])
    
    bg_data["events"]["pending_positive"] = [
        e for e in bg_data["events"]["pending_positive"]
        if datetime.strptime(e["expires"], "%Y-%m-%d %H:%M:%S") > now
    ]
    
    expired_count = original_count - len(bg_data["events"]["pending_positive"])
    return expired_count
