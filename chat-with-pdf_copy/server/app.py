from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
import sqlite3
from flask_cors import CORS
from components.database import (
    create_database,
    get_user_credentials_by_username,
    get_user_role,
    upload_file,
    get_files_by_username,
)
from components.chat import extract_text_from_pdf, generate_response  # Import the new chat functions

app = Flask(__name__)
CORS(app)

create_database()

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user_credentials = get_user_credentials_by_username(username)
    if user_credentials and check_password_hash(user_credentials[1], password):
        role = get_user_role(username)
        return jsonify({'message': 'Logged in', 'role': role})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    access_name = request.form['access_username']

    if file:
        filename = secure_filename(file.filename)
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file.save(os.path.join('uploads', filename))
        upload_file(filename, access_name)

        return jsonify({'message': 'File uploaded'})
    else:
        return jsonify({'message': 'Invalid file'}), 400

@app.route('/files', methods=['GET'])
def get_files():
    username = request.args.get('username')
    role = get_user_role(username)
    
    all_files = [file for file in os.listdir('uploads') if not os.path.isdir(os.path.join('uploads', file))]
    
    if role == 'admin':
        accessible_files = all_files
    else:
        accessible_files = get_files_by_username(username)
    
    filtered_files = [file for file in accessible_files if file in all_files]
    
    return jsonify({'files': filtered_files})

@app.route('/retreive/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory('uploads', filename)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    pdf_filename = data['pdf_filename']
    user_message = data['message']

    pdf_path = os.path.join('uploads', pdf_filename)
    pdf_content = extract_text_from_pdf(pdf_path)
    response = generate_response(pdf_content, user_message)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
