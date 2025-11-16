import sqlite3

# Use the correct database path
conn = sqlite3.connect('database/bva_app.db')
cursor = conn.cursor()

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", [t[0] for t in tables])

# Check if Marcin exists in any game table
for table in tables:
    table_name = table[0]
    try:
        cursor.execute(f"SELECT * FROM {table_name} WHERE username='Marcin' LIMIT 1")
        row = cursor.fetchone()
        if row:
            print(f"\nFound Marcin in table: {table_name}")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"Columns: {[c[1] for c in columns]}")
    except:
        pass

conn.close()
