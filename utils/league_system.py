# # -*- coding: utf-8 -*-
# """
# League and Ranking System
# System lig i rankingów dla BrainVenture Academy
# """

# import json
# import datetime
# from typing import Dict, List, Any, Optional
# from pathlib import Path

# class LeagueSystem:
#     """Zarządza systemem lig i rankingów"""
    
#     LEAGUES = {
#         "bronze": {
#             "name": "Liga Brązowa",
#             "min_xp": 0,
#             "max_xp": 999,
#             "color": "#CD7F32",
#             "icon": "🥉",
#             "weekly_reward": {"degencoins": 100, "xp": 50}
#         },
#         "silver": {
#             "name": "Liga Srebrna", 
#             "min_xp": 1000,
#             "max_xp": 2999,
#             "color": "#C0C0C0",
#             "icon": "🥈",
#             "weekly_reward": {"degencoins": 200, "xp": 100}
#         },
#         "gold": {
#             "name": "Liga Złota",
#             "min_xp": 3000,
#             "max_xp": 7999,
#             "color": "#FFD700", 
#             "icon": "🥇",
#             "weekly_reward": {"degencoins": 300, "xp": 150}
#         },
#         "platinum": {
#             "name": "Liga Platynowa",
#             "min_xp": 8000,
#             "max_xp": 19999,
#             "color": "#E5E4E2",
#             "icon": "💎",
#             "weekly_reward": {"degencoins": 500, "xp": 250}
#         },
#         "diamond": {
#             "name": "Liga Diamentowa",
#             "min_xp": 20000,
#             "max_xp": float('inf'),
#             "color": "#B9F2FF",
#             "icon": "💠",
#             "weekly_reward": {"degencoins": 1000, "xp": 500}
#         }
#     }
    
#     def __init__(self):
#         self.leaderboard_file = Path("data/leaderboard.json")
#         self.league_data_file = Path("data/league_data.json")
        
#     def get_user_league(self, total_xp: int) -> Dict[str, Any]:
#         """Określa ligę użytkownika na podstawie XP"""
#         for league_id, league_info in self.LEAGUES.items():
#             if league_info["min_xp"] <= total_xp <= league_info["max_xp"]:
#                 return {
#                     "league_id": league_id,
#                     "league_name": league_info["name"],
#                     "color": league_info["color"],
#                     "icon": league_info["icon"],
#                     "current_xp": total_xp,
#                     "next_league_xp": league_info["max_xp"] + 1 if league_info["max_xp"] != float('inf') else None,
#                     "progress_to_next": self._calculate_league_progress(total_xp, league_info)
#                 }
        
#         return self.LEAGUES["bronze"]  # Fallback
    
#     def _calculate_league_progress(self, current_xp: int, league_info: Dict[str, Any]) -> float:
#         """Oblicza postęp do następnej ligi"""
#         if league_info["max_xp"] == float('inf'):
#             return 100.0
        
#         league_range = league_info["max_xp"] - league_info["min_xp"]
#         current_progress = current_xp - league_info["min_xp"]
#         return min(100.0, (current_progress / league_range) * 100)
    
#     def get_league_leaderboard(self, league_id: str, limit: int = 10) -> List[Dict[str, Any]]:
#         """Pobiera ranking dla konkretnej ligi"""
#         # Implementacja pobierania rankingu z bazy danych
#         # Integracja z istniejącym systemem users_data.json
#         pass
    
#     def get_global_leaderboard(self, limit: int = 50) -> List[Dict[str, Any]]:
#         """Pobiera globalny ranking wszystkich użytkowników"""
#         # Implementacja globalnego rankingu
#         pass
    
#     def get_weekly_league_rewards(self, username: str) -> Dict[str, Any]:
#         """Oblicza tygodniowe nagrody ligowe"""
#         # Implementacja nagród tygodniowych
#         pass

# class RankingSystem:
#     """Zarządza różnymi typami rankingów"""
    
#     def __init__(self):
#         self.league_system = LeagueSystem()
    
#     def get_xp_ranking(self, limit: int = 10) -> List[Dict[str, Any]]:
#         """Ranking według XP"""
#         pass
    
#     def get_badge_ranking(self, limit: int = 10) -> List[Dict[str, Any]]:
#         """Ranking według liczby odznak"""
#         pass
    
#     def get_streak_ranking(self, limit: int = 10) -> List[Dict[str, Any]]:
#         """Ranking według najdłuższych streków"""
#         pass
    
#     def get_lesson_completion_ranking(self, limit: int = 10) -> List[Dict[str, Any]]:
#         """Ranking według ukończonych lekcji"""
#         pass
    
#     def get_monthly_active_ranking(self, limit: int = 10) -> List[Dict[str, Any]]:
#         """Ranking najaktywniejszych użytkowników tego miesiąca"""
#         pass

# # Integracja z dashboardem
# def add_league_display_to_dashboard():
#     """
#     Dodaje wyświetlanie ligi do dashboardu
#     Integruje się z istniejącym views/dashboard.py
#     """
#     league_system = LeagueSystem()
#     ranking_system = RankingSystem()
    
#     return {
#         "league_system": league_system,
#         "ranking_system": ranking_system
#     }
