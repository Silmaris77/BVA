"""
ALEX AI Sales Assistant Training System
Autopilot & Training Mechanics for FMCG Game
"""

from typing import Dict, List, Tuple, Optional
import random

# =============================================================================
# ALEX LEVEL SYSTEM
# =============================================================================

ALEX_LEVELS = {
    0: {
        "name": "Trainee",
        "name_pl": "Stażysta",
        "competence": 0.60,  # 60% efektywności względem gracza
        "penalty": -40,  # -40% penalty na wyniki
        "visits_per_day": 2,
        "required_points": 0,
        "emoji": "🎓"
    },
    1: {
        "name": "Junior",
        "name_pl": "Junior",
        "competence": 0.70,
        "penalty": -30,
        "visits_per_day": 3,
        "required_points": 100,
        "emoji": "📚"
    },
    2: {
        "name": "Mid",
        "name_pl": "Mid",
        "competence": 0.80,
        "penalty": -20,
        "visits_per_day": 4,
        "required_points": 300,
        "emoji": "💼"
    },
    3: {
        "name": "Senior",
        "name_pl": "Senior",
        "competence": 0.90,
        "penalty": -10,
        "visits_per_day": 5,
        "required_points": 600,
        "emoji": "⭐"
    },
    4: {
        "name": "Master",
        "name_pl": "Master",
        "competence": 0.95,
        "penalty": -5,
        "visits_per_day": 6,
        "required_points": 1000,
        "emoji": "🏆"
    }
}

# =============================================================================
# TRAINING MODULES
# =============================================================================

TRAINING_MODULES = {
    "planning": {
        "name_pl": "🎯 Planowanie & Organizacja",
        "description": "Routing, segmentacja ABC, zarządzanie czasem i terytorium",
        "skills": ["routing", "time_management", "abc_segmentation", "territory_planning"],
        "impact": "Lepsza efektywność tras i wizyt"
    },
    "communication": {
        "name_pl": "🗣️ Komunikacja & Prezentacja",
        "description": "Elevator pitch, prezentacja produktów, storytelling",
        "skills": ["elevator_pitch", "product_presentation", "storytelling", "listening"],
        "impact": "Wyższy interest level i zaangażowanie klienta"
    },
    "analysis": {
        "name_pl": "📊 Analiza & Insight",
        "description": "Analiza potrzeb, rozpoznawanie sygnałów zakupowych, data-driven selling",
        "skills": ["needs_analysis", "buying_signals", "data_interpretation", "market_analysis"],
        "impact": "Lepsze dopasowanie oferty do potrzeb"
    },
    "relationship": {
        "name_pl": "🤝 Budowanie relacji",
        "description": "Trust building, customer discovery, long-term relationship management",
        "skills": ["trust_building", "discovery", "empathy", "relationship_maintenance"],
        "impact": "Wyższa reputacja i lojalność klientów"
    },
    "negotiation": {
        "name_pl": "💼 Negocjacje & Zamykanie",
        "description": "Objection handling, closing techniques, value selling",
        "skills": ["objection_handling", "closing", "value_selling", "deal_structuring"],
        "impact": "Wyższe order values i success rate"
    }
}

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def calculate_alex_level(training_points: int) -> int:
    """
    Oblicza poziom ALEX na podstawie training points
    
    Args:
        training_points: Liczba punktów treningowych
        
    Returns:
        int: Poziom ALEX (0-4)
    """
    for level in range(4, -1, -1):
        if training_points >= ALEX_LEVELS[level]["required_points"]:
            return level
    return 0


def get_alex_stats(alex_level: int) -> Dict:
    """
    Pobiera statystyki ALEX dla danego poziomu
    
    Args:
        alex_level: Poziom ALEX (0-4)
        
    Returns:
        Dict: Słownik z statystykami
    """
    return ALEX_LEVELS.get(alex_level, ALEX_LEVELS[0])


def get_autopilot_penalty(alex_level: int, competencies: Dict[str, float]) -> float:
    """
    Oblicza penalty autopilota na podstawie poziomu ALEX i kompetencji
    
    Args:
        alex_level: Poziom ALEX (0-4)
        competencies: Dict z % ukończenia każdego modułu
        
    Returns:
        float: Penalty jako liczba ujemna (np. -40 dla Trainee, -5 dla Master)
    """
    base_penalty = ALEX_LEVELS[alex_level]["penalty"]
    
    # Bonus za ukończone moduły (max -10% dodatkowej redukcji penalty)
    avg_completion = sum(competencies.values()) / len(competencies) if competencies else 0
    competency_bonus = avg_completion * 10  # 0-10% redukcji
    
    # Im wyższy bonus, tym mniejszy (mniej negatywny) penalty
    adjusted_penalty = base_penalty + competency_bonus
    
    return adjusted_penalty


