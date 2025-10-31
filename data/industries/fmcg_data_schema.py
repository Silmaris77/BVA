"""
FMCG Data Schema for SQL Storage
Defines data structures for FMCG game stored in BusinessGame.extra_data and BusinessGameContract.extra_data
"""

from typing import TypedDict, List, Optional, Dict
from datetime import datetime

# =============================================================================
# CLIENT DATA SCHEMA (stored in BusinessGame or separate table)
# =============================================================================

class FMCGClientData(TypedDict):
    """
    Struktura danych klienta FMCG
    Przechowywane w BusinessGame.extra_data["clients"][client_id]
    """
    # Basic Info
    client_id: str  # np. "trad_001"
    name: str
    type: str  # "Sklep osiedlowy", "Dyskont", "Sieć lokalna"
    segment: str  # "traditional_trade", "modern_trade", "convenience"
    
    # Location
    location: str  # "Warszawa, Ursynów, Os. Kabaty"
    latitude: float
    longitude: float
    distance_from_base: float  # km
    
    # Status & Lifecycle
    status: str  # "PROSPECT", "ACTIVE", "LOST"
    status_since: str  # datetime ISO format
    
    # PROSPECT specific
    interest_level: int  # 0-100%
    first_contact_date: Optional[str]
    visits_count: int
    decision_deadline: Optional[str]
    
    # ACTIVE specific
    reputation: int  # -100 to +100
    last_visit_date: Optional[str]
    visit_frequency_required: int  # days (7/14/30)
    products_portfolio: List[str]  # ["PRODUCT_001", "PRODUCT_002"]
    monthly_value: int  # PLN
    market_share_vs_competition: int  # %
    satisfaction_score: int  # 1-5
    contract_renewal_date: Optional[str]
    
    # LOST specific
    lost_date: Optional[str]
    lost_reason: Optional[str]  # "no_visits", "competition", "price", "dissatisfaction"
    win_back_attempts: int
    win_back_difficulty: int  # 1-5
    
    # Client Profile (basic - always visible)
    owner_name: str
    personality_style: str  # "Tradycyjny", "Nowoczesny"
    priorities: List[str]  # ["Marża", "Rotacja towaru", "Wsparcie"]
    potential_monthly: int  # PLN potencjalna miesięczna wartość
    size_sqm: int
    employees_count: int
    
    # Sales Capacity (realistyczne limity zamówień)
    sales_capacity: Optional[Dict]  # Parametry sprzedaży dla kategorii (generowane automatycznie)
    
    # Client Discovery System (odkrywane stopniowo)
    knowledge_level: int  # 0-5 stars (obliczane na podstawie % odkrytych pól)
    discovered_info: 'FMCGClientDiscoveredInfo'  # Dane odkrywane podczas wizyt
    discovery_notes: List['FMCGClientNote']  # Historia notatek z wizyt
    
    # Sales History
    total_sales: int  # PLN all-time
    avg_order_value: int  # PLN
    orders_count: int


