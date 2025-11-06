"""
Uruchom migrację bazy danych - dodanie nowych kategorii notatek
"""

import sqlite3
from pathlib import Path

# Ścieżki
db_path = Path(__file__).parent / "database" / "bva_app.db"
migration_path = Path(__file__).parent / "migrations" / "add_new_note_categories.sql"

print("🔄 Uruchamianie migracji bazy danych...")
print(f"📁 Baza danych: {db_path}")
print(f"📜 Migracja: {migration_path}")

# Wczytaj SQL migracji
with open(migration_path, 'r', encoding='utf-8') as f:
    migration_sql = f.read()

# Połącz się z bazą danych
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Wykonaj migrację
    cursor.executescript(migration_sql)
    conn.commit()
    print("✅ Migracja zakończona pomyślnie!")
    
    # Sprawdź schemat nowej tabeli
    cursor.execute("PRAGMA table_info(user_notes)")
    columns = cursor.fetchall()
    
    print("\n📋 Schemat tabeli user_notes po migracji:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Policz notatki
    cursor.execute("SELECT COUNT(*) FROM user_notes")
    count = cursor.fetchone()[0]
    print(f"\n📊 Liczba notatek w bazie: {count}")
    
except Exception as e:
    print(f"❌ Błąd podczas migracji: {e}")
    conn.rollback()
finally:
    conn.close()

print("\n✅ Gotowe! Możesz teraz używać nowych kategorii notatek:")
print("  - visit_ideas (💡 Pomysły)")
print("  - market_analysis (📊 Analiza)")
print("  - training_notes (🎓 Szkolenie)")
