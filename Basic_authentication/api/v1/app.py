#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from typing import Optional

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize authentication based on environment variable
auth = None
AUTH_TYPE = getenv('AUTH_TYPE')

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth  # type: ignore
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth  # type: ignore
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handle unauthorized access

    Args:
        error: Error catch

    Return:
        Info of the error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handle forbidden resource

    Args:
        error: Error catch

    Return:
        Info of the error
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> Optional[str]:
    """
    Execute before each request to validate authentication and user.

    Return:
        String or None (Nothing if the request is valid)
    """
    if auth is None:
        return

    # Exclude certain paths from requiring authentication
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    # If the path does not require authentication, allow the request
    if not auth.require_auth(request.path, excluded_paths):
        return

    # If there's no authorization header, respond with 401
    if auth.authorization_header(request) is None:
        abort(401)

    # If the user cannot be authenticated, respond with 403
    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    # Retrieve host and port with fallback defaults
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
