from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.db import bookings, artists, users_collection
from database.models import booking_document

booking_bp = Blueprint("booking", __name__)


def _current_user():
    identity = get_jwt_identity()
    if isinstance(identity, dict):
        return identity.get("sub"), identity.get("role")
    return identity, None


# ---------------------------
# CREATE BOOKING (user only)
# POST /api/booking
# ---------------------------
@booking_bp.route("/booking", methods=["POST"])
@jwt_required()
def create_booking():
    email, role = _current_user()
    if role != "user":
        return jsonify({"error": "Only users can create bookings"}), 403

    data = request.get_json()
    if not data or not data.get("artist_id"):
        return jsonify({"error": "artist_id, date, time, requirements required"}), 400

    artist_id = data["artist_id"]
    try:
        artist = artists.find_one({"_id": ObjectId(artist_id), "verification_status": "approved"})
    except Exception:
        return jsonify({"error": "Invalid artist id"}), 400
    if not artist:
        return jsonify({"error": "Artist not found or not approved"}), 404

    payload = {
        "user_id": email,
        "artist_id": artist_id,
        "date": data.get("date", ""),
        "time": data.get("time", ""),
        "requirements": data.get("requirements", ""),
    }
    doc = booking_document(payload)
    result = bookings.insert_one(doc)
    return jsonify({
        "message": "Booking requested",
        "booking_id": str(result.inserted_id),
    }), 201


# ---------------------------
# UPDATE BOOKING STATUS — accept (artist) / complete (artist)
# PUT /api/booking/<booking_id>/status
# Body: { "status": "accepted" | "completed" }
# ---------------------------
@booking_bp.route("/booking/<booking_id>/status", methods=["PUT"])
@jwt_required()
def update_booking_status(booking_id):
    email, role = _current_user()
    data = request.get_json()
    new_status = (data or {}).get("status")
    if new_status not in ("accepted", "completed", "rejected"):
        return jsonify({"error": "status must be 'accepted', 'completed' or 'rejected'"}), 400

    try:
        booking = bookings.find_one({"_id": ObjectId(booking_id)})
    except Exception:
        return jsonify({"error": "Invalid booking id"}), 400
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if role != "artist":
        return jsonify({"error": "Only artist can accept or complete"}), 403
    artist = artists.find_one({"user_id": email})
    if not artist or str(artist["_id"]) != str(booking["artist_id"]):
        return jsonify({"error": "Not your booking"}), 403

    if new_status == "accepted":
        if booking.get("status") != "requested":
            return jsonify({"error": "Booking is not in requested state"}), 400
    elif new_status == "completed":
        if booking.get("status") not in ("requested", "accepted"):
            return jsonify({"error": "Booking cannot be completed from current state"}), 400

    bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": new_status}},
    )
    return jsonify({"message": f"Booking {new_status}"}), 200


# ---------------------------
# LEGACY: complete booking (artist)
# PUT /api/booking/complete/<booking_id>
# ---------------------------
@booking_bp.route("/booking/complete/<booking_id>", methods=["PUT"])
@jwt_required()
def complete_booking(booking_id):
    email, role = _current_user()
    artist = artists.find_one({"user_id": email})
    if not artist or role != "artist":
        return jsonify({"error": "Access denied"}), 403
    try:
        booking = bookings.find_one({"_id": ObjectId(booking_id)})
    except Exception:
        return jsonify({"error": "Invalid booking id"}), 400
    if not booking or str(booking["artist_id"]) != str(artist["_id"]):
        return jsonify({"error": "Booking not found"}), 404
    bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "completed"}},
    )
    return jsonify({"message": "Booking marked as completed"}), 200


# ---------------------------
# FETCH BOOKINGS BY ROLE (user: my bookings; artist: my bookings)
# GET /api/bookings
# ---------------------------
@booking_bp.route("/bookings", methods=["GET"])
@jwt_required()
def list_bookings():
    email, role = _current_user()
    if role == "user":
        cursor = bookings.find({"user_id": email})
    elif role == "artist":
        artist = artists.find_one({"user_id": email})
        if not artist:
            return jsonify([]), 200
        cursor = bookings.find({"artist_id": str(artist["_id"])})
    else:
        return jsonify({"error": "Access denied"}), 403

    out = []
    for b in cursor:
        b["_id"] = str(b["_id"])
        # Fetch artist name for display
        if role == "user":
            artist_doc = artists.find_one({"_id": ObjectId(b["artist_id"])})
            if artist_doc:
                # Try business_name from artist doc first
                name = artist_doc.get("business_name")
                if not name:
                    # Fallback to user name
                    u = users_collection.find_one({"email": artist_doc.get("user_id")})
                    name = u["name"] if u else "Artist"
                b["artist_name"] = name
        out.append(b)
    return jsonify(out), 200
