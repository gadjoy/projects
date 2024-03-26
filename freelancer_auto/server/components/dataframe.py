import pandas as pd
from datetime import datetime
import os

from components.freelancer import _get_project_by_id, _search_projects
from components.proposal import generate_proposal

def create_df(query):
    p = _search_projects(query)

    # Assuming 'p' is your JSON data
    data = p['projects']

    # Flatten the data
    df = pd.json_normalize(data)

    # Convert column names with '.' to '_'
    df.columns = df.columns.str.replace('.', '_')

    # create a column with the query string
    df['query'] = query

    # update the csv file with the new data
    csv = 'data/projects.csv'
    dir = os.path.dirname(csv)

    # Check if the directory exists, and if not, create it
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Read the existing data
    if os.path.exists(csv):
        df_existing = pd.read_csv(csv)

        # Find the IDs in the new DataFrame that are not in the existing DataFrame
        new_ids = set(df['id']) - set(df_existing['id'])

        # Keep only the rows with new IDs
        df_new = df[df['id'].isin(new_ids)]

        # Append the new rows to the CSV file
        df_new.to_csv(csv, mode='a', header=False)
    else:
        # If the CSV file doesn't exist, write the entire DataFrame
        df.to_csv(csv)

    return df

def create_filtered_df(query):

    df = create_df(query)

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

    # populate the new columns into the csv file only for the ids that are there in the df_filtered

    csv = 'data/projects.csv'

    # Read the existing data
    # df_existing = pd.read_csv(csv)

    # In the create_filtered_df function in components/dataframe.py

    # df_updated = pd.merge(df_existing, df_filtered, on='id', how='left', suffixes=('_existing', '_filtered'))

    # Write the updated DataFrame back to the CSV file
    # df_updated.to_csv(csv, index=False)

    return df_filtered

from flask import jsonify

def create_proposals(id):
    csv = 'data/projects.csv'

    # Read the existing data
    df_existing = pd.read_csv(csv)
    print("DataFrame read from CSV:", df_existing)

    # Filter the DataFrame to include only the row with the specified ID
    df_filtered = df_existing[df_existing['id'] == id]
    print("Filtered DataFrame:", df_filtered)

    # Generate proposals
    proposals = []
    for _, row in df_filtered.iterrows():
        proposal = generate_proposal(row['title'], row['description'])
        print("Proposal generated:", proposal)
        proposals.append(proposal)

    # Update the specific row in the existing DataFrame
    df_existing.loc[df_existing['id'] == id, 'proposal'] = proposals
    print("Updated DataFrame:", df_existing)

    # Write the updated DataFrame back to the CSV file
    df_existing.to_csv(csv, index=False)

    # Return the row with the specified ID as JSON
    return jsonify(df_existing.loc[df_existing['id'] == id].to_dict(orient='records'))
