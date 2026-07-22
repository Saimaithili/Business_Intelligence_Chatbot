import sqlite3
import bcrypt

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
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)",
            (full_name, email, hashed.decode("utf-8"))
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False


def login_user(email, password):
    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )
    user = cursor.fetchone()

    if user is None:
        return None

    stored_password = user[3]

    try:
        stored_hash = stored_password.encode("utf-8")

        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return user

    except ValueError:
        return None

    return None


def update_password(email, new_password):
    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        (hashed.decode("utf-8"), email)
    )
    conn.commit()


def update_profile(user_id, full_name, email):
    try:
        cursor.execute(
            "UPDATE users SET full_name=?, email=? WHERE id=?",
            (full_name, email, user_id)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # email already used by a different account
        return False