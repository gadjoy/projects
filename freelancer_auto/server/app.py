from flask import Flask, request, jsonify
import requests
import os, json
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS

from components.dataframe import create_df

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/search_projects', methods=['GET'])
def search_projects():
    query = request.args.get('query')
    limit = request.args.get('limit')
    df = create_df(query, limit)
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)