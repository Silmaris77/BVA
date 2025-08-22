import streamlit as st
from data.users import load_user_data, save_user_data
import time

def get_live_user_stats(username):
    """Pobierz aktualne statystyki użytkownika w czasie rzeczywistym"""
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    return {
        'xp': user_data.get('xp', 0),
        'level': calculate_level_from_xp(user_data.get('xp', 0)),
        'completed_lessons': user_data.get('completed_lessons', []),
        'lesson_progress': user_data.get('lesson_progress', {}),
        'skills': user_data.get('skills', {}),
        'achievements': user_data.get('achievements', [])
    }

def calculate_level_from_xp(xp):
    """Oblicz poziom na podstawie XP"""
    # Prosta formuła poziomu: każde 100 XP = 1 poziom
    return max(1, (xp // 100) + 1)

def get_xp_for_next_level(current_xp):
    """Oblicz ile XP potrzeba do następnego poziomu"""
    current_level = calculate_level_from_xp(current_xp)
    next_level_xp = current_level * 100
    return next_level_xp - current_xp

@st.cache_data(ttl=1)  # Cache na 1 sekundę dla lepszej wydajności
def get_cached_user_stats(username, timestamp):
    """Pobierz statystyki użytkownika z krótkim cache"""
    return get_live_user_stats(username)

def refresh_user_data():
    """Odśwież dane użytkownika w session_state"""
    if 'username' in st.session_state and st.session_state.username:
        users_data = load_user_data()
        user_data = users_data.get(st.session_state.username, {})
        st.session_state.user_data = user_data
        return user_data
    return None

def update_user_xp(xp_to_add):
    """Dodaj XP do użytkownika i odśwież dane"""
    users_data = load_user_data()
    username = st.session_state.username
    
    if username in users_data:
        user_data = users_data[username]
        current_xp = user_data.get('xp', 0)
        user_data['xp'] = current_xp + xp_to_add
        
        # Zapisz do pliku
        users_data[username] = user_data
        save_user_data(users_data)
        
        # Odśwież session_state
        st.session_state.user_data = user_data
        
        return user_data['xp']
    return 0

def live_xp_indicator():
    """Pokaż aktualny XP użytkownika w czasie rzeczywistym"""
    if 'username' in st.session_state:
        stats = get_live_user_stats(st.session_state.username)
        xp_to_next = get_xp_for_next_level(stats['xp'])
        
        st.markdown(f"""
        <div style="position: fixed; top: 10px; right: 10px; 
                    background: rgba(102, 126, 234, 0.9); color: white; 
                    padding: 10px; border-radius: 10px; z-index: 1000;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.3);">
            <div style="font-size: 14px; font-weight: bold;">
                💎 {stats['xp']} XP | 🏆 Level {stats['level']}
            </div>
            <div style="font-size: 12px; opacity: 0.9;">
                {xp_to_next} XP do następnego poziomu
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_xp_notification(xp_amount, reason=""):
    """Pokaż animowaną notyfikację o otrzymaniu XP lub ukończeniu"""
    if xp_amount > 0:
        # Standard XP notification
        st.markdown(f"""
        <div style="position: fixed; top: 50%; left: 50%; 
                    transform: translate(-50%, -50%);
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; padding: 20px; border-radius: 15px;
                    text-align: center; z-index: 2000;
                    animation: bounceIn 0.6s ease-out;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 24px; font-weight: bold;">
                🎉 +{xp_amount} XP!
            </div>
            {f'<div style="font-size: 16px; margin-top: 5px;">{reason}</div>' if reason else ''}
        </div>
        <style>
        @keyframes bounceIn {{
            0% {{ transform: translate(-50%, -50%) scale(0.3); opacity: 0; }}
            50% {{ transform: translate(-50%, -50%) scale(1.1); }}
            100% {{ transform: translate(-50%, -50%) scale(1); opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    elif reason:
        # General completion notification (no XP)
        st.markdown(f"""
        <div style="position: fixed; top: 50%; left: 50%; 
                    transform: translate(-50%, -50%);
                    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                    color: white; padding: 20px; border-radius: 15px;
                    text-align: center; z-index: 2000;
                    animation: bounceIn 0.6s ease-out;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 20px; font-weight: bold;">
                {reason}
            </div>
        </div>
        <style>
        @keyframes bounceIn {{
            0% {{ transform: translate(-50%, -50%) scale(0.3); opacity: 0; }}
            50% {{ transform: translate(-50%, -50%) scale(1.1); }}
            100% {{ transform: translate(-50%, -50%) scale(1); opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Automatycznie ukryj po 3 sekundach
        time.sleep(3)

def invalidate_user_cache():
    """Wyczyść cache danych użytkownika"""
    # Since we don't use cached functions anymore, this is a no-op
    pass