def get_autopilot_capacity(
    alex_level: int,
    total_visits_this_week: int
) -> Dict[str, any]:
    """
    Sprawdza ile wizyt autopilota jest jeszcze dostępnych
    
    Args:
        alex_level: Poziom ALEX (0-4)
        total_visits_this_week: Całkowita liczba wizyt w tym tygodniu
        
    Returns:
        Dict: {
            "max_autopilot_per_day": int,
            "max_autopilot_per_week": int,
            "can_use_autopilot": bool,
            "reason": str
        }
    """
    max_per_day = ALEX_LEVELS[alex_level]["visits_per_day"]
    
    # Limit tygodniowy: max 50% wszystkich wizyt może być autopilot
    max_per_week = max(1, int(total_visits_this_week * 0.5))
    
    return {
        "max_autopilot_per_day": max_per_day,
        "max_autopilot_per_week": max_per_week,
        "can_use_autopilot": True,
        "reason": f"Dostępne: {max_per_day}/dzień, max {max_per_week}/tydzień (50% wizyt)"
    }


def simulate_autopilot_visit(
    client_data: Dict,
    player_stats: Dict,
    alex_level: int,
    competencies: Dict[str, float]
) -> Dict:
    """
    Symuluje wizytę wykonaną przez autopilota (bez rozmowy AI)
    
    Args:
        client_data: Dane klienta (FMCGClientData)
        player_stats: Statystyki gracza (poziom, umiejętności)
        alex_level: Poziom ALEX (0-4)
        competencies: Kompetencje ALEX
        
    Returns:
        Dict: {
            "order_value": int,
            "reputation_change": int,
            "visit_quality": int (1-5),
            "time_saved": int (minuty),
            "penalty_applied": float,
            "summary": str
        }
    """
    # Oblicz penalty
    penalty = get_autopilot_penalty(alex_level, competencies)
    penalty_multiplier = 1 + (penalty / 100)  # np. 1 + (-40/100) = 0.6
    
    # Bazowe wartości (co gracz mógłby osiągnąć)
    base_order = client_data.get("potential_monthly", 1000) / 4  # 1/4 miesięcznego potencjału
    base_reputation = 5  # Standardowa wizyta +5
    
    # Zastosuj penalty
    autopilot_order = int(base_order * penalty_multiplier)
    autopilot_reputation = max(1, int(base_reputation * penalty_multiplier))
    
    # Jakość wizyty (zależy od poziomu ALEX)
    competence = ALEX_LEVELS[alex_level]["competence"]
    visit_quality = int(competence * 5)  # 0.6 * 5 = 3, 0.95 * 5 = 4.75
    
    # Oszczędność czasu (autopilot zawsze 30 min vs ~45-60 min manualnie)
    time_saved = random.randint(15, 30)
    
    # Generuj podsumowanie
    level_name = ALEX_LEVELS[alex_level]["name_pl"]
    summary = f"""
    🤖 **ALEX ({level_name})** wykonał wizytę automatycznie.
    
    **Wyniki:**
    - 📦 Zamówienie: {autopilot_order} PLN ({penalty:+.0f}% penalty)
    - ⭐ Reputacja: {autopilot_reputation:+d}
    - 💬 Jakość wizyty: {"⭐" * visit_quality} ({visit_quality}/5)
    - ⏱️ Czas: 30 min (oszczędność: {time_saved} min)
    
    **Analiza ALEX:**
    Wizyta przebiegła sprawnie. Klient otrzymał standardową prezentację i złożył zamówienie.
    Autopilot nie prowadził pogłębionej rozmowy, więc nie odkryto nowych informacji o kliencie.
    """
    
    return {
        "order_value": autopilot_order,
        "reputation_change": autopilot_reputation,
        "visit_quality": visit_quality,
        "time_saved": time_saved,
        "penalty_applied": penalty,
        "energy_cost": 25,  # Stała wartość - autopilot zawsze 30 min = ~25% energii
        "summary": summary.strip(),
        "discoveries": [],  # Autopilot nie odkrywa nowych informacji
        "conversation_quality": visit_quality
    }


