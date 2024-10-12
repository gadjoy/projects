import sqlite3
import pandas as pd

def create_connection():
    """Create a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect('freelancer.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables():
    """Create necessary tables if they don't exist."""
    conn = create_connection()
    if conn is not None:
        create_app_table(conn)
        create_user_table(conn)

def create_app_table(conn):
    """Create an 'app' table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                seo_url TEXT,
                submitdate DATETIME,
                budget_minimum REAL,
                budget_maximum REAL,
                currency_code TEXT,
                currency_exchange_rate REAL,
                bid_stats_bid_count INTEGER,
                bid_stats_bid_avg REAL,
                description TEXT,
                proposal TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def create_user_table(conn):
    """Create a 'user' table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def update_app(conn, df):
    """Update the 'app' table with data from the DataFrame."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_temp AS SELECT * FROM app WHERE 1=0
        """)
        df.to_sql('app_temp', conn, if_exists='replace', index=False)
        cursor.execute("""
            INSERT OR REPLACE INTO app (id, title, seo_url, submitdate, budget_minimum, budget_maximum, currency_code, currency_exchange_rate, bid_stats_bid_count, bid_stats_bid_avg, description)
            SELECT id, title, seo_url, submitdate, budget_minimum, budget_maximum, currency_code, currency_exchange_rate, bid_stats_bid_count, bid_stats_bid_avg, description FROM app_temp
        """)
        cursor.execute("""
            DROP TABLE IF EXISTS app_temp
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def update_user(conn, df_raw):
    """Update the 'user' table with raw data."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_temp AS SELECT * FROM user WHERE 1=0
        """)
        df_raw.to_sql('user_temp', conn, if_exists='replace', index=False)
        cursor.execute("""
            INSERT OR REPLACE INTO user SELECT * FROM user_temp
        """)
        cursor.execute("""
            DROP TABLE IF EXISTS user_temp
        """)
        conn.commit()
        print("User table updated successfully with raw data.")
    except sqlite3.Error as e:
        print(e)

def create_df(query, oauth_token, search_projects_function):
    """Create a DataFrame from the raw project data."""
    # Fetch raw project data using the provided search_projects_function
    p = search_projects_function(query, oauth_token)

    # Assuming 'p' is your JSON data
    data = p['projects']

    # Flatten the data
    df = pd.json_normalize(data)

    # Convert column names with '.' to '_'
    df.columns = df.columns.str.replace('.', '_')

    # Remove columns that don't exist in the database schema
    df = df[['id', 'title', 'seo_url', 'submitdate', 'budget_minimum', 'budget_maximum', 'currency_code', 'currency_exchange_rate', 'bid_stats_bid_count', 'bid_stats_bid_avg', 'description']]

    return df

def read_app(conn):
    """Read all projects from the 'app' table."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM app")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e)

def read_user(conn):
    """Read all projects from the 'user' table."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e)

def fetch_user_details():
    """Fetch and print all project details from the 'user' table."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user")
            projects = cursor.fetchall()
            for project in projects:
                print(project)
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print("Error: Unable to establish connection to the database.")

# Create tables if they don't exist
create_tables()