class FMCGClientDiscoveredInfo(TypedDict):
    """
    Informacje o kliencie odkrywane podczas wizyt.
    Każde pole może być None (nieodkryte) lub zawierać wartość (odkryte).
    """
    # Personality & Decision Making
    personality_description: Optional[str]  # "Konserwatywny, niechętny zmianom, liczy każdą złotówkę"
    decision_priorities: Optional[List[str]]  # ["Cena", "Jakość", "Wsparcie"] w kolejności ważności
    
    # Customer Base
    main_customers: Optional[str]  # "Seniorzy z osiedla (60+ lat)"
    customer_demographics: Optional[str]  # "Rodziny z dziećmi, młodzi profesjonaliści"
    
    # Competition
    competing_brands: Optional[List[str]]  # ["Dove", "Fa", "Danone", "Bakoma"]
    shelf_space_constraints: Optional[str]  # "Ograniczona półka, preferuje wolno rotujące"
    
    # Business Needs
    pain_points: Optional[List[str]]  # ["Wysokie ceny od hurtowni", "Brak wsparcia marketingowego"]
    business_goals: Optional[List[str]]  # ["Zwiększyć marżę", "Zmniejszyć koszty dostaw"]
    
    # Ordering Patterns
    typical_order_value: Optional[str]  # "300-500 zł"
    preferred_frequency: Optional[str]  # "Co 2 tygodnie"
    payment_terms: Optional[str]  # "Gotówka przy dostawie", "Przelew 14 dni"
    delivery_preferences: Optional[str]  # "Poniedziałki rano", "Małe dostawy częściej"
    
    # Store specifics
    best_selling_categories: Optional[List[str]]  # ["Napoje", "Słodycze", "Chemia"]
    seasonal_patterns: Optional[str]  # "Latem napoje +50%, zimą słodycze"
    
    # Relationship
    trust_level: Optional[str]  # "Sceptyczny", "Otwarty", "Zaufany partner"
    preferred_communication: Optional[str]  # "Krótkie, konkretne rozmowy", "Lubi long talk"
    
    # Sales Capacity Discovery (odkrywane stopniowo - wymaga ~4 wizyt)
    sales_capacity_discovered: Optional[Dict[str, Dict]]
    # {
    #   "Personal Care": {
    #     "weekly_sales_volume": 150,
    #     "shelf_space_facings": 12,
    #     "storage_capacity": 300,
    #     "rotation_days": 14,
    #     "max_order_per_sku": 24,
    #     "avg_products_in_category": 20,
    #     "discovered_date": "2025-10-30T10:00:00",
    #     "discovered_method": "conversation",  # "conversation", "observation", "mentor"
    #     "reputation_at_discovery": 35  # Reputacja gdy odkryto
    #   }
    # }
    
    # Market Share per kategoria (obliczane automatycznie)
    market_share_by_category: Optional[Dict[str, Dict]]
    # {
    #   "Personal Care": {
    #     "player_share": 35,  # % - ile z total_volume to produkty gracza
    #     "competitor_share": 65,
    #     "player_volume_weekly": 53,  # sztuk tygodniowo
    #     "total_volume_weekly": 150,
    #     "trend": "growing",  # "growing", "declining", "stable"
    #     "trend_percentage": 15,  # +15% vs miesiąc temu
    #     "last_updated": "2025-10-30T10:00:00",
    #     "history": [  # Ostatnie 6 miesięcy dla wykresu
    #       {"month": "2025-05", "player_share": 0, "player_volume": 0},
    #       {"month": "2025-06", "player_share": 20, "player_volume": 30},
    #       {"month": "2025-07", "player_share": 30, "player_volume": 45},
    #       {"month": "2025-08", "player_share": 35, "player_volume": 53}
    #     ]
    #   }
    # }


class FMCGClientNote(TypedDict):
    """
    Pojedyncza notatka/odkrycie z wizyty
    """
    visit_date: str  # datetime ISO
    note_text: str  # "Klient wspomniał, że jego seniorzy szukają tanich produktów"
    discovered_fields: List[str]  # ["main_customers", "decision_priorities"]
    context: str  # Fragment rozmowy gdzie to odkryto


# =============================================================================
# VISIT/CONTRACT DATA SCHEMA (BusinessGameContract.extra_data)
# =============================================================================

class FMCGVisitData(TypedDict):
    """
    Dodatkowe dane wizyty/kontraktu FMCG
    Przechowywane w BusinessGameContract.extra_data
    """
    # Client reference
    client_id: str
    client_type: str
    client_status: str  # at time of visit
    
    # Visit details
    visit_type: str  # "first_contact", "regular", "emergency", "win_back"
    visit_date: str  # datetime ISO format
    visit_duration_minutes: int
    travel_time_minutes: int
    energy_cost: int  # % energy consumed
    
    # Conversation outcome
    conversation_quality: int  # 1-5 stars from AI
    conversation_topic: str  # "product_presentation", "order", "relationship", "problem_solving"
    conversation_summary: Optional[str]  # AI-generated summary of conversation
    conversation_transcript: Optional[str]  # Full conversation text for AI analysis
    key_points: Optional[List[str]]  # Kluczowe ustalenia, obietnice
    client_mood_before: str  # "friendly", "neutral", "hostile"
    client_mood_after: str
    
    # Client Discovery (AI extracted from conversation)
    ai_discovered_info: Optional['FMCGClientDiscoveredInfo']  # Nowe informacje odkryte w tej wizycie
    knowledge_level_before: int  # 0-5 stars przed wizytą
    knowledge_level_after: int  # 0-5 stars po wizycie
    new_discoveries_count: int  # Ile pól odkryto w tej wizycie
    
    # Business outcome
    order_placed: bool
    order_value: int  # PLN
    products_sold: List[str]
    reputation_change: int  # +/- points
    
    # Tools used
    tools_used: List[str]  # ["gratis", "rabat", "pos_material"]
    budget_spent: int  # PLN
    
    # Tasks completed during visit
    tasks_completed: List[str]  # task IDs
    tasks_failed: List[str]


