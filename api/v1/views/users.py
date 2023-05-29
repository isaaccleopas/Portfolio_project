#!/usr/bin/python3
"""
This module handles all default RestFul API actions for Users.
"""
from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    Creates a new User object.
    """
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    name = req_data.get('name')
    email = req_data.get('email')
    password = req_data.get('password')
    if not name or not email or not password:
        abort(400, "Missing required fields")
    user = User(name=name, email=email, password=password)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    for k, v in req_data.items():
        setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
