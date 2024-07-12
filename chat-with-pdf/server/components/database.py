import sqlite3
from werkzeug.security import generate_password_hash

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
                 title TEXT NOT NULL,
                 access_id INTEGER,
                 FOREIGN KEY(access_id) REFERENCES user(id))''')

    # Check and insert admin user
    add_user(c, 'admin', 'admin123', 'admin')
    add_user(c, 'user1', 'user123', 'user')
    add_user(c, 'user2', 'user123', 'user')

    # Commit and close
    conn.commit()
    conn.close()

    print("Database and admin user created!")

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

def upload_file(title, access_ids):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO file (title, access_id) VALUES (?, ?)', (title, ','.join(map(str, access_ids))))
    conn.commit()
    conn.close()

def get_files_by_username(username):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM user WHERE username=?', (username,))
    user_id = cursor.fetchone()
    if user_id:
        user_id = user_id[0]
        cursor.execute('SELECT title FROM file WHERE access_id=?', (user_id,))
    else:
        cursor.execute('SELECT title FROM file WHERE access_id IS NULL')
    files = cursor.fetchall()
    conn.close()
    return [file[0] for file in files]

def get_user_ids(usernames):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM user WHERE username IN ({})'.format(','.join('?' * len(usernames))), usernames)
    user_ids = cursor.fetchall()
    conn.close()
    return [user_id[0] for user_id in user_ids]


def set_file_access(pdf_name, access_usernames):
    if not isinstance(pdf_name, str) or not all(isinstance(username, str) for username in access_usernames):
        raise ValueError("Both 'pdf_name' and 'access_usernames' must be strings")

    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    

    # Get user IDs from the access_usernames list
    access_ids = []
    for username in access_usernames:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()
        if user_id:
            access_ids.append(str(user_id[0]))

    if not access_ids:
        conn.close()
        raise ValueError("No valid users found for access.")

    # Update the access_id column in the file table
    access_id_str = ','.join(access_ids)
    cursor.execute("UPDATE file SET access_id = ? WHERE title = ?", (access_id_str, pdf_name))
    conn.commit()
    conn.close()



# def delete_file_table():
#     """Delete the file table from the database."""
#     conn = sqlite3.connect('site.db')
#     c = conn.cursor()

#     # Drop the file table
#     c.execute("DROP TABLE IF EXISTS file")
    
#     # Commit and close
#     conn.commit()
#     conn.close()

#     print("File table deleted!")
