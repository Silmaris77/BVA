"""
💎 Reputation System
3-level reputation tracking: Client + Company → Overall Rating
Replaces monetary rewards with progression-based unlocks
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime


# =============================================================================
# TIER DEFINITIONS
# =============================================================================

# Tier definitions - now based on POINTS not 0-100 scale
REPUTATION_TIERS = [
    {"name": "Trainee", "emoji": "🟤", "min_points": 0, "max_points": 100},
    {"name": "Junior", "emoji": "🔵", "min_points": 101, "max_points": 250},
    {"name": "Regular", "emoji": "🟢", "min_points": 251, "max_points": 500},
    {"name": "Senior", "emoji": "🟡", "min_points": 501, "max_points": 1000},
    {"name": "Expert", "emoji": "🟠", "min_points": 1001, "max_points": 2000},
    {"name": "Master", "emoji": "🔴", "min_points": 2001, "max_points": 999999}
]

# Unlockable features per tier
TIER_UNLOCKS = {
    "Trainee": ["basic_features"],
    "Junior": ["route_planner"],
    "Regular": ["client_insights"],
    "Senior": ["advanced_analytics"],
    "Expert": ["mentor_mode"],
    "Master": ["all_premium_features"]
}


# =============================================================================
# REPUTATION INITIALIZATION
# =============================================================================

def initialize_reputation_system() -> Dict:
    """Initialize reputation tracking structure in game_state
    
    Returns:
        Dict with reputation structure ready to add to game_state
    """
    initial_state = {
        "clients": {},  # {client_id: reputation_score}
        "company": {
            "task_performance": 0,        # Start: 0 (no tasks completed yet)
            "sales_performance": 0,       # Start: 0 (no sales yet)
            "professionalism": 100        # Start: 100, penalties subtract
        },
        "tier": "Trainee",
        "unlock_tokens": 0,
        "training_credits": 0,
        "xp": 0,
        "level": 1
    }
    
    # Calculate initial overall_rating based on starting values
    # Client Rep = 0 (no clients), Company Rep = 30 (only professionalism 100 × 0.30)
    # Overall = (0 × 0.60) + (30 × 0.40) = 12
    company_rep_initial = 100 * 0.30  # professionalism only
    overall_rating_initial = (0 * 0.60) + (company_rep_initial * 0.40)
    
    initial_state["overall_rating"] = round(overall_rating_initial, 1)  # 12.0
    
    return initial_state


# =============================================================================
# CLIENT REPUTATION CALCULATION
# =============================================================================

def calculate_client_reputation(client_data: Dict, game_state: Dict) -> float:
    """Calculate reputation score for a single client (0-100)
    
    Components:
    - Visit Quality (40%): Average star rating from visits
    - Relationship Level (30%): Current relationship score
    - Contract Performance (20%): On-time deliveries, no complaints
    - Product Mix Success (10%): Category diversification
    
    Args:
        client_data: Client dictionary with history
        game_state: Full game state (for context)
    
    Returns:
        Float 0-100 reputation score
    """
    # 1. Visit Quality (40%) - średnia jakość wizyt
    visit_history = client_data.get("visit_history", [])
    if visit_history:
        visit_qualities = [v.get("quality_rating", 0) for v in visit_history if v.get("quality_rating")]
        avg_quality_stars = sum(visit_qualities) / len(visit_qualities) if visit_qualities else 0
        visit_quality_pct = (avg_quality_stars / 5.0) * 100  # 0-5 stars → 0-100%
    else:
        visit_quality_pct = 0
    
    # 2. Relationship Level (30%)
    # Use either 'reputation' field (direct value) or 'relationship' (legacy)
    relationship = client_data.get("reputation", client_data.get("relationship", 0))  # 0-100
    
    # 3. Contract Performance (20%)
    orders = client_data.get("orders", [])
    if orders:
        on_time_deliveries = sum(1 for o in orders if o.get("delivered_on_time", True))
        contract_performance_pct = (on_time_deliveries / len(orders)) * 100
    else:
        contract_performance_pct = 100  # No orders = perfect performance
    
    # 4. Product Mix Success (10%) - ile kategorii kupują
    purchased_categories = set()
    for order in orders:
        for item in order.get("items", []):
            category = item.get("category", "unknown")
            purchased_categories.add(category)
    
    total_categories = 5  # FreshLife ma 5 głównych kategorii
    product_mix_pct = (len(purchased_categories) / total_categories) * 100
    
    # Weighted average
    client_reputation = (
        visit_quality_pct * 0.40 +
        relationship * 0.30 +
        contract_performance_pct * 0.20 +
        product_mix_pct * 0.10
    )
    
    return round(client_reputation, 1)


# =============================================================================
# CLIENT REPUTATION WEIGHTS
# =============================================================================

# Weights for different client statuses in reputation calculation
CLIENT_REPUTATION_WEIGHTS = {
    "ACTIVE": 1.0,      # Full impact - paying customers
    "PARTNER": 1.0,     # Full impact - strategic partners
    "LOST": 0.7,        # High impact - failure should be visible
    "PROSPECT": 0.5,    # Medium impact - shows prospecting skills
}


def get_client_weight(client: Dict) -> float:
    """Get reputation weight for a client based on status and contact history
    
    Args:
        client: Client data dict
    
    Returns:
        float: Weight (0.0-1.0) for reputation calculation
    """
    # Get status - handle both old and new structure
    status = client.get("status")
    if not status:
        # New Heinz structure - determine from convinced_products
        if client.get("convinced_products"):
            status = "ACTIVE"
        else:
            status = "PROSPECT"
    
    # PROSPECT not contacted has 0 weight
    if status == "PROSPECT" and not is_client_contacted(client):
        return 0.0
    
    return CLIENT_REPUTATION_WEIGHTS.get(status, 0.5)


def is_client_contacted(client: Dict) -> bool:
    """Check if client has been contacted/visited
    
    Args:
        client: Client data dict
    
    Returns:
        bool: True if client has been visited at least once
    """
    return (
        client.get("visits_count", 0) > 0 or
        client.get("visit_history") or
        client.get("last_visit_date") is not None or
        client.get("first_contact_date") is not None
    )


def calculate_average_client_reputation(game_state: Dict, clients: Dict = None) -> Tuple[float, Dict[str, int]]:
    """Calculate weighted average reputation across all contacted clients
    
    Uses weights based on client status:
    - ACTIVE/PARTNER: 1.0 (100%) - full impact
    - LOST: 0.7 (70%) - failure should be visible
    - PROSPECT (contacted): 0.5 (50%) - shows prospecting ability
    - PROSPECT (not contacted): 0.0 - ignored (no interaction yet)
    
    Args:
        game_state: Full game state
        clients: Optional clients dict (if None, uses game_state["clients"])
    
    Returns:
        Tuple[float, Dict]: (weighted_average_reputation, breakdown_by_status)
    """
    # Use provided clients or get from game_state
    if clients is None:
        clients = game_state.get("clients", {})
    
    weighted_sum = 0.0
    total_weight = 0.0
    
    # Count clients by status for breakdown
    breakdown = {
        "ACTIVE": 0,
        "PARTNER": 0,
        "LOST": 0,
        "PROSPECT_CONTACTED": 0,
        "PROSPECT_NOT_CONTACTED": 0
    }
    
    for client_id, client_data in clients.items():
        # Get weight for this client (handles status + contact check)
        weight = get_client_weight(client_data)
        
        # Skip if no weight (e.g., PROSPECT not contacted)
        if weight == 0:
            breakdown["PROSPECT_NOT_CONTACTED"] += 1
            continue
        
        # Get status for breakdown
        status = client_data.get("status")
        if not status:
            # New Heinz structure
            if client_data.get("convinced_products"):
                status = "ACTIVE"
            else:
                status = "PROSPECT"
        
        # Check if contacted (for breakdown)
        contacted = is_client_contacted(client_data)
        
        # Calculate reputation score
        rep_score = calculate_client_reputation(client_data, game_state)
        
        # Add to weighted sum
        weighted_sum += rep_score * weight
        total_weight += weight
        
        # Update breakdown
        if status == "PROSPECT":
            breakdown["PROSPECT_CONTACTED"] += 1
        else:
            breakdown[status] = breakdown.get(status, 0) + 1
        
        # Update stored reputation
        if "reputation" not in game_state:
            game_state["reputation"] = initialize_reputation_system()
        game_state["reputation"]["clients"][client_id] = rep_score
    
    # Calculate weighted average
    if total_weight > 0:
        avg_reputation = round(weighted_sum / total_weight, 1)
    else:
        avg_reputation = 0.0
    
    return avg_reputation, breakdown


# =============================================================================
# COMPANY REPUTATION CALCULATION
# =============================================================================

def calculate_task_performance(game_state: Dict) -> float:
    """Calculate task completion percentage
    
    Args:
        game_state: Full game state with weekly_stats
    
    Returns:
        Float 0-100 percentage
    """
    weekly_stats = game_state.get("weekly_stats", {})
    
    # Count completed vs assigned tasks across all weeks
    total_assigned = 0
    total_completed = 0
    
    for week_num, stats in weekly_stats.items():
        assigned = stats.get("tasks_assigned", 0)
        completed = stats.get("tasks_completed", 0)
        total_assigned += assigned
        total_completed += completed
    
    if total_assigned > 0:
        return round((total_completed / total_assigned) * 100, 1)
    else:
        # No tasks assigned yet = 0 performance (not perfect, just nothing done)
        # Will use saved value from game_state["reputation"]["company"]["task_performance"]
        return game_state.get("reputation", {}).get("company", {}).get("task_performance", 0)


def calculate_sales_performance(game_state: Dict) -> float:
    """Calculate progress towards scenario sales goals
    
    Components:
    - Scenario goal progress (60%): % achieved main sales target
    - Weekly sales trend (40%): Growth trend vs previous week
    
    Args:
        game_state: Full game state with scenario objectives
    
    Returns:
        Float 0-100 percentage
    """
    scenario_id = game_state.get("scenario_id", "")
    
    # Find sales-related objective
    sales_goal_progress = 0
    
    # Check if it's Heinz scenario with monthly sales goal
    if "heinz" in scenario_id.lower():
        # Goal: 15,000 PLN monthly sales
        target_sales = 15000
        current_month_sales = game_state.get("stats", {}).get("current_month_sales", 0)
        sales_goal_progress = min((current_month_sales / target_sales) * 100, 100)
    else:
        # Generic: calculate based on total sales vs week number
        week = game_state.get("week", 1)
        expected_sales_per_week = 2000  # Baseline
        expected_total = week * expected_sales_per_week
        actual_total = game_state.get("stats", {}).get("total_sales", 0)
        
        if expected_total > 0:
            sales_goal_progress = min((actual_total / expected_total) * 100, 100)
    
    # Weekly trend (compare to previous week)
    weekly_stats = game_state.get("weekly_stats", {})
    current_week = game_state.get("week", 1)
    
    current_week_sales = weekly_stats.get(str(current_week), {}).get("sales", 0)
    previous_week_sales = weekly_stats.get(str(current_week - 1), {}).get("sales", 1)  # Avoid div by 0
    
    if previous_week_sales > 0:
        growth_rate = (current_week_sales / previous_week_sales) * 100
        # Cap at 150% (50% growth is excellent)
        weekly_trend = min(growth_rate, 150)
    else:
        # No previous week or week 1 = use 0 (no trend data yet)
        weekly_trend = 0
    
    # Weighted average
    sales_performance = (
        sales_goal_progress * 0.60 +
        weekly_trend * 0.40
    )
    
    return round(min(sales_performance, 100), 1)


def calculate_professionalism(game_state: Dict) -> float:
    """Calculate professionalism score (100 - penalties)
    
    Penalties:
    - Late delivery: -5 points
    - Poor visit quality (<2 stars): -3 points
    - Fuel budget exceeded: -2 points
    - Broken promises: -10 points
    
    Args:
        game_state: Full game state
    
    Returns:
        Float 0-100 score
    """
    if "reputation" not in game_state:
        return 100.0
    
    # Start at 100, subtract penalties
    professionalism = game_state.get("reputation", {}).get("company", {}).get("professionalism", 100)
    
    # Penalties are applied in real-time by other functions
    # This just returns the current value
    return max(professionalism, 0.0)


def apply_professionalism_penalty(game_state: Dict, penalty_type: str, amount: int = None) -> Dict:
    """Apply penalty to professionalism score
    
    Args:
        game_state: Full game state
        penalty_type: Type of penalty ("late_delivery", "poor_visit", "fuel_exceeded", "broken_promise")
        amount: Optional custom penalty amount (overrides default)
    
    Returns:
        Updated game_state
    """
    penalties = {
        "late_delivery": 5,
        "poor_visit": 3,
        "fuel_exceeded": 2,
        "broken_promise": 10
    }
    
    penalty = amount if amount is not None else penalties.get(penalty_type, 0)
    
    if "reputation" not in game_state:
        game_state["reputation"] = initialize_reputation_system()
    
    current = game_state["reputation"]["company"]["professionalism"]
    game_state["reputation"]["company"]["professionalism"] = max(current - penalty, 0)
    
    # Log penalty
    if "penalty_history" not in game_state["reputation"]:
        game_state["reputation"]["penalty_history"] = []
    
    game_state["reputation"]["penalty_history"].append({
        "type": penalty_type,
        "amount": penalty,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "new_score": game_state["reputation"]["company"]["professionalism"]
    })
    
    return game_state


def calculate_company_reputation(game_state: Dict) -> float:
    """Calculate overall company reputation (0-100)
    
    Components:
    - Task Performance (30%)
    - Sales Performance (40%)
    - Professionalism (30%)
    
    Args:
        game_state: Full game state
    
    Returns:
        Float 0-100 company reputation score
    """
    task_perf = calculate_task_performance(game_state)
    sales_perf = calculate_sales_performance(game_state)
    prof = calculate_professionalism(game_state)
    
    company_rep = (
        task_perf * 0.30 +
        sales_perf * 0.40 +
        prof * 0.30
    )
    
    # Update stored values
    if "reputation" not in game_state:
        game_state["reputation"] = initialize_reputation_system()
    
    game_state["reputation"]["company"]["task_performance"] = task_perf
    game_state["reputation"]["company"]["sales_performance"] = sales_perf
    game_state["reputation"]["company"]["professionalism"] = prof
    
    return round(company_rep, 1)


# =============================================================================
# OVERALL RATING & TIER
# =============================================================================

def calculate_overall_rating(game_state: Dict, clients: Dict = None) -> float:
    """Calculate overall rating as POINTS (not 0-100 scale)
    
    Point-based system:
    - Company Points: Base score from task/sales/professionalism (30-50 typical)
    - Client Points: Sum of (client_reputation × weight) for all contacted clients
      - ACTIVE: reputation × 1.0
      - PROSPECT: reputation × 0.5  
      - LOST: reputation × 0.7
    
    Total Points = Company Points + Sum(Client Points)
    
    Args:
        game_state: Full game state
        clients: Optional clients dict (if None, uses game_state["clients"])
    
    Returns:
        Float: Total points (unbounded, typically 30-2000+)
    """
    # Get company reputation (0-100 scale)
    company_rep = calculate_company_reputation(game_state)
    
    # Convert to points (scale down to reasonable base)
    # Company rep 0-100 → 0-50 points base
    company_points = company_rep * 0.5
    
    # Get client points
    if clients is None:
        clients = game_state.get("clients", {})
    
    client_points = 0.0
    
    for client_id, client_data in clients.items():
        # Get weight (includes contact check)
        weight = get_client_weight(client_data)
        
        if weight == 0:
            continue  # Skip uncontacted prospects
        
        # Get client reputation score
        rep_score = calculate_client_reputation(client_data, game_state)
        
        # Add weighted points
        client_points += rep_score * weight
    
    # Total points
    total_points = company_points + client_points
    
    # Update stored value
    if "reputation" not in game_state:
        game_state["reputation"] = initialize_reputation_system()
    
    game_state["reputation"]["overall_rating"] = round(total_points, 1)
    game_state["reputation"]["company_points"] = round(company_points, 1)
    game_state["reputation"]["client_points"] = round(client_points, 1)
    
    return round(total_points, 1)


def get_tier(overall_rating: float) -> Dict:
    """Get tier information for given overall rating (points)
    
    Args:
        overall_rating: Total points (unbounded)
    
    Returns:
        Dict with tier info: {name, emoji, min_points, max_points}
    """
    for tier in REPUTATION_TIERS:
        if tier["min_points"] <= overall_rating <= tier["max_points"]:
            return tier
    
    # Fallback to Trainee
    return REPUTATION_TIERS[0]


def get_next_tier(current_tier_name: str) -> Optional[Dict]:
    """Get next tier in progression
    
    Args:
        current_tier_name: Current tier name (e.g., "Junior")
    
    Returns:
        Next tier dict or None if already Master
    """
    for i, tier in enumerate(REPUTATION_TIERS):
        if tier["name"] == current_tier_name:
            if i < len(REPUTATION_TIERS) - 1:
                return REPUTATION_TIERS[i + 1]
            else:
                return None  # Already at Master
    
    return REPUTATION_TIERS[0]  # Fallback


def update_tier(game_state: Dict) -> Tuple[Dict, bool]:
    """Update tier based on overall rating
    
    Args:
        game_state: Full game state
    
    Returns:
        Tuple (updated_game_state, tier_up_occurred)
    """
    overall_rating = calculate_overall_rating(game_state)
    current_tier = get_tier(overall_rating)
    
    if "reputation" not in game_state:
        game_state["reputation"] = initialize_reputation_system()
    
    old_tier_name = game_state["reputation"]["tier"]
    new_tier_name = current_tier["name"]
    
    game_state["reputation"]["tier"] = new_tier_name
    
    tier_up = False
    if new_tier_name != old_tier_name:
        # Check if it's an upgrade (not a downgrade)
        old_tier_idx = next(i for i, t in enumerate(REPUTATION_TIERS) if t["name"] == old_tier_name)
        new_tier_idx = next(i for i, t in enumerate(REPUTATION_TIERS) if t["name"] == new_tier_name)
        
        if new_tier_idx > old_tier_idx:
            tier_up = True
            
            # Log tier progression
            if "tier_history" not in game_state["reputation"]:
                game_state["reputation"]["tier_history"] = []
            
            game_state["reputation"]["tier_history"].append({
                "from": old_tier_name,
                "to": new_tier_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "overall_rating": overall_rating
            })
    
    return game_state, tier_up


# =============================================================================
# REWARD DISTRIBUTION
# =============================================================================

def award_task_reward(game_state: Dict, reward: Dict) -> Dict:
    """Award multi-currency reward for task completion
    
    Reward structure:
    {
        "xp": 100,
        "unlock_tokens": 2,
        "client_reputation": 5,
        "company_reputation": 3,
        "training_credits": 0
    }
    
    Args:
        game_state: Full game state
        reward: Reward dictionary
    
    Returns:
        Updated game_state with rewards applied
    """
    if "reputation" not in game_state:
        game_state["reputation"] = initialize_reputation_system()
    
    # XP
    game_state["reputation"]["xp"] += reward.get("xp", 0)
    
    # Unlock Tokens
    game_state["reputation"]["unlock_tokens"] += reward.get("unlock_tokens", 0)
    
    # Training Credits
    game_state["reputation"]["training_credits"] += reward.get("training_credits", 0)
    
    # Client Reputation boost (apply to all active clients)
    client_rep_boost = reward.get("client_reputation", 0)
    if client_rep_boost > 0:
        clients = game_state.get("clients", {})
        for client_id, client_data in clients.items():
            if client_data.get("status") in ["ACTIVE", "PARTNER"]:
                # Boost relationship score
                current_rel = client_data.get("relationship", 0)
                client_data["relationship"] = min(current_rel + client_rep_boost, 100)
    
    # Company Reputation boost (add to task performance)
    company_rep_boost = reward.get("company_reputation", 0)
    if company_rep_boost > 0:
        # This will be reflected in next task performance calculation
        # Track it in weekly stats
        week = game_state.get("week", 1)
        if "weekly_stats" not in game_state:
            game_state["weekly_stats"] = {}
        if str(week) not in game_state["weekly_stats"]:
            game_state["weekly_stats"][str(week)] = {}
        
        game_state["weekly_stats"][str(week)]["company_rep_boosts"] = \
            game_state["weekly_stats"][str(week)].get("company_rep_boosts", 0) + company_rep_boost
    
    # Recalculate overall rating
    calculate_overall_rating(game_state)
    
    # Check for tier progression
    game_state, tier_up = update_tier(game_state)
    
    # Log reward
    if "reward_history" not in game_state["reputation"]:
        game_state["reputation"]["reward_history"] = []
    
    game_state["reputation"]["reward_history"].append({
        "reward": reward,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tier_up": tier_up
    })
    
    return game_state


# =============================================================================
# WEEKLY RECALCULATION
# =============================================================================

def recalculate_all_reputation(game_state: Dict) -> Dict:
    """Recalculate all reputation components (called weekly)
    
    Args:
        game_state: Full game state
    
    Returns:
        Updated game_state with fresh reputation calculations
    """
    # Recalculate everything
    _, _ = calculate_average_client_reputation(game_state)  # Updates stored values
    calculate_company_reputation(game_state)
    overall_rating = calculate_overall_rating(game_state)
    
    # Update tier
    game_state, tier_up = update_tier(game_state)
    
    return game_state
