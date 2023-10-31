#!/usr/bin/python3
"""
Create views for Place objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def city_places(city_id):
    """Retrieves the list of all Place objects of a City and
    Creates a Place object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "user_id" not in data:
            abort(400, "Missing user_id")
        user = storage.get("User", data.get("user_id"))
        if user is None:
            abort(404)
        if "name" not in data:
            abort(400, "Missing name")
        data["city_id"] = city_id
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("places/<place_id>", methods=["GET", "DELETE", "PUT"])
def place(place_id):
    """Retrieves, Deletes and Updates a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in \
                    ["id", "user_id", "city_id", "created_at", "updated_at"]:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
