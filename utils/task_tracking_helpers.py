"""
Helper functions for weekly tasks tracking.
Updates game_state with metrics needed for task completion checks.
"""


def reset_weekly_task_stats(game_state):
    """
    Reset weekly task tracking statistics.
    Call this at the start of each week (Monday).
    """
    game_state["visits_this_week"] = []
    game_state["prospect_visits_this_week"] = 0
    game_state["activations_this_week"] = 0
    game_state["categories_sold_this_week"] = []
    game_state["weekly_sales"] = 0
    
    # Competitive tracking
    game_state["intel_visits_kotlin"] = 0
    game_state["wins_from_kotlin"] = 0


def track_visit_for_tasks(game_state, visit_data, client_data):
    """
    Update task-relevant metrics when a visit is completed.
    Call this after each visit.
    
    Args:
        game_state: Game state dict
        visit_data: Visit result dict (quality, order_value, etc.)
        client_data: Client being visited
    """
    # Ensure weekly lists exist
    if "visits_this_week" not in game_state:
        game_state["visits_this_week"] = []
    if "categories_sold_this_week" not in game_state:
        game_state["categories_sold_this_week"] = []
    
    # Track visit
    game_state["visits_this_week"].append(visit_data)
    
    # Track prospect visits
    if client_data.get("status") == "PROSPECT":
        game_state["prospect_visits_this_week"] = game_state.get("prospect_visits_this_week", 0) + 1
    
    # Track sales and categories
    if visit_data.get("order_value", 0) > 0:
        game_state["weekly_sales"] = game_state.get("weekly_sales", 0) + visit_data["order_value"]
        
        # Track categories
        for product in visit_data.get("products_ordered", []):
            category = product.get("category")
            if category and category not in game_state["categories_sold_this_week"]:
                game_state["categories_sold_this_week"].append(category)
    
    # Track competitive intel (if client uses competitor)
    current_supplier = client_data.get("current_supplier", "").lower()
    if "kotlin" in current_supplier:
        game_state["intel_visits_kotlin"] = game_state.get("intel_visits_kotlin", 0) + 1


def track_client_activation(game_state, client_data, previous_status):
    """
    Track when client changes from PROSPECT to ACTIVE.
    Call this when client status changes.
    
    Args:
        game_state: Game state dict
        client_data: Client that changed status
        previous_status: Previous status (e.g., "PROSPECT")
    """
    if previous_status == "PROSPECT" and client_data.get("status") == "ACTIVE":
        game_state["activations_this_week"] = game_state.get("activations_this_week", 0) + 1
        
        # Check if won from competitor
        previous_supplier = client_data.get("previous_supplier", "").lower()
        if "kotlin" in previous_supplier:
            game_state["wins_from_kotlin"] = game_state.get("wins_from_kotlin", 0) + 1


def initialize_weekly_stats_if_needed(game_state):
    """
    Initialize weekly stats if they don't exist.
    Safe to call multiple times.
    """
    if "visits_this_week" not in game_state:
        reset_weekly_task_stats(game_state)
