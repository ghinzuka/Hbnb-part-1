"""
Users controller module
"""

from flask import abort, request
from src.models.user import User
from src.persistence import repo
from src.persistence.db import DBRepository

def get_users():
    """Returns all users"""
    if isinstance(repo, DBRepository):
        users = User.query.all()
    else:
        users = repo.get_all('user')
    return [user.to_dict() for user in users]

def create_user():
    """Creates a new user"""
    data = request.get_json()

    try:
        user = User.create(data)
        repo.save(user)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return user.to_dict(), 201

def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    user = repo.get('user', user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200

def update_user(user_id: str):
    """Updates a user by ID"""
    data = request.get_json()

    try:
        user = User.update(user_id, data)
        repo.update(user)
    except ValueError as e:
        abort(400, str(e))

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200

def delete_user(user_id: str):
    """Deletes a user by ID"""
    user = repo.get('user', user_id)
    if not user:
        abort(404, f"User with ID {user_id} not found")

    repo.delete(user)
    return "", 204
