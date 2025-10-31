"""
FMCG Progression System - Weekly/Monthly Targets & Scoring

Obsługuje:
- Dynamiczne cele tygodniowe/miesięczne (rosną z poziomem)
- Scoring/benchmarking
- Achievement tracking
- Weekly/monthly summaries
"""

from typing import Dict, List, Tuple
from datetime import datetime


def get_targets_for_level(level: int) -> Dict[str, int]:
    """
    Zwraca cele tygodniowe i miesięczne dla danego poziomu kariery
    
    Targets progression:
    - Level 1 (Junior Sales Rep): 8k/tydzień, 35k/miesiąc
    - Level 2 (Sales Rep): 12k/tydzień, 50k/miesiąc
    - Level 3 (Senior Rep): 18k/tydzień, 75k/miesiąc
    - Level 4+ (Team Leader+): 25k+/tydzień, 100k+/miesiąc
    
    Args:
        level: Poziom kariery (1-10)
    
    Returns:
        {"weekly_sales": X, "weekly_visits": Y, "monthly_sales": Z}
    """
    target_map = {
        1: {"weekly_sales": 8000, "weekly_visits": 6, "monthly_sales": 35000},
        2: {"weekly_sales": 12000, "weekly_visits": 8, "monthly_sales": 50000},
        3: {"weekly_sales": 18000, "weekly_visits": 10, "monthly_sales": 75000},
        4: {"weekly_sales": 25000, "weekly_visits": 12, "monthly_sales": 100000},
        5: {"weekly_sales": 30000, "weekly_visits": 15, "monthly_sales": 130000},
        6: {"weekly_sales": 40000, "weekly_visits": 18, "monthly_sales": 170000},
        7: {"weekly_sales": 50000, "weekly_visits": 20, "monthly_sales": 220000},
        8: {"weekly_sales": 65000, "weekly_visits": 25, "monthly_sales": 280000},
        9: {"weekly_sales": 80000, "weekly_visits": 30, "monthly_sales": 350000},
        10: {"weekly_sales": 100000, "weekly_visits": 35, "monthly_sales": 450000},
    }
    
    return target_map.get(level, target_map[1])


def calculate_weekly_score(
    sales_actual: int,
    sales_target: int,
    visits_actual: int,
    visits_target: int,
    avg_quality: float  # 1.0 - 5.0
) -> Dict[str, float]:
    """
    Kalkuluje scoring tygodniowy na podstawie performance
    
    Komponenty:
    - Sales achievement: 50% wagi (0-100 points)
    - Visit completion: 25% wagi (0-100 points)
    - Quality: 25% wagi (0-100 points)
    
    Total: 0-100 points
    
    Returns:
        {
            "total_score": 85.5,
            "sales_score": 90.0,
            "visits_score": 80.0,
            "quality_score": 85.0,
            "grade": "A",  # S/A/B/C/D
            "performance_level": "Outstanding"
        }
    """
    # Sales score (0-100)
    sales_pct = (sales_actual / sales_target * 100) if sales_target > 0 else 0
    sales_score = min(100, sales_pct)  # Cap at 100
    
    # Visits score (0-100)
    visits_pct = (visits_actual / visits_target * 100) if visits_target > 0 else 0
    visits_score = min(100, visits_pct)
    
    # Quality score (1-5 stars → 0-100)
    quality_score = ((avg_quality - 1) / 4) * 100  # 1⭐=0%, 5⭐=100%
    
    # Weighted total
    total_score = (
        sales_score * 0.5 +
        visits_score * 0.25 +
        quality_score * 0.25
    )
    
    # Grade assignment
    if total_score >= 95:
        grade = "S"
        perf_level = "Exceptional"
    elif total_score >= 85:
        grade = "A"
        perf_level = "Outstanding"
    elif total_score >= 75:
        grade = "B"
        perf_level = "Good"
    elif total_score >= 60:
        grade = "C"
        perf_level = "Acceptable"
    else:
        grade = "D"
        perf_level = "Needs Improvement"
    
    return {
        "total_score": round(total_score, 1),
        "sales_score": round(sales_score, 1),
        "visits_score": round(visits_score, 1),
        "quality_score": round(quality_score, 1),
        "grade": grade,
        "performance_level": perf_level
    }


