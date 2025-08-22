# BADGE SYSTEM - STEP 3: Integration with Badge Tracking System
# =============================================================

import json
import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional, Union
from config.settings import BADGES, BADGE_CATEGORIES, BADGE_TIERS, XP_LEVELS

def check_badge_condition(badge_id: str, user_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> bool:
    """
    Sprawdź czy użytkownik spełnia warunki dla danej odznaki
    
    Args:
        badge_id: ID odznaki do sprawdzenia
        user_data: Dane użytkownika
        context: Kontekst wywołania (opcjonalny)
    
    Returns:
        bool: True jeśli warunki są spełnione
    """
    if badge_id not in BADGES:
        return False
    
    badge = BADGES[badge_id]
    condition = badge.get('condition')
    requirement = badge.get('requirement', 1)
    
    # ==========================================
    # KATEGORIA: GETTING STARTED
    # ==========================================
    
    if badge_id == "welcome":
        # Automatycznie przyznawane przy rejestracji
        return condition == "register_account" and user_data.get('user_id') is not None
    
    elif badge_id == "profile_complete":
        # Sprawdź czy profil jest kompletny
        required_fields = ['degen_type', 'avatar', 'theme']
        return all(user_data.get(field) for field in required_fields)
    
    elif badge_id == "first_degen_test":
        # Pierwszy test typu degena
        return user_data.get('test_taken', False) and user_data.get('degen_type') is not None
    
    elif badge_id == "first_lesson":
        # Pierwsza ukończona lekcja
        completed_lessons = user_data.get('completed_lessons', [])
        return len(completed_lessons) >= 1
    
    # ==========================================
    # KATEGORIA: LEARNING PROGRESS
    # ==========================================
    
    elif badge_id in ["lesson_rookie", "lesson_apprentice", "lesson_scholar", "lesson_master"]:
        # Odznaki za ukończenie określonej liczby lekcji
        completed_lessons = user_data.get('completed_lessons', [])
        return len(completed_lessons) >= requirement
    
    elif badge_id == "quiz_perfectionist":
        # Perfekcjonista - 100% w quizie
        if context and context.get('quiz_score') == 100:
            return True
        # Sprawdź poprzednie wyniki quizów
        lesson_progress = user_data.get('lesson_progress', {})
        for lesson_id, progress in lesson_progress.items():
            if progress.get('closing_quiz_score') == 100:
                return True
        return False
    
    elif badge_id == "speed_learner":
        # 3 lekcje w jeden dzień
        if context and context.get('lessons_in_day', 0) >= 3:
            return True
        # Sprawdź czy kiedykolwiek ukończył 3 lekcje w jeden dzień
        return check_lessons_per_day(user_data, 3)
    
    # ==========================================
    # KATEGORIA: ENGAGEMENT
    # ==========================================
    
    elif badge_id in ["login_streak_3", "login_streak_7", "login_streak_30"]:
        # Sprawdź streak logowania
        streak_required = requirement.get('streak', 0) if isinstance(requirement, dict) else 0
        if badge_id == "login_streak_3":
            streak_required = 3
        elif badge_id == "login_streak_7":
            streak_required = 7
        elif badge_id == "login_streak_30":
            streak_required = 30
        
        current_streak = user_data.get('login_streak', 0)
        return current_streak >= streak_required
    
    elif badge_id == "daily_mission_hero":
        # Wszystkie misje dzienne w jeden dzień
        if context and context.get('all_missions_in_day', False):
            return True
        return check_daily_missions_completion(user_data)
    
    elif badge_id == "weekend_scholar":
        # Nauka w weekend
        if context and context.get('is_weekend', False):
            return True
        return check_weekend_learning(user_data)
    
    elif badge_id == "night_owl":
        # Nauka po 22:00
        if context and context.get('hour', 0) >= 22:
            return True
        return check_late_learning(user_data)
    
    elif badge_id == "early_bird":
        # Nauka przed 8:00
        if context and context.get('hour', 24) < 8:
            return True
        return check_early_learning(user_data)
    
    # ==========================================
    # KATEGORIA: EXPERTISE
    # ==========================================
    
    elif badge_id in ["zen_master", "market_analyst", "strategy_guru", "psychology_expert"]:
        # Ukończenie wszystkich lekcji z kategorii
        category_map = {
            "zen_master": "mindfulness",
            "market_analyst": "market_analysis", 
            "strategy_guru": "strategies",
            "psychology_expert": "psychology"
        }
        target_category = category_map.get(badge_id)
        if target_category:
            return check_category_completion(user_data, target_category)
    
    elif badge_id in ["xp_collector", "xp_master"]:
        # Zgromadzenie określonej liczby XP
        total_xp = user_data.get('xp', 0)
        xp_required = 1000 if badge_id == "xp_collector" else 5000
        return total_xp >= xp_required
    
    # ==========================================
    # KATEGORIA: DEGEN MASTERY
    # ==========================================
    
    elif badge_id == "degen_explorer":
        # Poznanie wszystkich typów degenów
        return check_all_degen_types_explored(user_data)
    
    elif badge_id == "multi_degen":
        # 3 różne wyniki testów
        test_results = user_data.get('test_results_history', [])
        unique_results = set(result.get('degen_type') for result in test_results)
        return len(unique_results) >= 3
    
    elif badge_id == "self_aware":
        # Potwierdzenie typu degena
        return user_data.get('test_retaken', False) and user_data.get('degen_type_confirmed', False)
    
    elif badge_id == "degen_king":
        # Mistrzostwo we wszystkich aspektach
        return check_complete_degen_mastery(user_data)
    
    # ==========================================
    # KATEGORIA: SOCIAL
    # ==========================================
    
    elif badge_id == "community_member":
        # Dołączenie do społeczności
        return user_data.get('community_joined', False)
    
    elif badge_id == "helpful_friend":
        # Pomoc innemu użytkownikowi
        help_count = user_data.get('users_helped', 0)
        return help_count >= 1
    
    elif badge_id == "mentor":
        # Pomoc 5 użytkownikom
        help_count = user_data.get('users_helped', 0)
        return help_count >= 5
    
    elif badge_id == "influencer":
        # Udostępnienie osiągnięć
        return user_data.get('achievements_shared', 0) >= 1
    
    # ==========================================
    # KATEGORIA: ACHIEVEMENTS
    # ==========================================
    
    elif badge_id == "first_badge":
        # Pierwsza odznaka (automatycznie sprawdzane)
        return len(user_data.get('badges', [])) >= 1
    
    elif badge_id in ["badge_collector", "badge_master"]:
        # Kolekcjonowanie odznak
        badge_count = len(user_data.get('badges', []))
        required_count = 10 if badge_id == "badge_collector" else 25
        return badge_count >= required_count
    
    elif badge_id == "achievement_hunter":
        # Ukończenie całej kategorii odznak
        return check_category_badge_completion(user_data)
    
    # ==========================================
    # KATEGORIA: SPECIAL
    # ==========================================
    
    elif badge_id == "pioneer":
        # Jeden z pierwszych 100 użytkowników
        return check_early_adopter_status(user_data, 100)
    
    elif badge_id == "legend":
        # Wszystkie możliwe odznaki
        user_badges = set(user_data.get('badges', []))
        all_badges = set(BADGES.keys())
        return len(user_badges) == len(all_badges)
    
    elif badge_id == "dedicated_student":
        # 50 godzin nauki
        total_study_time = user_data.get('total_study_time_hours', 0)
        return total_study_time >= 50
    
    elif badge_id == "secret_discoverer":
        # Easter egg
        return user_data.get('easter_egg_found', False)
    
    elif badge_id == "midnight_learner":
        # Nauka o północy
        if context and context.get('hour') == 0:
            return True
        return check_midnight_learning(user_data)
    
    return False

def check_achievements(username: str, context: Optional[str] = None, **kwargs) -> List[str]:
    """
    Sprawdź wszystkie osiągnięcia użytkownika z integracją systemu śledzenia
    
    Args:
        username: Nazwa użytkownika
        context: Kontekst wywołania (opcjonalny)
        **kwargs: Dodatkowe dane kontekstowe
    
    Returns:
        List[str]: Lista nowo zdobytych odznak
    """
    print(f"🔍 DEBUG: check_achievements wywołane dla {username} z kontekstem: {context}")
    
    # Import here to avoid circular dependency
    try:
        from utils.badge_tracking import badge_tracker
        
        print("🔍 DEBUG: Używam nowego systemu badge_tracker")
        # Użyj nowego systemu śledzenia jeśli dostępny
        update_result = badge_tracker.update_badge_progress(username, kwargs, **kwargs)
        new_badges = update_result.get('new_badges', [])
        print(f"🔍 DEBUG: Badge tracker zwrócił: {new_badges}")
        return new_badges
        
    except ImportError as e:
        print(f"🔍 DEBUG: ImportError - używam fallback systemu: {e}")
        # Fallback do starego systemu
        user_data = load_user_data(username)
        if not user_data:
            return []
        
        current_badges = set(user_data.get('badges', []))
        new_badges = []
        context_data = kwargs if kwargs else {}
        
        print(f"🔍 DEBUG: Aktualne odznaki: {current_badges}")
        print(f"🔍 DEBUG: Sprawdzam odznaki dla kontekstu: {context_data}")
        
        # Sprawdź wszystkie możliwe odznaki
        for badge_id in BADGES.keys():
            if badge_id not in current_badges:
                if check_badge_condition(badge_id, user_data, context_data):
                    new_badges.append(badge_id)
                    current_badges.add(badge_id)
                    print(f"🔍 DEBUG: Znaleziono nową odznakę: {badge_id}")
        
        # Zapisz nowe odznaki
        if new_badges:
            user_data['badges'] = list(current_badges)
            
            # Dodaj XP za odznaki z uwzględnieniem tier multipliers
            total_xp = 0
            for badge_id in new_badges:
                badge = BADGES[badge_id]
                base_xp = badge.get('xp_reward', 0)
                tier = badge.get('tier', 'bronze')
                multiplier = BADGE_TIERS.get(tier, {}).get('multiplier', 1.0)
                badge_xp = int(base_xp * multiplier)
                total_xp += badge_xp
            
            user_data['xp'] = user_data.get('xp', 0) + total_xp
            
            # Sprawdź awanse poziomów
            check_level_up(user_data)
            
            # Zapisz aktywność
            print(f"🔍 DEBUG: Dodaję aktywność dla odznak: {new_badges}")
            add_badge_activity(user_data, new_badges)
            save_user_data(username, user_data)
            
            # Log nowych odznak
            print(f"🏅 Użytkownik {username} zdobył nowe odznaki: {', '.join(new_badges)} (+{total_xp} XP)")
        else:
            print("🔍 DEBUG: Brak nowych odznak")
        
        return new_badges

# ==========================================
# FUNKCJE POMOCNICZE
# ==========================================

def load_user_data(username: str) -> Dict[str, Any]:
    """Załaduj dane użytkownika"""
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            return users_data.get(username, {})
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}