# =============================================================================
# GAME STATE SCHEMA (BusinessGame.extra_data)
# =============================================================================

class FMCGGameState(TypedDict):
    """
    Stan gry FMCG
    Przechowywane w BusinessGame.extra_data
    """
    # Career
    level: int  # 1-10
    role: str  # "Junior Sales Representative"
    experience_points: int
    
    # Territory
    territory_name: str  # "Piaseczno"
    territory_latitude: float
    territory_longitude: float
    
    # Resources
    energy: int  # 0-100%
    energy_max: int  # 100
    marketing_budget: int  # PLN per month
    marketing_budget_used: int  # PLN this month
    
    # Clients overview
    clients_prospect: int
    clients_active: int
    clients_lost: int
    
    # Performance metrics
    monthly_sales: int  # PLN current month
    market_share: int  # %
    customer_satisfaction_avg: int  # 1-100
    
    # Calendar
    current_week: int
    current_day: str  # "Monday", "Tuesday", etc.
    visits_this_week: int
    visits_scheduled: List[dict]  # [{client_id, date, time}]
    
    # Route planning & tracking
    current_location: Optional[Dict]  # {"lat": ..., "lng": ...} lub None = "base"
    planned_visits_today: Optional[List[str]]  # Lista client_id w kolejności wizyt
    completed_visits_today: Optional[List[Dict]]  # [{client_id, lat, lng, distance_from_prev}]
    total_distance_today: float  # Suma km przejechanych dzisiaj
    route_optimization_used: bool  # Czy gracz użył optymalizacji trasy
    
    # Visit history (for conversation memory)
    visit_history: Optional[List[dict]]  # [{client_id, date, summary, key_points, quality, order_value}]
    
    # ALEX AI Sales Assistant & Autopilot
    alex_level: int  # 0-4 (0=Trainee, 1=Junior, 2=Mid, 3=Senior, 4=Master)
    alex_training_points: int  # Punkty z quizów/case'ów
    alex_competencies: Dict[str, float]  # {"planning": 0.6, "communication": 0.6, ...} - % ukończenia modułu
    alex_quiz_scores: Dict[str, int]  # {"quiz_001": 85, ...} - wyniki quizów
    alex_case_completions: List[str]  # ["case_001", "case_002"] - ukończone case studies
    autopilot_visits_count: int  # Liczba wizyt wykonanych przez autopilota (total)
    autopilot_visits_this_week: int  # Liczba wizyt autopilota w tym tygodniu
    autopilot_efficiency_avg: float  # Średnia efektywność autopilota (% względem manualnego)
    
    # Achievements
    first_sale: bool
    first_active_client: bool
    five_active_clients: bool
    reputation_100: bool  # Reputation +100 with any client
    
    # Progression System - Weekly/Monthly Targets
    weekly_target_sales: int  # Target sprzedaży na tydzień (PLN)
    weekly_actual_sales: int  # Aktualna sprzedaż w tym tygodniu (PLN)
    weekly_target_visits: int  # Target wizyt na tydzień
    weekly_best_sales: int  # Najlepszy wynik tygodniowy (rekord)
    weekly_streak: int  # Ile tygodni z rzędu osiągnięto cel
    monthly_target_sales: int  # Target sprzedaży na miesiąc (PLN)
    monthly_actual_sales: int  # Aktualna sprzedaż w tym miesiącu (PLN)
    monthly_best_sales: int  # Najlepszy wynik miesięczny (rekord)
    weekly_history: List[Dict]  # [{week: 1, sales: 12000, visits: 8, target_achieved: True}]
    
    # Last activity
    last_activity_date: str
    last_visit_client_id: Optional[str]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_new_client(
    client_id: str,
    name: str,
    client_type: str,
    segment: str,
    location: str,
    lat: float,
    lon: float,
    distance: float,
    owner_name: str,
    potential: int,
    size_sqm: int = 80,
    employees: int = 2
) -> FMCGClientData:
    """Tworzy nowego klienta w statusie PROSPECT"""
    # Import sales_capacity generator
    from utils.fmcg_order_realism import generate_sales_capacity
    
    return {
        "client_id": client_id,
        "name": name,
        "type": client_type,
        "segment": segment,
        "location": location,
        "latitude": lat,
        "longitude": lon,
        "distance_from_base": distance,
        "status": "PROSPECT",
        "status_since": datetime.now().isoformat(),
        "interest_level": 30,  # Starting interest
        "first_contact_date": None,
        "visits_count": 0,
        "decision_deadline": None,
        "reputation": 0,
        "last_visit_date": None,
        "visit_frequency_required": 14,
        "products_portfolio": [],
        "monthly_value": 0,
        "market_share_vs_competition": 0,
        "satisfaction_score": 3,
        "contract_renewal_date": None,
        "lost_date": None,
        "lost_reason": None,
        "win_back_attempts": 0,
        "win_back_difficulty": 1,
        "owner_name": owner_name,
        "personality_style": "Tradycyjny",
        "priorities": ["Marża", "Rotacja towaru", "Wsparcie"],
        "potential_monthly": potential,
        "size_sqm": size_sqm,
        "employees_count": employees,
        "sales_capacity": generate_sales_capacity(size_sqm, client_type),  # AUTO-GENERATE
        "knowledge_level": 0,  # Brak odkryć na start
        "discovered_info": {
            # Personality & Decision Making
            "personality_description": None,
            "decision_priorities": None,
            # Customer Base
            "main_customers": None,
            "customer_demographics": None,
            # Competition
            "competing_brands": None,
            "shelf_space_constraints": None,
            # Business Needs
            "pain_points": None,
            "business_goals": None,
            # Ordering Patterns
            "typical_order_value": None,
            "preferred_frequency": None,
            "payment_terms": None,
            "delivery_preferences": None,
            # Store specifics
            "best_selling_categories": None,
            "seasonal_patterns": None,
            # Relationship
            "trust_level": None,
            "preferred_communication": None,
            # Sales Capacity Discovery (puste na start - odkrywane stopniowo)
            "sales_capacity_discovered": {},
            # Market Share (wszystkie kategorie na 0%)
            "market_share_by_category": {
                "Personal Care": {
                    "player_share": 0,
                    "competitor_share": 100,
                    "player_volume_weekly": 0,
                    "total_volume_weekly": 0,  # Nieznane dopóki nie odkryte
                    "trend": "stable",
                    "trend_percentage": 0,
                    "last_updated": datetime.now().isoformat(),
                    "history": [{"month": datetime.now().strftime("%Y-%m"), "player_share": 0, "player_volume": 0}]
                },
                "Food": {
                    "player_share": 0,
                    "competitor_share": 100,
                    "player_volume_weekly": 0,
                    "total_volume_weekly": 0,
                    "trend": "stable",
                    "trend_percentage": 0,
                    "last_updated": datetime.now().isoformat(),
                    "history": [{"month": datetime.now().strftime("%Y-%m"), "player_share": 0, "player_volume": 0}]
                },
                "Home Care": {
                    "player_share": 0,
                    "competitor_share": 100,
                    "player_volume_weekly": 0,
                    "total_volume_weekly": 0,
                    "trend": "stable",
                    "trend_percentage": 0,
                    "last_updated": datetime.now().isoformat(),
                    "history": [{"month": datetime.now().strftime("%Y-%m"), "player_share": 0, "player_volume": 0}]
                },
                "Snacks": {
                    "player_share": 0,
                    "competitor_share": 100,
                    "player_volume_weekly": 0,
                    "total_volume_weekly": 0,
                    "trend": "stable",
                    "trend_percentage": 0,
                    "last_updated": datetime.now().isoformat(),
                    "history": [{"month": datetime.now().strftime("%Y-%m"), "player_share": 0, "player_volume": 0}]
                },
                "Beverages": {
                    "player_share": 0,
                    "competitor_share": 100,
                    "player_volume_weekly": 0,
                    "total_volume_weekly": 0,
                    "trend": "stable",
                    "trend_percentage": 0,
                    "last_updated": datetime.now().isoformat(),
                    "history": [{"month": datetime.now().strftime("%Y-%m"), "player_share": 0, "player_volume": 0}]
                }
            }
        },
        "discovery_notes": [],  # Historia notatek z wizyt
        "total_sales": 0,
        "avg_order_value": 0,
        "orders_count": 0
    }