def get_points_to_next_level(current_points: int, current_level: int) -> Tuple[int, int]:
    """
    Oblicza ile punktów brakuje do następnego poziomu
    
    Args:
        current_points: Aktualne training points
        current_level: Aktualny poziom ALEX (0-4)
        
    Returns:
        Tuple[int, int]: (punkty_brakujące, punkty_wymagane_na_następny_poziom)
    """
    if current_level >= 4:
        return (0, ALEX_LEVELS[4]["required_points"])
    
    next_level = current_level + 1
    required = ALEX_LEVELS[next_level]["required_points"]
    remaining = required - current_points
    
    return (remaining, required)


def calculate_training_points(quiz_score: int, quiz_type: str = "basic") -> int:
    """
    Oblicza training points za quiz
    
    Args:
        quiz_score: Wynik quizu (0-100%)
        quiz_type: "basic" lub "advanced"
        
    Returns:
        int: Training points
    """
    base_points = 20 if quiz_type == "basic" else 40
    
    # Bonus za wysokie wyniki
    if quiz_score >= 90:
        multiplier = 1.5
    elif quiz_score >= 80:
        multiplier = 1.2
    elif quiz_score >= 70:
        multiplier = 1.0
    elif quiz_score >= 60:
        multiplier = 0.7
    else:
        multiplier = 0.5
    
    return int(base_points * multiplier)


def calculate_case_study_points(
    case_difficulty: int,  # 1-5
    performance_score: int  # 0-100%
) -> int:
    """
    Oblicza training points za case study
    
    Args:
        case_difficulty: Trudność case (1-5)
        performance_score: Wynik oceny (0-100%)
        
    Returns:
        int: Training points
    """
    base_points = case_difficulty * 20  # 1=20, 2=40, ..., 5=100
    
    # Bonus za wysoką jakość
    if performance_score >= 90:
        multiplier = 1.5
    elif performance_score >= 80:
        multiplier = 1.3
    elif performance_score >= 70:
        multiplier = 1.0
    elif performance_score >= 60:
        multiplier = 0.8
    else:
        multiplier = 0.5
    
    return int(base_points * multiplier)


# =============================================================================
# ALEX ROUTE PLANNING & SUGGESTIONS
# =============================================================================

