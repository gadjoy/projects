from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from components.database import create_database, get_user_credentials_by_username, get_user_role

app = Flask(__name__)
CORS(app)

create_database()

pdfs = []

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
def upload_file():
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        pdf = {"name": filename, "url": f"/uploads/{filename}", "access": []}  # <--- Added access field to PDF metadata
        pdfs.append(pdf)  # <--- Store PDF metadata
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
    username = request.args.get('username')
    role = get_user_role(username)
    if role == 'admin':
        files = os.listdir('uploads')
    else:
        files = [pdf['name'] for pdf in pdfs if username in pdf['access']]
    cleaned_files = [file.replace('_', ' ') for file in files]
    return jsonify({'files': cleaned_files})


@app.route('/set-access', methods=['POST'])  # <--- Added new route for setting access control
def set_access():
    data = request.get_json()
    pdf_name = data['pdfName']
    access = data['access']
    
    for pdf in pdfs:
        if pdf['name'] == pdf_name:
            pdf['access'] = access
            break
    return jsonify({'message': 'Access settings updated successfully.'}), 200

if __name__ == '__main__':
    create_database()
    app.run(debug=True)