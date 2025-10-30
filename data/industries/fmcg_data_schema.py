"""
FMCG Data Schema for SQL Storage
Defines data structures for FMCG game stored in BusinessGame.extra_data and BusinessGameContract.extra_data
"""

from typing import TypedDict, List, Optional
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
    size_sqm: int
    employees_count: int
    
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
    
    # Visit history (for conversation memory)
    visit_history: Optional[List[dict]]  # [{client_id, date, summary, key_points, quality, order_value}]
    
    # Achievements
    first_sale: bool
    first_active_client: bool
    five_active_clients: bool
    reputation_100: bool  # Reputation +100 with any client
    
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
        "client_mood_before": "neutral",
        "client_mood_after": "friendly",
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
    lat: float = 52.0846,
    lon: float = 21.0250
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
        "visit_history": [],  # Historia wizyt dla AI memory
        "first_sale": False,
        "first_active_client": False,
        "five_active_clients": False,
        "reputation_100": False,
        "last_activity_date": datetime.now().isoformat(),
        "last_visit_client_id": None
    }
