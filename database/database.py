import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("database/users.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()


def create_user(full_name, email, password):
    try:
        cursor.execute(
            "INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)",
            (full_name, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(email, password):
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    return cursor.fetchone()