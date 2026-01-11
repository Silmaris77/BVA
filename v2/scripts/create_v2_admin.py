import sys
import os

# Add root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

import sqlite3
import bcrypt
import uuid
import datetime

db_path = os.path.join(BASE_DIR, "users.db")
username = "admin"
password = "admin123"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sprawdź czy tabela istnieje
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
if not cursor.fetchone():
    print("Tabela 'users' nie istnieje! Tworzę...")
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id VARCHAR NOT NULL UNIQUE,
        username VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        full_name VARCHAR(100),
        degen_type VARCHAR(50),
        xp INTEGER DEFAULT 0,
        degencoins INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        company VARCHAR(100),
        avatar_url VARCHAR(255),
        preferences TEXT,
        permissions TEXT,
        account_created_by VARCHAR(100),
        joined_date DATE NOT NULL,
        last_login DATETIME,
        test_taken BOOLEAN DEFAULT 0,
        intro_completed BOOLEAN DEFAULT 0,
        created_at DATETIME,
        updated_at DATETIME
    )''')

# Sprawdź czy użytkownik istnieje
cursor.execute("SELECT id FROM users WHERE username=?", (username,))
existing = cursor.fetchone()

password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
now = datetime.datetime.now()

if existing:
    print(f"Użytkownik '{username}' istnieje. Aktualizuję hasło na '{password}'...")
    cursor.execute("UPDATE users SET password_hash=?, updated_at=? WHERE username=?", 
                   (password_hash, now, username))
else:
    print(f"Tworzę użytkownika '{username}' z hasłem '{password}'...")
    user_id = str(uuid.uuid4())
    cursor.execute('''INSERT INTO users 
        (user_id, username, password_hash, email, full_name, xp, level, degencoins, 
         degen_type, company, joined_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (user_id, username, password_hash, "admin@bva.pl", "Administrator", 
         1000, 5, 500, "Admin", "BrainVentureAcademy", now, now, now))

conn.commit()
print(f"\n✓ Gotowe!")
print(f"Login: {username}")
print(f"Hasło: {password}")
conn.close()
