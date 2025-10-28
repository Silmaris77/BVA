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

def get_quiz_performance_stats(username: str, days: int = 30) -> Dict:
    """
    Analizuje wyniki quizów użytkownika za ostatnie N dni
    
    Returns:
        Dict zawierający:
        - total_quizzes: łączna liczba ukończonych quizów
        - avg_score: średni wynik (%)
        - quizzes_by_category: rozbicie po kategorii (opening/closing/practice)
        - pass_rate: % zdanych quizów
        - perfect_scores: liczba quizów z wynikiem 100%
        - weak_areas: obszary wymagające poprawy (quiz_id z wynikiem <70%)
        - improvement_trend: trend poprawy wyników (rosnący/stabilny/spadający)
    """
    users_data = load_user_data()
    if username not in users_data:
        return {}
    
    activity_log = users_data[username].get('activity_log', [])
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    # Filtruj quizy z ostatnich N dni
    quiz_activities = [
        entry for entry in activity_log
        if entry['type'] == 'quiz_completed' 
        and entry['timestamp'] > cutoff_date
        and not entry['details'].get('is_self_diagnostic', False)  # Pomijamy quizy autodiagnozy
    ]
    
    if not quiz_activities:
        return {
            'total_quizzes': 0,
            'avg_score': 0,
            'quizzes_by_category': {},
            'pass_rate': 0,
            'perfect_scores': 0,
            'weak_areas': [],
            'improvement_trend': 'brak danych'
        }
    
    # Oblicz statystyki
    scores = [q['details'].get('score_percentage', 0) for q in quiz_activities]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    passed_quizzes = sum(1 for q in quiz_activities if q['details'].get('passed', False))
    pass_rate = (passed_quizzes / len(quiz_activities) * 100) if quiz_activities else 0
    
    perfect_scores = sum(1 for s in scores if s >= 99)  # 99+ to traktujemy jako 100%
    
    # Rozbicie po kategorii
    by_category = {}
    for quiz in quiz_activities:
        category = quiz['details'].get('quiz_category', 'other')
        if category not in by_category:
            by_category[category] = {
                'count': 0,
                'avg_score': 0,
                'scores': []
            }
        by_category[category]['count'] += 1
        by_category[category]['scores'].append(quiz['details'].get('score_percentage', 0))
    
    # Oblicz średnie dla każdej kategorii
    for category in by_category:
        scores_list = by_category[category]['scores']
        by_category[category]['avg_score'] = round(sum(scores_list) / len(scores_list), 1) if scores_list else 0
        del by_category[category]['scores']  # Usuń surowe dane
    
    # Słabe obszary (wynik < 70%)
    weak_areas = []
    for quiz in quiz_activities:
        score = quiz['details'].get('score_percentage', 0)
        if score < 70:
            weak_areas.append({
                'quiz_title': quiz['details'].get('quiz_title', 'Unknown'),
                'score': round(score, 1),
                'date': datetime.fromisoformat(quiz['timestamp']).strftime('%Y-%m-%d')
            })
    
    # Trend poprawy - porównaj pierwszą i drugą połowę okresu
    if len(quiz_activities) >= 4:
        midpoint = len(quiz_activities) // 2
        first_half_scores = scores[:midpoint]
        second_half_scores = scores[midpoint:]
        
        avg_first = sum(first_half_scores) / len(first_half_scores)
        avg_second = sum(second_half_scores) / len(second_half_scores)
        
        if avg_second > avg_first + 5:
            trend = 'rosnący'
        elif avg_second < avg_first - 5:
            trend = 'spadający'
        else:
            trend = 'stabilny'
    else:
        trend = 'za mało danych'
    
    return {
        'total_quizzes': len(quiz_activities),
        'avg_score': round(avg_score, 1),
        'quizzes_by_category': by_category,
        'pass_rate': round(pass_rate, 1),
        'perfect_scores': perfect_scores,
        'weak_areas': weak_areas[:5],  # Top 5 najsłabszych
        'improvement_trend': trend,
        'highest_score': round(max(scores), 1) if scores else 0,
        'lowest_score': round(min(scores), 1) if scores else 0
    }

