"""
Moduł do zapisywania i ładowania notatek użytkownika w lekcjach (Action Plan, Reflection Journal).
Obsługuje zarówno JSON (fallback) jak i SQL (preferowane).
"""
import json
import os
from datetime import datetime
from typing import Dict, Optional, Any
import streamlit as st


def _get_sql_available():
    """Sprawdza czy SQL jest dostępny"""
    try:
        from database.models import User, LessonNotes
        from database.connection import session_scope
        return True
    except ImportError:
        return False


def save_lesson_notes(username: str, lesson_id: str, notes_data: Dict[str, str]) -> bool:
    """
    Zapisuje notatki użytkownika (preferuje SQL, fallback na JSON).
    
    Args:
        username: Nazwa użytkownika
        lesson_id: ID lekcji
        notes_data: Słownik z notatkami, np.:
            {
                'action_today': 'Wydrukuję checklist...',
                'action_tomorrow': 'Pierwsza wizyta...',
                'action_week': 'Powtórka...',
                'reflection_discovery': 'Złota zasada...',
                'reflection_doubts': 'Jak przejść...',
                'reflection_application': 'Jutro wizyta...'
            }
    
    Returns:
        True jeśli zapis się powiódł
    """
    # Preferuj SQL
    if _get_sql_available():
        success = _save_lesson_notes_to_sql(username, lesson_id, notes_data)
        if success:
            return True
        print("⚠️ SQL save failed, falling back to JSON")
    
    # Fallback: JSON
    return _save_lesson_notes_to_json(username, lesson_id, notes_data)


def _save_lesson_notes_to_sql(username: str, lesson_id: str, notes_data: Dict[str, str]) -> bool:
    """Zapisuje notatki do SQL"""
    try:
        from database.models import User, LessonNotes
        from database.connection import session_scope
        
        with session_scope() as session:
            # Znajdź użytkownika
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return False
            
            # Zapisz każde pole jako osobny rekord
            for field_name, value in notes_data.items():
                # Sprawdź czy rekord istnieje
                note = session.query(LessonNotes).filter_by(
                    user_id=user.user_id,
                    lesson_id=lesson_id,
                    field_name=field_name
                ).first()
                
                if note:
                    # Update
                    note.value = value
                    note.updated_at = datetime.utcnow()
                else:
                    # Insert
                    note = LessonNotes(
                        user_id=user.user_id,
                        lesson_id=lesson_id,
                        field_name=field_name,
                        value=value
                    )
                    session.add(note)
            
            session.commit()
            return True
            
    except Exception as e:
        print(f"❌ Error saving lesson notes to SQL: {e}")
        import traceback
        traceback.print_exc()
        return False


def _save_lesson_notes_to_json(username: str, lesson_id: str, notes_data: Dict[str, str]) -> bool:
    """Zapisuje notatki do JSON (fallback)"""
    try:
        from data.users_sql import load_user_data, save_user_data
        
        users_data = load_user_data()
        
        if username not in users_data:
            return False
        
        # Inicjalizacja struktury lesson_notes jeśli nie istnieje
        if 'lesson_notes' not in users_data[username]:
            users_data[username]['lesson_notes'] = {}
        
        # Inicjalizacja notatek dla tej lekcji
        if lesson_id not in users_data[username]['lesson_notes']:
            users_data[username]['lesson_notes'][lesson_id] = {}
        
        # Zaktualizuj notatki
        users_data[username]['lesson_notes'][lesson_id].update(notes_data)
        users_data[username]['lesson_notes'][lesson_id]['last_updated'] = datetime.now().isoformat()
        
        # Zapisz
        save_user_data(users_data)
        return True
        
    except Exception as e:
        print(f"❌ Error saving lesson notes to JSON: {e}")
        return False


def load_lesson_notes(username: str, lesson_id: str) -> Dict[str, str]:
    """
    Ładuje notatki użytkownika (preferuje SQL, fallback na JSON).
    
    Args:
        username: Nazwa użytkownika
        lesson_id: ID lekcji
    
    Returns:
        Słownik z notatkami lub pusty słownik jeśli brak
    """
    # Preferuj SQL
    if _get_sql_available():
        notes = _load_lesson_notes_from_sql(username, lesson_id)
        if notes:
            return notes
    
    # Fallback: JSON
    return _load_lesson_notes_from_json(username, lesson_id)


def _load_lesson_notes_from_sql(username: str, lesson_id: str) -> Dict[str, str]:
    """Ładuje notatki z SQL"""
    try:
        from database.models import User, LessonNotes
        from database.connection import session_scope
        
        with session_scope() as session:
            # Znajdź użytkownika
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return {}
            
            # Pobierz wszystkie notatki dla tej lekcji
            notes = session.query(LessonNotes).filter_by(
                user_id=user.user_id,
                lesson_id=lesson_id
            ).all()
            
            # Konwertuj do dict
            result = {}
            for note in notes:
                result[note.field_name] = note.value or ""
            
            return result
            
    except Exception as e:
        print(f"❌ Error loading lesson notes from SQL: {e}")
        return {}


def _load_lesson_notes_from_json(username: str, lesson_id: str) -> Dict[str, str]:
    """Ładuje notatki z JSON (fallback)"""
    try:
        from data.users_sql import load_user_data
        
        users_data = load_user_data()
        
        if username not in users_data:
            return {}
        
        lesson_notes = users_data[username].get('lesson_notes', {})
        return lesson_notes.get(lesson_id, {})
        
    except Exception as e:
        print(f"❌ Error loading lesson notes from JSON: {e}")
        return {}


def save_single_note(username: str, lesson_id: str, field_name: str, value: str) -> bool:
    """
    Zapisuje pojedynczą notatkę (dla auto-save).
    
    Args:
        username: Nazwa użytkownika
        lesson_id: ID lekcji
        field_name: Nazwa pola (np. 'action_today', 'reflection_discovery')
        value: Wartość notatki
    
    Returns:
        True jeśli zapis się powiódł
    """
    notes_data = {field_name: value}
    return save_lesson_notes(username, lesson_id, notes_data)


def get_notes_as_json(username: str, lesson_id: str) -> str:
    """
    Zwraca notatki w formacie JSON dla JavaScript.
    
    Args:
        username: Nazwa użytkownika
        lesson_id: ID lekcji
    
    Returns:
        JSON string z notatkami
    """
    notes = load_lesson_notes(username, lesson_id)
    return json.dumps(notes, ensure_ascii=False)


def save_lesson_notes_from_session_state(username: str, lesson_id: str) -> bool:
    """
    Zapisuje wszystkie notatki z session_state (używane przy kliknięciu "Zakończ lekcję").
    
    Args:
        username: Nazwa użytkownika
        lesson_id: ID lekcji
    
    Returns:
        True jeśli zapis się powiódł
    """
    try:
        import streamlit as st
        
        # Zbierz wszystkie notatki z session_state
        notes_data = {}
        for field in ['action_today', 'action_tomorrow', 'action_week',
                      'reflection_discovery', 'reflection_doubts', 'reflection_application']:
            key = f'lesson_note_{lesson_id}_{field}'
            if key in st.session_state:
                value = st.session_state[key]
                if value:  # Tylko jeśli ma wartość
                    notes_data[field] = value
        
        # Zapisz jeśli są jakieś notatki
        if notes_data:
            return save_lesson_notes(username, lesson_id, notes_data)
        
        return True  # Brak notatek to nie błąd
        
    except Exception as e:
        print(f"❌ Error saving lesson notes from session state: {e}")
        return False