def suggest_route_with_alex(
    base_location: Dict[str, float],
    selected_shops: List[Dict],
    alex_level: int,
    competencies: Dict[str, float],
    clients_data: Dict = None
) -> Dict:
    """
    ALEX sugeruje optymalną trasę z wyjaśnieniem
    
    Args:
        base_location: {"lat": ..., "lng": ...}
        selected_shops: Lista słowników z client_id, lat, lng, name
        alex_level: Poziom ALEX (0-4)
        competencies: Dict kompetencji ALEX
        clients_data: Pełne dane klientów (dla advanced routing)
        
    Returns:
        Dict: {
            "suggested_order": List[str],  # client_ids w sugerowanej kolejności
            "reasoning": str,  # Wyjaśnienie dlaczego taka kolejność
            "distance_km": float,
            "time_minutes": int,
            "energy_cost": int,
            "savings_vs_manual": Dict,  # Oszczędności względem wyboru gracza
            "alerts": List[str],  # Smart alerts (deadlines, high potential, etc.)
            "confidence": float  # 0-1, jak pewny jest ALEX tej sugestii
        }
    """
    from utils.fmcg_mechanics import optimize_route, calculate_route_distance
    from datetime import datetime, timedelta
    
    if not selected_shops:
        return {
            "suggested_order": [],
            "reasoning": "Nie wybrano klientów do odwiedzenia.",
            "distance_km": 0,
            "time_minutes": 0,
            "energy_cost": 0,
            "savings_vs_manual": {},
            "alerts": [],
            "confidence": 0.0
        }
    
    # Get ALEX stats
    alex_stats = get_alex_stats(alex_level)
    planning_competence = competencies.get("planning", 0.0)
    
    # =================================================================
    # LEVEL 0 (TRAINEE): Basic shortest path optimization
    # =================================================================
    if alex_level == 0:
        # Simple optimize_route (shortest path)
        suggested_order, distance = optimize_route(base_location, selected_shops)
        
        reasoning = f"""
        {alex_stats['emoji']} **ALEX {alex_stats['name_pl']}** sugeruje podstawową optymalizację:
        
        **Logika:** Najkrótsza trasa (shortest path algorithm)
        - Minimalizacja dystansu między punktami
        - Brak zaawansowanej analizy
        
        💡 **Wskazówka:** Wytrenuj ALEX do wyższego poziomu aby otrzymać lepsze sugestie!
        """
        
        alerts = []
        confidence = 0.6 + (planning_competence * 0.2)  # 60-80%
    
    # =================================================================
    # LEVEL 1 (JUNIOR): + ABC Segmentation
    # =================================================================
    elif alex_level == 1:
        # Optimize + priorytetyzuj klientów A przed B przed C
        if clients_data:
            # Sort by ABC segment (A > B > C), then optimize within segments
            shops_with_priority = []
            for shop in selected_shops:
                client_id = shop.get("client_id")
                client = clients_data.get(client_id, {})
                potential = client.get("potential_monthly", 1000)
                
                # ABC classification
                if potential >= 3000:
                    priority = 1  # A
                elif potential >= 1500:
                    priority = 2  # B
                else:
                    priority = 3  # C
                
                shops_with_priority.append({**shop, "priority": priority, "potential": potential})
            
            # Sort by priority first, then optimize route
            shops_with_priority.sort(key=lambda x: (x["priority"], -x["potential"]))
            suggested_order = [s["client_id"] for s in shops_with_priority]
            
            # Calculate distance
            distance = calculate_route_distance(base_location, shops_with_priority, suggested_order)
            
            reasoning = f"""
            {alex_stats['emoji']} **ALEX {alex_stats['name_pl']}** zastosował segmentację ABC:
            
            **Logika:** Priorytet klientów wg potencjału (A > B > C)
            - Klienci A (wysokie PLN): wizyta pierwsza
            - Klienci B (średnie PLN): wizyta środek
            - Klienci C (niskie PLN): wizyta końcowa
            
            📊 **Zaleta:** Najlepsi klienci dostaną najwięcej uwagi i czasu
            """
            
            alerts = _generate_abc_alerts(shops_with_priority)
            confidence = 0.7 + (planning_competence * 0.2)  # 70-90%
        else:
            # Fallback to basic optimization
            suggested_order, distance = optimize_route(base_location, selected_shops)
            reasoning = "Optymalizacja podstawowa (brak danych klientów dla ABC)"
            alerts = []
            confidence = 0.65
    
    # =================================================================
    # LEVEL 2 (MID): + Clustering (wizyty w okolicy)
    # =================================================================
    elif alex_level == 2:
        # Cluster nearby shops, optimize clusters
        if clients_data:
            clustered_shops = _cluster_shops_by_proximity(selected_shops, max_distance_km=3.0)
            
            # Optimize order within and between clusters
            suggested_order = _optimize_clustered_route(base_location, clustered_shops)
            distance = calculate_route_distance(base_location, selected_shops, suggested_order)
            
            reasoning = f"""
            {alex_stats['emoji']} **ALEX {alex_stats['name_pl']}** użył clusteringu geograficznego:
            
            **Logika:** Grupowanie wizyt w okolicy (do 3 km)
            - Zidentyfikowano {len(clustered_shops)} klastry
            - Optymalizacja trasy między i wewnątrz klastrów
            - Minimalizacja "pustych przebiegów"
            
            🗺️ **Zaleta:** Efektywne wykorzystanie czasu w danym rejonie
            """
            
            alerts = _generate_clustering_alerts(clustered_shops)
            confidence = 0.8 + (planning_competence * 0.15)  # 80-95%
        else:
            suggested_order, distance = optimize_route(base_location, selected_shops)
            reasoning = "Optymalizacja podstawowa (brak danych dla clusteringu)"
            alerts = []
            confidence = 0.75
    
    # =================================================================
    # LEVEL 3 (SENIOR): + Deadlines & Visit Frequency
    # =================================================================
    elif alex_level == 3:
        if clients_data:
            shops_with_urgency = []
            today = datetime.now()
            
            for shop in selected_shops:
                client_id = shop.get("client_id")
                client = clients_data.get(client_id, {})
                
                # Calculate urgency
                last_visit = client.get("last_visit_date")
                required_freq = client.get("visit_frequency_required", 14)  # dni
                
                if last_visit:
                    last_visit_dt = datetime.fromisoformat(last_visit)
                    days_since = (today - last_visit_dt).days
                    urgency_score = days_since / required_freq  # >1.0 = przeterminowane
                else:
                    urgency_score = 2.0  # Nowy klient = high priority
                
                potential = client.get("potential_monthly", 1000)
                
                shops_with_urgency.append({
                    **shop,
                    "urgency": urgency_score,
                    "potential": potential,
                    "days_since_visit": days_since if last_visit else 999
                })
            
            # Sort by urgency first, then potential
            shops_with_urgency.sort(key=lambda x: (-x["urgency"], -x["potential"]))
            suggested_order = [s["client_id"] for s in shops_with_urgency]
            
            distance = calculate_route_distance(base_location, shops_with_urgency, suggested_order)
            
            overdue_count = sum(1 for s in shops_with_urgency if s["urgency"] > 1.0)
            
            reasoning = f"""
            {alex_stats['emoji']} **ALEX {alex_stats['name_pl']}** priorytetyzuje deadline'y:
            
            **Logika:** Pilność wizyt + potencjał sprzedaży
            - Klienci z przeterminowaną wizytą: **{overdue_count}**
            - Sortowanie: urgency score × potential
            - Zapobieganie utracie klientów (LOST status)
            
            ⏰ **Zaleta:** Utrzymanie relacji z zagrożonymi klientami
            """
            
            alerts = _generate_urgency_alerts(shops_with_urgency)
            confidence = 0.85 + (planning_competence * 0.12)  # 85-97%
        else:
            suggested_order, distance = optimize_route(base_location, selected_shops)
            reasoning = "Optymalizacja podstawowa (brak danych o deadline'ach)"
            alerts = []
            confidence = 0.82
    
    # =================================================================
    # LEVEL 4 (MASTER): + Energy Management & Sales Potential
    # =================================================================
    else:  # alex_level == 4
        if clients_data:
            shops_optimized = []
            today = datetime.now()
            
            for shop in selected_shops:
                client_id = shop.get("client_id")
                client = clients_data.get(client_id, {})
                
                # Multi-factor scoring
                potential = client.get("potential_monthly", 1000)
                reputation = client.get("reputation", 0)
                last_visit = client.get("last_visit_date")
                required_freq = client.get("visit_frequency_required", 14)
                
                # Urgency
                if last_visit:
                    days_since = (today - datetime.fromisoformat(last_visit)).days
                    urgency = days_since / required_freq
                else:
                    urgency = 2.0
                
                # Sales potential (potential × reputation bonus)
                rep_multiplier = 1.0 + (reputation / 200)  # Max 1.5x dla rep=100
                sales_score = potential * rep_multiplier
                
                # Combined score (60% sales, 40% urgency)
                combined_score = (sales_score * 0.6) + (urgency * potential * 0.4)
                
                shops_optimized.append({
                    **shop,
                    "score": combined_score,
                    "potential": potential,
                    "urgency": urgency,
                    "reputation": reputation
                })
            
            # Sort by combined score, then apply route optimization
            shops_optimized.sort(key=lambda x: -x["score"])
            
            # Further optimize for energy (start with closest, end with closest to base)
            suggested_order = _optimize_energy_efficient_route(base_location, shops_optimized)
            distance = calculate_route_distance(base_location, shops_optimized, suggested_order)
            
            high_value_count = sum(1 for s in shops_optimized if s["potential"] >= 3000)
            
            reasoning = f"""
            {alex_stats['emoji']} **ALEX {alex_stats['name_pl']}** zastosował zaawansowaną optymalizację:
            
            **Logika:** Multi-factor scoring + energy management
            - Scoring: 60% sales potential + 40% urgency
            - Reputation bonus: do +50% dla wysokiej reputacji
            - Energy optimization: najmniej "pustych km"
            - High-value clients: **{high_value_count}** (potencjał >3000 PLN)
            
            🏆 **Zaleta:** Maksymalizacja ROI (Return on Time Investment)
            """
            
            alerts = _generate_master_alerts(shops_optimized, distance)
            confidence = 0.95 + (planning_competence * 0.05)  # 95-100%
        else:
            suggested_order, distance = optimize_route(base_location, selected_shops)
            reasoning = "Optymalizacja podstawowa (brak danych dla zaawansowanej analizy)"
            alerts = []
            confidence = 0.90
    
    # Calculate time and energy
    visit_time_per_shop = 45  # min average
    travel_time = int(distance * 2)  # ~2 min per km
    total_time = (len(selected_shops) * visit_time_per_shop) + travel_time
    energy_cost = int(distance * 1.0 + len(selected_shops) * 15)
    
    # Calculate savings (vs manual order would be worse by ~15-30%)
    manual_distance_estimate = distance * 1.2  # Assume manual is 20% worse
    savings_km = manual_distance_estimate - distance
    savings_time = int(savings_km * 2)  # minutes
    
    return {
        "suggested_order": suggested_order,
        "reasoning": reasoning.strip(),
        "distance_km": round(distance, 1),
        "time_minutes": total_time,
        "energy_cost": min(energy_cost, 100),
        "savings_vs_manual": {
            "distance_km": round(savings_km, 1),
            "time_minutes": savings_time,
            "energy_percent": int(savings_km * 1.0)
        },
        "alerts": alerts,
        "confidence": min(confidence, 1.0)
    }


