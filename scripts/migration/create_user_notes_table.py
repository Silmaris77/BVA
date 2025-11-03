"""
Migration Script: Create user_notes table
Date: 2025-11-02
Description: Uruchamia migrację tworząc tabelę user_notes w bazie danych
"""

import sqlite3
from pathlib import Path


def run_migration():
    """Uruchom migrację: stwórz tabelę user_notes"""
    
    # Ścieżka do bazy danych (2 poziomy w górę od scripts/migration/)
    db_path = Path(__file__).parent.parent.parent / "database" / "bva_app.db"
    
    if not db_path.exists():
        print(f"❌ Baza danych nie istnieje: {db_path}")
        print("   Sprawdź czy ścieżka jest poprawna.")
        return False
    
    # Ścieżka do pliku SQL (2 poziomy w górę)
    sql_file = Path(__file__).parent.parent.parent / "migrations" / "create_user_notes_table.sql"
    
    if not sql_file.exists():
        print(f"❌ Plik SQL nie istnieje: {sql_file}")
        return False
    
    try:
        # Wczytaj SQL
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Połącz się z bazą
        print(f"📂 Łączenie z bazą: {db_path}")
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Wykonaj migrację
        print("⚙️  Wykonywanie migracji...")
        
        # Wykonaj wszystko przez executescript (lepiej obsługuje triggery)
        cursor.executescript(sql_content)
        print("   ✅ Migracja wykonana")
        
        conn.commit()
        
        # Weryfikacja - sprawdź czy tabela istnieje
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='user_notes'
        """)
        
        if cursor.fetchone():
            print("✅ Migracja zakończona sukcesem!")
            print("   Tabela user_notes została utworzona.")
            
            # Sprawdź strukturę tabeli
            cursor.execute("PRAGMA table_info(user_notes)")
            columns = cursor.fetchall()
            print(f"\n📋 Struktura tabeli ({len(columns)} kolumn):")
            for col in columns:
                print(f"   - {col[1]}: {col[2]}")
            
            # Sprawdź indeksy
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND tbl_name='user_notes'
            """)
            indexes = cursor.fetchall()
            print(f"\n🔍 Indeksy ({len(indexes)}):")
            for idx in indexes:
                print(f"   - {idx[0]}")
            
            conn.close()
            return True
        else:
            print("❌ Błąd: Tabela user_notes nie została utworzona")
            conn.close()
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Błąd SQL: {e}")
        if 'conn' in locals():
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Błąd: {e}")
        if 'conn' in locals():
            conn.close()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🗃️  MIGRATION: Create user_notes table")
    print("=" * 60)
    print()
    
    success = run_migration()
    
    print()
    if success:
        print("🎉 Gotowe! Możesz teraz używać NotesRepository.")
    else:
        print("⚠️  Migracja nie powiodła się. Sprawdź błędy powyżej.")
    print("=" * 60)
