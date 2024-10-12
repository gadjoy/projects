import pandas as pd
from datetime import datetime
from components.freelancer import _get_project_by_id, _search_projects
from components.proposal import generate_proposal
from flask import jsonify
from .database import create_connection, create_tables, update_app, update_user, read_app, read_user

def create_df(query, oauth_token):
    p = _search_projects(query, oauth_token)

    # Assuming 'p' is your JSON data
    data = p['projects']

    # Flatten the data
    df = pd.json_normalize(data)

    # Convert column names with '.' to '_'
    df.columns = df.columns.str.replace('.', '_')

    # Remove columns that don't exist in the database schema
    df = df[['id', 'title', 'seo_url', 'submitdate', 'budget_minimum', 'budget_maximum', 'currency_code', 'currency_exchange_rate', 'bid_stats_bid_count', 'bid_stats_bid_avg']]

    # Update the database with the new data
    conn = create_connection()
    if conn is not None:
        create_tables()
        update_app(conn, df)

    return df

def update_user_table(df_raw):
    # Store raw data in the 'user' table
    conn = create_connection()
    if conn is not None:
        update_user(conn, df_raw)

def create_filtered_df(query, oauth_token):
    df_raw = create_df(query, oauth_token)  # Get raw data before filtering
    update_user_table(df_raw)

    df = df_raw.copy()  # Create a copy for filtering

    # Define the columns you want to keep
    columns = ['id', 'title', 'seo_url', 'submitdate', 'budget_minimum', 'budget_maximum', 'currency_code', 'currency_exchange_rate', 'bid_stats_bid_count', 'bid_stats_bid_avg']

    # Create a new DataFrame with only the columns you want
    df_filtered = df[columns]

    # Convert the budget columns to USD
    df_filtered['budget_maximum_usd'] = df_filtered['budget_maximum'] * df_filtered['currency_exchange_rate']
    df_filtered['budget_minimum_usd'] = df_filtered['budget_minimum'] * df_filtered['currency_exchange_rate']

    # Define your function
    def get_description(id):
        # Replace this with your actual function
        return _get_project_by_id(id, oauth_token)['description']

    # Create a new column 'description' by applying 'get_description' to each ID
    df_filtered['description'] = df_filtered['id'].apply(get_description)

    # Convert the 'submitdate' to a human-readable format
    df_filtered['submitdate'] = df_filtered['submitdate'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

    # Convert the 'submitdate' to a datetime object
    df_filtered['submitdate'] = pd.to_datetime(df_filtered['submitdate'])

    # Update the database with the filtered data
    conn = create_connection()
    if conn is not None:
        update_app(conn, df_filtered)  # Update 'app' table with filtered data

    return df_filtered
