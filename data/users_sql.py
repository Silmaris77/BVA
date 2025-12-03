"""
Pure SQL User Management - NO JSON
Zastępuje data.users i data.users_new
"""

from typing import Optional, Dict, Any
from datetime import datetime
from database.models import User
from database.connection import session_scope


def login_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Login user - pure SQL
    
    Args:
        username: Username
        password: Plain text password (TODO: hash comparison)
    
    Returns:
        User data dict or None
    """
    try:
        with session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            
            if user and user.password_hash == password:  # TODO: proper hash comparison
                # Update last login
                user.last_login = datetime.now()
                session.commit()
                
                # Return user data as dict
                return user.to_dict()
            
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None


def register_user(username: str, password: str, **kwargs) -> bool:
    """
    Register new user - pure SQL
    
    Args:
        username: Username
        password: Password
        **kwargs: Additional user fields
    
    Returns:
        True if successful
    """
    try:
        with session_scope() as session:
            # Check if exists
            existing = session.query(User).filter_by(username=username).first()
            if existing:
                return False
            
            # Create new user
            import uuid
            new_user = User(
                user_id=str(uuid.uuid4()),
                username=username,
                password_hash=password,  # TODO: hash password
                xp=kwargs.get('xp', 0),
                level=kwargs.get('level', 1),
                degencoins=kwargs.get('degencoins', 0),
                test_taken=kwargs.get('test_taken', False),
                company=kwargs.get('company'),
                permissions=kwargs.get('permissions'),
                joined_date=datetime.now().date()
            )
            
            session.add(new_user)
            session.commit()
            return True
            
    except Exception as e:
        print(f"Registration error: {e}")
        return False


def load_user_data() -> Dict[str, Any]:
    """
    Load all users - pure SQL
    
    Returns:
        Dict {username: user_data}
    """
    try:
        result = {}
        with session_scope() as session:
            users = session.query(User).all()
            for user in users:
                result[user.username] = user.to_dict()
        return result
    except Exception as e:
        print(f"Load users error: {e}")
        return {}


def save_user_data(users_data: Dict[str, Any]) -> bool:
    """
    Save all users - pure SQL
    DEPRECATED: Use save_single_user instead
    
    Args:
        users_data: Dict {username: user_data}
    
    Returns:
        True if successful
    """
    try:
        with session_scope() as session:
            for username, user_data in users_data.items():
                user = session.query(User).filter_by(username=username).first()
                
                if user:
                    user.update_from_dict(user_data)
                else:
                    # Create new
                    user = User.from_dict(username, user_data)
                    session.add(user)
            
            session.commit()
            return True
    except Exception as e:
        print(f"Save users error: {e}")
        return False


def save_single_user(username: str, user_data: Dict[str, Any]) -> bool:
    """
    Save single user - pure SQL
    
    Args:
        username: Username
        user_data: User data dict
    
    Returns:
        True if successful
    """
    try:
        with session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            
            if user:
                user.update_from_dict(user_data)
            else:
                user = User.from_dict(username, user_data)
                session.add(user)
            
            session.commit()
            return True
    except Exception as e:
        print(f"Save user error for {username}: {e}")
        return False


def get_current_user_data(username: str) -> Dict[str, Any]:
    """
    Get current user data - pure SQL
    
    Args:
        username: Username
    
    Returns:
        User data dict
    """
    try:
        with session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            if user:
                return user.to_dict()
            return {}
    except Exception as e:
        print(f"Get user error for {username}: {e}")
        return {}


def update_user_xp(username: str, xp_amount: int) -> bool:
    """
    Update user XP - pure SQL
    
    Args:
        username: Username
        xp_amount: XP to add
    
    Returns:
        True if successful
    """
    try:
        with session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            if user:
                user.xp = (user.xp or 0) + xp_amount
                session.commit()
                return True
            return False
    except Exception as e:
        print(f"Update XP error for {username}: {e}")
        return False
