#!/usr/bin/python3
"""
Create views for Review objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route(
        "places/<place_id>/reviews",
        strict_slashed=False, methods=["GET", "POST"])
def place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    if request.method == "POST":
        data = request.get_json()
        if not data or type(data) != dict:
            abort(400, "Not a JSON")
        if "user_id" not in data:
            abort(400, "Missing user_id")
        user = storage.get("User", data["user_id"])
        if not user:
            abort(404)
        if "text" not in data:
            abort(400, "Missing text")
        review = Review(**data)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def review(review_id):
    """Retrieves, Deletes and Updates a Review object"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if not data or type(data) != dict:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in \
                    ["id", "user_id", "place_id", "created_at", "updated_at"]:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200