def _generate_abc_alerts(shops: List[Dict]) -> List[str]:
    """Generuje alerty dla Junior level (ABC segmentation)"""
    alerts = []
    
    a_clients = [s for s in shops if s.get("priority") == 1]
    c_clients = [s for s in shops if s.get("priority") == 3]
    
    if len(a_clients) >= 2:
        alerts.append(f"⭐ Masz {len(a_clients)} klientów A - priorytet!")
    
    if len(c_clients) > len(a_clients):
        alerts.append(f"⚠️ Więcej klientów C niż A - rozważ fokus na high-value")
    
    return alerts


def _generate_clustering_alerts(clusters: List[List]) -> List[str]:
    """Generuje alerty dla Mid level (clustering)"""
    alerts = []
    
    if len(clusters) > 1:
        alerts.append(f"🗺️ Zidentyfikowano {len(clusters)} rejony - efektywna trasa!")
    
    largest_cluster = max(clusters, key=len) if clusters else []
    if len(largest_cluster) >= 3:
        alerts.append(f"📍 {len(largest_cluster)} klientów w jednym rejonie - zaoszczędzisz czas!")
    
    return alerts


def _generate_urgency_alerts(shops: List[Dict]) -> List[str]:
    """Generuje alerty dla Senior level (deadlines)"""
    alerts = []
    
    overdue = [s for s in shops if s.get("urgency", 0) > 1.0]
    critical = [s for s in shops if s.get("urgency", 0) > 1.5]
    
    if critical:
        alerts.append(f"🚨 KRYTYCZNE: {len(critical)} klientów wymaga natychmiastowej wizyty!")
    elif overdue:
        alerts.append(f"⏰ {len(overdue)} klientów ma przeterminowaną wizytę")
    
    high_days = [s for s in shops if s.get("days_since_visit", 0) > 21]
    if high_days:
        alerts.append(f"⚠️ {len(high_days)} klientów bez wizyty >3 tygodnie - ryzyko LOST!")
    
    return alerts


