import sqlite3

DB_NAME = "mock.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(sql_query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query, params)
        if sql_query.strip().lower().startswith("select"):
            return [dict(row) for row in cursor.fetchall()]
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()