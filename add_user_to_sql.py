"""
Dodaj użytkownika do bazy SQL jeśli istnieje tylko w JSON
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Parametry
username_to_add = "mil2"

# Ścieżki
db_path = Path(__file__).parent / "database" / "bva_app.db"
json_path = Path(__file__).parent / "users_data.json"  # POPRAWIONE

print(f"🔍 Szukam użytkownika '{username_to_add}' w JSON...")

# Wczytaj dane z JSON
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
except FileNotFoundError:
    print(f"❌ Plik {json_path} nie istnieje")
    exit(1)

if username_to_add not in users_data:
    print(f"❌ Użytkownik '{username_to_add}' nie istnieje w JSON")
    print(f"Dostępni użytkownicy: {', '.join(users_data.keys())}")
    exit(1)

user_data = users_data[username_to_add]
print(f"✅ Znaleziono użytkownika w JSON")
print(f"   user_id: {user_data.get('user_id')}")
print(f"   degen_type: {user_data.get('degen_type')}")
print(f"   level: {user_data.get('level')}")

# Połącz z SQL
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sprawdź czy już istnieje
cursor.execute("SELECT id FROM users WHERE username = ?", (username_to_add,))
existing = cursor.fetchone()

if existing:
    print(f"⚠️ Użytkownik '{username_to_add}' już istnieje w SQL (id={existing[0]})")
    conn.close()
    exit(0)

# Dodaj użytkownika do SQL
print(f"\n📝 Dodaję użytkownika do bazy SQL...")

try:
    cursor.execute("""
        INSERT INTO users (
            user_id, username, password_hash, degen_type,
            xp, degencoins, level, joined_date, test_taken,
            company, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_data.get('user_id'),
        username_to_add,
        user_data.get('password', 'haslo123'),  # Hasło z JSON
        user_data.get('degen_type'),
        user_data.get('xp', 0),
        user_data.get('degencoins', 0),
        user_data.get('level', 1),
        user_data.get('joined_date', datetime.now().strftime('%Y-%m-%d')),
        1 if user_data.get('test_taken', False) else 0,
        user_data.get('company', 'Milwaukee'),  # Company z JSON lub domyślnie Milwaukee
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    
    conn.commit()
    
    # Pobierz nowe ID
    cursor.execute("SELECT id FROM users WHERE username = ?", (username_to_add,))
    new_id = cursor.fetchone()[0]
    
    print(f"✅ Użytkownik dodany pomyślnie!")
    print(f"   SQL id: {new_id}")
    print(f"   username: {username_to_add}")
    
    # Wyświetl wszystkich użytkowników
    cursor.execute("SELECT id, username FROM users ORDER BY id")
    all_users = cursor.fetchall()
    
    print(f"\n📋 Użytkownicy w bazie SQL ({len(all_users)}):")
    for uid, uname in all_users:
        marker = " ← NOWY" if uid == new_id else ""
        print(f"   {uid}: {uname}{marker}")
    
except Exception as e:
    print(f"❌ Błąd podczas dodawania użytkownika: {e}")
    conn.rollback()
finally:
    conn.close()

print(f"\n✅ Gotowe! Użytkownik '{username_to_add}' może teraz używać notatnika.")
