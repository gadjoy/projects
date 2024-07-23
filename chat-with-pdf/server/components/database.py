import sqlite3
from werkzeug.security import generate_password_hash

def create_database():
    """Create the database and tables using sqlite3."""
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    # Drop tables
    c.execute("DROP TABLE IF EXISTS user")
    c.execute("DROP TABLE IF EXISTS file")

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS user (
                 id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 role TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS file (
                 id INTEGER PRIMARY KEY,
                 title TEXT NOT NULL,
                 access_name TEXT NOT NULL,
                 FOREIGN KEY(access_name) REFERENCES user(username))''')

    # Check and insert admin user
    _add_user(c, 'admin', 'admin123', 'admin')
    _add_user(c, 'user1', 'user123', 'user')
    _add_user(c, 'user2', 'user123', 'user')

    # Commit and close
    conn.commit()
    conn.close()

    print("Database and admin user created!")

def _add_user(c, username, password, role):
    # Check if the user already exists
    c.execute("SELECT * FROM user WHERE username=?", (username,))
    if not c.fetchone():
        # Insert the new user
        c.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                  (username, generate_password_hash(password), role))

def get_user_credentials_by_username(username):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    # Selecting only username and password_hash columns
    c.execute("SELECT username, password FROM user WHERE username = ?", (username,))
    user_credentials = c.fetchone()
    conn.close()
    return user_credentials

def get_user_role(username):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('SELECT role FROM user WHERE username = ?', (username,))
    role = c.fetchone()
    conn.close()
    if role:
        return role[0]
    else:
        return None

def upload_file(title, access_name):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO file (title, access_name) VALUES (?, ?)', (title, access_name))
    conn.commit()
    conn.close()

def get_files_by_username(username):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM file WHERE access_name=?', (username,))
    files = cursor.fetchall()
    conn.close()
    return [file[0] for file in files]