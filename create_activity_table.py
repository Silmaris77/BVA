import sqlite3
import datetime

db_path = "users.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Utwórz tabelę activity_logs
print("Tworzę tabelę activity_logs...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    metadata_json TEXT,
    xp_awarded INTEGER DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
''')

# 2. Pobierz user_id dla admina
cursor.execute("SELECT user_id FROM users WHERE username='admin'")
row = cursor.fetchone()

if row:
    user_id = row[0]
    print(f"Dodaję przykładowe logi dla admina (user_id: {user_id})...")
    
    # Przykładowe dane
    activities = [
        (user_id, "login", "Zalogowano do systemu v2", None, 0, datetime.datetime.now()),
        (user_id, "lesson_completed", "Ukończono moduł 'Strategia'", '{"lesson_id": "strategy_101"}', 500, datetime.datetime.now() - datetime.timedelta(hours=2)),
        (user_id, "game_started", "Rozpoczęto symulację 'Negocjacje'", '{"game_id": "negotiation_sim"}', 0, datetime.datetime.now() - datetime.timedelta(days=1)),
        (user_id, "achievement_unlocked", "Odblokowano osiągnięcie 'Pierwsza krew'", None, 100, datetime.datetime.now() - datetime.timedelta(days=2))
    ]
    
    cursor.executemany('''
        INSERT INTO activity_logs (user_id, activity_type, description, metadata_json, xp_awarded, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', activities)
    
    conn.commit()
    print("Gotowe. Dane testowe dodane.")
else:
    print("Nie znaleziono użytkownika admin!")

conn.close()
