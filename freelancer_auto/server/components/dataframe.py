import pandas as pd
from datetime import datetime

from components.freelancer import _get_project_by_id, _search_projects
from components.proposal import generate_proposal

def create_df(query, limit):
    p = _search_projects(query, limit)

    # Assuming 'p' is your JSON data
    data = p['projects']

    # Flatten the data
    df = pd.json_normalize(data)

    # Convert column names with '.' to '_'
    df.columns = df.columns.str.replace('.', '_')

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
        return _get_project_by_id(id)['description']

    # Create a new column 'description' by applying 'get_description' to each ID
    df_filtered['description'] = df_filtered['id'].apply(get_description)

    # Convert the 'submitdate' to a human-readable format
    df_filtered['submitdate'] = df_filtered['submitdate'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

    # Convert the 'submitdate' to a datetime object
    df_filtered['submitdate'] = pd.to_datetime(df_filtered['submitdate'])

    # Generate proposals
    df_filtered['proposal'] = df_filtered.apply(lambda row: generate_proposal(row['title'], row['description']), axis=1)

    return df