def save_user_data(username: str, user_data: Dict[str, Any]) -> bool:
    """Zapisz dane użytkownika"""
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
        
        # Załaduj istniejące dane
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
        except FileNotFoundError:
            users_data = {}
        
        # Aktualizuj dane użytkownika
        users_data[username] = user_data
        
        # Zapisz
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False

def add_badge_activity(user_data: Dict[str, Any], new_badges: List[str]):
    """Dodaj aktywność o zdobytych odznakach"""
    # Użyj standardowej funkcji add_recent_activity
    try:
        from data.users_fixed import add_recent_activity
        import streamlit as st
        
        username = st.session_state.get('username')
        if username:
            badge_names = [BADGES[badge_id]['name'] for badge_id in new_badges]
            add_recent_activity(username, "badge_earned", {"badge_names": badge_names})
    except Exception as e:
        print(f"Error adding badge activity: {e}")
        # Fallback - dodaj lokalnie jak wcześniej (ale z poprawnym formatem)
        activity_entry = {
            "type": "badge_earned",
            "details": {"badge_names": [BADGES[badge_id]['name'] for badge_id in new_badges]},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        activities = user_data.get('recent_activities', [])
        activities.insert(0, activity_entry)
        user_data['recent_activities'] = activities[:10]  # Ostatnie 10

def check_level_up(user_data: Dict[str, Any]) -> Optional[int]:
    """Sprawdź czy użytkownik awansował na nowy poziom"""
    current_xp = user_data.get("xp", 0)
    current_level = user_data.get("level", 1)
    
    new_level = current_level
    for level, required_xp in sorted(XP_LEVELS.items()):
        if current_xp >= required_xp:
            new_level = level
    
    if new_level > current_level:
        user_data["level"] = new_level
        return new_level
    
    return None

# ==========================================
# SPECJALNE FUNKCJE SPRAWDZAJĄCE
# ==========================================

def check_lessons_per_day(user_data: Dict[str, Any], required_count: int) -> bool:
    """Sprawdź czy użytkownik ukończył określoną liczbę lekcji w jeden dzień"""
    lesson_progress = user_data.get('lesson_progress', {})
    lesson_dates = {}
    
    for lesson_id, progress in lesson_progress.items():
        # Sprawdź różne możliwe timestampy ukończenia
        completion_fields = ['summary_timestamp', 'closing_quiz_timestamp', 'content_timestamp']
        for field in completion_fields:
            if field in progress:
                try:
                    timestamp = datetime.fromisoformat(progress[field].replace(' ', 'T'))
                    date_str = timestamp.strftime('%Y-%m-%d')
                    lesson_dates[date_str] = lesson_dates.get(date_str, 0) + 1
                    break
                except:
                    continue
    
    return any(count >= required_count for count in lesson_dates.values())

def check_daily_missions_completion(user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy użytkownik ukończył wszystkie misje dzienne w jeden dzień"""
    # Implementacja zależna od struktury daily missions
    return user_data.get('daily_missions_completed_in_day', False)

def check_weekend_learning(user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy użytkownik uczył się w weekend"""
    lesson_progress = user_data.get('lesson_progress', {})
    
    for lesson_id, progress in lesson_progress.items():
        completion_fields = ['summary_timestamp', 'closing_quiz_timestamp', 'content_timestamp']
        for field in completion_fields:
            if field in progress:
                try:
                    timestamp = datetime.fromisoformat(progress[field].replace(' ', 'T'))
                    if timestamp.weekday() >= 5:  # Sobota = 5, Niedziela = 6
                        return True
                except:
                    continue
    
    return False

def check_late_learning(user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy użytkownik uczył się po 22:00"""
    lesson_progress = user_data.get('lesson_progress', {})
    
    for lesson_id, progress in lesson_progress.items():
        completion_fields = ['summary_timestamp', 'closing_quiz_timestamp', 'content_timestamp']
        for field in completion_fields:
            if field in progress:
                try:
                    timestamp = datetime.fromisoformat(progress[field].replace(' ', 'T'))
                    if timestamp.hour >= 22:
                        return True
                except:
                    continue
    
    return False

def check_early_learning(user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy użytkownik uczył się przed 8:00"""
    lesson_progress = user_data.get('lesson_progress', {})
    
    for lesson_id, progress in lesson_progress.items():
        completion_fields = ['summary_timestamp', 'closing_quiz_timestamp', 'content_timestamp']
        for field in completion_fields:
            if field in progress:
                try:
                    timestamp = datetime.fromisoformat(progress[field].replace(' ', 'T'))
                    if timestamp.hour < 8:
                        return True
                except:
                    continue
    
    return False

def check_midnight_learning(user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy użytkownik uczył się dokładnie o północy"""
    lesson_progress = user_data.get('lesson_progress', {})
    
    for lesson_id, progress in lesson_progress.items():
        completion_fields = ['summary_timestamp', 'closing_quiz_timestamp', 'content_timestamp']
        for field in completion_fields:
            if field in progress:
                try:
                    timestamp = datetime.fromisoformat(progress[field].replace(' ', 'T'))
                    if timestamp.hour == 0 and timestamp.minute == 0:
                        return True
                except:
                    continue
    
    return False

def check_category_completion(user_data: Dict[str, Any], category: str) -> bool:
    """Sprawdź czy użytkownik ukończył wszystkie lekcje z kategorii"""
    # Implementacja zależna od struktury kategorii w course_data
    # Zwraca False jako placeholder - wymaga integracji z course_data
    return False

def check_all_degen_types_explored(user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy użytkownik poznał wszystkie typy degenów"""
    explored_types = user_data.get('explored_degen_types', [])
    from config.settings import DEGEN_TYPES
    return len(explored_types) >= len(DEGEN_TYPES)

def check_complete_degen_mastery(user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy użytkownik osiągnął pełne mistrzostwo degena"""
    required_conditions = [
        user_data.get('test_taken', False),
        user_data.get('degen_type_confirmed', False),
        len(user_data.get('explored_degen_types', [])) >= 8,
        user_data.get('degen_strategies_created', 0) >= 3
    ]
    return all(required_conditions)

def check_category_badge_completion(user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy użytkownik ukończył wszystkie odznaki z jakiejś kategorii"""
    user_badges = set(user_data.get('badges', []))
    
    for category_id, category_info in BADGE_CATEGORIES.items():
        category_badges = [badge_id for badge_id, badge in BADGES.items() 
                          if badge.get('category') == category_id]
        if all(badge_id in user_badges for badge_id in category_badges):
            return True
    
    return False

def check_early_adopter_status(user_data: Dict[str, Any], user_limit: int) -> bool:
    """Sprawdź czy użytkownik jest wczesnym adopter"""
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        # Sortuj użytkowników po dacie dołączenia
        users_by_date = sorted(
            users_data.items(),
            key=lambda x: x[1].get('joined_date', '9999-12-31')
        )
        
        # Sprawdź czy user jest w pierwszych {user_limit}
        user_position = next(
            (i for i, (username, _) in enumerate(users_by_date) 
             if users_data.get(username) == user_data), 
            user_limit + 1
        )
        
        return user_position < user_limit
    except:
        return False

# ==========================================
# FUNKCJE KOMPATYBILNOŚCI
# ==========================================

def add_xp(username: str, xp_amount: int):
    """Dodaj XP użytkownikowi (kompatybilność wsteczna)"""
    user_data = load_user_data(username)
    if not user_data:
        return False, 1
    
    current_xp = user_data.get("xp", 0)
    current_level = user_data.get("level", 1)
    
    # Dodaj XP
    new_xp = current_xp + xp_amount
    user_data["xp"] = new_xp
    
    # Sprawdź awanse
    new_level = check_level_up(user_data)
    
    # Zapisz dane
    save_user_data(username, user_data)
    
    if new_level and new_level > current_level:
        return True, new_level
    
    return False, current_level

# ==========================================
# ENHANCED FUNCTIONS FOR STEP 3 INTEGRATION
# ==========================================

def get_detailed_badge_progress(username: str, badge_id: str) -> Dict[str, Any]:
    """
    Pobierz szczegółowy postęp odznaki z nowym systemem śledzenia
    
    Args:
        username: Nazwa użytkownika  
        badge_id: ID odznaki
    
    Returns:
        Dict ze szczegółowym postępem
    """
    try:
        from utils.badge_tracking import badge_tracker
        return badge_tracker.get_badge_progress_detailed(username, badge_id)
    except ImportError:
        # Fallback do podstawowego sprawdzenia
        user_data = load_user_data(username)
        if not user_data or badge_id not in BADGES:
            return {'error': 'User or badge not found'}
        
        if badge_id in user_data.get('badges', []):
            return {'badge_id': badge_id, 'status': 'earned', 'progress': 100}
        
        # Podstawowa ocena postępu
        condition_met = check_badge_condition(badge_id, user_data, {})
        return {
            'badge_id': badge_id,
            'status': 'in_progress' if not condition_met else 'ready',
            'progress': 100 if condition_met else 0
        }

def get_badge_recommendations_enhanced(username: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Pobierz rekomendacje odznak z nowym systemem
    
    Args:
        username: Nazwa użytkownika
        limit: Limit rekomendacji
    
    Returns:
        Lista rekomendowanych odznak
    """
    try:
        from utils.badge_tracking import badge_tracker
        return badge_tracker.get_recommended_badges(username, limit)
    except ImportError:
        # Podstawowe rekomendacje
        user_data = load_user_data(username)
        if not user_data:
            return []
        
        recommendations = []
        user_badges = set(user_data.get('badges', []))
        
        # Znajdź odznaki blisko ukończenia
        for badge_id, badge_info in BADGES.items():
            if badge_id not in user_badges and len(recommendations) < limit:
                # Sprawdź czy warunki są blisko spełnienia
                if _is_badge_achievable_soon(badge_id, user_data):
                    badge_copy = badge_info.copy()
                    badge_copy['badge_id'] = badge_id
                    recommendations.append(badge_copy)
        
        return recommendations

def _is_badge_achievable_soon(badge_id: str, user_data: Dict[str, Any]) -> bool:
    """Sprawdź czy odznaka jest osiągalna wkrótce"""
    badge_info = BADGES.get(badge_id, {})
    category = badge_info.get('category', '')
    
    # Podstawowe heurystyki
    if category == 'getting_started':
        return True  # Zawsze łatwe do zdobycia
    
    if 'lesson' in badge_id:
        completed = len(user_data.get('completed_lessons', []))
        requirement = badge_info.get('requirement', 1)
        if isinstance(requirement, int):
            return completed >= requirement * 0.7  # 70% postępu
    
    if 'xp' in badge_id:
        current_xp = user_data.get('xp', 0)
        return current_xp >= 500  # Ma trochę XP
    
    return False

def get_user_badge_statistics(username: str) -> Dict[str, Any]:
    """
    Pobierz statystyki odznak użytkownika
    
    Args:
        username: Nazwa użytkownika
    
    Returns:
        Dict ze statystykami odznak
    """
    try:
        from utils.badge_tracking import badge_tracker
        return badge_tracker.get_badge_statistics(username)
    except ImportError:
        # Podstawowe statystyki
        user_data = load_user_data(username)
        if not user_data:
            return {'error': 'User not found'}
        
        user_badges = user_data.get('badges', [])
        
        # Oblicz podstawowe statystyki
        stats = {
            'total_earned': len(user_badges),
            'categories': {},
            'tiers': {'bronze': 0, 'silver': 0, 'gold': 0, 'platinum': 0, 'diamond': 0},
            'total_xp': 0
        }
        
        # Analiza według kategorii i tier
        for badge_id in user_badges:
            if badge_id in BADGES:
                badge_info = BADGES[badge_id]
                category = badge_info.get('category', 'unknown')
                tier = badge_info.get('tier', 'bronze')
                xp = badge_info.get('xp_reward', 0)
                
                # Zlicz kategorie
                if category not in stats['categories']:
                    stats['categories'][category] = 0
                stats['categories'][category] += 1
                
                # Zlicz tier
                stats['tiers'][tier] += 1
                
                # Dodaj XP
                multiplier = BADGE_TIERS.get(tier, {}).get('multiplier', 1.0)
                stats['total_xp'] += int(xp * multiplier)
        
        return stats

# ==========================================
# ENHANCED MIGRATION AND UTILITY FUNCTIONS  
# ==========================================

def migrate_user_badge_data(username: str) -> bool:
    """
    Migruj dane odznak użytkownika do nowego formatu
    
    Args:
        username: Nazwa użytkownika
    
    Returns:
        bool: Sukces migracji
    """
    try:
        from utils.badge_tracking import badge_tracker
        
        # Pobierz dane i wymuś migrację przez cache miss
        badge_data = badge_tracker.get_user_badge_data(username, use_cache=False)
        
        # Zapisz zmigrowane dane
        user_data = load_user_data(username)
        if user_data:
            badge_tracker._save_badge_data(username, user_data, badge_data)
            return True
        
        return False
        
    except ImportError:
        print("Badge tracking system not available for migration")
        return False

def validate_badge_data_integrity(username: str) -> Dict[str, Any]:
    """
    Waliduj integralność danych odznak użytkownika
    
    Args:
        username: Nazwa użytkownika
    
    Returns:
        Dict z wynikami walidacji
    """
    user_data = load_user_data(username)
    if not user_data:
        return {'error': 'User not found'}
    
    validation_results = {
        'valid': True,
        'issues': [],
        'recommendations': []
    }
    
    user_badges = user_data.get('badges', [])
    
    # Sprawdź czy wszystkie odznaki istnieją w konfiguracji
    for badge_id in user_badges:
        if badge_id not in BADGES:
            validation_results['valid'] = False
            validation_results['issues'].append(f"Badge '{badge_id}' not found in configuration")
    
    # Sprawdź czy użytkownik nie ma duplikatów
    if len(user_badges) != len(set(user_badges)):
        validation_results['valid'] = False
        validation_results['issues'].append("Duplicate badges found")
        validation_results['recommendations'].append("Remove duplicate badges")
    
    # Sprawdź XP z odznak
    expected_badge_xp = 0
    for badge_id in user_badges:
        if badge_id in BADGES:
            badge_info = BADGES[badge_id]
            base_xp = badge_info.get('xp_reward', 0)
            tier = badge_info.get('tier', 'bronze')
            multiplier = BADGE_TIERS.get(tier, {}).get('multiplier', 1.0)
            expected_badge_xp += int(base_xp * multiplier)
    
    # Sprawdź logiczność warunków odznak
    for badge_id in user_badges:
        if badge_id in BADGES:
            # Re-sprawdź warunki odznaki
            condition_met = check_badge_condition(badge_id, user_data, {})
            if not condition_met:
                validation_results['issues'].append(f"Badge '{badge_id}' earned but conditions not met")
                validation_results['recommendations'].append(f"Re-validate badge '{badge_id}' conditions")
    
    return validation_results