"""
Adapter - Compatibility Layer
Zapewnia kompatybilność wsteczną z istniejącym kodem używającym data.users

Ten plik pozwala istniejącemu kodowi działać bez zmian, jednocześnie
korzystając z nowej warstwy Repository w tle.
"""

import sys
from pathlib import Path

# Import nowego repository
from data.repositories import UserRepository

# Singleton instance
_user_repo = None


def _get_repo():
    """Pobiera singleton instance repository"""
    global _user_repo
    if _user_repo is None:
        _user_repo = UserRepository()
    return _user_repo


# =============================================================================
# COMPATIBILITY FUNCTIONS - Zachowują starą sygnaturę
# =============================================================================

def save_user_data(users_data):
    """
    Save all users data to storage (COMPATIBILITY FUNCTION)
    
    NOTE: Ta funkcja jest zachowana dla kompatybilności wstecznej.
    W nowym kodzie używaj UserRepository.save()
    
    Args:
        users_data: Dict {username: user_data}
    """
    repo = _get_repo()
    
    # Zapisz każdego użytkownika osobno
    success = True
    for username, user_data in users_data.items():
        if not repo.save(username, user_data):
            success = False
    
    return success


def load_user_data():
    """
    Load all users data from storage (COMPATIBILITY FUNCTION)
    
    NOTE: Ta funkcja jest zachowana dla kompatybilności wstecznej.
    W nowym kodzie używaj UserRepository.get_all()
    
    Returns:
        Dict: {username: user_data}
    """
    repo = _get_repo()
    return repo.get_all()


# Pozostałe funkcje - bez zmian, bo już używają pojedynczego użytkownika
def register_user(username, password, password_confirm):
    """Register a new user"""
    repo = _get_repo()
    users_data = repo.get_all()
    
    if username in users_data:
        return "Username already taken!"
    elif password != password_confirm:
        return "Passwords do not match!"
    elif not username or not password:
        return "Username and password are required!"
    else:
        import uuid
        from datetime import datetime
        
        user_id = str(uuid.uuid4())
        new_user_data = {
            "user_id": user_id,
            "password": password,
            "degen_type": None,
            "xp": 0,
            "degencoins": 0,
            "level": 1,
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "last_login": None,
            "completed_lessons": [],
            "badges": [],
            "test_taken": False,
            "inspirations": {
                "read": [],
                "favorites": []
            },
            "daily_stats": {}
        }
        
        # Zapisz przez repository
        if repo.save(username, new_user_data):
            # Inicjalizuj dostęp do lekcji
            initialize_lesson_access_for_new_user(username)
            return "Registration successful!"
        else:
            return "Registration failed!"


def initialize_lesson_access_for_new_user(username):
    """Zainicjalizuj domyślny dostęp do lekcji dla nowego użytkownika"""
    from data.lessons import load_lessons
    
    repo = _get_repo()
    user_data = repo.get(username)
    
    if not user_data:
        return False
    
    if 'lesson_access' not in user_data:
        lessons = load_lessons()
        user_data['lesson_access'] = {}
        
        for lesson_id in lessons.keys():
            if "Wprowadzenie" in lesson_id or "wprowadzenie" in lesson_id.lower():
                user_data['lesson_access'][lesson_id] = True
            else:
                if "Mózg emocjonalny" in lesson_id:
                    user_data['lesson_access'][lesson_id] = False
                else:
                    user_data['lesson_access'][lesson_id] = True
        
        repo.save(username, user_data)
        return True
    
    return False


