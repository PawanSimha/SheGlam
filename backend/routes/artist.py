import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename

from config import (
    allowed_file_artist,
    GOVT_ID_OPTIONS,
    INDIAN_CITIES,
    UPLOAD_CERTIFICATES,
    UPLOAD_GOVT_IDS,
)
from database.db import artists
from database.models import artist_document

artist_bp = Blueprint("artist", __name__)


# ---------------------------
# REGISTRATION OPTIONS (for dropdowns: cities, govt ID types)
# GET /api/artist/registration-options
# ---------------------------
@artist_bp.route("/artist/registration-options", methods=["GET"])
def registration_options():
    return jsonify({
        "govt_id_options": GOVT_ID_OPTIONS,
        "cities": INDIAN_CITIES,
    }), 200


def _current_user():
    identity = get_jwt_identity()
    if isinstance(identity, dict):
        return identity.get("sub"), identity.get("role")
    return identity, None


# ---------------------------
# ARTIST REGISTRATION (artist only, JWT required)
# POST /api/artist/register
# ---------------------------
@artist_bp.route("/artist/register", methods=["POST"])
@jwt_required()
def register_artist():
    email, role = _current_user()
    if role != "artist":
        return jsonify({"error": "Only artists can register as artist"}), 403

    cert_file = request.files.get("certificate")
    govt_file = request.files.get("govt_id")
    if not cert_file or cert_file.filename == "" or not govt_file or govt_file.filename == "":
        return jsonify({"error": "Certificate and government ID files are required"}), 400
    if not allowed_file_artist(cert_file.filename) or not allowed_file_artist(govt_file.filename):
        return jsonify({"error": "Certificate and government ID must be JPG or PNG only"}), 400

    govt_id_type = (request.form.get("govt_id_type") or "").strip()
    if govt_id_type not in GOVT_ID_OPTIONS:
        return jsonify({"error": "Government ID type must be one of: " + ", ".join(GOVT_ID_OPTIONS)}), 400

    location = (request.form.get("location") or "").strip()
    if location and location not in INDIAN_CITIES:
        return jsonify({"error": "Location must be selected from the list of Indian cities"}), 400

    cert_name = secure_filename(cert_file.filename)
    govt_name = secure_filename(govt_file.filename)
    cert_path = UPLOAD_CERTIFICATES / cert_name
    govt_path = UPLOAD_GOVT_IDS / govt_name
    cert_file.save(str(cert_path))
    govt_file.save(str(govt_path))

    experience_years = request.form.get("experience_years", "0")
    try:
        experience_years = int(experience_years)
        if experience_years < 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Experience years must be a valid positive integer"}), 400

    spec = request.form.get("specialization", "")
    specialization = [s.strip() for s in spec.split(",") if s.strip()] or [spec]

    data = {
        "user_id": email,
        "experience_years": experience_years,
        "specialization": specialization,
        "location": location,
        "price_range": request.form.get("price_range", ""),
        "certificate_file": cert_name,
        "certificate_link": request.form.get("certificate_link", ""),
        "govt_id_type": govt_id_type,
        "govt_id_file": govt_name,
    }
    artists.insert_one(artist_document(data))
    return jsonify({"message": "Artist registered, pending verification"}), 201


# ---------------------------
# PUBLIC ARTIST LISTING (only approved artists, no govt ID)
# GET /api/artists
# ---------------------------
@artist_bp.route("/artists", methods=["GET"])
def list_artists():
    location = request.args.get("location", "").strip()
    min_rating = request.args.get("min_rating", type=float)
    query = {"verification_status": "approved"}
    if location:
        # Sanitize location for regex (escape special characters)
        safe_location = re.escape(location)
        query["location"] = {"$regex": safe_location, "$options": "i"}
    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}

    projection = {"govt_id_file": 0, "govt_id_type": 0}
    # Sort by rating descending (top artists first)
    artists_list = list(artists.find(query, projection).sort("rating", -1))
    
    # Helper for serialization
    from database.db import users_collection
    for a in artists_list:
        a["_id"] = str(a["_id"])
        if "created_at" in a:
             # handle datetime serialization
            if hasattr(a["created_at"], "isoformat"):
                a["created_at"] = a["created_at"].isoformat()
            else:
                 a["created_at"] = str(a["created_at"])
        
        # Fetch name if business_name not present
        if "business_name" not in a or not a["business_name"]:
            u = users_collection.find_one({"email": a.get("user_id")})
            a["name"] = u["name"] if u else "Artist"
                 
    return jsonify(artists_list), 200


# ---------------------------
# ARTIST PROFILE BY ID (public, no govt ID)
# GET /api/artist/<artist_id>
# ---------------------------
@artist_bp.route("/artist/<artist_id>", methods=["GET"])
def get_artist(artist_id):
    from bson import ObjectId
    try:
        artist = artists.find_one(
            {"_id": ObjectId(artist_id), "verification_status": "approved"},
            {"govt_id_file": 0, "govt_id_type": 0, "certificate_file": 0, "certificate_link": 0}
        )
    except Exception:
        return jsonify({"error": "Invalid artist id"}), 400
    if not artist:
        return jsonify({"error": "Artist not found"}), 404
    artist["_id"] = str(artist["_id"])
    
    # Ensure name is available
    if "business_name" not in artist:
        from database.db import users_collection
        u = users_collection.find_one({"email": artist.get("user_id")})
        artist["business_name"] = u["name"] if u else "Artist"

    if "created_at" in artist and hasattr(artist["created_at"], "isoformat"):
        artist["created_at"] = artist["created_at"].isoformat()
    return jsonify(artist), 200


# ---------------------------
# ARTIST PROFILE MANAGEMENT (own profile, JWT)
# GET /api/artist/me  — get my artist profile
# ---------------------------
@artist_bp.route("/artist/me", methods=["GET"])
@jwt_required()
def my_artist_profile():
    email, role = _current_user()
    if role != "artist":
        return jsonify({"error": "Access denied"}), 403
    artist = artists.find_one({"user_id": email})
    if not artist:
        return jsonify({"error": "Artist profile not found"}), 404
    artist["_id"] = str(artist["_id"])
    if "created_at" in artist and hasattr(artist["created_at"], "isoformat"):
        artist["created_at"] = artist["created_at"].isoformat()
    return jsonify(artist), 200