def create_visit_record(
    client_id: str,
    client_type: str,
    visit_type: str,
    duration: int,
    travel_time: int,
    energy_cost: int,
    conversation_quality: int,
    reputation_change: int,
    order_value: int = 0,
    products_sold: Optional[List[str]] = None,
    tools_used: Optional[List[str]] = None
) -> FMCGVisitData:
    """Tworzy rekord wizyty u klienta"""
    return {
        "client_id": client_id,
        "client_type": client_type,
        "client_status": "ACTIVE",  # Updated at visit time
        "visit_type": visit_type,
        "visit_date": datetime.now().isoformat(),
        "visit_duration_minutes": duration,
        "travel_time_minutes": travel_time,
        "energy_cost": energy_cost,
        "conversation_quality": conversation_quality,
        "conversation_topic": "regular_visit",
        "conversation_summary": None,
        "conversation_transcript": None,
        "key_points": None,
        "client_mood_before": "neutral",
        "client_mood_after": "friendly",
        "ai_discovered_info": None,
        "knowledge_level_before": 0,
        "knowledge_level_after": 0,
        "new_discoveries_count": 0,
        "order_placed": order_value > 0,
        "order_value": order_value,
        "products_sold": products_sold or [],
        "reputation_change": reputation_change,
        "tools_used": tools_used or [],
        "budget_spent": 0,
        "tasks_completed": [],
        "tasks_failed": []
    }


