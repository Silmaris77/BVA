from sqlalchemy import create_engine, text
from v2.backend.database import DATABASE_URL

def migrate():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            # Check if column exists
            result = conn.execute(text("PRAGMA table_info(users)")).fetchall()
            columns = [row[1] for row in result]
            
            if 'preferences' not in columns:
                print("Adding 'preferences' column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN preferences TEXT")) # SQLite stores JSON as TEXT
                print("Migration successful.")
            else:
                print("'preferences' column already exists.")
                
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
