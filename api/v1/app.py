#!/usr/bin/python3
"""
Starts a Flask web application
"""
import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    if os.getenv("HBNB_API_HOST"):
        host = os.getenv("HBNB_API_HOST")
    if os.getenv("HBNB_API_PORT"):
        port = os.getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
