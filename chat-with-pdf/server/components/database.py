import sqlite3
from werkzeug.security import generate_password_hash

def get_user_credentials_by_username(username):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    # Selecting only username and password_hash columns
    c.execute("SELECT username, password FROM user WHERE username = ?", (username,))
    user_credentials = c.fetchone()
    conn.close()
    return user_credentials

def add_user(c, username, password, role):
    # Check if the user already exists
    c.execute("SELECT * FROM user WHERE username=?", (username,))
    if not c.fetchone():
        # Insert the new user
        c.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                  (username, generate_password_hash(password), role))

def create_database():
    """Create the database and tables using sqlite3."""
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS user (
                 id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 role TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS file (
                 id INTEGER PRIMARY KEY,
                 path TEXT NOT NULL,
                 user_id INTEGER,
                 FOREIGN KEY(user_id) REFERENCES user(id))''')

    # Check and insert admin user
    add_user(c, 'admin', 'admin123', 'admin')
    add_user(c, 'user1', 'user123', 'user')
    add_user(c, 'user2', 'user123', 'user')

    # Commit and close
    conn.commit()
    conn.close()

    print("Database and admin user created!")