def _generate_master_alerts(shops: List[Dict], distance: float) -> List[str]:
    """Generuje alerty dla Master level (comprehensive)"""
    alerts = []
    
    # High value opportunities
    high_value = [s for s in shops if s.get("potential", 0) >= 3000]
    if high_value:
        total_potential = sum(s.get("potential", 0) for s in high_value)
        alerts.append(f"💰 High-value opportunity: {len(high_value)} klientów, potencjał {total_potential:,} PLN/mc")
    
    # Reputation insights
    high_rep = [s for s in shops if s.get("reputation", 0) >= 50]
    if high_rep:
        alerts.append(f"⭐ {len(high_rep)} klientów z wysoką reputacją - łatwa sprzedaż!")
    
    # Energy warning
    if distance > 30:
        alerts.append(f"⚡ UWAGA: długa trasa ({distance:.1f} km) - zaplanuj przerwę lub podziel na 2 dni")
    
    # Efficiency
    if len(shops) >= 5:
        alerts.append(f"🎯 Optymalna ilość wizyt ({len(shops)}) - maksymalna efektywność!")
    
    return alerts


def _cluster_shops_by_proximity(shops: List[Dict], max_distance_km: float = 3.0) -> List[List[Dict]]:
    """Grupuje sklepy w klastry geograficzne"""
    import math
    
    def distance(shop1, shop2):
        lat1, lng1 = shop1.get("lat", 0), shop1.get("lng", 0)
        lat2, lng2 = shop2.get("lat", 0), shop2.get("lng", 0)
        
        # Haversine approximation
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c  # km
    
    clusters = []
    remaining = shops.copy()
    
    while remaining:
        # Start new cluster with first shop
        cluster = [remaining.pop(0)]
        
        # Add nearby shops to cluster
        i = 0
        while i < len(remaining):
            for shop in cluster:
                if distance(remaining[i], shop) <= max_distance_km:
                    cluster.append(remaining.pop(i))
                    i = 0
                    break
            else:
                i += 1
        
        clusters.append(cluster)
    
    return clusters


