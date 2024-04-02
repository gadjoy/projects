from flask import Flask, request, jsonify
from flask_cors import CORS
from components.dataframe import create_filtered_df
from components.proposal import generate_proposal
from components.freelancer import _get_project_by_id
from components.freelancer import _place_project_bid

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/search_projects', methods=['GET'])
def search_projects():
    query = request.args.get('query')
    df_filtered = create_filtered_df(query)
    return df_filtered.to_json(orient='records')

@app.route('/generate_proposal', methods=['GET', 'POST'])
def generate_proposal_route():
    if request.method == 'POST':
        data = request.json
        project_id = data.get('project_id')
        if not project_id:
            return jsonify({'error': 'Project ID is required'}), 400

        project = _get_project_by_id(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        project_title = project['title']
        project_description = project['description']
        proposal = generate_proposal(project_title, project_description)
        return jsonify({'proposal': proposal})
    elif request.method == 'GET':
        project_id = request.args.get('project_id')
        if not project_id:
            return jsonify({'error': 'Project ID is required'}), 400

        project = _get_project_by_id(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        project_title = project['title']
        project_description = project['description']
        proposal = generate_proposal(project_title, project_description)
        return jsonify({'proposal': proposal})
    else:
        return jsonify({'error': 'Method not allowed'}), 405


@app.route('/place_bid', methods=['POST'])
def place_bid():
    project_id = request.args.get('project_id')
    amount = request.args.get('amount')
    proposal = request.args.get('proposal')
    return _place_project_bid(project_id, amount, proposal)

if __name__ == '__main__':
    app.run(debug=True)
