import json
import os
import uuid
from datetime import datetime, timezone
import streamlit as st

def save_user_data(users_data):
    """Save user data to JSON file"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2, ensure_ascii=False)

def load_user_data():
    """Load user data from JSON file"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def register_user(username, password, password_confirm):
    """Register a new user"""
    users_data = load_user_data()
    if username in users_data:
        return "Username already taken!"
    elif password != password_confirm:
        return "Passwords do not match!"
    elif not username or not password:
        return "Username and password are required!"
    else:
        user_id = str(uuid.uuid4())
        users_data[username] = {
            "user_id": user_id,
            "password": password,
            "degen_type": None,
            "xp": 0,
            "degencoins": 0,
            "level": 1,
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "last_login": None,  # Będzie ustawione przy pierwszym logowaniu
            "completed_lessons": [],
            "badges": [],
            "test_taken": False,
            # Nowe pola dla Inspiracji
            "inspirations": {
                "read": [],      # Lista ID przeczytanych inspiracji
                "favorites": []  # Lista ID ulubionych inspiracji
            }
        }
        save_user_data(users_data)
        return "Registration successful!"

def login_user(username, password):
    """Login a user"""
    users_data = load_user_data()
    if username in users_data and users_data[username]["password"] == password:
        # Zaktualizuj datę ostatniego logowania
        users_data[username]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_user_data(users_data)
        return users_data[username]
    return None

def update_user_xp(username, xp_amount):
    """Update user's XP and level"""
    users_data = load_user_data()
    if username in users_data:
        users_data[username]["xp"] += xp_amount
        save_user_data(users_data)
        return True
    return False

def update_single_user_field(username, field_name, field_value):
    """Update a single field in a user's data"""
    users_data = load_user_data()
    if username in users_data:
        users_data[username][field_name] = field_value
        save_user_data(users_data)
        return True
    return False

def get_current_user_data(username=None):
    """Get current user data with safe defaults"""
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return {}
    
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    # Ensure inspirations data exists with default structure
    if 'inspirations' not in user_data:
        user_data['inspirations'] = {
            'read': [],
            'favorites': []
        }
        users_data[username] = user_data
        save_user_data(users_data)
    
    return user_data

# Nowe funkcje dla Inspiracji
def save_user_inspiration_data(username, read_list=None, favorites_list=None):
    """Save user's inspiration read/favorite data"""
    if not username:
        return False
    
    users_data = load_user_data()
    if username not in users_data:
        return False
    
    # Initialize inspirations data if not exists
    if 'inspirations' not in users_data[username]:
        users_data[username]['inspirations'] = {'read': [], 'favorites': []}
    
    # Update read list if provided
    if read_list is not None:
        users_data[username]['inspirations']['read'] = read_list
    
    # Update favorites list if provided  
    if favorites_list is not None:
        users_data[username]['inspirations']['favorites'] = favorites_list
    
    save_user_data(users_data)
    return True

def get_user_read_inspirations(username=None):
    """Get list of user's read inspirations"""
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return []
    
    user_data = get_current_user_data(username)
    return user_data.get('inspirations', {}).get('read', [])

def get_user_favorite_inspirations(username=None):
    """Get list of user's favorite inspirations"""
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return []
    
    user_data = get_current_user_data(username)
    return user_data.get('inspirations', {}).get('favorites', [])

def mark_inspiration_as_read_for_user(inspiration_id, username=None):
    """Mark inspiration as read for specific user"""
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return False
    
    read_list = get_user_read_inspirations(username)
    if inspiration_id not in read_list:
        read_list.append(inspiration_id)
        return save_user_inspiration_data(username, read_list=read_list)
    
    return True

def toggle_inspiration_favorite_for_user(inspiration_id, username=None):
    """Toggle inspiration favorite status for specific user"""
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return False
    
    favorites_list = get_user_favorite_inspirations(username)
    
    if inspiration_id in favorites_list:
        # Remove from favorites
        favorites_list.remove(inspiration_id)
    else:
        # Add to favorites
        favorites_list.append(inspiration_id)
    
    return save_user_inspiration_data(username, favorites_list=favorites_list)

def is_inspiration_read_by_user(inspiration_id, username=None):
    """Check if inspiration is read by specific user"""
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return False
    
    read_list = get_user_read_inspirations(username)
    return inspiration_id in read_list

def is_inspiration_favorite_by_user(inspiration_id, username=None):
    """Check if inspiration is favorite by specific user"""
    if username is None:
        username = st.session_state.get('username')
    
    if not username:
        return False
    
    favorites_list = get_user_favorite_inspirations(username)
    return inspiration_id in favorites_list
