"""
Lesson Repository - warstwa abstrakcji dla danych lekcji
Obsługuje JSON i SQL backend
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from .base_repository import BaseRepository


class LessonRepository(BaseRepository):
    """
    Repository dla lekcji
    Obsługuje: completed_lessons, lesson_progress, lesson_access
    """
    
    def __init__(self, backend: Optional[str] = None):
        super().__init__(backend)
        
        # Lazy loading SQL
        self._sql_initialized = False
        self.sql_available = False
        self.users_file = Path(__file__).parent.parent.parent / "users_data.json"
    
    def _ensure_sql_initialized(self) -> bool:
        """Lazy loading - inicjalizuje SQL tylko gdy pierwszy raz potrzebny"""
        if not self._sql_initialized:
            self._sql_initialized = True
            try:
                from database.models import User, LessonProgress, CompletedLesson, LessonAccess
                from database.connection import session_scope
                
                self.User = User
                self.LessonProgress = LessonProgress
                self.CompletedLesson = CompletedLesson
                self.LessonAccess = LessonAccess
                self.session_scope = session_scope
                self.sql_available = True
            except ImportError:
                self.sql_available = False
                print("⚠️  SQL dependencies not available for LessonRepository")
        
        return self.sql_available
    
    # =============================================================================
    # ABSTRACT METHODS (required by BaseRepository - not used directly)
    # =============================================================================
    
    def get(self, *args, **kwargs):
        """Not used - use specific methods like get_completed_lessons()"""
        raise NotImplementedError("Use specific methods: get_completed_lessons, get_lesson_progress, get_lesson_access")
    
    def save(self, *args, **kwargs):
        """Not used - use specific methods like add_completed_lesson()"""
        raise NotImplementedError("Use specific methods: add_completed_lesson, save_lesson_progress, set_lesson_access")
    
    def delete(self, *args, **kwargs):
        """Not implemented"""
        raise NotImplementedError("Delete not implemented for lessons")
    
    def exists(self, *args, **kwargs):
        """Not implemented"""
        raise NotImplementedError("Use specific methods to check existence")
    
    # =============================================================================
    # COMPLETED LESSONS
    # =============================================================================
    
    def get_completed_lessons(self, username: str) -> List[str]:
        """Pobiera listę ukończonych lekcji"""
        if self._should_use_sql_for_read(username):
            self._ensure_sql_initialized()
            if self.sql_available:
                return self._get_completed_lessons_from_sql(username)
        
        return self._get_completed_lessons_from_json(username)
    
    def add_completed_lesson(self, username: str, lesson_id: str) -> bool:
        """Dodaje lekcję do ukończonych"""
        self._ensure_sql_initialized()  # Ensure SQL is ready
        
        success = True
        
        # Wymuszenie SQL jeśli backend="sql"
        if self.backend == "sql":
            if self.sql_available:
                return self._add_completed_lesson_to_sql(username, lesson_id)
            else:
                print("⚠️  SQL not available, falling back to JSON")
                return self._add_completed_lesson_to_json(username, lesson_id)
        
        # Dual write mode
        if self._is_dual_write_enabled():
            success &= self._add_completed_lesson_to_json(username, lesson_id)
            if self.sql_available:
                success &= self._add_completed_lesson_to_sql(username, lesson_id)
        
        # SQL write
        elif self._should_use_sql_for_write(username):
            if self.sql_available:
                success = self._add_completed_lesson_to_sql(username, lesson_id)
            else:
                success = self._add_completed_lesson_to_json(username, lesson_id)
        
        # JSON write
        else:
            success = self._add_completed_lesson_to_json(username, lesson_id)
        
        return success
    
    def _get_completed_lessons_from_json(self, username: str) -> List[str]:
        """Pobiera completed_lessons z JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            return users.get(username, {}).get('completed_lessons', [])
        except Exception as e:
            print(f"❌ Error reading completed lessons from JSON: {e}")
            return []
    
    def _get_completed_lessons_from_sql(self, username: str) -> List[str]:
        """Pobiera completed_lessons z SQL"""
        if not self.sql_available:
            return []
        
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                if not user:
                    return []
                
                lessons = session.query(self.CompletedLesson).filter_by(user_id=user.user_id).all()
                return [lesson.lesson_id for lesson in lessons]
        except Exception as e:
            print(f"❌ Error reading completed lessons from SQL: {e}")
            return []
    
    def _add_completed_lesson_to_json(self, username: str, lesson_id: str) -> bool:
        """Dodaje completed lesson do JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            if username not in users:
                return False
            
            completed = users[username].get('completed_lessons', [])
            if lesson_id not in completed:
                completed.append(lesson_id)
                users[username]['completed_lessons'] = completed
                
                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump(users, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Error adding completed lesson to JSON: {e}")
            return False
    
    def _add_completed_lesson_to_sql(self, username: str, lesson_id: str) -> bool:
        """Dodaje completed lesson do SQL"""
        if not self.sql_available:
            return False
        
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                if not user:
                    return False
                
                # Sprawdź czy już istnieje
                existing = session.query(self.CompletedLesson).filter_by(
                    user_id=user.user_id,
                    lesson_id=lesson_id
                ).first()
                
                if not existing:
                    completed = self.CompletedLesson(
                        user_id=user.user_id,
                        lesson_id=lesson_id
                    )
                    session.add(completed)
                    session.commit()
                
                return True
        except Exception as e:
            print(f"❌ Error adding completed lesson to SQL: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # =============================================================================
    # LESSON PROGRESS
    # =============================================================================
    
    def get_lesson_progress(self, username: str, lesson_id: str) -> Dict[str, Any]:
        """Pobiera postęp w lekcji"""
        if self._should_use_sql_for_read(username):
            self._ensure_sql_initialized()
            if self.sql_available:
                return self._get_lesson_progress_from_sql(username, lesson_id)
        
        return self._get_lesson_progress_from_json(username, lesson_id)
    
    def save_lesson_progress(self, username: str, lesson_id: str, section_name: str, progress_data: Dict[str, Any]) -> bool:
        """Zapisuje postęp w sekcji lekcji"""
        self._ensure_sql_initialized()  # Ensure SQL is ready
        
        success = True
        
        # Wymuszenie SQL jeśli backend="sql"
        if self.backend == "sql":
            if self.sql_available:
                return self._save_lesson_progress_to_sql(username, lesson_id, section_name, progress_data)
            else:
                print("⚠️  SQL not available, falling back to JSON")
                return self._save_lesson_progress_to_json(username, lesson_id, section_name, progress_data)
        
        # Dual write mode
        if self._is_dual_write_enabled():
            success &= self._save_lesson_progress_to_json(username, lesson_id, section_name, progress_data)
            if self.sql_available:
                success &= self._save_lesson_progress_to_sql(username, lesson_id, section_name, progress_data)
        
        # SQL write
        elif self._should_use_sql_for_write(username):
            if self.sql_available:
                success = self._save_lesson_progress_to_sql(username, lesson_id, section_name, progress_data)
            else:
                success = self._save_lesson_progress_to_json(username, lesson_id, section_name, progress_data)
        
        # JSON write
        else:
            success = self._save_lesson_progress_to_json(username, lesson_id, section_name, progress_data)
        
        return success
    
    def _get_lesson_progress_from_json(self, username: str, lesson_id: str) -> Dict[str, Any]:
        """Pobiera lesson_progress z JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            lesson_progress = users.get(username, {}).get('lesson_progress', {})
            return lesson_progress.get(lesson_id, {})
        except Exception as e:
            print(f"❌ Error reading lesson progress from JSON: {e}")
            return {}
    
    def _get_lesson_progress_from_sql(self, username: str, lesson_id: str) -> Dict[str, Any]:
        """Pobiera lesson_progress z SQL"""
        if not self.sql_available:
            return {}
        
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                if not user:
                    return {}
                
                progress_records = session.query(self.LessonProgress).filter_by(
                    user_id=user.user_id,
                    lesson_id=lesson_id
                ).all()
                
                # Konwertuj do formatu JSON
                result = {}
                for record in progress_records:
                    result.update(record.to_dict())
                
                return result
        except Exception as e:
            print(f"❌ Error reading lesson progress from SQL: {e}")
            return {}
    
    def _save_lesson_progress_to_json(self, username: str, lesson_id: str, section_name: str, progress_data: Dict[str, Any]) -> bool:
        """Zapisuje lesson_progress do JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            if username not in users:
                return False
            
            if 'lesson_progress' not in users[username]:
                users[username]['lesson_progress'] = {}
            
            if lesson_id not in users[username]['lesson_progress']:
                users[username]['lesson_progress'][lesson_id] = {}
            
            # Merge progress data
            users[username]['lesson_progress'][lesson_id].update(progress_data)
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Error saving lesson progress to JSON: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _save_lesson_progress_to_sql(self, username: str, lesson_id: str, section_name: str, progress_data: Dict[str, Any]) -> bool:
        """Zapisuje lesson_progress do SQL"""
        if not self.sql_available:
            return False
        
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                if not user:
                    return False
                
                # Sprawdź czy rekord istnieje
                progress = session.query(self.LessonProgress).filter_by(
                    user_id=user.user_id,
                    lesson_id=lesson_id,
                    section_name=section_name
                ).first()
                
                if progress:
                    # Update existing
                    progress.xp_awarded = progress_data.get(f"{section_name}_xp_awarded", progress.xp_awarded)
                    progress.completed = progress_data.get(f"{section_name}_completed", progress.completed)
                    progress.xp = progress_data.get(f"{section_name}_xp", progress.xp)
                    progress.degencoins = progress_data.get(f"{section_name}_degencoins", progress.degencoins)
                    
                    timestamp_str = progress_data.get(f"{section_name}_timestamp")
                    if timestamp_str:
                        try:
                            progress.timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                        except (ValueError, TypeError):
                            pass
                else:
                    # Create new
                    progress = self.LessonProgress.from_dict(user.user_id, lesson_id, section_name, progress_data)
                    session.add(progress)
                
                session.commit()
                return True
        except Exception as e:
            print(f"❌ Error saving lesson progress to SQL: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # =============================================================================
    # LESSON ACCESS
    # =============================================================================
    
    def get_lesson_access(self, username: str) -> Dict[str, bool]:
        """Pobiera dostęp do lekcji"""
        if self._should_use_sql_for_read(username):
            self._ensure_sql_initialized()
            if self.sql_available:
                return self._get_lesson_access_from_sql(username)
        
        return self._get_lesson_access_from_json(username)
    
    def set_lesson_access(self, username: str, lesson_id: str, has_access: bool) -> bool:
        """Ustawia dostęp do lekcji"""
        self._ensure_sql_initialized()  # Ensure SQL is ready
        
        success = True
        
        # Wymuszenie SQL jeśli backend="sql"
        if self.backend == "sql":
            if self.sql_available:
                return self._set_lesson_access_to_sql(username, lesson_id, has_access)
            else:
                print("⚠️  SQL not available, falling back to JSON")
                return self._set_lesson_access_to_json(username, lesson_id, has_access)
        
        # Dual write mode
        if self._is_dual_write_enabled():
            success &= self._set_lesson_access_to_json(username, lesson_id, has_access)
            if self.sql_available:
                success &= self._set_lesson_access_to_sql(username, lesson_id, has_access)
        
        # SQL write
        elif self._should_use_sql_for_write(username):
            if self.sql_available:
                success = self._set_lesson_access_to_sql(username, lesson_id, has_access)
            else:
                success = self._set_lesson_access_to_json(username, lesson_id, has_access)
        
        # JSON write
        else:
            success = self._set_lesson_access_to_json(username, lesson_id, has_access)
        
        return success
    
    def _get_lesson_access_from_json(self, username: str) -> Dict[str, bool]:
        """Pobiera lesson_access z JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            return users.get(username, {}).get('lesson_access', {})
        except Exception as e:
            print(f"❌ Error reading lesson access from JSON: {e}")
            return {}
    
    def _get_lesson_access_from_sql(self, username: str) -> Dict[str, bool]:
        """Pobiera lesson_access z SQL"""
        if not self.sql_available:
            return {}
        
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                if not user:
                    return {}
                
                access_records = session.query(self.LessonAccess).filter_by(user_id=user.user_id).all()
                return {record.lesson_id: record.has_access for record in access_records}
        except Exception as e:
            print(f"❌ Error reading lesson access from SQL: {e}")
            return {}
    
    def _set_lesson_access_to_json(self, username: str, lesson_id: str, has_access: bool) -> bool:
        """Ustawia lesson_access w JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            if username not in users:
                return False
            
            if 'lesson_access' not in users[username]:
                users[username]['lesson_access'] = {}
            
            users[username]['lesson_access'][lesson_id] = has_access
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Error setting lesson access in JSON: {e}")
            return False
    
    def _set_lesson_access_to_sql(self, username: str, lesson_id: str, has_access: bool) -> bool:
        """Ustawia lesson_access w SQL"""
        if not self.sql_available:
            return False
        
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                if not user:
                    return False
                
                # Sprawdź czy rekord istnieje
                access = session.query(self.LessonAccess).filter_by(
                    user_id=user.user_id,
                    lesson_id=lesson_id
                ).first()
                
                if access:
                    access.has_access = has_access
                else:
                    access = self.LessonAccess(
                        user_id=user.user_id,
                        lesson_id=lesson_id,
                        has_access=has_access
                    )
                    session.add(access)
                
                session.commit()
                return True
        except Exception as e:
            print(f"❌ Error setting lesson access in SQL: {e}")
            import traceback
            traceback.print_exc()
            return False
