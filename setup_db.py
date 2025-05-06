import sqlite3

# Path to your database
DB_NAME = "mock.db"

def execute_sql_script(script_path):
    """Execute the SQL script file."""
    with open(script_path, 'r') as file:
        sql_script = file.read()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.executescript(sql_script)
        print(f"Executed script: {script_path}")
    except Exception as e:
        print(f"Error executing script: {e}")
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Execute the schema and seed data
    execute_sql_script("db/schema.sql")
    execute_sql_script("sample_data/seed.sql")
