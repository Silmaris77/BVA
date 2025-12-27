"""
Moduł do śledzenia aktywności użytkownika w aplikacji
Zbiera dane o: logowaniach, lekcjach, ćwiczeniach, narzędziach, inspiracjach
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from data.users_new import load_user_data, save_user_data

def log_activity(username: str, activity_type: str, details: Optional[Dict] = None):
    """
    Zapisuje aktywność użytkownika do SQL
    
    activity_type:
    - 'login' - logowanie
    - 'lesson_started' - rozpoczęcie fragmentu lekcji
    - 'lesson_completed' - ukończenie fragmentu/całej lekcji
    - 'ai_exercise' - ćwiczenie AI
    - 'tool_used' - użycie narzędzia (symulator, feedback360, etc.)
    - 'inspiration_read' - przeczytanie inspiracji
    - 'test_completed' - ukończenie testu diagnostycznego
    - 'quiz_completed' - ukończenie quizu
    """
    if not username:
        return False
    
    try:
        from database.connection import session_scope
        from database.models import User, ActivityLog
        
        with session_scope() as session:
            # Znajdź użytkownika
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return False
            
            # Utwórz wpis activity log
            activity_log = ActivityLog(
                user_id=user.user_id,
                activity_type=activity_type,
                details=details or {},
                timestamp=datetime.now()
            )
            
            session.add(activity_log)
            session.commit()
            
            return True
            
    except Exception as e:
        print(f"Error logging activity: {e}")
        return False

def get_activity_summary(username: str, days: int = 7) -> Dict:
    """
    Zwraca podsumowanie aktywności użytkownika za ostatnie N dni z SQL
    """
    from database.connection import session_scope
    from database.models import User, ActivityLog, CompletedLesson
    
    with session_scope() as session:
        # Pobierz użytkownika
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return {}
        
        # Filtruj aktywności z ostatnich N dni
        cutoff_date = datetime.now() - timedelta(days=days)
        activities = session.query(ActivityLog)\
            .filter(ActivityLog.user_id == user.user_id)\
            .filter(ActivityLog.timestamp >= cutoff_date)\
            .order_by(ActivityLog.timestamp.desc())\
            .all()
        
        # Oblicz statystyki
        summary = {
            'period_days': days,
            'total_activities': len(activities),
            'unique_login_days': len(set(
                activity.timestamp.date().isoformat()
                for activity in activities
                if activity.activity_type == 'login'
            )),
            'lessons': {
                'started': len([a for a in activities if a.activity_type == 'lesson_start']),
                'completed': len([a for a in activities if a.activity_type == 'lesson_complete']),
            },
            'ai_exercises': {
                'sessions': len([a for a in activities if a.activity_type == 'ai_exercise']),
            },
            'tools_used': {},
            'inspirations_read': len([a for a in activities if a.activity_type == 'inspiration_read']),
            'tests_completed': []
        }
        
        # Zbierz szczegóły użycia narzędzi
        for activity in activities:
            if activity.activity_type == 'tool_used':
                details = activity.details or {}
                tool_name = details.get('tool_name', 'unknown')
                summary['tools_used'][tool_name] = summary['tools_used'].get(tool_name, 0) + 1
            elif activity.activity_type == 'test_completed':
                details = activity.details or {}
                test_name = details.get('test_name', 'unknown')
                if test_name not in summary['tests_completed']:
                    summary['tests_completed'].append(test_name)
        
        # Dodaj dane z profilu użytkownika
        summary['user_profile'] = {
            'xp': user.xp,
            'level': user.level,
            'completed_lessons_total': session.query(CompletedLesson)\
                .filter(CompletedLesson.user_id == user.user_id).count(),
            'kolb_test': None,  # TODO: przenieść do SQL jeśli potrzebne
            'neuroleader_test': None,  # TODO: przenieść do SQL jeśli potrzebne
        }
        
        return summary

def get_login_pattern(username: str, days: int = 30) -> Dict:
    """
    Analizuje wzorzec logowań użytkownika z SQL
    """
    from database.connection import session_scope
    from database.models import User, ActivityLog
    
    with session_scope() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return {}
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Pobierz aktywności logowania
        login_activities = session.query(ActivityLog)\
            .filter(ActivityLog.user_id == user.user_id)\
            .filter(ActivityLog.activity_type == 'login')\
            .filter(ActivityLog.timestamp >= cutoff_date)\
            .order_by(ActivityLog.timestamp.asc())\
            .all()
        
        logins = [activity.timestamp for activity in login_activities]
        
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
    Analizuje statystyki ukończenia lekcji z SQL
    """
    from database.connection import session_scope
    from database.models import User, CompletedLesson, LessonProgress
    
    with session_scope() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return {}
        
        # Pobierz wszystkie lekcje
        from data.lessons import load_lessons
        all_lessons = load_lessons()
        total_lessons = len(all_lessons)
        
        # Ukończone lekcje
        completed_count = session.query(CompletedLesson)\
            .filter(CompletedLesson.user_id == user.user_id).count()
        
        # Lekcje w trakcie (rozpoczęte ale nieukończone)
        # Pobierz lekcje z progressem
        in_progress = session.query(LessonProgress)\
            .filter(LessonProgress.user_id == user.user_id)\
            .all()
        
        # Pobierz ukończone IDs
        completed_lessons = session.query(CompletedLesson.lesson_id)\
            .filter(CompletedLesson.user_id == user.user_id)\
            .all()
        completed_ids = [lesson_id for (lesson_id,) in completed_lessons]
        
        # Lekcje rozpoczęte ale nieukończone
        started_lessons = [
            lp.lesson_id for lp in in_progress
            if lp.intro_completed and lp.lesson_id not in completed_ids
        ]
        
        return {
            'total_available': total_lessons,
            'completed': completed_count,
            'in_progress': len(started_lessons),
            'completion_rate': round((completed_count / total_lessons * 100), 1) if total_lessons > 0 else 0,
            'abandoned': len(started_lessons),  # Rozpoczęte ale nieukończone
        }

