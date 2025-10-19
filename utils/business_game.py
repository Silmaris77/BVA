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
    calculate_employee_costs, get_contract_by_id
)

# =============================================================================
# INICJALIZACJA FIRMY
# =============================================================================

def initialize_business_game(username: str) -> Dict:
    """Inicjalizuje Business Games dla nowego użytkownika
    
    NOTE: Monety są teraz przechowywane w user_data['degencoins'], nie tutaj!
    """
    return {
        "firm": {
            "name": f"{username}'s Consulting",
            "founded": datetime.now().strftime("%Y-%m-%d"),
            "level": GAME_CONFIG["starting_level"],
            # coins - USUNIĘTE! Teraz używamy user_data['degencoins']
            "reputation": GAME_CONFIG["starting_reputation"]
        },
        "employees": [],
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
    reputation = user_data["business_game"]["firm"]["reputation"]
    return get_firm_level(coins, reputation)

def update_firm_level(user_data: Dict) -> Tuple[Dict, bool]:
    """Aktualizuje poziom firmy, zwraca (updated_user_data, level_up_occurred)
    
    Args:
        user_data: Pełne dane użytkownika
    """
    business_data = user_data["business_game"]
    old_level = business_data["firm"]["level"]
    new_level = get_current_firm_level(user_data)
    
    if new_level > old_level:
        business_data["firm"]["level"] = new_level
        business_data["history"]["level_ups"].append({
            "from_level": old_level,
            "to_level": new_level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        user_data["business_game"] = business_data
        return user_data, True
    
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
        
        # Wybierz po jednym z każdego poziomu trudności (1-5)
        new_pool = []
        for difficulty in range(1, 6):  # 1, 2, 3, 4, 5 gwiazdek
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
    
    # Sprawdź dzienny limit
    today = datetime.now().strftime("%Y-%m-%d")
    today_accepted = sum(
        1 for c in business_data["contracts"]["active"] 
        if c.get("accepted_date", "").startswith(today)
    )
    
    capacity = calculate_daily_capacity(
        business_data["firm"]["level"], 
        business_data["employees"]
    )
    
    if today_accepted >= capacity:
        return False, f"Dzienny limit kontraktów wyczerpany ({capacity})"
    
    if today_accepted >= GAME_CONFIG["max_daily_contracts"]:
        return False, f"Absolutny dzienny limit: {GAME_CONFIG['max_daily_contracts']}"
    
    return True, ""

def accept_contract(business_data: Dict, contract_id: str) -> Tuple[Dict, bool, str]:
    """Przyjmuje kontrakt"""
    can_accept, reason = can_accept_contract(business_data)
    if not can_accept:
        return business_data, False, reason
    
    # Znajdź kontrakt w dostępnej puli
    contract = next(
        (c for c in business_data["contracts"]["available_pool"] if c["id"] == contract_id),
        None
    )
    
    if not contract:
        return business_data, False, "Kontrakt nie znaleziony"
    
    # Przenieś do aktywnych
    active_contract = contract.copy()
    active_contract["accepted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    active_contract["deadline"] = (
        datetime.now() + timedelta(days=contract["czas_realizacji_dni"])
    ).strftime("%Y-%m-%d %H:%M:%S")
    active_contract["status"] = "in_progress"
    active_contract["solution"] = ""
    
    business_data["contracts"]["active"].append(active_contract)
    
    # Usuń z dostępnej puli
    business_data["contracts"]["available_pool"] = [
        c for c in business_data["contracts"]["available_pool"] if c["id"] != contract_id
    ]
    
    return business_data, True, "Kontrakt przyjęty!"

def submit_contract_solution(
    user_data: Dict, 
    contract_id: str, 
    solution: str
) -> Tuple[Dict, bool, str]:
    """Przesyła rozwiązanie kontraktu (bez oceny AI - uproszczona wersja MVP)
    
    Args:
        user_data: Pełne dane użytkownika (modyfikuje degencoins)
    """
    business_data = user_data["business_game"]
    
    # Znajdź aktywny kontrakt
    contract = next(
        (c for c in business_data["contracts"]["active"] if c["id"] == contract_id),
        None
    )
    
    if not contract:
        return user_data, False, "Kontrakt nie znaleziony w aktywnych"
    
    # Sprawdź minimalną długość rozwiązania
    word_count = len(solution.split())
    min_words = contract.get("min_slow", 300)
    
    if word_count < min_words:
        return user_data, False, f"Rozwiązanie zbyt krótkie. Minimum: {min_words} słów (masz: {word_count})"
    
    # NOWY SYSTEM OCENY - używa evaluate_contract_solution()
    # Obsługuje 3 tryby: heuristic, ai, game_master
    from utils.business_game_evaluation import evaluate_contract_solution
    
    rating, feedback, details = evaluate_contract_solution(
        user_data=user_data,
        contract=contract,
        solution=solution
    )
    
    # Jeśli rating=0, oznacza to że trafiło do kolejki Mistrza Gry
    # W tym przypadku NIE finalizujemy kontraktu od razu
    if rating == 0:
        # Kontrakt pozostaje aktywny, czeka na ocenę
        # Zapisz informację że oczekuje
        contract["status"] = "pending_review"
        contract["pending_review_id"] = details.get("review_id")
        user_data["business_game"] = business_data
        return user_data, True, feedback
    
    # Oblicz nagrodę (dla ocen 1-5)
    reward = calculate_contract_reward(contract, rating, business_data)
    
    # Zaktualizuj finanse i statystyki
    user_data['degencoins'] = user_data.get('degencoins', 0) + reward["coins"]
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
    
    # Zapisz zaktualizowane business_data przed level up check
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
    
    return user_data, True, success_msg

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

# =============================================================================
# ZARZĄDZANIE PRACOWNIKAMI
# =============================================================================

def can_hire_employee(user_data: Dict, employee_type: str) -> Tuple[bool, str]:
    """Sprawdza czy można zatrudnić pracownika
    
    Args:
        user_data: Pełne dane użytkownika (sprawdza degencoins)
    """
    business_data = user_data["business_game"]
    emp_data = EMPLOYEE_TYPES.get(employee_type)
    if not emp_data:
        return False, "Nieznany typ pracownika"
    
    # Sprawdź poziom firmy
    if business_data["firm"]["level"] < emp_data["wymagany_poziom"]:
        return False, f"Wymagany poziom firmy: {emp_data['wymagany_poziom']}"
    
    # Sprawdź limit pracowników
    current_count = len(business_data["employees"])
    max_employees = FIRM_LEVELS[business_data["firm"]["level"]]["max_pracownikow"]
    
    if current_count >= max_employees:
        return False, f"Maksimum pracowników na tym poziomie: {max_employees}"
    
    # Sprawdź monety (teraz z user_data)
    if user_data.get('degencoins', 0) < emp_data["koszt_zatrudnienia"]:
        return False, f"Niewystarczające środki. Potrzebujesz: {emp_data['koszt_zatrudnienia']} monet"
    
    return True, ""

def hire_employee(user_data: Dict, employee_type: str) -> Tuple[Dict, bool, str]:
    """Zatrudnia pracownika
    
    Args:
        user_data: Pełne dane użytkownika (modyfikuje degencoins)
    """
    business_data = user_data["business_game"]
    can_hire, reason = can_hire_employee(user_data, employee_type)
    if not can_hire:
        return user_data, False, reason
    
    emp_data = EMPLOYEE_TYPES[employee_type]
    
    # Odejmij koszt zatrudnienia (teraz z user_data)
    user_data['degencoins'] = user_data.get('degencoins', 0) - emp_data["koszt_zatrudnienia"]
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

def fire_employee(user_data: Dict, employee_id: str) -> Tuple[Dict, bool, str]:
    """Zwalnia pracownika
    
    Args:
        user_data: Pełne dane użytkownika
    """
    business_data = user_data["business_game"]
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
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Zapisz zmiany
    user_data["business_game"] = business_data
    
    return user_data, True, f"Zwolniono: {emp_data['nazwa']}"

def calculate_daily_costs(business_data: Dict) -> float:
    """Oblicza dzienny koszt pracowników"""
    return calculate_employee_costs(business_data["employees"])

def process_daily_costs(user_data: Dict) -> Dict:
    """Przetwarza dzienne koszty (wywoływane raz dziennie)
    
    Args:
        user_data: Pełne dane użytkownika (modyfikuje degencoins)
    """
    business_data = user_data["business_game"]
    daily_cost = calculate_daily_costs(business_data)
    
    if daily_cost > 0:
        user_data['degencoins'] = user_data.get('degencoins', 0) - daily_cost
        business_data["stats"]["total_costs"] += daily_cost
        
        business_data["history"]["transactions"].append({
            "type": "daily_costs",
            "amount": -daily_cost,
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
    
    score = (
        weights["revenue"] * stats["total_revenue"] +
        weights["avg_rating"] * (stats["avg_rating"] * 1000) +
        weights["reputation"] * firm["reputation"] +
        weights["level"] * (firm["level"] * 5000) +
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

def get_firm_summary(user_data: Dict) -> Dict:
    """Zwraca podsumowanie firmy
    
    Args:
        user_data: Pełne dane użytkownika (pobiera degencoins)
    """
    business_data = user_data["business_game"]
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
