#!/usr/bin/env python3
"""Simple flask app"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)


@app.route("/")
def home():
    """return a string"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'])
def regs_user():
    """register users for POST request"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    auth = Auth()
    try:
        user = auth.register_user(email, pwd)
        if user:
            return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
