from datetime import datetime

import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from database.db import users_collection

auth_bp = Blueprint("auth", __name__)

from config import ADMIN_EMAIL, ADMIN_PASSWORD


def _hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _check_password(password, password_hash):
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)


# ---------------------------
# SIGNUP
# POST /auth/signup
# ---------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = (data.get("email") or "").strip().lower()
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if email == ADMIN_EMAIL:
        return jsonify({"error": "This email is reserved for admin"}), 400
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    password = data.get("password")
    if not password or len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    role = data.get("role", "user")
    if role not in ("user", "artist"):
        return jsonify({"error": "Invalid role"}), 400

    users_collection.insert_one({
        "name": (data.get("name") or "").strip(),
        "email": email,
        "password_hash": _hash_password(password),
        "role": role,
        "phone": (data.get("phone") or "").strip(),
        "created_at": datetime.utcnow(),
    })
    return jsonify({"message": "Signup successful"}), 201


# ---------------------------
# LOGIN
# POST /auth/login
# ---------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    # Hardcoded admin: login with fixed credentials (no DB lookup)
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        user = users_collection.find_one({"email": ADMIN_EMAIL})
        if not user:
            users_collection.insert_one({
                "name": "Admin",
                "email": ADMIN_EMAIL,
                "password_hash": _hash_password(ADMIN_PASSWORD),
                "role": "admin",
                "phone": "",
                "created_at": datetime.utcnow(),
            })
        identity = {"sub": ADMIN_EMAIL, "role": "admin"}
        token = create_access_token(identity=identity)
        resp = jsonify({
            "message": "Login successful",
            "role": "admin",
            "email": ADMIN_EMAIL,
        })
        set_access_cookies(resp, token)
        return resp, 200

    user = users_collection.find_one({"email": email})
    pw_hash = user.get("password_hash") or user.get("password") if user else None
    if not user or not pw_hash or not _check_password(password, pw_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    identity = {"sub": user["email"], "role": user["role"]}
    token = create_access_token(identity=identity)
    resp = jsonify({
        "message": "Login successful",
        "role": user["role"],
        "email": user["email"],
    })
    set_access_cookies(resp, token)
    return resp, 200


# ---------------------------
# PROTECTED: get current user (optional, for dashboards)
# GET /auth/me
# ---------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    identity = get_jwt_identity()
    if isinstance(identity, dict):
        email = identity.get("sub")
        role = identity.get("role")
    else:
        email = identity
        role = None
    user = users_collection.find_one(
        {"email": email},
        {"password_hash": 0}
    )
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    return jsonify(user), 200


# ---------------------------
# LOGOUT
# POST /auth/logout
# ---------------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(resp)
    return resp, 200