def get_achievement_tier(weekly_history: List[Dict]) -> Dict[str, any]:
    """
    Określa tier achievementów na podstawie historii
    
    Tiers:
    - Bronze: 5+ tygodni z celem osiągniętym
    - Silver: 10+ tygodni + seria 3
    - Gold: 20+ tygodni + seria 5 + najlepszy tydzień 150%+ targetu
    - Platinum: 30+ tygodni + seria 8 + avg score 85+
    - Diamond: 50+ tygodni + seria 12 + avg score 95+
    
    Returns:
        {
            "tier": "Gold",
            "tier_emoji": "🥇",
            "tier_color": "#fbbf24",
            "progress_to_next": 0.65,  # 65% do następnego tiera
            "requirements_met": ["20+ weeks", "5-week streak"],
            "requirements_pending": ["150% best week"]
        }
    """
    if not weekly_history:
        return {
            "tier": "None",
            "tier_emoji": "🆕",
            "tier_color": "#9ca3af",
            "progress_to_next": 0.0,
            "requirements_met": [],
            "requirements_pending": ["Ukończ pierwszy tydzień"]
        }
    
    # Calculate stats
    total_weeks = len(weekly_history)
    achieved_weeks = sum(1 for w in weekly_history if w.get("target_achieved", False))
    
    # Best streak
    max_streak = 0
    current_streak = 0
    for week in weekly_history:
        if week.get("target_achieved", False):
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    
    # Best week performance
    best_week_pct = 0
    for week in weekly_history:
        target = week.get("target_sales", 8000)
        actual = week.get("sales", 0)
        week_pct = (actual / target * 100) if target > 0 else 0
        best_week_pct = max(best_week_pct, week_pct)
    
    # Average score (if available)
    scored_weeks = [w for w in weekly_history if "score" in w]
    avg_score = sum(w["score"] for w in scored_weeks) / len(scored_weeks) if scored_weeks else 0
    
    # Tier determination
    if achieved_weeks >= 50 and max_streak >= 12 and avg_score >= 95:
        tier_data = {
            "tier": "Diamond",
            "tier_emoji": "💎",
            "tier_color": "#3b82f6",
            "progress_to_next": 1.0,
            "requirements_met": ["50+ weeks", "12-week streak", "95+ avg score"],
            "requirements_pending": ["MAX LEVEL"]
        }
    elif achieved_weeks >= 30 and max_streak >= 8 and avg_score >= 85:
        progress = min(1.0, (achieved_weeks / 50 + max_streak / 12 + avg_score / 95) / 3)
        tier_data = {
            "tier": "Platinum",
            "tier_emoji": "🏆",
            "tier_color": "#a78bfa",
            "progress_to_next": progress,
            "requirements_met": ["30+ weeks", "8-week streak", "85+ avg score"],
            "requirements_pending": [f"{50 - achieved_weeks} weeks to Diamond"]
        }
    elif achieved_weeks >= 20 and max_streak >= 5 and best_week_pct >= 150:
        progress = min(1.0, (achieved_weeks / 30 + max_streak / 8 + avg_score / 85) / 3)
        tier_data = {
            "tier": "Gold",
            "tier_emoji": "🥇",
            "tier_color": "#fbbf24",
            "progress_to_next": progress,
            "requirements_met": ["20+ weeks", "5-week streak", "150% best week"],
            "requirements_pending": [f"{30 - achieved_weeks} weeks to Platinum"]
        }
    elif achieved_weeks >= 10 and max_streak >= 3:
        progress = min(1.0, (achieved_weeks / 20 + max_streak / 5) / 2)
        pending = []
        if best_week_pct < 150:
            pending.append(f"Best week: {best_week_pct:.0f}% (need 150%)")
        if achieved_weeks < 20:
            pending.append(f"{20 - achieved_weeks} weeks to Gold")
        
        tier_data = {
            "tier": "Silver",
            "tier_emoji": "🥈",
            "tier_color": "#94a3b8",
            "progress_to_next": progress,
            "requirements_met": ["10+ weeks", "3-week streak"],
            "requirements_pending": pending
        }
    elif achieved_weeks >= 5:
        progress = min(1.0, (achieved_weeks / 10 + max_streak / 3) / 2)
        tier_data = {
            "tier": "Bronze",
            "tier_emoji": "🥉",
            "tier_color": "#cd7f32",
            "progress_to_next": progress,
            "requirements_met": ["5+ weeks"],
            "requirements_pending": [f"{10 - achieved_weeks} weeks to Silver", f"Seria: {max_streak}/3"]
        }
    else:
        progress = achieved_weeks / 5
        tier_data = {
            "tier": "Beginner",
            "tier_emoji": "🌱",
            "tier_color": "#22c55e",
            "progress_to_next": progress,
            "requirements_met": [],
            "requirements_pending": [f"{5 - achieved_weeks} weeks to Bronze"]
        }
    
    return tier_data


def should_level_up(game_state: Dict) -> Tuple[bool, str]:
    """
    Sprawdza czy gracz spełnia kryteria awansu
    
    Kryteria awansu (przykład Level 1 → 2):
    - Miesięczna sprzedaż >= 50k PLN
    - 3+ aktywnych klientów
    - 4+ tygodnie z celem osiągniętym
    
    Returns:
        (should_level_up: bool, reason: str)
    """
    current_level = game_state.get("level", 1)
    
    # Level 1 → 2 requirements
    if current_level == 1:
        monthly_sales = game_state.get("monthly_actual_sales", 0)
        active_clients = game_state.get("clients_active", 0)
        weekly_history = game_state.get("weekly_history", [])
        achieved_weeks = sum(1 for w in weekly_history if w.get("target_achieved", False))
        
        if monthly_sales >= 50000 and active_clients >= 3 and achieved_weeks >= 4:
            return True, "Osiągnięto 50k sprzedaży, 3+ aktywnych klientów, 4+ tygodnie z celem"
        else:
            pending = []
            if monthly_sales < 50000:
                pending.append(f"Sprzedaż: {monthly_sales:,}/50,000 PLN")
            if active_clients < 3:
                pending.append(f"Klienci: {active_clients}/3")
            if achieved_weeks < 4:
                pending.append(f"Tygodnie: {achieved_weeks}/4")
            
            return False, " | ".join(pending)
    
    # For other levels (TODO: define criteria)
    return False, "Kryteria awansu nie zdefiniowane dla tego poziomu"
