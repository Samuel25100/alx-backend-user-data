#!/usr/bin/env python3
"""handles all routes for the Session authentication"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def post_in_session():
    """handle post request for email and password"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({ "error": "email missing" }), 400
    if not password:
        return jsonify({ "error": "password missing" }), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({ "error": "no user found for this email" }), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            session_nm = getenv('SESSION_NAME')
            out = jsonify(user.to_json())
            out.set_cookie(session_nm, session_id)
            return out
    return jsonify({ "error": "wrong password" }), 401