def login_user(username, password):
    """Login a user"""
    repo = _get_repo()
    user_data = repo.get(username)
    
    if user_data and user_data.get("password") == password:
        from datetime import datetime
        
        # Zaktualizuj datę ostatniego logowania
        user_data["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        repo.save(username, user_data)
        
        # Zapisz dzisiejsze statystyki
        try:
            from views.dashboard import save_daily_stats
            save_daily_stats(username)
        except ImportError:
            pass
        
        # Zaloguj aktywność
        try:
            from utils.activity_tracker import log_activity
            log_activity(username, 'login', {
                'timestamp': datetime.now().isoformat()
            })
        except ImportError:
            pass
        
        return user_data
    
    return None


def update_user_xp(username, xp_amount):
    """Update user's XP and level"""
    repo = _get_repo()
    user_data = repo.get(username)
    
    if user_data:
        user_data["xp"] = user_data.get("xp", 0) + xp_amount
        repo.save(username, user_data)
        
        # Aktualizuj dzisiejsze statystyki
        try:
            from views.dashboard import update_daily_stats_if_needed
            update_daily_stats_if_needed(username)
        except ImportError:
            pass
        
        return True
    
    return False


def award_xp_for_activity(username: str, activity_type: str, xp_amount: int, details = None):
    """
    Zunifikowana funkcja do przyznawania XP i logowania aktywności
    """
    if not username:
        return False
    
    success = update_user_xp(username, xp_amount)
    
    if success:
        try:
            from utils.activity_tracker import log_activity
            activity_details = details or {}
            activity_details['xp_earned'] = xp_amount
            log_activity(username, activity_type, activity_details)
        except ImportError:
            pass
    
    return success


def update_single_user_field(username, field_name, field_value):
    """Update a single field in a user's data"""
    repo = _get_repo()
    user_data = repo.get(username)
    
    if user_data:
        user_data[field_name] = field_value
        return repo.save(username, user_data)
    
    return False


def get_current_user_data(username=None):
    """Get current user data with safe defaults"""
    import streamlit as st
    
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return {}
    
    repo = _get_repo()
    user_data = repo.get(username)
    
    if not user_data:
        return {}
    
    # Ensure inspirations data exists
    if 'inspirations' not in user_data:
        user_data['inspirations'] = {
            'read': [],
            'favorites': []
        }
        repo.save(username, user_data)
    
    return user_data


# =============================================================================
# INSPIRATIONS FUNCTIONS
# =============================================================================

def save_user_inspiration_data(username, read_list=None, favorites_list=None):
    """Save user's inspiration read/favorite data"""
    if not username:
        return False
    
    repo = _get_repo()
    user_data = repo.get(username)
    
    if not user_data:
        return False
    
    if 'inspirations' not in user_data:
        user_data['inspirations'] = {'read': [], 'favorites': []}
    
    if read_list is not None:
        user_data['inspirations']['read'] = read_list
    
    if favorites_list is not None:
        user_data['inspirations']['favorites'] = favorites_list
    
    return repo.save(username, user_data)


def get_user_read_inspirations(username=None):
    """Get list of user's read inspirations"""
    import streamlit as st
    
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return []
    
    user_data = get_current_user_data(username)
    return user_data.get('inspirations', {}).get('read', [])


def get_user_favorite_inspirations(username=None):
    """Get list of user's favorite inspirations"""
    import streamlit as st
    
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return []
    
    user_data = get_current_user_data(username)
    return user_data.get('inspirations', {}).get('favorites', [])


def mark_inspiration_as_read_for_user(inspiration_id, username=None):
    """Mark inspiration as read for specific user"""
    import streamlit as st
    
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return False
    
    read_list = get_user_read_inspirations(username)
    if inspiration_id not in read_list:
        read_list.append(inspiration_id)
        result = save_user_inspiration_data(username, read_list=read_list)
        
        if result:
            try:
                from utils.inspirations_loader import get_inspiration_by_id
                inspiration = get_inspiration_by_id(inspiration_id)
                inspiration_title = inspiration.get('title', 'Nieznany artykuł') if inspiration else 'Nieznany artykuł'
                
                from data.users_fixed import add_recent_activity
                add_recent_activity(username, "inspiration_read", {
                    "inspiration_id": inspiration_id,
                    "inspiration_title": inspiration_title
                })
                
                from utils.activity_tracker import log_activity
                log_activity(username, 'inspiration_read', {
                    'inspiration_id': inspiration_id,
                    'inspiration_title': inspiration_title
                })
            except Exception as e:
                print(f"Error adding inspiration read activity: {e}")
        
        return result
    
    return True


def toggle_inspiration_favorite_for_user(inspiration_id, username=None):
    """Toggle inspiration favorite status for specific user"""
    import streamlit as st
    
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return False
    
    favorites_list = get_user_favorite_inspirations(username)
    
    if inspiration_id in favorites_list:
        favorites_list.remove(inspiration_id)
    else:
        favorites_list.append(inspiration_id)
    
    return save_user_inspiration_data(username, favorites_list=favorites_list)


def is_inspiration_read_by_user(inspiration_id, username=None):
    """Check if inspiration is read by specific user"""
    import streamlit as st
    
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return False
    
    read_list = get_user_read_inspirations(username)
    return inspiration_id in read_list


def is_inspiration_favorite_by_user(inspiration_id, username=None):
    """Check if inspiration is favorite by specific user"""
    import streamlit as st
    
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return False
    
    favorites_list = get_user_favorite_inspirations(username)
    return inspiration_id in favorites_list


# =============================================================================
# HELPER FUNCTION - Save single user
# =============================================================================

def save_single_user(username, user_data):
    """
    Save single user data (helper for compatibility)
    
    Args:
        username: Username
        user_data: User data dict
    
    Returns:
        bool: True if successful
    """
    repo = _get_repo()
    return repo.save(username, user_data)
