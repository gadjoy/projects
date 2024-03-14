from flask import Flask, request
from flask_cors import CORS, cross_origin

from components.dataframe import create_filtered_df, create_proposals
from components.freelancer import _place_project_bid

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/search_projects', methods=['GET'])
@cross_origin()
def search_projects():
    query = request.args.get('query')
    df_filtered = create_filtered_df(query)
    return df_filtered.to_json(orient='records')

@app.route('/generate_proposal', methods=['GET'])
def generate_proposal():
    id = request.args.get('id')
    return create_proposals(id)

@app.route('/place_bid', methods=['POST'])
def place_bid():
    project_id = request.args.get['project_id']
    amount = request.args.get['amount']
    proposal = request.args.get['proposal']
    return _place_project_bid(project_id, amount, proposal)

if __name__ == '__main__':
    app.run(debug=True)