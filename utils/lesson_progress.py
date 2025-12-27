import json
import os
from datetime import datetime
import streamlit as st
from data.users import load_user_data, save_user_data
from data.repositories import LessonRepository
from utils.activity_tracker import log_activity

# Initialize repository (will use config to determine backend)
_lesson_repo = None

def get_lesson_repository():
    """Get or create lesson repository instance"""
    global _lesson_repo
    if _lesson_repo is None:
        _lesson_repo = LessonRepository()
    return _lesson_repo

def save_lesson_progress(username, lesson_id, step, notes=None):
    """Save user's progress in a lesson"""
    progress_file = 'lesson_progress.json'
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
    else:
        progress_data = {}
    
    if username not in progress_data:
        progress_data[username] = {}
    
    progress_data[username][str(lesson_id)] = {
        'current_step': step,
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'notes': notes or {},
        'bookmarks': progress_data.get(username, {}).get(str(lesson_id), {}).get('bookmarks', [])
    }
    
    with open(progress_file, 'w') as f:
        json.dump(progress_data, f)

def get_lesson_progress(username, lesson_id):
    """Get user's progress in a lesson"""
    if os.path.exists('lesson_progress.json'):
        with open('lesson_progress.json', 'r') as f:
            progress_data = json.load(f)
            
        if username in progress_data and str(lesson_id) in progress_data[username]:
            return progress_data[username][str(lesson_id)]
    
    return {
        'current_step': 'intro',
        'notes': {},
        'bookmarks': []
    }