def initialize_activity_tracking(username: str):
    """
    Inicjalizuje tracking aktywności dla użytkownika (dla kompatybilności wstecznej)
    W wersji SQL nie jest już potrzebna - aktywności zapisują się do tabeli ActivityLog
    """
    # Ta funkcja jest teraz NOP (no operation) - tracking działa automatycznie przez SQL
    return True

def get_quiz_performance_stats(username: str, days: int = 30) -> Dict:
    """
    Analizuje wyniki quizów użytkownika za ostatnie N dni z SQL
    
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
    from database.connection import session_scope
    from database.models import User, ActivityLog
    
    with session_scope() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return {}
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filtruj quizy z ostatnich N dni
        quiz_activities = session.query(ActivityLog)\
            .filter(ActivityLog.user_id == user.user_id)\
            .filter(ActivityLog.activity_type == 'quiz_completed')\
            .filter(ActivityLog.timestamp >= cutoff_date)\
            .order_by(ActivityLog.timestamp.asc())\
            .all()
        
        # Pomijamy quizy autodiagnozy
        quiz_activities = [
            activity for activity in quiz_activities
            if not (activity.details or {}).get('is_self_diagnostic', False)
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
        scores = [(activity.details or {}).get('score_percentage', 0) for activity in quiz_activities]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        passed_quizzes = sum(1 for activity in quiz_activities 
                            if (activity.details or {}).get('passed', False))
        pass_rate = (passed_quizzes / len(quiz_activities) * 100) if quiz_activities else 0
        
        perfect_scores = sum(1 for s in scores if s >= 99)  # 99+ to traktujemy jako 100%
        
        # Rozbicie po kategorii
        by_category = {}
        for activity in quiz_activities:
            details = activity.details or {}
            category = details.get('quiz_category', 'other')
            if category not in by_category:
                by_category[category] = {
                    'count': 0,
                    'avg_score': 0,
                    'scores': []
                }
            by_category[category]['count'] += 1
            by_category[category]['scores'].append(details.get('score_percentage', 0))
        
        # Oblicz średnie dla każdej kategorii
        for category in by_category:
            scores_list = by_category[category]['scores']
            by_category[category]['avg_score'] = round(sum(scores_list) / len(scores_list), 1) if scores_list else 0
            del by_category[category]['scores']  # Usuń surowe dane
        
        # Słabe obszary (wynik < 70%)
        weak_areas = []
        for activity in quiz_activities:
            details = activity.details or {}
            score = details.get('score_percentage', 0)
            if score < 70:
                weak_areas.append({
                    'quiz_title': details.get('quiz_title', 'Unknown'),
                    'score': round(score, 1),
                    'date': activity.timestamp.strftime('%Y-%m-%d')
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
    Zbiera historię przyrostu XP użytkownika na podstawie activity_log z SQL
    
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
    from collections import defaultdict
    from database.connection import session_scope
    from database.models import User, ActivityLog
    
    with session_scope() as session:
        # Pobierz użytkownika
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return {
                'daily_xp': [],
                'total_xp_gained': 0,
                'avg_daily_xp': 0,
                'most_productive_day': (None, 0),
                'current_xp': 0,
                'current_level': 1
            }
        
        # Filtruj aktywności po dacie
        cutoff_date = datetime.now() - timedelta(days=days)
        activities = session.query(ActivityLog)\
            .filter(ActivityLog.user_id == user.user_id)\
            .filter(ActivityLog.timestamp >= cutoff_date)\
            .order_by(ActivityLog.timestamp.asc())\
            .all()
        
        # Mapowanie aktywności na XP (wartości domyślne)
        xp_mapping = {
            'lesson_started': 5,
            'lesson_completed': 50,
            'quiz_completed': 20,
            'ai_exercise': 15,
            'inspiration_read': 1,
            'test_completed': 5,
            'tool_used': 1
        }
        
        # Grupuj XP po dniach
        daily_xp_dict = defaultdict(int)
        
        for activity in activities:
            date_key = activity.timestamp.strftime('%Y-%m-%d')
            details = activity.details or {}
            
            # Preferuj XP z details, w przeciwnym razie użyj mapowania
            if 'xp_earned' in details:
                base_xp = details['xp_earned']
            else:
                base_xp = xp_mapping.get(activity.activity_type, 0)
            
            # Dodatkowe XP za quizy (bonus za wysokie wyniki)
            if activity.activity_type == 'quiz_completed':
                score_percentage = details.get('score_percentage', 0)
                if score_percentage >= 90:
                    base_xp += 30
                elif score_percentage >= 80:
                    base_xp += 20
                elif score_percentage >= 70:
                    base_xp += 10
            
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
            'current_xp': user.xp,
            'current_level': user.level
        }
