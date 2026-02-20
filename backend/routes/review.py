from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.db import reviews, bookings, artists
from database.models import review_document

review_bp = Blueprint("review", __name__)


def _current_user():
    identity = get_jwt_identity()
    if isinstance(identity, dict):
        return identity.get("sub"), identity.get("role")
    return identity, None


# ---------------------------
# ADD REVIEW (user only, after booking completed; one review per booking)
# POST /api/review
# ---------------------------
@review_bp.route("/review", methods=["POST"])
@jwt_required()
def add_review():
    email, role = _current_user()
    if role != "user":
        return jsonify({"error": "Only users can add reviews"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    booking_id = data.get("booking_id")
    rating = data.get("rating")
    if not booking_id or rating is None:
        return jsonify({"error": "booking_id and rating required"}), 400
    try:
        r = int(rating)
        if r < 1 or r > 5:
            raise ValueError("1-5")
    except (TypeError, ValueError):
        return jsonify({"error": "rating must be 1 to 5"}), 400

    booking = bookings.find_one({
        "_id": ObjectId(booking_id),
        "status": "completed",
        "user_id": email,
    })
    if not booking:
        return jsonify({"error": "Invalid or incomplete booking, or not your booking"}), 400

    if reviews.find_one({"booking_id": booking_id}):
        return jsonify({"error": "You have already reviewed this booking"}), 400

    doc = review_document({
        "user_id": email,
        "artist_id": str(booking["artist_id"]),
        "booking_id": booking_id,
        "rating": r,
        "comment": (data.get("comment") or "").strip(),
    })
    reviews.insert_one(doc)

    artist_reviews = list(reviews.find({"artist_id": str(booking["artist_id"])}))
    avg_rating = sum(x["rating"] for x in artist_reviews) / len(artist_reviews)
    artists.update_one(
        {"_id": ObjectId(booking["artist_id"])},
        {"$set": {"rating": round(avg_rating, 1), "total_services": len(artist_reviews)}},
    )
    return jsonify({"message": "Review added"}), 201
