#!/usr/bin/python3
"""
Creates views
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


objects = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    """Return json with status info"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    """Returns the number of each objects by type"""
    stats = {}
    for key, cls in objects.items():
        stats[key] = storage.count(cls)
    return jsonify(stats)