def save_lesson_note(username, lesson_id, step, note):
    """Save a note for a specific part of the lesson"""
    progress = get_lesson_progress(username, lesson_id)
    if 'notes' not in progress:
        progress['notes'] = {}
    
    if step not in progress['notes']:
        progress['notes'][step] = []
    
    note_entry = {
        'text': note,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    progress['notes'][step].append(note_entry)
    
    save_lesson_progress(username, lesson_id, progress['current_step'], progress['notes'])

def add_bookmark(username, lesson_id, step, description):
    """Add a bookmark to a specific part of the lesson"""
    progress = get_lesson_progress(username, lesson_id)
    
    bookmark = {
        'step': step,
        'description': description,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if 'bookmarks' not in progress:
        progress['bookmarks'] = []
    
    progress['bookmarks'].append(bookmark)
    save_lesson_progress(username, lesson_id, progress['current_step'], progress.get('notes', {}))

def get_bookmarks(username, lesson_id):
    """Get all bookmarks for a lesson"""
    progress = get_lesson_progress(username, lesson_id)
    return progress.get('bookmarks', [])

def award_fragment_xp(lesson_id, fragment_type, xp_amount):
    """
    Przyznaj XP za ukończenie fragmentu lekcji
    
    Args:
        lesson_id: ID lekcji
        fragment_type: 'intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary'
        xp_amount: Ilość XP do przyznania
    """
    username = st.session_state.username
    repo = get_lesson_repository()
    
    # Pobierz aktualny postęp z repository
    lesson_progress = repo.get_lesson_progress(username, lesson_id)
    
    # Sprawdź czy XP za ten fragment już zostało przyznane
    fragment_key = f"{fragment_type}_xp_awarded"
    if not lesson_progress.get(fragment_key, False):
        # Dodaj XP do SQL
        from data.users import update_user_xp
        update_user_xp(username, xp_amount)
        
        # Przygotuj dane postępu
        progress_data = {
            f"{fragment_type}_xp_awarded": True,
            f"{fragment_type}_completed": True,
            f"{fragment_type}_xp": xp_amount,
            f"{fragment_type}_degencoins": 0,  # Już nie używane
            f"{fragment_type}_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Zapisz postęp przez repository
        repo.save_lesson_progress(username, lesson_id, fragment_type, progress_data)
        
        # LOGUJ AKTYWNOŚĆ DO ACTIVITY_LOG (dla dashboard i historii XP)
        log_activity(
            username=username,
            activity_type='lesson_completed' if fragment_type == 'summary' else 'lesson_started',
            details={
                'lesson_id': lesson_id,
                'fragment_type': fragment_type,
                'xp_earned': xp_amount
            }
        )
        
        return True, xp_amount
    
    return False, 0

def get_lesson_fragment_progress(lesson_id):
    """Pobierz postęp fragmentów dla danej lekcji"""
    username = st.session_state.username
    repo = get_lesson_repository()
    
    # Pobierz z repository (automatycznie wybierze JSON lub SQL)
    return repo.get_lesson_progress(username, lesson_id)

def calculate_lesson_completion(lesson_id):
    """Oblicz procent ukończenia lekcji"""
    progress = get_lesson_fragment_progress(lesson_id)
    
    # Nowa 4-etapowa struktura (preferowana)
    new_steps = ['intro', 'content', 'practical_exercises', 'summary']
    new_completed = sum(1 for step in new_steps if progress.get(f"{step}_completed", False))
    
    # Sprawdź czy lekcja używa nowej struktury (przynajmniej jeden z nowych kroków jest ukończony)
    uses_new_structure = any(progress.get(f"{step}_completed", False) for step in new_steps)
    
    if uses_new_structure:
        # Użyj nowej 4-etapowej struktury
        return (new_completed / len(new_steps)) * 100
    else:
        # Fallback do starej 7-krokowej struktury dla backward compatibility
        old_steps = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
        old_completed = sum(1 for step in old_steps if progress.get(f"{step}_completed", False))
        return (old_completed / len(old_steps)) * 100

def is_lesson_fully_completed(lesson_id):
    """Sprawdź czy lekcja jest w pełni ukończona"""
    return calculate_lesson_completion(lesson_id) == 100

def get_fragment_xp_breakdown(lesson_total_xp):
    """Oblicz podział XP na fragmenty lekcji"""
    return {
        'intro': int(lesson_total_xp * 0.3),    # 30% za wprowadzenie
        'content': int(lesson_total_xp * 0.5),  # 50% za treść
        'quiz': int(lesson_total_xp * 0.2)      # 20% za quiz (+ bonus za wynik)
    }

def mark_lesson_as_completed(lesson_id):
    """Oznacz lekcję jako w pełni ukończoną"""
    username = st.session_state.username
    repo = get_lesson_repository()
    
    # Sprawdź czy już ukończona
    completed = repo.get_completed_lessons(username)
    
    if lesson_id not in completed:
        # Dodaj do completed lessons przez repository
        success = repo.add_completed_lesson(username, lesson_id)
        
        if success:
            # Odśwież user_data w session_state
            users_data = load_user_data()
            if username in users_data:
                st.session_state.user_data = users_data[username]
            
            # Add recent activity for lesson completion
            try:
                from data.users_fixed import add_recent_activity
                add_recent_activity(username, "lesson_completed", {"lesson_id": lesson_id})
            except ImportError:
                pass  # Activity system not available
            except Exception:
                pass
            
            # Zaloguj także w nowym systemie activity tracking
            try:
                from utils.activity_tracker import log_activity
                log_activity(username, 'lesson_complete', {
                    'lesson_id': lesson_id
                })
            except ImportError:
                pass
            except Exception:
                pass
            # Aktualizuj dzisiejsze statystyki
            try:
                from views.dashboard import update_daily_stats_if_needed
                update_daily_stats_if_needed(username)
            except ImportError:
                pass  # Dashboard module not available
            except Exception:
                pass  # Ignore other errors
            
            # Check for achievements after completing lesson
            try:
                from utils.achievements import check_achievements
                check_achievements(username, 'lesson_completion', lesson_id=lesson_id)
            except ImportError:
                pass  # Achievement system not available
            
            return True
    
    return False

def check_and_mark_lesson_completion(lesson_id):
    """Sprawdź czy lekcja jest ukończona i jeśli tak, oznacz ją jako ukończoną"""
    if is_lesson_fully_completed(lesson_id):
        return mark_lesson_as_completed(lesson_id)
    return False