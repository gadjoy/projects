import sqlite3
import pandas as pd

def update_database(df, table_name):
    db_file = 'data/projects.db'
    with sqlite3.connect(db_file) as conn:
        df.to_sql(table_name, conn, if_exists='replace' if table_name == 'filtered_projects' else 'append', index=False)

def read_from_database(query):
    db_file = 'data/projects.db'
    with sqlite3.connect(db_file) as conn:
        return pd.read_sql_query(query, conn)
