import sqlite3
import bcrypt
import uuid
import datetime

db_path = "users.db"
username = "admin"
password = "admin"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sprawdź czy tabela istnieje
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
if not cursor.fetchone():
    print("Tabela 'users' nie istnieje! Tworzę...")
    # SQL z models.py (w przybliżeniu)
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id VARCHAR NOT NULL UNIQUE,
        username VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        degen_type VARCHAR(50),
        xp INTEGER DEFAULT 0,
        degencoins INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        company VARCHAR(100),
        permissions TEXT,
        account_created_by VARCHAR(100),
        joined_date DATE NOT NULL,
        last_login DATETIME,
        test_taken BOOLEAN DEFAULT 0,
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
    print(f"Użytkownik {username} istnieje. Aktualizuję hasło...")
    cursor.execute("UPDATE users SET password_hash=? WHERE username=?", (password_hash, username))
else:
    print(f"Tworzę użytkownika {username}...")
    user_id = str(uuid.uuid4())
    cursor.execute('''INSERT INTO users 
        (user_id, username, password_hash, xp, level, degencoins, degen_type, company, joined_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (user_id, username, password_hash, 1000, 5, 500, "Admin", "BrainVentureAcademy", now, now))

conn.commit()
print("Gotowe. Konto admina zaktualizowane.")
conn.close()