def initialize_fmcg_game_state(
    territory: str = "Piaseczno",
    lat: float = 52.0748,  # Centrum Piaseczna (Rynek Piasecki)
    lon: float = 21.0274
) -> FMCGGameState:
    """Inicjalizuje nowy stan gry FMCG"""
    return {
        "level": 1,
        "role": "Junior Sales Representative",
        "experience_points": 0,
        "territory_name": territory,
        "territory_latitude": lat,
        "territory_longitude": lon,
        "energy": 100,
        "energy_max": 100,
        "marketing_budget": 2000,
        "marketing_budget_used": 0,
        "clients_prospect": 5,
        "clients_active": 0,
        "clients_lost": 0,
        "monthly_sales": 0,
        "market_share": 0,
        "customer_satisfaction_avg": 0,
        "current_week": 1,
        "current_day": "Monday",
        "visits_this_week": 0,
        "visits_scheduled": [],
        "current_location": None,  # None = baza
        "planned_visits_today": [],
        "completed_visits_today": [],
        "total_distance_today": 0.0,
        "route_optimization_used": False,
        "visit_history": [],  # Historia wizyt dla AI memory
        "alex_level": 0,  # 0 = Trainee (początek)
        "alex_training_points": 0,
        "alex_competencies": {
            "planning": 0.0,
            "communication": 0.0,
            "analysis": 0.0,
            "relationship": 0.0,
            "negotiation": 0.0
        },
        "alex_quiz_scores": {},
        "alex_case_completions": [],
        "autopilot_visits_count": 0,
        "autopilot_visits_this_week": 0,
        "autopilot_efficiency_avg": 0.0,
        "first_sale": False,
        "first_active_client": False,
        "five_active_clients": False,
        "reputation_100": False,
        
        # Progression targets (Level 1 defaults)
        "weekly_target_sales": 8000,  # Level 1: 8k PLN/tydzień
        "weekly_actual_sales": 0,
        "weekly_target_visits": 6,  # Level 1: 6 wizyt/tydzień
        "weekly_best_sales": 0,
        "weekly_streak": 0,
        "monthly_target_sales": 35000,  # Level 1: 35k PLN/miesiąc
        "monthly_actual_sales": 0,
        "monthly_best_sales": 0,
        "weekly_history": [],
        
        "last_activity_date": datetime.now().isoformat(),
        "last_visit_client_id": None
    }
