import pandas as pd
from datetime import datetime
import os
import sqlite3
from components.freelancer import _get_project_by_id, _search_projects
from components.proposal import generate_proposal
from flask import jsonify

def create_df(query,oauth_token):
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
    db_file = 'data/projects.db'
    with sqlite3.connect(db_file) as conn:
        existing_ids = pd.read_sql_query("SELECT id FROM projects", conn)['id']
        df_to_insert = df[~df['id'].isin(existing_ids)]
        
        if not df_to_insert.empty:
            df_to_insert.to_sql('projects', conn, if_exists='append', index=False)

    return df

def create_filtered_df(query, oauth_token):
    df = create_df(query,oauth_token)

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
    db_file = 'data/projects.db'
    with sqlite3.connect(db_file) as conn:
        df_filtered.to_sql('filtered_projects', conn, if_exists='replace', index=False)

    return df_filtered

def create_proposals(id):
    db_file = 'data/projects.db'
    
    # Read the existing data
    with sqlite3.connect(db_file) as conn:
        df_existing = pd.read_sql_query("SELECT * FROM projects", conn)

    # Filter the DataFrame to include only the row with the specified ID
    df_filtered = df_existing[df_existing['id'] == id]

    # Generate proposals
    proposals = []
    for _, row in df_filtered.iterrows():
        proposal = generate_proposal(row['title'], row['description'])
        proposals.append(proposal)

    # Update the specific row in the existing DataFrame
    with sqlite3.connect(db_file) as conn:
        for proposal in proposals:
            conn.execute("UPDATE projects SET proposal = ? WHERE id = ?", (proposal, id))

    # Return the row with the specified ID as JSON
    return jsonify(df_existing.loc[df_existing['id'] == id].to_dict(orient='records'))