"""
Helper funkcja do pobierania INTEGER user_id z bazy SQL na podstawie username
"""

import sqlite3
from pathlib import Path


def get_user_sql_id(username: str) -> int:
    """
    Pobiera INTEGER PRIMARY KEY (id) użytkownika z tabeli users w SQL
    
    Args:
        username: Nazwa użytkownika
    
    Returns:
        int: ID użytkownika (INTEGER PRIMARY KEY) lub None jeśli nie znaleziono
    """
    db_path = Path(__file__).parent.parent / "database" / "bva_app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return row[0]
        else:
            return None
    except Exception as e:
        print(f"Error getting user SQL id for {username}: {e}")
        return None
