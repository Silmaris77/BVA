import sqlite3
from v2.backend.database import DB_PATH

def create_tool_results_table():
    print(f"Connecting to {DB_PATH}...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # SQL for ToolResult table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS tool_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR NOT NULL,
            tool_id VARCHAR(50) NOT NULL,
            input_data TEXT,
            output_data TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        );
        """
        
        print("Creating table tool_results...")
        cursor.execute(create_table_sql)
        
        # Index on user_id
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_tool_results_user_id ON tool_results (user_id)")
        
        conn.commit()
        conn.close()
        print("Table tool_results created successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_tool_results_table()
