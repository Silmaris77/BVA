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
            "completed_lessons": [],
            "badges": [],
            "test_taken": False
        }
        save_user_data(users_data)
        return "Registration successful!"

def login_user(username, password):
    """Login a user"""
    users_data = load_user_data()
    if username in users_data and users_data[username]["password"] == password:
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

def get_current_user_data(username: str = None):
    """Get current user data, ensuring 'recent_activities' exists."""
    if username is None and 'username' in st.session_state:
        username = st.session_state.username
    elif username is None:
        return None # Or raise an error, or return a default guest structure

    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    # Ensure 'recent_activities' list exists
    if 'recent_activities' not in user_data:
        user_data['recent_activities'] = []
        # Save the updated user data back to the file
        users_data[username] = user_data
        save_user_data(users_data)
    return user_data

def add_recent_activity(username: str, activity_type: str, details: dict):
    """Add a new recent activity for a user, ensuring timestamp is UTC ISO format."""
    users_data = load_user_data()
    if username not in users_data:
        print(f"Error: User {username} not found. Cannot add activity.")
        return

    # Validate degen type if it's a degen_type_discovered activity
    if activity_type == "degen_type_discovered":
        degen_type = details.get("degen_type")
        if not _validate_degen_type(degen_type):
            print(f"Warning: Invalid degen type '{degen_type}'. Using user's actual degen type.")
            # Use the user's actual degen type instead
            actual_degen_type = users_data[username].get("degen_type")
            if actual_degen_type:
                details["degen_type"] = actual_degen_type
            else:
                print(f"Error: No valid degen type found for user {username}")
                return

    # Ensure 'recent_activities' list exists for the user
    if 'recent_activities' not in users_data[username]:
        users_data[username]['recent_activities'] = []

    activity_entry = {
        "type": activity_type,
        "details": details,
        "timestamp": datetime.now(timezone.utc).isoformat() # Store as UTC ISO string
    }
    
    users_data[username]['recent_activities'].insert(0, activity_entry)
    # Keep only the latest N activities (e.g., 10 or 20)
    users_data[username]['recent_activities'] = users_data[username]['recent_activities'][:20]
    
    save_user_data(users_data)

def _validate_degen_type(degen_type):
    """Validate if the degen type is valid"""
    try:
        from data.test_questions import DEGEN_TYPES
        return degen_type in DEGEN_TYPES
    except ImportError:
        # If we can't import DEGEN_TYPES, accept any string
        return isinstance(degen_type, str) and len(degen_type) > 0
