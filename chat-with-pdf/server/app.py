from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

from components.database import create_database, get_user_credentials_by_username

app = Flask(__name__)
CORS(app)

create_database()

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user_credentials = get_user_credentials_by_username(username)
    if user_credentials and check_password_hash(user_credentials[1], password):
        return jsonify({'message': 'Logged in'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return jsonify({'message': 'File uploaded'})
    else:
        return jsonify({'message': 'Invalid file'}), 400

@app.route('/retreive/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory('uploads', filename)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

@app.route('/files', methods=['GET'])
def get_files():
    files = os.listdir('uploads')
    cleaned_files = [file.replace('_', ' ') for file in files]
    return jsonify({'files': cleaned_files})

if __name__ == '__main__':
    create_database()
    app.run(debug=True)