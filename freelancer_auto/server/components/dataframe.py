import pandas as pd
from datetime import datetime
import os
from .freelancer import _search_projects, _get_project_by_id  # Import _get_project_by_id from local module
from components.proposal import generate_proposal
from flask import jsonify
from .database import update_database, read_from_database  # Relative import

# Your functions...



def create_df(query, oauth_token):
    p = _search_projects(query, oauth_token)
    data = p['projects']
    df = pd.json_normalize(data)
    df.columns = df.columns.str.replace('.', '_')
    df = df[['id', 'title', 'seo_url', 'submitdate', 'budget_minimum', 'budget_maximum', 'currency_code', 'currency_exchange_rate', 'bid_stats_bid_count', 'bid_stats_bid_avg']]

    existing_ids = read_from_database("SELECT id FROM projects")['id']
    df_to_insert = df[~df['id'].isin(existing_ids)]
    
    if not df_to_insert.empty:
        update_database(df_to_insert, 'projects')

    return df

def create_filtered_df(query, oauth_token):
    df = create_df(query, oauth_token)
    columns = ['id', 'title', 'seo_url', 'submitdate', 'budget_minimum', 'budget_maximum', 'currency_code', 'currency_exchange_rate', 'bid_stats_bid_count', 'bid_stats_bid_avg']
    df_filtered = df[columns]
    df_filtered['budget_maximum_usd'] = df_filtered['budget_maximum'] * df_filtered['currency_exchange_rate']
    df_filtered['budget_minimum_usd'] = df_filtered['budget_minimum'] * df_filtered['currency_exchange_rate']

    def get_description(id):
        return _get_project_by_id(id, oauth_token)['description']

    df_filtered['description'] = df_filtered['id'].apply(get_description)

    df_filtered['submitdate'] = df_filtered['submitdate'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    df_filtered['submitdate'] = pd.to_datetime(df_filtered['submitdate'])

    update_database(df_filtered, 'filtered_projects')

    return df_filtered

def create_proposals(id):
    df_existing = read_from_database("SELECT * FROM projects WHERE id = {}".format(id))
    df_filtered = df_existing[df_existing['id'] == id]

    proposals = []
    for _, row in df_filtered.iterrows():
        proposal = generate_proposal(row['title'], row['description'])
        proposals.append(proposal)

    for proposal in proposals:
        update_database(df_existing, 'projects')

    return jsonify(df_existing.loc[df_existing['id'] == id].to_dict(orient='records'))
