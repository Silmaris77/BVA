"""
Moduł do śledzenia aktywności użytkownika w aplikacji
Zbiera dane o: logowaniach, lekcjach, ćwiczeniach, narzędziach, inspiracjach
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from data.users import load_user_data, save_user_data

def log_activity(username: str, activity_type: str, details: Optional[Dict] = None):
    """
    Zapisuje aktywność użytkownika
    
    activity_type:
    - 'login' - logowanie
    - 'lesson_start' - rozpoczęcie lekcji
    - 'lesson_complete' - ukończenie lekcji
    - 'ai_exercise' - ćwiczenie AI
    - 'tool_used' - użycie narzędzia (symulator, feedback360, etc.)
    - 'inspiration_read' - przeczytanie inspiracji
    - 'test_completed' - ukończenie testu diagnostycznego
    """
    if not username:
        return False
    
    users_data = load_user_data()
    if username not in users_data:
        return False
    
    # Inicjalizuj activity_log jeśli nie istnieje
    if 'activity_log' not in users_data[username]:
        users_data[username]['activity_log'] = []
    
    # Dodaj timestamp
    activity_entry = {
        'type': activity_type,
        'timestamp': datetime.now().isoformat(),
        'details': details or {}
    }
    
    users_data[username]['activity_log'].append(activity_entry)
    
    # Zachowaj tylko ostatnie 90 dni aktywności
    cutoff_date = (datetime.now() - timedelta(days=90)).isoformat()
    users_data[username]['activity_log'] = [
        entry for entry in users_data[username]['activity_log']
        if entry['timestamp'] > cutoff_date
    ]
    
    save_user_data(users_data)
    return True

def get_activity_summary(username: str, days: int = 7) -> Dict:
    """
    Zwraca podsumowanie aktywności użytkownika za ostatnie N dni
    """
    users_data = load_user_data()
    if username not in users_data:
        return {}
    
    user_data = users_data[username]
    activity_log = user_data.get('activity_log', [])
    
    # Filtruj aktywności z ostatnich N dni
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    recent_activities = [
        entry for entry in activity_log
        if entry['timestamp'] > cutoff_date
    ]
    
    # Oblicz statystyki
    summary = {
        'period_days': days,
        'total_activities': len(recent_activities),
        'unique_login_days': len(set(
            datetime.fromisoformat(entry['timestamp']).date().isoformat()
            for entry in recent_activities
            if entry['type'] == 'login'
        )),
        'lessons': {
            'started': len([e for e in recent_activities if e['type'] == 'lesson_start']),
            'completed': len([e for e in recent_activities if e['type'] == 'lesson_complete']),
        },
        'ai_exercises': {
            'sessions': len([e for e in recent_activities if e['type'] == 'ai_exercise']),
        },
        'tools_used': {},
        'inspirations_read': len([e for e in recent_activities if e['type'] == 'inspiration_read']),
        'tests_completed': []
    }
    
    # Zbierz szczegóły użycia narzędzi
    for entry in recent_activities:
        if entry['type'] == 'tool_used':
            tool_name = entry['details'].get('tool_name', 'unknown')
            summary['tools_used'][tool_name] = summary['tools_used'].get(tool_name, 0) + 1
        elif entry['type'] == 'test_completed':
            test_name = entry['details'].get('test_name', 'unknown')
            if test_name not in summary['tests_completed']:
                summary['tests_completed'].append(test_name)
    
    # Dodaj dane z profilu użytkownika
    summary['user_profile'] = {
        'xp': user_data.get('xp', 0),
        'level': user_data.get('level', 1),
        'completed_lessons_total': len(user_data.get('completed_lessons', [])),
        'kolb_test': user_data.get('kolb_test', {}).get('dominant_style') if user_data.get('kolb_test') else None,
        'neuroleader_test': user_data.get('neuroleader_result', {}).get('type') if user_data.get('neuroleader_result') else None,
    }
    
    return summary

def get_login_pattern(username: str, days: int = 30) -> Dict:
    """
    Analizuje wzorzec logowań użytkownika
    """
    users_data = load_user_data()
    if username not in users_data:
        return {}
    
    activity_log = users_data[username].get('activity_log', [])
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    logins = [
        datetime.fromisoformat(entry['timestamp'])
        for entry in activity_log
        if entry['type'] == 'login' and entry['timestamp'] > cutoff_date
    ]
    
    if not logins:
        return {
            'active_days': 0,
            'total_logins': 0,
            'avg_logins_per_day': 0,
            'most_active_day_of_week': None,
            'most_active_hour': None,
        }
    
    # Analiza dni tygodnia (0=Poniedziałek, 6=Niedziela)
    days_of_week = [login.weekday() for login in logins]
    day_names = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
    most_active_day = day_names[max(set(days_of_week), key=days_of_week.count)] if days_of_week else None
    
    # Analiza godzin
    hours = [login.hour for login in logins]
    most_active_hour = max(set(hours), key=hours.count) if hours else None
    
    # Unikalne dni
    unique_days = len(set(login.date() for login in logins))
    
    return {
        'active_days': unique_days,
        'total_logins': len(logins),
        'avg_logins_per_day': round(len(logins) / days, 2),
        'activity_rate': round((unique_days / days) * 100, 1),  # Procent dni z logowaniem
        'most_active_day_of_week': most_active_day,
        'most_active_hour': most_active_hour,
        'last_login': logins[-1].strftime('%Y-%m-%d %H:%M') if logins else None
    }

def get_lesson_completion_stats(username: str) -> Dict:
    """
    Analizuje statystyki ukończenia lekcji
    """
    users_data = load_user_data()
    if username not in users_data:
        return {}
    
    user_data = users_data[username]
    
    # Pobierz wszystkie lekcje
    from data.lessons import load_lessons
    all_lessons = load_lessons()
    total_lessons = len(all_lessons)
    
    completed_lessons = user_data.get('completed_lessons', [])
    lesson_progress = user_data.get('lesson_progress', {})
    
    # Lekcje rozpoczęte ale nieukończone
    started_lessons = [
        lesson_id for lesson_id, progress in lesson_progress.items()
        if progress.get('intro_completed') and lesson_id not in completed_lessons
    ]
    
    return {
        'total_available': total_lessons,
        'completed': len(completed_lessons),
        'in_progress': len(started_lessons),
        'completion_rate': round((len(completed_lessons) / total_lessons * 100), 1) if total_lessons > 0 else 0,
        'abandoned': len(started_lessons),  # Rozpoczęte ale nieukończone
    }

def initialize_activity_tracking(username: str):
    """
    Inicjalizuje tracking aktywności dla użytkownika (np. przy pierwszym logowaniu)
    """
    users_data = load_user_data()
    if username not in users_data:
        return False
    
    if 'activity_log' not in users_data[username]:
        users_data[username]['activity_log'] = []
        save_user_data(users_data)
    
    return True
