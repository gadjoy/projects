from flask import Flask, request, jsonify
from flask_cors import CORS
from components.dataframe import create_filtered_df
from components.proposal import generate_proposal
from components.freelancer import _get_project_by_id, _place_project_bid
import requests  # Import the requests module separately
import os
import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Store the OAuth token and API key globally
oauth_token = None
api_key = None

# Define backend version
backend_version = '1.0.0'  # Update with your backend version
build = 'built:001'

# Manually set the modified date here
backend_modified_date = "01-04-2024"

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/set_tokens', methods=['POST'])
def set_tokens():
    global oauth_token, api_key

    data = request.json
    oauth_token = data.get('oauth_token')
    api_key = data.get('api_key')
    # Do something with the tokens, like storing them in a database or using them for authentication
    return jsonify({'message': 'Tokens set successfully'})

@app.route('/search_projects', methods=['GET'])
def search_projects():
    global oauth_token
    query = request.args.get('query')
    if not oauth_token:
        return jsonify({'error': 'OAuth token is required'}), 400
    df_filtered = create_filtered_df(query, oauth_token)
    return df_filtered.to_json(orient='records')

@app.route('/generate_proposal', methods=['POST', 'GET'])
def generate_proposal_route():
    global oauth_token, api_key

    if request.method == 'POST' or request.method == 'GET':
        project_id = request.args.get('project_id') or request.json.get('project_id')
        if not project_id:
            return jsonify({'error': 'Project ID is required'}), 400
 
        if not (oauth_token and api_key):
            return jsonify({'error': 'OAuth token and API key are required'}), 401

        project = _get_project_by_id(project_id, oauth_token)
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        project_title = project['title']
        project_description = project['description']
        proposal = generate_proposal(project_title, project_description, api_key)
        return jsonify({'proposal': proposal})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/place_bid', methods=['POST'])
def place_bid():
    global oauth_token
    if not oauth_token:
        return jsonify({'error': 'OAuth token is required'}), 400
    project_id = request.args.get('project_id')
    amount = request.args.get('amount')
    proposal = request.args.get('proposal')
    return _place_project_bid(project_id, amount, proposal, oauth_token)

@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({
        'backend_version': f"api@{backend_version} {build} {backend_modified_date}",
    })

if __name__ == '__main__':
    app.run(debug=True)