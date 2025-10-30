"""
FMCG Core Mechanics
Podstawowe mechaniki gry: wizyty, reputacja, statusy klientów, energia
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

from data.industries.fmcg_data_schema import (
    FMCGClientData,
    FMCGVisitData,
    FMCGGameState,
    create_visit_record
)
from data.repositories.business_game_repository import BusinessGameRepository


# =============================================================================
# CLIENT STATUS MANAGEMENT
# =============================================================================

def convert_prospect_to_active(client: FMCGClientData, first_order_value: int) -> FMCGClientData:
    """
    Konwertuje klienta PROSPECT → ACTIVE po pierwszej sprzedaży
    
    Args:
        client: Dane klienta w statusie PROSPECT
        first_order_value: Wartość pierwszego zamówienia (PLN)
    
    Returns:
        Zaktualizowany klient w statusie ACTIVE
    """
    if client["status"] != "PROSPECT":
        raise ValueError(f"Klient musi być PROSPECT, jest: {client['status']}")
    
    # Update status
    client["status"] = "ACTIVE"
    client["status_since"] = datetime.now().isoformat()
    
    # Initialize ACTIVE-specific fields
    client["reputation"] = 50  # Start z neutralną reputacją
    client["last_visit_date"] = datetime.now().isoformat()
    client["monthly_value"] = first_order_value
    client["total_sales"] = first_order_value
    client["orders_count"] = 1
    client["avg_order_value"] = first_order_value
    
    # Clear PROSPECT fields
    client["first_contact_date"] = None
    client["decision_deadline"] = None
    
    return client


def lose_client(client: FMCGClientData, reason: str) -> FMCGClientData:
    """
    Traci klienta ACTIVE → LOST
    
    Args:
        client: Dane klienta w statusie ACTIVE
        reason: Powód utraty ("no_visits", "competition", "price", "dissatisfaction")
    
    Returns:
        Zaktualizowany klient w statusie LOST
    """
    if client["status"] != "ACTIVE":
        raise ValueError(f"Klient musi być ACTIVE, jest: {client['status']}")
    
    # Update status
    client["status"] = "LOST"
    client["status_since"] = datetime.now().isoformat()
    client["lost_date"] = datetime.now().isoformat()
    client["lost_reason"] = reason
    client["win_back_attempts"] = 0
    
    # Calculate win-back difficulty based on reason and reputation
    reputation = client.get("reputation", 0)
    if reason == "no_visits":
        difficulty = 2  # Łatwiej odzyskać - zaniedbanie
    elif reason == "dissatisfaction" and reputation < -50:
        difficulty = 5  # Bardzo trudno - zły stosunek
    elif reason == "competition":
        difficulty = 4  # Trudno - konkurencja oferuje więcej
    elif reason == "price":
        difficulty = 3  # Średnio - problem cenowy
    else:
        difficulty = 3  # Default
    
    client["win_back_difficulty"] = difficulty
    
    return client


def win_back_client(client: FMCGClientData) -> FMCGClientData:
    """
    Próba odzyskania klienta LOST → PROSPECT
    
    Args:
        client: Dane klienta w statusie LOST
    
    Returns:
        Zaktualizowany klient (PROSPECT jeśli sukces, LOST jeśli porażka)
    """
    if client["status"] != "LOST":
        raise ValueError(f"Klient musi być LOST, jest: {client['status']}")
    
    client["win_back_attempts"] += 1
    
    # Max 2 próby
    if client["win_back_attempts"] > 2:
        raise ValueError("Przekroczono limit prób odzyskania (max 2)")
    
    # Convert back to PROSPECT (będzie musiał znowu przekonać)
    client["status"] = "PROSPECT"
    client["status_since"] = datetime.now().isoformat()
    client["interest_level"] = 20  # Niski poziom zainteresowania
    client["first_contact_date"] = datetime.now().isoformat()
    client["visits_count"] = 0
    
    # Set decision deadline (2 tygodnie)
    deadline = datetime.now() + timedelta(days=14)
    client["decision_deadline"] = deadline.isoformat()
    
    # Reset reputation to 0 (fresh start)
    client["reputation"] = 0
    
    return client


def check_client_status_changes(client: FMCGClientData) -> Optional[str]:
    """
    Sprawdza czy klient powinien zmienić status
    
    Args:
        client: Dane klienta
    
    Returns:
        Powód zmiany statusu lub None jeśli brak zmian:
        - "no_visits_timeout" - brak wizyt > 30 dni
        - "reputation_too_low" - reputacja < -50
        - "decision_deadline_passed" - PROSPECT nie zdecydował w terminie
    """
    status = client["status"]
    
    # ACTIVE → LOST checks
    if status == "ACTIVE":
        # Check last visit date
        last_visit = client.get("last_visit_date")
        if last_visit:
            last_visit_date = datetime.fromisoformat(last_visit)
            days_since_visit = (datetime.now() - last_visit_date).days
            
            if days_since_visit > 30:
                return "no_visits_timeout"
        
        # Check reputation
        reputation = client.get("reputation", 0)
        if reputation < -50:
            return "reputation_too_low"
    
    # PROSPECT → LOST checks
    elif status == "PROSPECT":
        # Check decision deadline
        deadline = client.get("decision_deadline")
        if deadline:
            deadline_date = datetime.fromisoformat(deadline)
            if datetime.now() > deadline_date and client.get("visits_count", 0) >= 3:
                # Był 3 razy, nie kupił w terminie → LOST
                return "decision_deadline_passed"
    
    return None


# =============================================================================
# REPUTATION SYSTEM
# =============================================================================

def calculate_reputation_change(
    visit_quality: int,  # 1-5 stars
    tasks_completed: int = 0,
    tasks_failed: int = 0,
    order_placed: bool = False,
    tools_used: List[str] = None
) -> int:
    """
    Oblicza zmianę reputacji po wizycie
    
    Args:
        visit_quality: Ocena wizyty 1-5⭐
        tasks_completed: Liczba wykonanych zadań
        tasks_failed: Liczba nieudanych zadań
        order_placed: Czy złożono zamówienie
        tools_used: Lista użytych narzędzi trade marketing
    
    Returns:
        Zmiana reputacji (-20 do +25)
    """
    reputation_change = 0
    
    # Base change from visit quality
    if visit_quality == 5:
        reputation_change += 10  # Świetna rozmowa
    elif visit_quality == 4:
        reputation_change += 5   # Dobra rozmowa
    elif visit_quality == 3:
        reputation_change += 2   # OK rozmowa
    elif visit_quality == 2:
        reputation_change -= 5   # Słaba rozmowa
    else:  # 1 star
        reputation_change -= 15  # Fatalna rozmowa
    
    # Bonus for regular visit (pokazanie zaangażowania)
    reputation_change += 3
    
    # Tasks impact
    reputation_change += tasks_completed * 5  # +5 za każde zadanie
    reputation_change -= tasks_failed * 3     # -3 za każde nieudane
    
    # Order placed bonus
    if order_placed:
        reputation_change += 5
    
    # Trade marketing tools bonus
    if tools_used:
        for tool in tools_used:
            if tool == "gratis":
                reputation_change += 3  # Darmowe próbki
            elif tool == "rabat":
                reputation_change += 2  # Rabat
            elif tool == "pos_material":
                reputation_change += 2  # Materiały POS
            elif tool == "promocja":
                reputation_change += 4  # Promocja
            elif tool == "free_delivery":
                reputation_change += 2  # Darmowa dostawa
    
    # Cap at reasonable limits
    return max(-20, min(25, reputation_change))


def apply_reputation_decay(client: FMCGClientData, days_since_last_visit: int) -> int:
    """
    Oblicza spadek reputacji za brak wizyt
    
    Args:
        client: Dane klienta
        days_since_last_visit: Dni od ostatniej wizyty
    
    Returns:
        Zmiana reputacji (zawsze <= 0)
    """
    if client["status"] != "ACTIVE":
        return 0
    
    visit_frequency = client.get("visit_frequency_required", 14)
    
    # Decay starts after required frequency
    if days_since_last_visit <= visit_frequency:
        return 0
    
    overdue_days = days_since_last_visit - visit_frequency
    decay = -3 * overdue_days  # -3 pkt za każdy dzień spóźnienia
    
    return max(-50, decay)  # Cap at -50


def update_client_reputation(client: FMCGClientData, reputation_change: int) -> FMCGClientData:
    """
    Aktualizuje reputację klienta
    
    Args:
        client: Dane klienta
        reputation_change: Zmiana reputacji (+/-)
    
    Returns:
        Zaktualizowany klient
    """
    if client["status"] != "ACTIVE":
        # Tylko ACTIVE clients mają reputację
        return client
    
    current_reputation = client.get("reputation", 0)
    new_reputation = current_reputation + reputation_change
    
    # Cap at -100 to +100
    new_reputation = max(-100, min(100, new_reputation))
    
    client["reputation"] = new_reputation
    
    return client


# =============================================================================
# VISIT SYSTEM
# =============================================================================

def calculate_visit_energy_cost(distance_km: float, visit_duration_minutes: int = 45) -> int:
    """
    Oblicza koszt energii dla wizyty
    
    Args:
        distance_km: Dystans do klienta (km)
        visit_duration_minutes: Czas wizyty (minuty)
    
    Returns:
        Koszt energii (%)
    """
    # Dojazd: ~0.5% energy na km (w obie strony)
    travel_cost = distance_km * 1.0  # *2 for round trip, but /2 for single direction
    
    # Wizyta: ~0.3% energy na minutę
    visit_cost = visit_duration_minutes * 0.3
    
    total_cost = int(travel_cost + visit_cost)
    
    # Min 5%, Max 40%
    return max(5, min(40, total_cost))


def calculate_travel_time(distance_km: float) -> int:
    """
    Oblicza czas dojazdu (minuty)
    
    Args:
        distance_km: Dystans (km)
    
    Returns:
        Czas w minutach (jedna strona)
    """
    # Założenie: średnia prędkość 40 km/h w mieście, 60 km/h poza
    if distance_km < 10:
        avg_speed = 40  # km/h
    else:
        avg_speed = 50  # km/h
    
    minutes = int((distance_km / avg_speed) * 60)
    return max(5, minutes)  # Min 5 minut


def execute_visit_placeholder(
    client: FMCGClientData,
    game_state: FMCGGameState,
    conversation_quality: int = 3,  # Placeholder: 1-5 stars
    order_value: int = 0,
    tasks_completed: int = 0,
    tools_used: List[str] = None
) -> Tuple[FMCGClientData, FMCGGameState, FMCGVisitData]:
    """
    Wykonuje wizytę u klienta (wersja placeholder bez AI)
    
    PLACEHOLDER: conversation_quality jest przekazywany jako parametr.
    Docelowo będzie z Gemini AI.
    
    Args:
        client: Dane klienta
        game_state: Stan gry
        conversation_quality: Ocena rozmowy 1-5⭐ (PLACEHOLDER)
        order_value: Wartość zamówienia (PLN)
        tasks_completed: Liczba wykonanych zadań
        tools_used: Lista użytych narzędzi
    
    Returns:
        (updated_client, updated_game_state, visit_record)
    """
    # Calculate visit costs
    distance = client.get("distance_from_base", 0)
    visit_duration = random.randint(30, 60)  # 30-60 min
    travel_time = calculate_travel_time(distance)
    energy_cost = calculate_visit_energy_cost(distance, visit_duration)
    
    # Check energy availability
    current_energy = game_state.get("energy", 100)
    if current_energy < energy_cost:
        raise ValueError(f"Niewystarczająca energia! Potrzeba: {energy_cost}%, dostępne: {current_energy}%")
    
    # Consume energy
    game_state["energy"] = current_energy - energy_cost
    
    # Calculate reputation change
    reputation_change = calculate_reputation_change(
        visit_quality=conversation_quality,
        tasks_completed=tasks_completed,
        order_placed=(order_value > 0),
        tools_used=tools_used or []
    )
    
    # Update client
    client["last_visit_date"] = datetime.now().isoformat()
    client["visits_count"] = client.get("visits_count", 0) + 1
    
    # Handle PROSPECT first visit
    if client["status"] == "PROSPECT" and client.get("first_contact_date") is None:
        client["first_contact_date"] = datetime.now().isoformat()
        # Set decision deadline (2 weeks)
        deadline = datetime.now() + timedelta(days=14)
        client["decision_deadline"] = deadline.isoformat()
    
    # Handle PROSPECT → ACTIVE conversion
    was_converted = False
    if client["status"] == "PROSPECT" and order_value > 0:
        client = convert_prospect_to_active(client, order_value)
        was_converted = True
    
    # Update reputation (only for ACTIVE)
    if client["status"] == "ACTIVE":
        client = update_client_reputation(client, reputation_change)
        
        # Update sales stats (but not if just converted - already done in convert_prospect_to_active)
        if not was_converted and order_value > 0:
            client["total_sales"] = client.get("total_sales", 0) + order_value
            client["orders_count"] = client.get("orders_count", 0) + 1
            client["avg_order_value"] = client["total_sales"] // client["orders_count"]
    
    # Update game state metrics
    game_state["visits_this_week"] = game_state.get("visits_this_week", 0) + 1
    game_state["monthly_sales"] = game_state.get("monthly_sales", 0) + order_value
    
    # Update client counts in game state
    if client["status"] == "ACTIVE" and client.get("orders_count", 0) == 1:
        # First order - increment active count
        game_state["clients_active"] = game_state.get("clients_active", 0) + 1
        game_state["clients_prospect"] = game_state.get("clients_prospect", 0) - 1
    
    # Create visit record
    visit_record = create_visit_record(
        client_id=client["client_id"],
        client_type=client["type"],
        visit_type="first_contact" if client.get("visits_count", 0) == 1 else "regular",
        duration=visit_duration,
        travel_time=travel_time,
        energy_cost=energy_cost,
        conversation_quality=conversation_quality,
        reputation_change=reputation_change,
        order_value=order_value,
        products_sold=[],  # TODO: implement product selection
        tools_used=tools_used or []
    )
    
    return client, game_state, visit_record


# =============================================================================
# ENERGY MANAGEMENT
# =============================================================================

def check_energy_availability(game_state: FMCGGameState, required_energy: int) -> bool:
    """
    Sprawdza czy jest wystarczająca energia
    
    Args:
        game_state: Stan gry
        required_energy: Wymagana energia (%)
    
    Returns:
        True jeśli wystarczy energii
    """
    current_energy = game_state.get("energy", 100)
    return current_energy >= required_energy


def regenerate_energy(game_state: FMCGGameState) -> FMCGGameState:
    """
    Regeneruje energię do 100% (nowy dzień)
    
    Args:
        game_state: Stan gry
    
    Returns:
        Zaktualizowany game_state
    """
    game_state["energy"] = game_state.get("energy_max", 100)
    return game_state


# =============================================================================
# DAY ADVANCEMENT
# =============================================================================

def advance_day(game_state: FMCGGameState, clients: Dict[str, FMCGClientData]) -> Tuple[FMCGGameState, Dict[str, FMCGClientData]]:
    """
    Przechodzi do następnego dnia
    
    - Regeneruje energię
    - Aplikuje reputation decay
    - Sprawdza statusy klientów
    - Resetuje licznik wizyt tygodniowych (jeśli piątek)
    
    Args:
        game_state: Stan gry
        clients: Słownik klientów
    
    Returns:
        (updated_game_state, updated_clients)
    """
    # Regenerate energy
    game_state = regenerate_energy(game_state)
    
    # Advance day counter
    current_day = game_state.get("current_day", "Monday")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    current_idx = days.index(current_day) if current_day in days else 0
    next_idx = (current_idx + 1) % len(days)
    game_state["current_day"] = days[next_idx]
    
    # Reset weekly counter on Monday
    if next_idx == 0:
        game_state["current_week"] = game_state.get("current_week", 1) + 1
        game_state["visits_this_week"] = 0
        game_state["coaching_visits_this_week"] = 0  # Reset coaching counter
    
    # Process all clients
    clients_to_lose = []
    
    for client_id, client in clients.items():
        if client["status"] == "ACTIVE":
            # Calculate reputation decay
            last_visit = client.get("last_visit_date")
            if last_visit:
                last_visit_date = datetime.fromisoformat(last_visit)
                days_since_visit = (datetime.now() - last_visit_date).days
                
                decay = apply_reputation_decay(client, days_since_visit)
                if decay < 0:
                    client = update_client_reputation(client, decay)
        
        # Check for status changes
        change_reason = check_client_status_changes(client)
        if change_reason:
            clients_to_lose.append((client_id, change_reason))
    
    # Lose clients that need to be lost
    for client_id, reason in clients_to_lose:
        clients[client_id] = lose_client(clients[client_id], reason)
        game_state["clients_active"] = game_state.get("clients_active", 0) - 1
        game_state["clients_lost"] = game_state.get("clients_lost", 0) + 1
    
    # Update last activity date
    game_state["last_activity_date"] = datetime.now().isoformat()
    
    return game_state, clients


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_client_status_summary(clients: Dict[str, FMCGClientData]) -> Dict[str, int]:
    """
    Zwraca podsumowanie statusów klientów
    
    Returns:
        {"PROSPECT": X, "ACTIVE": Y, "LOST": Z}
    """
    summary = {"PROSPECT": 0, "ACTIVE": 0, "LOST": 0}
    
    for client in clients.values():
        status = client.get("status", "PROSPECT")
        summary[status] = summary.get(status, 0) + 1
    
    return summary


def get_clients_needing_visit(clients: Dict[str, FMCGClientData], urgent_threshold_days: int = 10) -> List[str]:
    """
    Zwraca listę ID klientów wymagających pilnej wizyty
    
    Args:
        clients: Słownik klientów
        urgent_threshold_days: Próg pilności (dni)
    
    Returns:
        Lista client_id
    """
    urgent = []
    
    for client_id, client in clients.items():
        if client["status"] == "ACTIVE":
            last_visit = client.get("last_visit_date")
            if last_visit:
                last_visit_date = datetime.fromisoformat(last_visit)
                days_since = (datetime.now() - last_visit_date).days
                visit_freq = client.get("visit_frequency_required", 14)
                
                if days_since >= visit_freq - urgent_threshold_days:
                    urgent.append(client_id)
    
    return urgent


# =============================================================================
# SQL INTEGRATION
# =============================================================================

def save_fmcg_visit_to_sql(
    username: str,
    visit_record: FMCGVisitData,
    game_state: FMCGGameState
) -> bool:
    """
    Zapisuje wizytę FMCG do SQL jako BusinessGameContract
    
    Args:
        username: Nazwa użytkownika
        visit_record: Dane wizyty
        game_state: Aktualny stan gry (potrzebny do game_id)
    
    Returns:
        True jeśli sukces
    """
    try:
        repo = BusinessGameRepository()
        
        # Ensure SQL is available
        if not repo._ensure_sql_initialized():
            print("⚠️  SQL not available, visit not saved")
            return False
        
        with repo.session_scope() as session:
            # Find active FMCG game for user
            user = session.query(repo.User).filter_by(username=username).first()
            if not user:
                print(f"❌ User {username} not found in SQL")
                return False
            
            # Find FMCG game
            game = session.query(repo.BusinessGame).filter_by(
                user_id=user.id,
                scenario_type="fmcg",
                status="in_progress"
            ).first()
            
            if not game:
                print(f"❌ Active FMCG game not found for {username}")
                return False
            
            # Create contract record for visit
            visit_date = datetime.fromisoformat(visit_record['visit_date'])
            visit_id = f"{visit_record['client_id']}_{visit_date.strftime('%Y%m%d_%H%M%S')}"
            
            contract = repo.BusinessGameContract(
                game_id=game.id,
                contract_id=f"visit_{visit_id}",
                status="completed",
                title=f"Wizyta u {visit_record['client_id']}",
                category="visit",
                client=visit_record['client_id'],
                description=f"Wizyta handlowa - {visit_record['client_type']}",
                completed_at=visit_date,
                rating=visit_record.get('conversation_quality', 3),
                extra_data={
                    "visit_type": visit_record['visit_type'],
                    "visit_duration_minutes": visit_record['visit_duration_minutes'],
                    "travel_time_minutes": visit_record['travel_time_minutes'],
                    "energy_cost": visit_record['energy_cost'],
                    "conversation_quality": visit_record['conversation_quality'],
                    "conversation_topic": visit_record.get('conversation_topic', ''),
                    "client_mood_before": visit_record.get('client_mood_before', ''),
                    "client_mood_after": visit_record.get('client_mood_after', ''),
                    "reputation_change": visit_record['reputation_change'],
                    "order_placed": visit_record.get('order_placed', False),
                    "order_value": visit_record.get('order_value', 0),
                    "products_sold": visit_record.get('products_sold', []),
                    "tools_used": visit_record.get('tools_used', []),
                    "budget_spent": visit_record.get('budget_spent', 0),
                    "tasks_completed": visit_record.get('tasks_completed', []),
                    "tasks_failed": visit_record.get('tasks_failed', [])
                }
            )
            
            session.add(contract)
            session.commit()
            
            print(f"[FMCG] Visit {visit_id} saved to SQL")
            return True
            
    except Exception as e:
        print(f"[FMCG] Error saving visit to SQL: {e}")
        return False


def update_fmcg_game_state_sql(
    username: str,
    game_state: FMCGGameState,
    clients: Dict[str, FMCGClientData]
) -> bool:
    """
    Aktualizuje stan gry FMCG w SQL
    
    Args:
        username: Nazwa użytkownika
        game_state: Stan gry do zapisania
        clients: Słownik klientów do zapisania
    
    Returns:
        True jeśli sukces
    """
    try:
        repo = BusinessGameRepository()
        
        # Merge clients back into game_state
        game_state["clients"] = clients
        
        # Prepare full game data matching initialize_fmcg_game_new structure
        from datetime import datetime
        
        full_game_data = {
            # Metadata
            "scenario_id": "fmcg_piaseczno_v1",
            "scenario_modifiers": {},
            "scenario_objectives": [
                {"id": "first_sale", "description": "Zrealizuj pierwszą sprzedaż", "completed": game_state.get("first_sale", False)},
                {"id": "first_active", "description": "Przekształć PROSPECT w ACTIVE", "completed": game_state.get("first_active_client", False)},
                {"id": "5_clients", "description": "Miej 5 aktywnych klientów", "completed": game_state.get("five_active_clients", False)}
            ],
            "objectives_completed": [],
            
            # Career/Firm info
            "firm": {
                "name": "FMCG Corp",
                "logo": "🏪",
                "founded": datetime.now().strftime("%Y-%m-%d"),
                "level": game_state.get("level", 1),
                "reputation": 0
            },
            
            # FMCG-specific state w extra_data (główne dane gry)
            "fmcg_state": game_state,
            
            # Office
            "office": {
                "type": "company_office",
                "upgraded_at": None
            },
            
            # Empty collections
            "employees": [],
            "contracts": {
                "active": [],
                "completed": [],
                "failed": [],
                "available_pool": []
            },
            
            # Stats
            "stats": {
                "total_sales": game_state.get("monthly_sales", 0),
                "clients_acquired": game_state.get("clients_active", 0),
                "clients_lost": game_state.get("clients_lost", 0),
                "visits_completed": game_state.get("visits_this_week", 0),
                "avg_conversation_rating": 0.0,
                "total_reputation_gained": 0
            },
            
            # Ranking
            "ranking": {
                "overall_score": 0.0,
                "current_positions": {
                    "overall": None,
                    "sales": None,
                    "reputation": None
                },
                "previous_positions": {},
                "badges": []
            },
            
            # Events
            "events": {
                "history": [],
                "last_roll": None
            },
            
            # Money
            "money": 0,
            "initial_money": 0,
            
            # History
            "history": {
                "transactions": [],
                "milestones": []
            }
        }
        
        # Use existing repository save method (SQL)
        success = repo.save(username, "fmcg", full_game_data)
        
        if success:
            print(f"[FMCG] Game state updated in SQL for {username}")
        else:
            print(f"[FMCG] Failed to update FMCG game state in SQL (user may not exist)")
        
        # ALWAYS save to JSON as well (fallback for users without SQL)
        try:
            import json
            import os
            
            users_file = "users_data.json"
            if os.path.exists(users_file):
                with open(users_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                
                if username in users_data:
                    users_data[username]["fmcg_game_state"] = game_state
                    users_data[username]["fmcg_clients"] = clients
                    
                    with open(users_file, 'w', encoding='utf-8') as f:
                        json.dump(users_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"[FMCG] Game state saved to JSON for {username}")
                    return True
        except Exception as json_error:
            print(f"[FMCG] Failed to save to JSON: {json_error}")
        
        return success
        
    except Exception as e:
        print(f"[FMCG] Error updating FMCG game state: {e}")
        import traceback
        traceback.print_exc()
        return False


def load_fmcg_game_state_sql(username: str) -> Optional[Tuple[FMCGGameState, Dict[str, FMCGClientData]]]:
    """
    Wczytuje stan gry FMCG z JSON lub SQL
    
    Args:
        username: Nazwa użytkownika
    
    Returns:
        Tuple (game_state, clients) lub None jeśli brak gry
    """
    try:
        # Try loading from JSON first (primary storage)
        import json
        import os
        
        users_file = "users_data.json"
        
        if os.path.exists(users_file):
            with open(users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            if username in users_data:
                game_state = users_data[username].get("fmcg_game_state")
                clients = users_data[username].get("fmcg_clients")
                
                if game_state and clients:
                    return (game_state, clients)
        
        # Fallback to SQL/repository
        repo = BusinessGameRepository()
        game_data = repo.get(username, "fmcg")
        
        if not game_data:
            print(f"[FMCG] No FMCG game found for {username}")
            return None
        
        # Extract state and clients
        game_state = game_data.get("fmcg_state")
        clients = game_data.get("clients", {})
        
        if not game_state:
            print(f"[FMCG] FMCG game data missing fmcg_state for {username}")
            return None
        
        print(f"[FMCG] Game state loaded from SQL for {username}")
        return (game_state, clients)
        
    except Exception as e:
        print(f"[FMCG] Error loading FMCG game state: {e}")
        return None


def get_client_conversation_history(
    username: str,
    client_id: str,
    limit: int = 5
) -> List[Dict]:
    """
    Pobiera historię rozmów z danym klientem z JSON game_state
    
    Args:
        username: Nazwa użytkownika
        client_id: ID klienta
        limit: Ile ostatnich wizyt pobrać (default: 5)
    
    Returns:
        Lista wizyt z podsumowaniami rozmów, od najnowszej
    """
    try:
        # Load game state from JSON
        game_tuple = load_fmcg_game_state_sql(username)
        
        if not game_tuple:
            return []
        
        game_state, clients = game_tuple
        
        # Get visit history from game_state
        visit_history = game_state.get("visit_history", [])
        
        # Filter by client_id and limit
        client_visits = [
            visit for visit in visit_history
            if visit.get("client_id") == client_id
        ]
        
        # Sort by date (newest first) and limit
        client_visits.sort(key=lambda x: x.get("date", ""), reverse=True)
        return client_visits[:limit]
            
    except Exception as e:
        print(f"Error loading conversation history: {e}")
        return []
