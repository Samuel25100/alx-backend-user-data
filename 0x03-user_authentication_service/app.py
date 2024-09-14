#!/usr/bin/env python3
"""Simple flask app"""
from flask import Flask, jsonify, request, abort, make_response
from flask import redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route("/")
def home():
    """return a string"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def regs_user():
    """register users for POST request"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        user = AUTH.register_user(email, pwd)
        if user:
            return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """handle login confirmation"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if AUTH.valid_login(email=email, password=pwd):
        se_id = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email, "message": "logged in"}))
        resp.set_cookie('session_id', se_id)
        return resp
    return abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """handle logout based on session_id"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or not session_id:
        return abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile")
def profile():
    """handle route for profile of user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or not session_id:
        return abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=['POST'])
def reset_password():
    """handle the reset password token"""
    email = request.cookies.get('email')
    if not email:
        return abort(403)
    try:
        usr_tk = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": usr_tk}), 200
    except Exception:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
