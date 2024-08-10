# app.py - Updated Flask application with file access logic for users

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Mock database (replace with actual database integration)
users = [
    {'username': 'admin', 'password': generate_password_hash('admin_password')},
    {'username': 'user', 'password': generate_password_hash('user_password')}
]

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = next((u for u in users if u['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['username'] = username
            if username == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('logged_in') and session.get('username') == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))

# User dashboard route
@app.route('/user/dashboard')
def user_dashboard():
    if session.get('logged_in') and session.get('username') == 'user':
        # Get list of files in the uploads directory
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('user_dashboard.html', files=files)
    else:
        return redirect(url_for('login'))

# Route to handle file upload (admin only)
@app.route('/upload', methods=['POST'])
def upload_file():
    if session.get('logged_in') and session.get('username') == 'admin':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid file type', 'error')
            return redirect(request.url)
    else:
        return redirect(url_for('login'))

# Route to view uploaded files (for user)
@app.route('/view_file/<filename>')
def view_file(filename):
    if session.get('logged_in') and session.get('username') == 'user':
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
