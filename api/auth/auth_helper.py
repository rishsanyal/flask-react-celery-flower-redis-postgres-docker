from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app import sql_db, create_app

from auth.auth_models import User, UserProfile
from auth.auth_mock_generator import generate_users

app = create_app()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@postgresql/mydb'
# sql_db = SQLAlchemy(app)


def get_user_by_username(username: str):
    """Get user by username."""
    with app.app_context():
        return User.query.filter_by(username=username).first()

def get_user_by_id(user_id: int):
    """Get user by user id.

    Args:
        user_id (int): Get user by id from database

    Returns:
        User: User object
    """
    with app.app_context():
        return User.query.filter_by(id=user_id).first()

def get_user_profile_by_id(user_id):
    """Get user profile by user id."""
    with app.app_context():
        return UserProfile.query.filter_by(user_id=user_id).first()

def create_mock_users():
    """ Create user profile and user in database """

    user_info = generate_users()

    with app.app_context():
        for user in user_info:
            user_info = {
                "username": user['username'],
                "password": user['password']
            }
            # Create user
            user_entry = User(**user_info)
            sql_db.session.add(user_entry)
            sql_db.session.commit()

            user_profile_info= {
                "full_name": user['profile']['full_name'],
                "email": user['profile']['email'],
                "phone": user['profile']['phone'],
            }
            # Create user profile
            user_profile = UserProfile(**user_profile_info)

            # Add user to database
            sql_db.session.add(user_profile)
            sql_db.session.commit()

def get_all_users():
    """Get all users."""
    with app.app_context():
        return User.query.all()