def _optimize_clustered_route(base_location: Dict, clusters: List[List[Dict]]) -> List[str]:
    """Optymalizuje trasę między i wewnątrz klastrów"""
    from utils.fmcg_mechanics import optimize_route
    
    if not clusters:
        return []
    
    # For each cluster, optimize internal route
    optimized_clusters = []
    for cluster in clusters:
        if len(cluster) == 1:
            optimized_clusters.append(cluster)
        else:
            order, _ = optimize_route(base_location, cluster)
            optimized_clusters.append([s for s in cluster if s["client_id"] in order])
    
    # Optimize order of clusters (visit closest cluster first)
    # Simple: sort by distance of first shop in cluster from base
    import math
    
    def dist_from_base(cluster):
        if not cluster:
            return 999
        shop = cluster[0]
        lat, lng = shop.get("lat", 0), shop.get("lng", 0)
        base_lat, base_lng = base_location.get("lat", 0), base_location.get("lng", 0)
        
        dlat = math.radians(lat - base_lat)
        dlng = math.radians(lng - base_lng)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(base_lat)) * math.cos(math.radians(lat)) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c
    
    optimized_clusters.sort(key=dist_from_base)
    
    # Flatten to single order list
    final_order = []
    for cluster in optimized_clusters:
        final_order.extend([s["client_id"] for s in cluster])
    
    return final_order


def _optimize_energy_efficient_route(base_location: Dict, shops: List[Dict]) -> List[str]:
    """Optymalizuje trasę pod kątem zużycia energii (min empty km)"""
    from utils.fmcg_mechanics import optimize_route
    
    # Use standard optimization but ensure return to base is short
    # Strategy: end with shop closest to base
    if not shops:
        return []
    
    import math
    
    def dist_from_base(shop):
        lat, lng = shop.get("lat", 0), shop.get("lng", 0)
        base_lat, base_lng = base_location.get("lat", 0), base_location.get("lng", 0)
        
        dlat = math.radians(lat - base_lat)
        dlng = math.radians(lng - base_lng)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(base_lat)) * math.cos(math.radians(lat)) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c
    
    # Find shop closest to base
    closest_to_base = min(shops, key=dist_from_base)
    
    # Optimize route, then rotate so closest is last
    order, _ = optimize_route(base_location, shops)
    
    # Rotate order to end with closest to base
    try:
        idx = order.index(closest_to_base["client_id"])
        rotated_order = order[idx+1:] + order[:idx+1]
        return rotated_order
    except (ValueError, KeyError):
        return order


# =============================================================================
# TESTING / DEMO
# =============================================================================

if __name__ == "__main__":
    print("🤖 ALEX AI Sales Assistant - System Test\n")
    
    # Test poziomów
    for points in [0, 100, 300, 600, 1000]:
        level = calculate_alex_level(points)
        stats = get_alex_stats(level)
        print(f"Points: {points:4d} → Level {level} ({stats['name_pl']}) - Penalty: {stats['penalty']:+d}%")
    
    print("\n" + "="*60 + "\n")
    
    # Test autopilota
    dummy_client = {
        "name": "Sklep Testowy",
        "potential_monthly": 2000
    }
    
    dummy_player = {
        "level": 1
    }
    
    competencies = {
        "planning": 0.3,
        "communication": 0.5,
        "analysis": 0.2,
        "relationship": 0.4,
        "negotiation": 0.1
    }
    
    for level in range(5):
        print(f"\n{ALEX_LEVELS[level]['emoji']} ALEX Level {level} ({ALEX_LEVELS[level]['name_pl']}):")
        result = simulate_autopilot_visit(dummy_client, dummy_player, level, competencies)
        print(result['summary'])
