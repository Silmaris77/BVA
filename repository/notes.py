"""
Repository: User Notes
Obsługa CRUD dla notatek gracza w systemie FMCG Game

Kategorie notatek:
- product_card: Karty produktów (cena, marża, USP)
- elevator_pitch: Elevator pitches
- mentor_tip: Wskazówki od mentora
- manager_feedback: Feedback od menedżera
- client_profile: Profile klientów
- personal: Notatki własne
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json


class NotesRepository:
    """Repository do zarządzania notatkami użytkownika"""
    
    def __init__(self, db_path: str = None):
        # Domyślna ścieżka do bazy danych w projekcie
        if db_path is None:
            from pathlib import Path
            self.db_path = str(Path(__file__).parent.parent / "database" / "bva_app.db")
        else:
            self.db_path = db_path
    
    def _get_connection(self) -> sqlite3.Connection:
        """Utwórz połączenie z bazą danych"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ===== CREATE =====
    
    def create_note(
        self,
        user_id: int,
        category: str,
        title: str,
        content: str,
        related_product_id: Optional[int] = None,
        related_client_id: Optional[int] = None,
        is_pinned: bool = False,
        color_tag: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> int:
        """
        Utwórz nową notatkę
        
        Returns:
            note_id nowo utworzonej notatki
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Konwertuj tagi na JSON
        tags_json = json.dumps(tags) if tags else None
        
        cursor.execute("""
            INSERT INTO user_notes (
                user_id, category, title, content,
                related_product_id, related_client_id,
                is_pinned, color_tag, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, category, title, content,
            related_product_id, related_client_id,
            1 if is_pinned else 0, color_tag, tags_json
        ))
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return note_id
    
    # ===== READ =====
    
    def get_note_by_id(self, note_id: int) -> Optional[Dict]:
        """Pobierz notatkę po ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_notes WHERE note_id = ?", (note_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def get_user_notes(
        self,
        user_id: int,
        category: Optional[str] = None,
        pinned_only: bool = False
    ) -> List[Dict]:
        """
        Pobierz notatki użytkownika
        
        Args:
            user_id: ID użytkownika
            category: Filtr po kategorii (opcjonalnie)
            pinned_only: Tylko przypięte notatki
            
        Returns:
            Lista notatek (przypięte na początku)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM user_notes WHERE user_id = ?"
        params = [user_id]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if pinned_only:
            query += " AND is_pinned = 1"
        
        # Sortowanie: przypięte na górze, potem po dacie edycji
        query += " ORDER BY is_pinned DESC, updated_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_notes_by_category(self, user_id: int) -> Dict[str, List[Dict]]:
        """
        Pobierz wszystkie notatki pogrupowane po kategorii
        
        Returns:
            Dict: {category: [notes]}
        """
        all_notes = self.get_user_notes(user_id)
        
        categories = {
            'product_card': [],
            'elevator_pitch': [],
            'mentor_tip': [],
            'manager_feedback': [],
            'client_profile': [],
            'personal': []
        }
        
        for note in all_notes:
            category = note['category']
            if category in categories:
                categories[category].append(note)
        
        return categories
    
    def search_notes(
        self,
        user_id: int,
        search_term: str,
        category: Optional[str] = None
    ) -> List[Dict]:
        """
        Wyszukaj notatki po tytule lub treści
        
        Args:
            user_id: ID użytkownika
            search_term: Fraza do wyszukania
            category: Opcjonalny filtr kategorii
            
        Returns:
            Lista pasujących notatek
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT * FROM user_notes 
            WHERE user_id = ? 
            AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)
        """
        params = [user_id, f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY is_pinned DESC, updated_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_notes_for_product(self, user_id: int, product_id: int) -> List[Dict]:
        """Pobierz wszystkie notatki związane z produktem"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM user_notes 
            WHERE user_id = ? AND related_product_id = ?
            ORDER BY is_pinned DESC, updated_at DESC
        """, (user_id, product_id))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_notes_for_client(self, user_id: int, client_id: int) -> List[Dict]:
        """Pobierz wszystkie notatki związane z klientem"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM user_notes 
            WHERE user_id = ? AND related_client_id = ?
            ORDER BY is_pinned DESC, updated_at DESC
        """, (user_id, client_id))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    # ===== UPDATE =====
    
    def update_note(
        self,
        note_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        is_pinned: Optional[bool] = None,
        color_tag: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Aktualizuj notatkę (partial update)
        
        Returns:
            True jeśli zaktualizowano, False jeśli nie znaleziono
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Przygotuj listę pól do aktualizacji
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        
        if is_pinned is not None:
            updates.append("is_pinned = ?")
            params.append(1 if is_pinned else 0)
        
        if color_tag is not None:
            updates.append("color_tag = ?")
            params.append(color_tag)
        
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))
        
        if not updates:
            conn.close()
            return False
        
        # Dodaj note_id do parametrów
        params.append(note_id)
        
        query = f"UPDATE user_notes SET {', '.join(updates)} WHERE note_id = ?"
        cursor.execute(query, params)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def toggle_pin(self, note_id: int) -> bool:
        """
        Przełącz status przypięcia notatki
        
        Returns:
            True jeśli zaktualizowano
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Pobierz aktualny status
        cursor.execute("SELECT is_pinned FROM user_notes WHERE note_id = ?", (note_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        # Odwróć status
        new_status = 0 if row['is_pinned'] else 1
        cursor.execute("UPDATE user_notes SET is_pinned = ? WHERE note_id = ?", 
                      (new_status, note_id))
        
        conn.commit()
        conn.close()
        return True
    
    # ===== DELETE =====
    
    def delete_note(self, note_id: int) -> bool:
        """
        Usuń notatkę
        
        Returns:
            True jeśli usunięto, False jeśli nie znaleziono
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM user_notes WHERE note_id = ?", (note_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    def delete_user_notes(self, user_id: int, category: Optional[str] = None) -> int:
        """
        Usuń wszystkie notatki użytkownika (lub tylko z danej kategorii)
        
        Returns:
            Liczba usuniętych notatek
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute(
                "DELETE FROM user_notes WHERE user_id = ? AND category = ?",
                (user_id, category)
            )
        else:
            cursor.execute("DELETE FROM user_notes WHERE user_id = ?", (user_id,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    # ===== STATISTICS =====
    
    def get_notes_stats(self, user_id: int) -> Dict[str, int]:
        """
        Statystyki notatek użytkownika
        
        Returns:
            Dict z liczbą notatek per kategoria + total
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM user_notes
            WHERE user_id = ?
            GROUP BY category
        """, (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        stats = {
            'product_card': 0,
            'elevator_pitch': 0,
            'mentor_tip': 0,
            'manager_feedback': 0,
            'client_profile': 0,
            'personal': 0,
            'total': 0
        }
        
        for row in rows:
            category = row['category']
            count = row['count']
            stats[category] = count
            stats['total'] += count
        
        return stats
    
    # ===== HELPERS =====
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Konwertuj Row na Dict i parsuj JSON"""
        note = dict(row)
        
        # Parsuj tags z JSON
        if note.get('tags'):
            try:
                note['tags'] = json.loads(note['tags'])
            except:
                note['tags'] = []
        else:
            note['tags'] = []
        
        # Konwertuj is_pinned na bool
        note['is_pinned'] = bool(note['is_pinned'])
        
        return note


# ===== PRZYKŁADOWE UŻYCIE =====
if __name__ == "__main__":
    # Test repository
    repo = NotesRepository()
    
    # Przykład: Utwórz notatkę
    note_id = repo.create_note(
        user_id=1,
        category='product_card',
        title='Chocolate Supreme',
        content='Cena: €15.20\nMarża: 35%\nUSP: Premium kakao z Ghany',
        is_pinned=True,
        tags=['czekolada', 'premium']
    )
    print(f"✅ Utworzono notatkę ID: {note_id}")
    
    # Przykład: Pobierz notatki użytkownika
    notes = repo.get_user_notes(user_id=1, category='product_card')
    print(f"📋 Notatki użytkownika: {len(notes)}")
    
    # Przykład: Wyszukaj
    results = repo.search_notes(user_id=1, search_term='czekolada')
    print(f"🔍 Wyniki wyszukiwania: {len(results)}")
    
    # Przykład: Statystyki
    stats = repo.get_notes_stats(user_id=1)
    print(f"📊 Statystyki: {stats}")
