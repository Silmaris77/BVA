import sqlite3

db_path = "users.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Usuń starą tabelę
cursor.execute("DROP TABLE IF EXISTS users")
print("Usunięto tabelę users.")

conn.commit()
conn.close()
