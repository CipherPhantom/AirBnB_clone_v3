#!/usr/bin/python3
"""
Create views for User objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def users():
    """Retrieves the list of all User objects"""
    if request.method == "GET":
        users = [user.to_dict() for user in storage.all("User").values()]
        return jsonify(users)
    if request.method == "POST":
        data = request.get_json()
        if not data or type(data) != dict:
            abort(400, "Not a JSON")
        if "email" not in data:
            abort(400, "Missing email")
        if "password" not in data:
            abort(400, "Missing password")
        user = User(**data)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route(
        "/users/<user_id>",
        strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def user(user_id):
    """Retrieves, Deletes and Updates a User object"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if not data or type(data) != dict:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict())
