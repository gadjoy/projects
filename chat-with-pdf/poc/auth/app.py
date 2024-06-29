from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('files', lazy=True))

def create_database():
    """Create the database and tables."""
    db.create_all()
    # Create an admin user for testing
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()

    if not User.query.filter_by(username='user1').first():
        user1 = User(username='user1', password=generate_password_hash('user123'), role='user')
        db.session.add(user1)
        db.session.commit()

    if not User.query.filter_by(username='user2').first():
        user2 = User(username='user2', password=generate_password_hash('user123'), role='user')
        db.session.add(user2)
        db.session.commit()
        
    print("Database and admin user created!")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Login Failed'
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('upload.html')
    else:
        files = File.query.filter_by(user_id=current_user.id).all()
        return render_template('user_dashboard.html', files=files)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if current_user.role == 'admin':
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join('/home/vivek/projects/chat-with-pdf/poc/auth/save', filename))
        new_file = File(path=filename, user_id=None)  # Assign user later
        db.session.add(new_file)
        db.session.commit()
        return 'File uploaded'
    return 'Unauthorized'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        create_database()
    app.run(debug=True)