def get_xp_history(username: str, days: int = 30) -> Dict:
    """
    Zbiera historię przyrostu XP użytkownika na podstawie activity_log
    
    Args:
        username: Nazwa użytkownika
        days: Liczba dni wstecz do analizy
        
    Returns:
        Dict z historią XP:
        {
            'daily_xp': [(date, xp_earned), ...],
            'total_xp_gained': int,
            'avg_daily_xp': float,
            'most_productive_day': (date, xp_amount),
            'current_xp': int,
            'current_level': int
        }
    """
    users_data = load_user_data()
    if username not in users_data:
        return {
            'daily_xp': [],
            'total_xp_gained': 0,
            'avg_daily_xp': 0,
            'most_productive_day': (None, 0),
            'current_xp': 0,
            'current_level': 1
        }
    
    user_data = users_data[username]
    activity_log = user_data.get('activity_log', [])
    
    # Filtruj po dacie
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_activities = [
        entry for entry in activity_log
        if datetime.fromisoformat(entry['timestamp']) >= cutoff_date
    ]
    
    # Mapowanie aktywności na XP (zgodnie z systemem nagród)
    # UWAGA: To są wartości domyślne - faktyczne XP może pochodzić z details['xp_earned']
    xp_mapping = {
        'lesson_started': 5,
        'lesson_completed': 50,
        'quiz_completed': 20,  # bazowe, może być więcej za dobre wyniki
        'ai_exercise': 15,
        'inspiration_read': 1,  # ZAKTUALIZOWANE: 1 XP za inspirację
        'test_completed': 5,    # ZAKTUALIZOWANE: 5 XP za test diagnostyczny
        'tool_used': 1          # ZAKTUALIZOWANE: 1 XP za użycie narzędzia
    }
    
    # Grupuj XP po dniach
    from collections import defaultdict
    daily_xp_dict = defaultdict(int)
    
    for entry in recent_activities:
        activity_type = entry['type']
        timestamp = datetime.fromisoformat(entry['timestamp'])
        date_key = timestamp.strftime('%Y-%m-%d')
        details = entry.get('details', {})
        
        # Preferuj XP z details (jeśli zostało zapisane), w przeciwnym razie użyj mapowania
        if 'xp_earned' in details:
            base_xp = details['xp_earned']
        else:
            # Bazowe XP za aktywność z mapowania
            base_xp = xp_mapping.get(activity_type, 0)
        # Dodatkowe XP za quizy (bonus za wysokie wyniki)
        if activity_type == 'quiz_completed':
            details = entry.get('details', {})
            score_percentage = details.get('score_percentage', 0)
            if score_percentage >= 90:
                base_xp += 30  # Bonus za 90%+
            elif score_percentage >= 80:
                base_xp += 20  # Bonus za 80%+
            elif score_percentage >= 70:
                base_xp += 10  # Bonus za 70%+
        
        daily_xp_dict[date_key] += base_xp
    
    # Sortuj po dacie
    daily_xp = sorted(daily_xp_dict.items(), key=lambda x: x[0])
    
    # Oblicz statystyki
    total_xp_gained = sum(xp for _, xp in daily_xp)
    avg_daily_xp = total_xp_gained / days if days > 0 else 0
    
    most_productive_day = max(daily_xp, key=lambda x: x[1]) if daily_xp else (None, 0)
    
    return {
        'daily_xp': daily_xp,
        'total_xp_gained': total_xp_gained,
        'avg_daily_xp': round(avg_daily_xp, 1),
        'most_productive_day': most_productive_day,
        'current_xp': user_data.get('xp', 0),
        'current_level': user_data.get('level', 1)
    }
