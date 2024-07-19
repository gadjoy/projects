from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os,sqlite3
from flask_cors import CORS
from components.database import (
    create_database,
    get_user_credentials_by_username,
    get_user_role,
    upload_file,
    get_files_by_username,
)

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
    if role == 'admin':
        files = os.listdir('uploads')
    else:
        files = get_files_by_username(username)
    cleaned_files = [file.replace('_', ' ') for file in files]
    return jsonify({'files': cleaned_files})

@app.route('/retreive/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory('uploads', filename)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

<<<<<<< HEAD
# @app.route('/files', methods=['GET'])
# def get_files():
#     files = os.listdir('uploads')
#     cleaned_files = [file.replace('_', ' ') for file in files]
#     return jsonify({'files': cleaned_files})

@app.route('/files', methods=['GET'])
def get_files():
    upload_folder = 'uploads'
    # Create the directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    files = os.listdir(upload_folder)
    return jsonify(files)


=======
>>>>>>> origin/vivek/freelancer/dev
if __name__ == '__main__':
    # delete_file_table()
    create_database()
    app.run(debug=True)
