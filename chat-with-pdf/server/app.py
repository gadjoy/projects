from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os,sqlite3
from flask_cors import CORS
import json
from components.database import (
    create_database,
    get_user_credentials_by_username,
    get_user_role,
    upload_file as db_upload_file,
    get_files_by_username,
    set_file_access,
    get_user_ids
    # ,delete_file_table
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
def upload_file_route():
    file = request.files['file']
    access_usernames = request.form.getlist('access_usernames[]')

    if file:
        filename = secure_filename(file.filename)
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file.save(os.path.join('uploads', filename))
        access_ids = get_user_ids(access_usernames)
        db_upload_file(title=filename, access_ids=access_ids)
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
        files = get_files_by_username(username)
    cleaned_files = [file.replace('_', ' ') for file in files]
    return jsonify({'files': cleaned_files})

@app.route('/set-access', methods=['POST'])
def set_access():
    data = request.get_json()
    pdf_name = data.get('pdfName')
    access = data.get('access')

    # Validate input data
    if not pdf_name or not access:
        return jsonify({'message': 'Invalid request data.'}), 400

    if not isinstance(pdf_name, str) or not isinstance(access, str):
        return jsonify({'message': 'Invalid data types.'}), 400

    try:
        # Update access settings
        set_file_access(pdf_name, access)
        return jsonify({'message': 'Access settings updated successfully.'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        app.logger.error(f'An error occurred: {e}')
        return jsonify({'message': 'An error occurred.'}), 500

def set_file_access(pdf_name, access_id):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()

    # Check if the PDF exists
    cursor.execute("SELECT id FROM file WHERE name = ?", (pdf_name,))
    file_row = cursor.fetchone()

    if file_row:
        file_id = file_row[0]

        # Update the access_id column based on the access value
        cursor.execute("UPDATE file SET access_id = ? WHERE id = ?", (access_id, file_id))
        conn.commit()
    else:
        raise ValueError(f"PDF '{pdf_name}' not found.")

    conn.close()


if __name__ == '__main__':
    # delete_file_table()
    create_database()
    app.run(debug=True)
