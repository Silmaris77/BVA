"""
Migration: Add LessonNotes table for storing user notes (Action Plan, Reflection Journal)

Dodaje nową tabelę lesson_notes do przechowywania notatek użytkownika:
- Action Plan (action_today, action_tomorrow, action_week)
- Reflection Journal (reflection_discovery, reflection_doubts, reflection_application)
- Dowolne inne notatki w przyszłości

Struktura:
- user_id, lesson_id, field_name (unique constraint)
- value (TEXT) - treść notatki
- created_at, updated_at
"""

import sys
from pathlib import Path

# Add BVA root to path
APP_DIR = Path(__file__).parent
sys.path.insert(0, str(APP_DIR))

from database.connection import get_engine, session_scope
from database.models import Base, GUID
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, Index
from datetime import datetime
import uuid


def run_migration():
    """Dodaje tabelę lesson_notes"""
    
    print("🔧 Migration: Add LessonNotes table")
    print("=" * 60)
    
    # Get engine
    engine = get_engine()
    
    try:
        # Sprawdź czy tabela już istnieje
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        
        if 'lesson_notes' in inspector.get_table_names():
            print("✅ Tabela 'lesson_notes' już istnieje!")
            return
        
        # Utwórz tabelę przez SQL (unikamy konfliktu z Base.metadata)
        print("📝 Tworzę tabelę lesson_notes...")
        
        create_table_sql = """
        CREATE TABLE lesson_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id CHAR(36) NOT NULL,
            lesson_id VARCHAR(255) NOT NULL,
            field_name VARCHAR(100) NOT NULL,
            value TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            UNIQUE (user_id, lesson_id, field_name)
        )
        """
        
        with engine.connect() as conn:
            conn.execute(text(create_table_sql))
            conn.execute(text("CREATE INDEX idx_user_lesson_notes ON lesson_notes(user_id, lesson_id)"))
            conn.commit()
        
        print("✅ Tabela lesson_notes utworzona pomyślnie!")
        
        # Pokaż strukturę
        print("\n📊 Struktura tabeli:")
        print("  - id (PRIMARY KEY)")
        print("  - user_id (FOREIGN KEY → users.user_id)")
        print("  - lesson_id (VARCHAR 255)")
        print("  - field_name (VARCHAR 100) - np. 'action_today', 'reflection_discovery'")
        print("  - value (TEXT) - treść notatki")
        print("  - created_at (DATETIME)")
        print("  - updated_at (DATETIME)")
        print("\n🔑 Constraints:")
        print("  - UNIQUE(user_id, lesson_id, field_name)")
        print("  - INDEX(user_id, lesson_id)")
        
        print("\n✅ Migracja zakończona pomyślnie!")
        
    except Exception as e:
        print(f"❌ Błąd podczas migracji: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 Uruchamianie migracji: Add LessonNotes table")
    print()
    run_migration()
