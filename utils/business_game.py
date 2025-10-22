"""
Business Games - Core Logic
Zarządzanie firmą, kontraktami, pracownikami, finansami i rankingami
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

from data.business_data import (
    FIRM_LEVELS, EMPLOYEE_TYPES, CONTRACTS_POOL, GAME_CONFIG,
    get_firm_level, get_available_contracts, calculate_daily_capacity,
    calculate_employee_costs, get_contract_by_id, OFFICE_TYPES
)
from data.scenarios import get_scenario, get_default_scenario_id

# =============================================================================
# INICJALIZACJA FIRMY
# =============================================================================

def initialize_business_game_with_scenario(username: str, industry_id: str, scenario_id: str) -> Dict:
    """Inicjalizuje Business Games z wybranym scenariuszem
    
    Args:
        username: Nazwa użytkownika
        industry_id: ID branży (np. "consulting")
        scenario_id: ID scenariusza (np. "startup_mode")
    
    Returns:
        Dict z pełnymi danymi gry zainicjalizowanymi według scenariusza
    """
    scenario = get_scenario(industry_id, scenario_id)
    if not scenario:
        # Fallback do standardowego scenariusza
        scenario_id = get_default_scenario_id(industry_id)
        scenario = get_scenario(industry_id, scenario_id)
        
        # Jeśli nadal None, użyj domyślnych wartości
        if not scenario:
            raise ValueError(f"Nie można znaleźć scenariusza dla branży {industry_id}")
    
    initial = scenario['initial_conditions']
    
    return {
        # Metadata scenariusza
        "scenario_id": scenario_id,
        "scenario_modifiers": scenario['modifiers'],
        "scenario_objectives": scenario['objectives'],
        "objectives_completed": [],  # Lista ID ukończonych celów
        
        "firm": {
            "name": f"{username}'s Consulting",
            "logo": "🏢",
            "founded": datetime.now().strftime("%Y-%m-%d"),
            "level": GAME_CONFIG["starting_level"],
            "reputation": initial['reputation']
        },
        "employees": initial.get('employees', []),
        "office": {
            "type": initial['office_type'],
            "upgraded_at": None if initial['office_type'] == "home_office" else datetime.now().strftime("%Y-%m-%d")
        },
        "contracts": {
            "active": initial.get('contracts_in_progress', []),
            "completed": [],
            "available_pool": [],
            "last_refresh": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "stats": {
            "total_revenue": 0,
            "total_costs": 0,
            "net_profit": 0,
            "contracts_completed": 0,
            "contracts_5star": 0,
            "contracts_4star": 0,
            "contracts_3star": 0,
            "contracts_2star": 0,
            "contracts_1star": 0,
            "avg_rating": 0.0,
            "category_stats": {
                "Konflikt": {"completed": 0, "total_earned": 0, "avg_rating": 0.0},
                "Coaching": {"completed": 0, "total_earned": 0, "avg_rating": 0.0},
                "Kultura": {"completed": 0, "total_earned": 0, "avg_rating": 0.0},
                "Kryzys": {"completed": 0, "total_earned": 0, "avg_rating": 0.0},
                "Leadership": {"completed": 0, "total_earned": 0, "avg_rating": 0.0}
            },
            "last_30_days": {
                "revenue": 0,
                "contracts": 0,
                "avg_rating": 0.0
            },
            "last_7_days": {
                "revenue": 0,
                "contracts": 0,
                "avg_rating": 0.0
            }
        },
        "ranking": {
            "overall_score": 0.0,
            "current_positions": {
                "overall": None,
                "revenue": None,
                "quality": None,
                "productivity_30d": None
            },
            "previous_positions": {},
            "badges": []
        },
        "events": {
            "history": [],
            "last_roll": None,
            "active_effects": []
        },
        "money": initial['money'],  # SALDO FIRMY - oddzielne od DegenCoins gracza!
        "history": {
            "transactions": [{
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "initial_capital",
                "amount": initial['money'],
                "description": f"Kapitał początkowy - Scenariusz: {scenario['name']}",
                "balance_after": initial['money']
            }] if initial['money'] != 0 else [],
            "level_ups": []
        },
        # Specjalne dane dla scenariusza
        "initial_money": initial['money']  # Zachowaj dla referencji
    }


def initialize_business_game(username: str) -> Dict:
    """Inicjalizuje Business Games dla nowego użytkownika
    
    NOTE: Monety są teraz przechowywane w user_data['degencoins'], nie tutaj!
    """
    return {
        "firm": {
            "name": f"{username}'s Consulting",
            "logo": "🏢",  # Domyślne logo - można zmienić w ustawieniach
            "founded": datetime.now().strftime("%Y-%m-%d"),
            "level": GAME_CONFIG["starting_level"],
            # coins - USUNIĘTE! Teraz używamy user_data['degencoins']
            "reputation": GAME_CONFIG["starting_reputation"]
        },
        "employees": [],
        "office": {
            "type": "home_office",  # Wszyscy zaczynają z home office
            "upgraded_at": None
        },
        "contracts": {
            "active": [],
            "completed": [],
            "available_pool": [],
            "last_refresh": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "stats": {
            "total_revenue": 0,
            "total_costs": 0,
            "net_profit": 0,
            "contracts_completed": 0,
            "contracts_5star": 0,
            "contracts_4star": 0,
            "contracts_3star": 0,
            "contracts_2star": 0,
            "contracts_1star": 0,
            "avg_rating": 0.0,
            "category_stats": {
                "Konflikt": {"completed": 0, "total_earned": 0, "avg_rating": 0.0},
                "Coaching": {"completed": 0, "total_earned": 0, "avg_rating": 0.0},
                "Kultura": {"completed": 0, "total_earned": 0, "avg_rating": 0.0},
                "Kryzys": {"completed": 0, "total_earned": 0, "avg_rating": 0.0},
                "Leadership": {"completed": 0, "total_earned": 0, "avg_rating": 0.0}
            },
            "last_30_days": {
                "revenue": 0,
                "contracts": 0,
                "avg_rating": 0.0
            },
            "last_7_days": {
                "revenue": 0,
                "contracts": 0,
                "avg_rating": 0.0
            }
        },
        "ranking": {
            "overall_score": 0.0,
            "current_positions": {
                "overall": None,
                "revenue": None,
                "quality": None,
                "productivity_30d": None
            },
            "previous_positions": {},
            "badges": []
        },
        "events": {
            "history": [],  # Historia zdarzeń losowych
            "last_roll": None,  # Ostatnie losowanie
            "active_effects": []  # Aktywne efekty (buffs/debuffs)
        },
        "history": {
            "transactions": [],  # Historia finansowa
            "level_ups": []  # Historia awansów
        }
    }

# =============================================================================
# ZARZĄDZANIE FIRMĄ
# =============================================================================

def get_current_firm_level(user_data: Dict) -> int:
    """Pobiera aktualny poziom firmy
    
    Args:
        user_data: Pełne dane użytkownika (potrzebne do user_data['degencoins'])
    """
    coins = user_data.get('degencoins', 0)
    
    # Backward compatibility: obsługa obu struktur
    if "business_games" in user_data and "consulting" in user_data["business_games"]:
        reputation = user_data["business_games"]["consulting"]["firm"]["reputation"]
    elif "business_game" in user_data:
        reputation = user_data["business_game"]["firm"]["reputation"]
    else:
        reputation = 0
    
    return get_firm_level(coins, reputation)

def update_firm_level(user_data: Dict) -> Tuple[Dict, bool]:
    """Aktualizuje poziom firmy, zwraca (updated_user_data, level_up_occurred)
    
    Args:
        user_data: Pełne dane użytkownika
    """
    # Backward compatibility: obsługa obu struktur
    if "business_games" in user_data and "consulting" in user_data["business_games"]:
        business_data = user_data["business_games"]["consulting"]
        industry_id = "consulting"
    elif "business_game" in user_data:
        business_data = user_data["business_game"]
        industry_id = None
    else:
        return user_data, False
    
    old_level = business_data["firm"]["level"]
    new_level = get_current_firm_level(user_data)
    
    if new_level > old_level:
        business_data["firm"]["level"] = new_level
        business_data["history"]["level_ups"].append({
            "from_level": old_level,
            "to_level": new_level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Zapisz z powrotem do odpowiedniej struktury
        if industry_id:
            user_data["business_games"][industry_id] = business_data
        else:
            user_data["business_game"] = business_data
        return user_data, True
    
    # Zapisz z powrotem nawet jeśli nie było level up
    if industry_id:
        user_data["business_games"][industry_id] = business_data
    else:
        user_data["business_game"] = business_data
    return user_data, False

def rename_firm(business_data: Dict, new_name: str) -> Dict:
    """Zmienia nazwę firmy"""
    business_data["firm"]["name"] = new_name
    return business_data

# =============================================================================
# ZARZĄDZANIE KONTRAKTAMI
# =============================================================================

def refresh_contract_pool(business_data: Dict, force: bool = False) -> Dict:
    """Odświeża pulę dostępnych kontraktów"""
    last_refresh = datetime.strptime(
        business_data["contracts"]["last_refresh"], 
        "%Y-%m-%d %H:%M:%S"
    )
    now = datetime.now()
    hours_since_refresh = (now - last_refresh).total_seconds() / 3600
    
    # Wypełnij pulę jeśli jest pusta (pierwsze uruchomienie) lub minęło 24h
    is_first_time = len(business_data["contracts"]["available_pool"]) == 0
    
    if hours_since_refresh >= GAME_CONFIG["contract_pool_refresh_hours"] or force or is_first_time:
        # Wybierz po jednym kontrakcie z każdego poziomu trudności
        firm_level = business_data["firm"]["level"]
        available_contracts = [c for c in CONTRACTS_POOL if c["wymagany_poziom"] <= firm_level]
        
        # Grupuj kontrakty według trudności
        contracts_by_difficulty = {}
        for contract in available_contracts:
            difficulty = contract["trudnosc"]
            if difficulty not in contracts_by_difficulty:
                contracts_by_difficulty[difficulty] = []
            contracts_by_difficulty[difficulty].append(contract)
        
        # Wybierz kontrakty
        new_pool = []
        
        # TRUDNOŚĆ 1: Pokaż WSZYSTKIE proste kontrakty (dla początkujących)
        if 1 in contracts_by_difficulty:
            for contract in contracts_by_difficulty[1]:
                new_pool.append(contract.copy())
        
        # TRUDNOŚĆ 2-5: Po jednym losowym z każdego poziomu
        for difficulty in range(2, 6):  # 2, 3, 4, 5 gwiazdek
            if difficulty in contracts_by_difficulty and len(contracts_by_difficulty[difficulty]) > 0:
                selected = random.choice(contracts_by_difficulty[difficulty])
                new_pool.append(selected.copy())  # Copy aby nie modyfikować oryginału
        
        # Dodaj informacje o dostępności
        for contract in new_pool:
            contract["available_until"] = (now + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        
        business_data["contracts"]["available_pool"] = new_pool
        business_data["contracts"]["last_refresh"] = now.strftime("%Y-%m-%d %H:%M:%S")
    
    return business_data

def can_accept_contract(business_data: Dict) -> Tuple[bool, str]:
    """Sprawdza czy użytkownik może przyjąć kolejny kontrakt"""
    active_count = len(business_data["contracts"]["active"])
    
    if active_count >= GAME_CONFIG["max_active_contracts"]:
        return False, f"Maksimum aktywnych kontraktów: {GAME_CONFIG['max_active_contracts']}"
    
    # Sprawdź dzienny limit - liczymy WSZYSTKIE kontrakty dzisiaj (accepted + completed)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Kontrakty przyjęte dzisiaj (w active)
    today_accepted = sum(
        1 for c in business_data["contracts"]["active"] 
        if c.get("accepted_date", "").startswith(today)
    )
    
    # Kontrakty ukończone dzisiaj (w completed) - też się liczą do limitu!
    today_completed = sum(
        1 for c in business_data["contracts"]["completed"]
        if c.get("completed_date", "").startswith(today)
    )
    
    # Suma = przyjęte + ukończone dzisiaj
    today_total = today_accepted + today_completed
    
    capacity = calculate_daily_capacity(
        business_data["firm"]["level"], 
        business_data["employees"]
    )
    
    if today_total >= capacity:
        return False, f"⏰ Dzienny limit kontraktów wyczerpany! Wykonano już {today_total} z {capacity} dostępnych kontraktów dzisiaj. Wróć jutro lub awansuj firmę!"
    
    if today_total >= GAME_CONFIG["max_daily_contracts"]:
        return False, f"Absolutny dzienny limit: {GAME_CONFIG['max_daily_contracts']}"
    
    return True, ""

def accept_contract(business_data: Dict, contract_id: str, user_data: Optional[Dict] = None) -> Tuple[Dict, bool, str, Optional[Tuple]]:
    """Przyjmuje kontrakt i opcjonalnie triggeruje wydarzenie
    
    Returns:
        (updated_business_data, success, message, triggered_event)
        triggered_event = (event_id, event_data) lub None
    """
    can_accept, reason = can_accept_contract(business_data)
    if not can_accept:
        return business_data, False, reason, None
    
    # Znajdź kontrakt w dostępnej puli
    contract = next(
        (c for c in business_data["contracts"]["available_pool"] if c["id"] == contract_id),
        None
    )
    
    if not contract:
        return business_data, False, "Kontrakt nie znaleziony", None
    
    # Przenieś do aktywnych
    active_contract = contract.copy()
    active_contract["accepted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Oblicz deadline z uwzględnieniem deadline_boost
    base_days = contract["czas_realizacji_dni"]
    bonus_days = 0
    
    # Sprawdź aktywne efekty deadline_boost
    if "events" in business_data:
        active_effects = business_data["events"].get("active_effects", [])
        for i, effect in enumerate(active_effects):
            if effect.get("type") == "deadline_boost" and effect.get("remaining_contracts", 0) > 0:
                bonus_days = effect.get("days", 0)
                # Zmniejsz licznik pozostałych kontraktów
                business_data["events"]["active_effects"][i]["remaining_contracts"] -= 1
                
                # Zaznacz kontrakt jako zboostowany
                active_contract["affected_by_event"] = {
                    "type": "deadline_boost",
                    "event_title": "Energy Burst",
                    "days_added": bonus_days
                }
                
                # Usuń efekt jeśli licznik osiągnął 0
                if business_data["events"]["active_effects"][i]["remaining_contracts"] == 0:
                    business_data["events"]["active_effects"].pop(i)
                
                break
    
    active_contract["deadline"] = (
        datetime.now() + timedelta(days=base_days + bonus_days)
    ).strftime("%Y-%m-%d %H:%M:%S")
    active_contract["status"] = "in_progress"
    active_contract["solution"] = ""
    
    business_data["contracts"]["active"].append(active_contract)
    
    # Usuń z dostępnej puli
    business_data["contracts"]["available_pool"] = [
        c for c in business_data["contracts"]["available_pool"] if c["id"] != contract_id
    ]
    
    return business_data, True, "Kontrakt przyjęty!", None

def submit_contract_solution(
    user_data: Dict, 
    contract_id: str, 
    solution: str,
    start_time: Optional[datetime] = None,
    paste_events: Optional[list] = None
) -> Tuple[Dict, bool, str, Optional[Tuple[str, Dict]]]:
    """Przesyła rozwiązanie kontraktu (bez oceny AI - uproszczona wersja MVP)
    
    Args:
        user_data: Pełne dane użytkownika (modyfikuje degencoins)
        contract_id: ID kontraktu
        solution: Tekst rozwiązania
        start_time: Kiedy użytkownik rozpoczął pisanie (dla anti-cheat)
        paste_events: Lista zdarzeń paste (dla anti-cheat)
        
    Returns:
        Tuple[user_data, success, message, triggered_event]
        triggered_event: None lub (event_id, event_data) jeśli wydarzenie się wylosowało
    """
    # Backward compatibility: obsługa obu struktur (business_game i business_games)
    if "business_games" in user_data and "consulting" in user_data["business_games"]:
        business_data = user_data["business_games"]["consulting"]
        industry_id = "consulting"
    elif "business_game" in user_data:
        business_data = user_data["business_game"]
        industry_id = None
    else:
        return user_data, False, "Brak danych gry w user_data", None
    
    # Znajdź aktywny kontrakt
    contract = next(
        (c for c in business_data["contracts"]["active"] if c["id"] == contract_id),
        None
    )
    
    if not contract:
        return user_data, False, "Kontrakt nie znaleziony w aktywnych", None
    
    # Sprawdź minimalną długość rozwiązania
    word_count = len(solution.split())
    min_words = contract.get("min_slow", 300)
    
    if word_count < min_words:
        return user_data, False, f"Rozwiązanie zbyt krótkie. Minimum: {min_words} słów (masz: {word_count})", None
    
    # ANTI-CHEAT: Sprawdź oszustwa PRZED oceną
    anti_cheat_result = None
    if start_time:
        from utils.anti_cheat import check_for_cheating
        
        submit_time = datetime.now()
        anti_cheat_result = check_for_cheating(
            solution=solution,
            start_time=start_time,
            submit_time=submit_time,
            paste_events=paste_events,
            use_ai_detection=True  # Włącz Gemini AI detection
        )
    
    # NOWY SYSTEM OCENY - używa evaluate_contract_solution()
    # Obsługuje 3 tryby: heuristic, ai, game_master
    from utils.business_game_evaluation import evaluate_contract_solution
    
    rating, feedback, details = evaluate_contract_solution(
        user_data=user_data,
        contract=contract,
        solution=solution
    )
    
    # ANTI-CHEAT: Aplikuj karę do oceny jeśli wykryto oszustwa
    if anti_cheat_result and anti_cheat_result["is_suspicious"]:
        from utils.anti_cheat import apply_anti_cheat_penalty, format_anti_cheat_warning
        
        original_rating = rating
        rating = apply_anti_cheat_penalty(rating, anti_cheat_result["total_penalty"])
        
        # Dodaj ostrzeżenie do feedbacku
        cheat_warning = format_anti_cheat_warning(anti_cheat_result)
        feedback = f"⚠️ **WYKRYTO PODEJRZANĄ AKTYWNOŚĆ**\n\n{cheat_warning}\n\n---\n\n{feedback}"
        
        # Zapisz w details
        details["anti_cheat"] = {
            "original_rating": original_rating,
            "penalized_rating": rating,
            "flags": anti_cheat_result["flags"],
            "penalty": anti_cheat_result["total_penalty"]
        }
    
    # Jeśli rating=0, oznacza to że trafiło do kolejki Mistrza Gry
    # W tym przypadku NIE finalizujemy kontraktu od razu
    if rating == 0:
        # Kontrakt pozostaje aktywny, czeka na ocenę
        # Zapisz informację że oczekuje
        contract["status"] = "pending_review"
        contract["pending_review_id"] = details.get("review_id")
        user_data["business_game"] = business_data
        return user_data, True, feedback, None
    
    # Oblicz nagrodę (dla ocen 1-5)
    reward = calculate_contract_reward(contract, rating, business_data)
    
    # Zaktualizuj finanse i statystyki
    # DODAJ DO SALDA FIRMY, nie do DegenCoins gracza!
    business_data["money"] = business_data.get("money", 0) + reward["coins"]
    business_data["firm"]["reputation"] += reward["reputation"]
    
    # Statystyki zależą od tego czy kontrakt był płatny
    if reward.get("rejection_penalty", False):
        # Odrzucony kontrakt
        business_data["stats"]["contracts_rejected"] = business_data["stats"].get("contracts_rejected", 0) + 1
    else:
        # Zaakceptowany kontrakt
        business_data["stats"]["total_revenue"] += reward["coins"]
        business_data["stats"]["contracts_completed"] += 1
    
    # Zaktualizuj statystyki ocen (wszystkie, nawet odrzucone)
    rating_key = f"contracts_{rating}star"
    if rating_key in business_data["stats"]:
        business_data["stats"][rating_key] += 1
    
    # Zaktualizuj średnią ocenę
    total_contracts = business_data["stats"]["contracts_completed"]
    total_stars = sum(
        business_data["stats"][f"contracts_{r}star"] * r 
        for r in range(1, 6)
    )
    business_data["stats"]["avg_rating"] = round(total_stars / total_contracts, 2) if total_contracts > 0 else 0.0
    
    # Zaktualizuj statystyki kategorii
    category = contract["kategoria"]
    if category in business_data["stats"]["category_stats"]:
        cat_stats = business_data["stats"]["category_stats"][category]
        cat_stats["completed"] += 1
        cat_stats["total_earned"] += reward["coins"]
        # Przelicz średnią ocenę dla kategorii
        old_avg = cat_stats["avg_rating"]
        old_count = cat_stats["completed"] - 1
        cat_stats["avg_rating"] = round(
            (old_avg * old_count + rating) / cat_stats["completed"], 2
        ) if cat_stats["completed"] > 0 else rating
    
    # Dodaj do historii transakcji
    business_data["history"]["transactions"].append({
        "type": "contract_reward",
        "contract_id": contract_id,
        "contract_title": contract["tytul"],
        "amount": reward["coins"],
        "rating": rating,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Przenieś do ukończonych
    completed_contract = contract.copy()
    completed_contract["solution"] = solution
    completed_contract["rating"] = rating
    completed_contract["feedback"] = feedback  # Feedback z systemu oceny
    completed_contract["evaluation_details"] = details  # Szczegóły oceny
    completed_contract["reward"] = reward
    completed_contract["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    completed_contract["status"] = "completed"
    
    business_data["contracts"]["completed"].append(completed_contract)
    
    # Usuń z aktywnych
    business_data["contracts"]["active"] = [
        c for c in business_data["contracts"]["active"] if c["id"] != contract_id
    ]
    
    # Zapisz zaktualizowane business_data przed level up check (backward compatibility)
    if industry_id:
        user_data["business_games"][industry_id] = business_data
    else:
        user_data["business_game"] = business_data
    
    # Sprawdź level up
    user_data, leveled_up = update_firm_level(user_data)
    
    # Komunikat zależny od oceny
    if reward.get("rejection_penalty", False):
        # Kontrakt odrzucony (1-2★)
        success_msg = f"⚠️ Kontrakt oceniony na {'⭐' * rating} ({rating}/5)\n\n"
        success_msg += f"❌ Klient odrzucił rozwiązanie - brak zapłaty!\n"
        success_msg += f"💔 Reputacja: {reward['reputation']} (kara za złą pracę)\n\n"
        success_msg += "💡 Spróbuj bardziej merytorycznego rozwiązania w następnym kontrakcie."
    else:
        # Kontrakt zaakceptowany (3-5★)
        success_msg = f"✅ Kontrakt ukończony! {'⭐' * rating} ({rating}/5)\n"
        success_msg += f"💰 Zarobiono: {reward['coins']} monet\n"
        success_msg += f"📈 Reputacja: +{reward['reputation']}"
    
    if leveled_up:
        success_msg += f"\n\n🎉 GRATULACJE! Awansowałeś na poziom {user_data['business_game']['firm']['level']}!"
    
    return user_data, True, success_msg, None

def simulate_contract_evaluation(solution: str, contract: Dict) -> int:
    """Symuluje ocenę kontraktu (uproszczona wersja dla MVP)"""
    # W pełnej wersji tutaj będzie prawdziwa ocena AI
    # Na razie prosta heurystyka
    
    word_count = len(solution.split())
    min_words = contract.get("min_slow", 300)
    
    # Bazowa ocena na podstawie długości
    if word_count >= min_words * 2:
        base_rating = 5
    elif word_count >= min_words * 1.5:
        base_rating = 4
    elif word_count >= min_words * 1.2:
        base_rating = 3
    elif word_count >= min_words:
        base_rating = 2
    else:
        base_rating = 1
    
    # Dodatkowe punkty za obecność kluczowych słów (bardzo uproszczone)
    keywords = ["strategia", "plan", "framework", "coaching", "feedback", "komunikacja", 
                "analiza", "rozwiązanie", "krok", "proces", "cel", "pytanie"]
    keyword_count = sum(1 for kw in keywords if kw.lower() in solution.lower())
    
    if keyword_count >= 8:
        base_rating = min(5, base_rating + 1)
    
    return base_rating

def calculate_contract_reward(contract: Dict, rating: int, business_data: Dict) -> Dict:
    """Oblicza nagrodę za kontrakt uwzględniając bonusy od pracowników
    
    ZASADY WYPŁAT:
    - 1-2 gwiazdki: 0 monet (kontrakt odrzucony przez klienta)
    - 3 gwiazdki: nagroda_base (minimalna wypłata)
    - 4 gwiazdki: nagroda_4star
    - 5 gwiazdek: nagroda_5star (maksymalna wypłata)
    """
    # Odrzucone kontrakty (1-2★) = 0 monet
    if rating <= 2:
        return {
            "coins": 0,
            "reputation": -5,  # Kara do reputacji za złą pracę
            "base": 0,
            "bonus_multiplier": 0,
            "rejection_penalty": True
        }
    
    # Akceptowalne kontrakty (3-5★) = płatne
    base_reward = contract["nagroda_base"]
    
    if rating == 5:
        base_reward = contract["nagroda_5star"]
    elif rating == 4:
        base_reward = contract["nagroda_4star"]
    # rating == 3 używa nagroda_base (już ustawione)
    
    # Sprawdź bonusy od pracowników
    category = contract["kategoria"]
    bonus_multiplier = 1.0
    
    for employee in business_data["employees"]:
        emp_type = EMPLOYEE_TYPES.get(employee["type"])
        if emp_type and emp_type["bonus_type"] == "category_boost":
            if emp_type["specjalizacja"] == category:
                bonus_multiplier += emp_type["bonus_value"]
    
    final_coins = int(base_reward * bonus_multiplier)
    reputation = contract["reputacja"]
    
    return {
        "coins": final_coins,
        "reputation": reputation,
        "base": base_reward,
        "bonus_multiplier": bonus_multiplier,
        "rejection_penalty": False
    }


def submit_contract_ai_conversation(user_data: Dict, contract_id: str) -> Tuple[Dict, bool, str, Optional[Tuple[str, Dict]]]:
    """Zakończ AI Conversation contract, policz nagrody i zaktualizuj dane użytkownika.

    Uwaga: Funkcja używa utils.ai_conversation_engine.calculate_final_conversation_score
    by pobrać końcowy wynik (gwiazdki, punkty, metryki) i aplikuje odpowiednie nagrody.
    """
    from utils.ai_conversation_engine import calculate_final_conversation_score

    # Pobierz business_data dla domyślnej branży (backward compatibility)
    if "business_games" in user_data and "consulting" in user_data["business_games"]:
        business_data = user_data["business_games"]["consulting"]
    elif "business_game" in user_data:
        business_data = user_data["business_game"]
    else:
        return user_data, False, "Brak danych gry w user_data", None

    # Znajdź aktywny kontrakt
    contract = next((c for c in business_data["contracts"]["active"] if c["id"] == contract_id), None)
    if not contract:
        return user_data, False, "Kontrakt nie znaleziony w aktywnych", None

    # Pobierz wynik z engine
    try:
        result = calculate_final_conversation_score(contract_id)
    except Exception as e:
        return user_data, False, f"Błąd przy obliczaniu wyniku rozmowy: {e}", None

    stars = result.get("stars", 1)
    total_points = result.get("total_points", 0)
    metrics = result.get("metrics", {})

    # Reward mapping - użyj nagród z kontraktu (zakładamy wartości base i 5star)
    reward_base = contract.get("nagroda_base", 0)
    reward_5star = contract.get("nagroda_5star", reward_base)

    # Liniowa interpolacja nagrody w zależności od gwiazdek (1-5)
    reward = int(reward_base + ((stars - 1) / 4.0) * (reward_5star - reward_base))

    # DODAJ DO SALDA FIRMY, nie do DegenCoins gracza!
    business_data["money"] = business_data.get("money", 0) + reward

    # Zaktualizuj reputację firmy
    rep_change = int((stars - 3) * 10)  # -20..+20
    business_data["firm"]["reputation"] = business_data["firm"].get("reputation", 0) + rep_change

    # Przenieś kontrakt do completed (z podstawowymi danymi)
    completed_contract = contract.copy()
    completed_contract["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    completed_contract["stars"] = stars
    completed_contract["points"] = total_points
    completed_contract["reward"] = reward
    completed_contract["metrics"] = metrics
    completed_contract["status"] = "completed"

    business_data["contracts"]["completed"].append(completed_contract)

    # Usuń z aktywnych
    business_data["contracts"]["active"] = [c for c in business_data["contracts"]["active"] if c["id"] != contract_id]

    # Zaktualizuj statystyki
    business_data["stats"]["contracts_completed"] = business_data["stats"].get("contracts_completed", 0) + 1
    rating_key = f"contracts_{stars}star"
    if rating_key in business_data["stats"]:
        business_data["stats"][rating_key] += 1

    # Dodaj do historii transakcji
    if "history" not in business_data:
        business_data["history"] = {"transactions": []}
    business_data["history"]["transactions"].append({
        "type": "contract_reward",
        "contract_id": contract_id,
        "contract_title": contract.get("tytul", ""),
        "amount": reward,
        "rating": stars,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # Zapisz zmiany z powrotem
    if "business_games" in user_data and "consulting" in user_data["business_games"]:
        user_data["business_games"]["consulting"] = business_data
    else:
        user_data["business_game"] = business_data

    # Sprawdź level up
    user_data, leveled_up = update_firm_level(user_data)

    success_msg = f"✅ Kontrakt {contract_id} zakończony. Otrzymano {reward} monet. Gwiazdki: {stars}/5"
    if leveled_up:
        success_msg += f"\n\n🎉 Awansowałeś na poziom {user_data['business_game']['firm']['level']}!"

    return user_data, True, success_msg, None

# =============================================================================
# ZARZĄDZANIE PRACOWNIKAMI
# =============================================================================

def can_hire_employee(user_data: Dict, employee_type: str, industry_id: str = "consulting") -> Tuple[bool, str]:
    """Sprawdza czy można zatrudnić pracownika
    
    Args:
        user_data: Pełne dane użytkownika (sprawdza degencoins)
        employee_type: Typ pracownika do zatrudnienia
        industry_id: ID branży (domyślnie "consulting")
    """
    # Get game data for specific industry
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        business_data = user_data["business_games"][industry_id]
    elif "business_game" in user_data:
        business_data = user_data["business_game"]
    else:
        return False, "Brak danych gry"
    
    emp_data = EMPLOYEE_TYPES.get(employee_type)
    if not emp_data:
        return False, "Nieznany typ pracownika"
    
    # Sprawdź poziom firmy
    if business_data["firm"]["level"] < emp_data["wymagany_poziom"]:
        return False, f"Wymagany poziom firmy: {emp_data['wymagany_poziom']}"
    
    # Sprawdź limit pracowników na podstawie BIURA (nie poziomu firmy)
    current_count = len(business_data["employees"])
    
    # Pobierz typ biura (domyślnie home_office dla starych zapisów)
    office_type = business_data.get("office", {}).get("type", "home_office")
    max_employees = OFFICE_TYPES[office_type]["max_pracownikow"]
    
    if current_count >= max_employees:
        # Znajdź następne biuro w ścieżce upgrade'u
        from data.business_data import OFFICE_UPGRADE_PATH
        current_index = OFFICE_UPGRADE_PATH.index(office_type)
        if current_index < len(OFFICE_UPGRADE_PATH) - 1:
            next_office = OFFICE_UPGRADE_PATH[current_index + 1]
            next_office_info = OFFICE_TYPES[next_office]
            return False, f"Limit pracowników osiągnięty ({max_employees}). Ulepsz biuro do {next_office_info['nazwa']} (koszt: {next_office_info['koszt_ulepszenia']} zł)"
        else:
            return False, f"Maksimum pracowników: {max_employees}"
    
    # Sprawdź saldo firmy (nie osobiste DegenCoins!)
    if business_data.get('money', 0) < emp_data["koszt_zatrudnienia"]:
        return False, f"Niewystarczające środki. Potrzebujesz: {emp_data['koszt_zatrudnienia']} PLN"
    
    return True, ""

def hire_employee(user_data: Dict, employee_type: str, industry_id: str = "consulting") -> Tuple[Dict, bool, str]:
    """Zatrudnia pracownika
    
    Args:
        user_data: Pełne dane użytkownika (modyfikuje degencoins)
        employee_type: Typ pracownika do zatrudnienia
        industry_id: ID branży (domyślnie "consulting")
    """
    # Get game data for specific industry
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        business_data = user_data["business_games"][industry_id]
    elif "business_game" in user_data:
        business_data = user_data["business_game"]
    else:
        return user_data, False, "Brak danych gry"
    
    can_hire, reason = can_hire_employee(user_data, employee_type, industry_id)
    if not can_hire:
        return user_data, False, reason
    
    emp_data = EMPLOYEE_TYPES[employee_type]
    
    # Odejmij koszt zatrudnienia Z SALDA FIRMY (nie z osobistych DegenCoins!)
    business_data["money"] = business_data.get("money", 0) - emp_data["koszt_zatrudnienia"]
    business_data["stats"]["total_costs"] += emp_data["koszt_zatrudnienia"]
    
    # Dodaj pracownika
    new_employee = {
        "type": employee_type,
        "hired_date": datetime.now().strftime("%Y-%m-%d"),
        "id": f"EMP-{len(business_data['employees']) + 1:03d}"
    }
    business_data["employees"].append(new_employee)
    
    # Dodaj do historii
    business_data["history"]["transactions"].append({
        "type": "employee_hired",
        "employee_type": employee_type,
        "amount": -emp_data["koszt_zatrudnienia"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Zapisz zmiany
    user_data["business_game"] = business_data
    
    return user_data, True, f"Zatrudniono: {emp_data['nazwa']}!"

def fire_employee(user_data: Dict, employee_id: str, industry_id: str = "consulting") -> Tuple[Dict, bool, str]:
    """Zwalnia pracownika
    
    Args:
        user_data: Pełne dane użytkownika
        employee_id: ID pracownika do zwolnienia
        industry_id: ID branży (domyślnie "consulting")
    """
    # Get game data for specific industry
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        business_data = user_data["business_games"][industry_id]
    elif "business_game" in user_data:
        business_data = user_data["business_game"]
    else:
        return user_data, False, "Brak danych gry"
    
    employee = next(
        (e for e in business_data["employees"] if e["id"] == employee_id),
        None
    )
    
    if not employee:
        return user_data, False, "Pracownik nie znaleziony"
    
    emp_data = EMPLOYEE_TYPES[employee["type"]]
    
    # Usuń pracownika
    business_data["employees"] = [
        e for e in business_data["employees"] if e["id"] != employee_id
    ]
    
    # Dodaj do historii
    business_data["history"]["transactions"].append({
        "type": "employee_fired",
        "employee_type": employee["type"],
        "amount": 0,  # Zwolnienie nie ma kosztu finansowego, ale zapisujemy dla kompletności
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Zapisz zmiany
    user_data["business_game"] = business_data
    
    return user_data, True, f"Zwolniono: {emp_data['nazwa']}"

def calculate_daily_costs(business_data: Dict) -> float:
    """Oblicza dzienny koszt pracowników (bez biura)"""
    return calculate_employee_costs(business_data["employees"])

def calculate_total_daily_costs(business_data: Dict) -> float:
    """Oblicza łączne dzienne koszty: pracownicy + biuro"""
    employee_costs = calculate_employee_costs(business_data["employees"])
    
    # Dodaj koszty biura
    office_type = business_data.get("office", {}).get("type", "home_office")
    office_costs = OFFICE_TYPES[office_type]["koszt_dzienny"]
    
    return employee_costs + office_costs

def process_daily_costs(user_data: Dict) -> Dict:
    """Przetwarza dzienne koszty (wywoływane raz dziennie)
    
    Args:
        user_data: Pełne dane użytkownika (modyfikuje degencoins)
    """
    business_data = user_data["business_game"]
    
    # Koszty pracowników
    employee_cost = calculate_daily_costs(business_data)
    
    # Koszty biura
    office_type = business_data.get("office", {}).get("type", "home_office")
    office_cost = OFFICE_TYPES[office_type]["koszt_dzienny"]
    
    total_cost = employee_cost + office_cost
    
    if total_cost > 0:
        business_data["money"] = business_data.get("money", 0) - total_cost
        business_data["stats"]["total_costs"] += total_cost
        
        # Transakcja dla pracowników (jeśli > 0)
        if employee_cost > 0:
            business_data["history"]["transactions"].append({
                "type": "daily_costs",
                "amount": -employee_cost,
                "description": "Koszty dzienne: pracownicy",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Transakcja dla biura (jeśli > 0)
        if office_cost > 0:
            business_data["history"]["transactions"].append({
                "type": "office_rent",
                "amount": -office_cost,
                "description": f"Koszty dzienne: {OFFICE_TYPES[office_type]['nazwa']}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        user_data["business_game"] = business_data
    
    return user_data

# =============================================================================
# RANKINGI
# =============================================================================

def calculate_overall_score(business_data: Dict) -> float:
    """Oblicza Overall Score dla rankingu"""
    stats = business_data["stats"]
    firm = business_data["firm"]
    weights = GAME_CONFIG["ranking_weights"]["overall"]
    
    # Poziom 1 = 0 punktów bazowych (tylko awanse na wyższe poziomy dają bonus)
    level_bonus = max(0, firm["level"] - 1) * 5000
    
    score = (
        weights["revenue"] * stats["total_revenue"] +
        weights["avg_rating"] * (stats["avg_rating"] * 1000) +
        weights["reputation"] * firm["reputation"] +
        weights["level"] * level_bonus +
        weights["contracts"] * (stats["contracts_completed"] * 100)
    )
    
    return round(score, 2)

def update_user_ranking(business_data: Dict) -> Dict:
    """Aktualizuje overall score użytkownika"""
    business_data["ranking"]["overall_score"] = calculate_overall_score(business_data)
    return business_data

def get_all_rankings(all_users_data: List[Dict], ranking_type: str = "overall") -> List[Dict]:
    """Generuje ranking wszystkich użytkowników"""
    rankings = []
    
    for user_data in all_users_data:
        if "business_game" not in user_data:
            continue
        
        bg_data = user_data["business_game"]
        stats = bg_data["stats"]
        
        # Brak bariery wejścia - każdy może być w rankingu od początku
        # (zmieniono z warunku: if stats["contracts_completed"] < min_contracts)
        
        if ranking_type == "overall":
            score = bg_data["ranking"]["overall_score"]
        elif ranking_type == "revenue":
            score = stats["total_revenue"]
        elif ranking_type == "quality":
            score = stats["avg_rating"]
        elif ranking_type == "productivity_30d":
            score = stats["last_30_days"]["contracts"]
        else:
            score = 0
        
        rankings.append({
            "username": user_data.get("username", "Unknown"),
            "firm_name": bg_data["firm"]["name"],
            "firm_level": bg_data["firm"]["level"],
            "score": score,
            "stats": stats,
            "founded": bg_data["firm"]["founded"]
        })
    
    # Sortuj malejąco
    rankings.sort(key=lambda x: x["score"], reverse=True)
    
    # Dodaj pozycje
    for idx, firm in enumerate(rankings, 1):
        firm["position"] = idx
    
    return rankings

# =============================================================================
# STATYSTYKI I RAPORTY
# =============================================================================

def get_revenue_chart_data(business_data: Dict, days: int = 30) -> Dict:
    """Generuje dane do wykresu przychodów"""
    # Uproszczona wersja - w pełnej implementacji analizujemy transactions
    transactions = business_data["history"]["transactions"]
    
    daily_revenue = {}
    for trans in transactions:
        if trans["type"] == "contract_reward":
            date = trans["timestamp"][:10]
            daily_revenue[date] = daily_revenue.get(date, 0) + trans["amount"]
    
    return {
        "dates": list(daily_revenue.keys())[-days:],
        "revenue": list(daily_revenue.values())[-days:]
    }

def get_category_distribution(business_data: Dict) -> Dict:
    """Zwraca rozkład kontraktów po kategoriach"""
    category_stats = business_data["stats"]["category_stats"]
    return {
        cat: stats["completed"] 
        for cat, stats in category_stats.items() 
        if stats["completed"] > 0
    }


# =============================================================================
# SYSTEM SCENARIUSZY - MODYFIKATORY I CELE
# =============================================================================

def apply_scenario_modifier(base_value: float, modifier_type: str, game_data: Dict) -> float:
    """
    Aplikuje modyfikator scenariusza do wartości bazowej
    
    Args:
        base_value: Wartość bazowa do zmodyfikowania
        modifier_type: Typ modyfikatora (np. "revenue_multiplier")
        game_data: Dane gry zawierające scenario_modifiers
    
    Returns:
        Zmodyfikowana wartość
    """
    modifiers = game_data.get("scenario_modifiers", {})
    multiplier = modifiers.get(modifier_type, 1.0)
    return base_value * multiplier


def get_scenario_info(game_data: Dict) -> Optional[Dict]:
    """
    Pobiera informacje o aktywnym scenariuszu
    
    Args:
        game_data: Dane gry
    
    Returns:
        Dict z info o scenariuszu lub None
    """
    scenario_id = game_data.get("scenario_id")
    if not scenario_id:
        return None
    
    # TODO: Tutaj można dodać więcej info z SCENARIOS
    return {
        "id": scenario_id,
        "modifiers": game_data.get("scenario_modifiers", {}),
        "objectives": game_data.get("scenario_objectives", []),
        "completed": game_data.get("objectives_completed", [])
    }


def check_objective_completion(game_data: Dict, user_data: Dict, objective: Dict) -> bool:
    """
    Sprawdza czy cel scenariusza został osiągnięty
    
    Args:
        game_data: Dane gry (business_games[industry_id])
        user_data: Pełne dane użytkownika
        objective: Dict z celem do sprawdzenia
    
    Returns:
        True jeśli cel osiągnięty
    """
    obj_type = objective.get("type")
    target = objective.get("target")
    
    if obj_type == "revenue_total":
        return game_data["stats"]["total_revenue"] >= target
    
    elif obj_type == "reputation":
        return game_data["firm"]["reputation"] >= target
    
    elif obj_type == "level":
        return game_data["firm"]["level"] >= target
    
    elif obj_type == "money":
        # Dla "Corporate Rescue" - sprawdza czy wyszedł na zero
        initial_money = game_data.get("initial_money", 0)
        if initial_money < 0:
            current_money = user_data.get("degencoins", 0)
            return current_money >= target
        return True
    
    elif obj_type == "employees":
        target_count = target if target is not None else 0
        return len(game_data.get("employees", [])) >= target_count
    
    return False


def update_objectives_progress(game_data: Dict, user_data: Dict) -> List[Dict]:
    """
    Aktualizuje postęp celów i zwraca listę nowo ukończonych celów
    
    Args:
        game_data: Dane gry
        user_data: Pełne dane użytkownika
    
    Returns:
        Lista nowo ukończonych celów z nagrodami
    """
    objectives = game_data.get("scenario_objectives", [])
    completed = game_data.get("objectives_completed", [])
    newly_completed = []
    
    for i, objective in enumerate(objectives):
        obj_id = f"obj_{i}"
        
        # Już ukończony? Skip
        if obj_id in completed:
            continue
        
        # Sprawdź czy teraz ukończony
        if check_objective_completion(game_data, user_data, objective):
            completed.append(obj_id)
            newly_completed.append({
                "description": objective["description"],
                "reward_money": objective.get("reward_money", 0)
            })
    
    game_data["objectives_completed"] = completed
    return newly_completed


def get_objectives_summary(game_data: Dict, user_data: Dict) -> Dict:
    """
    Zwraca podsumowanie celów scenariusza z postępem
    
    Args:
        game_data: Dane gry
        user_data: Pełne dane użytkownika
    
    Returns:
        Dict z celami i ich statusem
    """
    objectives = game_data.get("scenario_objectives", [])
    completed_ids = game_data.get("objectives_completed", [])
    
    summary = []
    for i, objective in enumerate(objectives):
        obj_id = f"obj_{i}"
        is_completed = obj_id in completed_ids
        
        # Pobierz aktualny postęp
        obj_type = objective.get("type")
        target = objective.get("target")
        current = 0
        
        if obj_type == "revenue_total":
            current = game_data["stats"]["total_revenue"]
        elif obj_type == "reputation":
            current = game_data["firm"]["reputation"]
        elif obj_type == "level":
            current = game_data["firm"]["level"]
        elif obj_type == "money":
            current = user_data.get("degencoins", 0)
        elif obj_type == "employees":
            current = len(game_data.get("employees", []))
        
        summary.append({
            "id": obj_id,
            "description": objective["description"],
            "type": obj_type,
            "current": current,
            "target": target,
            "completed": is_completed,
            "reward": objective.get("reward_money", 0)
        })
    
    return {
        "objectives": summary,
        "total": len(objectives),
        "completed_count": len(completed_ids)
    }


def get_firm_summary(user_data: Dict, industry_id: str = "consulting") -> Dict:
    """Zwraca podsumowanie firmy
    
    Args:
        user_data: Pełne dane użytkownika (pobiera degencoins)
        industry_id: ID branży (domyślnie consulting)
    """
    # Pobierz dane gry z backward compatibility
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        business_data = user_data["business_games"][industry_id]
    elif "business_game" in user_data:
        business_data = user_data["business_game"]
    else:
        # Fallback - zwróć minimalne dane
        return {
            "name": "Firma",
            "level": 1,
            "level_name": FIRM_LEVELS[1]["nazwa"],
            "coins": user_data.get('degencoins', 0),
            "reputation": 50,
            "founded": "N/A",
            "total_revenue": 0,
            "total_costs": 0,
            "net_profit": 0,
            "contracts_completed": 0,
            "avg_rating": 0.0,
            "employees_count": 0,
            "daily_capacity": 0,
            "daily_costs": 0
        }
    
    firm = business_data["firm"]
    stats = business_data["stats"]
    
    return {
        "name": firm["name"],
        "level": firm["level"],
        "level_name": FIRM_LEVELS[firm["level"]]["nazwa"],
        "coins": user_data.get('degencoins', 0),  # Teraz z user_data!
        "reputation": firm["reputation"],
        "founded": firm["founded"],
        "total_revenue": stats["total_revenue"],
        "total_costs": stats["total_costs"],
        "net_profit": stats["total_revenue"] - stats["total_costs"],
        "contracts_completed": stats["contracts_completed"],
        "avg_rating": stats["avg_rating"],
        "employees_count": len(business_data["employees"]),
        "daily_capacity": calculate_daily_capacity(firm["level"], business_data["employees"]),
        "daily_costs": calculate_daily_costs(business_data)
    }

# =============================================================================
# MIGRACJA DANYCH - Wydarzenia do transakcji
# =============================================================================

def migrate_event_transactions(user_data: Dict, industry_id: str = "consulting") -> Tuple[Dict, int]:
    """Migruje stare wydarzenia z monetami do transakcji finansowych
    
    Przeszukuje events.history i dodaje brakujące transakcje event_reward/event_cost
    do history.transactions dla wydarzeń, które miały efekt 'coins'.
    
    Args:
        user_data: Pełne dane użytkownika
        industry_id: ID branży (domyślnie consulting)
        
    Returns:
        (updated_user_data, liczba_dodanych_transakcji)
    """
    # Pobierz dane gry (z backward compatibility)
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        business_data = user_data["business_games"][industry_id]
    elif "business_game" in user_data:
        business_data = user_data["business_game"]
    else:
        return user_data, 0
    
    # Sprawdź czy są wydarzenia
    events_history = business_data.get("events", {}).get("history", [])
    if not events_history:
        return user_data, 0
    
    # Pobierz istniejące transakcje event_reward/event_cost
    existing_transactions = business_data.get("history", {}).get("transactions", [])
    existing_event_ids = set()
    for trans in existing_transactions:
        if trans.get("type") in ["event_reward", "event_cost"] and "event_id" in trans:
            existing_event_ids.add(trans["event_id"])
    
    # Przejdź przez wydarzenia i dodaj brakujące transakcje
    added_count = 0
    for event in events_history:
        event_id = event.get("event_id")
        effects = event.get("effects", {})
        
        # Sprawdź czy wydarzenie ma efekt coins
        if "coins" not in effects:
            continue
        
        # Sprawdź czy już jest transakcja dla tego wydarzenia
        if event_id in existing_event_ids:
            continue
        
        coins_amount = effects["coins"]
        timestamp = event.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Dodaj transakcję
        new_transaction = {
            "type": "event_reward" if coins_amount > 0 else "event_cost",
            "amount": coins_amount,
            "event_id": event_id,
            "event_title": event.get("title", "Unknown Event"),
            "timestamp": timestamp,
            "migrated": True  # Oznacz jako zmigrowane
        }
        
        business_data["history"]["transactions"].append(new_transaction)
        added_count += 1
    
    # Zapisz zmiany
    if added_count > 0:
        # Zapisz w nowej strukturze
        if "business_games" not in user_data:
            user_data["business_games"] = {}
        user_data["business_games"][industry_id] = business_data
        # Backward compatibility - zapisz też w starej strukturze
        if "business_game" in user_data and industry_id == "consulting":
            user_data["business_game"] = business_data
    
    return user_data, added_count


def close_business_game(username: str, user_data: Dict, industry_id: str) -> Dict:
    """Zamyka firmę i przenosi saldo do DegenCoins gracza
    
    Args:
        username: Nazwa użytkownika
        user_data: Pełne dane użytkownika
        industry_id: ID branży (np. "consulting")
    
    Returns:
        Zaktualizowane user_data
    """
    if "business_games" not in user_data or industry_id not in user_data["business_games"]:
        return user_data
    
    business_data = user_data["business_games"][industry_id]
    firm_money = business_data.get("money", 0)
    
    # Jeśli firma ma dodatnie saldo, przekaż do DegenCoins
    if firm_money > 0:
        user_data["degencoins"] = user_data.get("degencoins", 0) + firm_money
        
        # Dodaj transakcję do historii
        if "transaction_history" not in user_data:
            user_data["transaction_history"] = []
        
        user_data["transaction_history"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "business_closure",
            "amount": firm_money,
            "description": f"Zamknięcie firmy: {business_data['firm']['name']}",
            "industry": industry_id
        })
    
    # Usuń dane firmy
    del user_data["business_games"][industry_id]
    
    # Backward compatibility
    if "business_game" in user_data and industry_id == "consulting":
        del user_data["business_game"]
    
    return user_data