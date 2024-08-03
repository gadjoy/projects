import pytest
# from app import create_app, db
from flask_login import LoginManager, UserMixin
# from your_model_file import User  # Adjust the import path according to your project structure

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

# @pytest.fixture
# def client():
#     app = create_app('testing')  # Assuming you have a function to create your app with different configurations
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use in-memory SQLite database for tests
#     app.config['SECRET_KEY'] = 'your-secret-key'
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             # Setup test data
#             test_user = User(username='testuser', password='testpassword')  # Adjust according to your User model
#             db.session.add(test_user)
#             db.session.commit()
#         yield client
#         db.drop_all()

import requests

def test_login():
    # Base URL of the API
    base_url = "http://localhost:5000"

    # Attempt to login with the test user credentials
    login_url = f"{base_url}/login"
    response = requests.post(login_url, data={'username': 'admin', 'password': 'admin123'})
    assert response.status_code == 200
    assert 'Logged in' in response.text

    # Attempt to login with invalid credentials
    response = requests.post(login_url, data={'username': 'wronguser', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert 'Invalid credentials' in response.text