#!/usr/bin/python3
"""
Create views for Review objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_view.route(
        "places/<place_id>/reviews",
        strict_slashed=False)
