from bson import ObjectId
from flask import Blueprint, jsonify, send_from_directory
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import UPLOAD_GOVT_IDS
from database.db import artists, users_collection

admin_bp = Blueprint("admin", __name__)


def _require_admin():
    identity = get_jwt_identity()
    if isinstance(identity, dict):
        role = identity.get("role")
    else:
        role = None
    if role != "admin":
        return None
    return identity


def _serialize_doc(doc, exclude=None):
    if doc is None:
        return None
    doc = dict(doc)
    doc["_id"] = str(doc["_id"])
    for key in (exclude or []):
        doc.pop(key, None)
    for k, v in list(doc.items()):
        if hasattr(v, "isoformat"):
            doc[k] = v.isoformat()
    return doc


# ---------------------------
# VIEW ALL USERS (admin only)
# GET /api/admin/users
# ---------------------------
@admin_bp.route("/admin/users", methods=["GET"])
@jwt_required()
def get_all_users():
    if _require_admin() is None:
        return jsonify({"error": "Admin access required"}), 403
    users_list = list(users_collection.find({}, {"password_hash": 0, "password": 0}))
    for u in users_list:
        u["_id"] = str(u["_id"])
        if "created_at" in u and hasattr(u["created_at"], "isoformat"):
            u["created_at"] = u["created_at"].isoformat()
    return jsonify(users_list), 200


# ---------------------------
# VIEW ALL ARTISTS (admin only)
# GET /api/admin/artists
# ---------------------------
@admin_bp.route("/admin/artists", methods=["GET"])
@jwt_required()
def get_all_artists():
    if _require_admin() is None:
        return jsonify({"error": "Admin access required"}), 403
    artists_list = list(artists.find({}))
    for a in artists_list:
        a["_id"] = str(a["_id"])
        if "created_at" in a and hasattr(a["created_at"], "isoformat"):
            a["created_at"] = a["created_at"].isoformat()
            
        # Fetch name
        if "business_name" not in a:
            u = users_collection.find_one({"email": a.get("user_id")})
            a["business_name"] = u["name"] if u else "Unknown"
            
    return jsonify(artists_list), 200


# ---------------------------
# REMOVE USER (admin only)
# DELETE /api/admin/user/<user_id>
# ---------------------------
@admin_bp.route("/admin/user/<user_id>", methods=["DELETE"])
@jwt_required()
def remove_user(user_id):
    if _require_admin() is None:
        return jsonify({"error": "Admin access required"}), 403
    from config import ADMIN_EMAIL
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.get("email") == ADMIN_EMAIL:
        return jsonify({"error": "Cannot remove admin user"}), 403
    users_collection.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "User removed"}), 200


# ---------------------------
# REMOVE ARTIST (admin only)
# DELETE /api/admin/artist/<artist_id>
# ---------------------------
@admin_bp.route("/admin/artist/<artist_id>", methods=["DELETE"])
@jwt_required()
def remove_artist(artist_id):
    if _require_admin() is None:
        return jsonify({"error": "Admin access required"}), 403
    result = artists.delete_one({"_id": ObjectId(artist_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Artist not found"}), 404
    return jsonify({"message": "Artist removed"}), 200


# ---------------------------
# VIEW PENDING ARTISTS (admin only)
# GET /api/admin/artists/pending
# ---------------------------
@admin_bp.route("/admin/artists/pending", methods=["GET"])
@jwt_required()
def get_pending_artists():
    if _require_admin() is None:
        return jsonify({"error": "Admin access required"}), 403
    pending = list(artists.find({"verification_status": "pending"}))
    for p in pending:
        p["_id"] = str(p["_id"])
        if "created_at" in p and hasattr(p["created_at"], "isoformat"):
            p["created_at"] = p["created_at"].isoformat()
        
        # Fetch name
        if "business_name" not in p:
            u = users_collection.find_one({"email": p.get("user_id")})
            p["business_name"] = u["name"] if u else "Unknown"
            
    return jsonify(pending), 200


# ---------------------------
# APPROVE ARTIST (admin only)
# PUT /api/admin/artist/approve/<artist_id>
# ---------------------------
@admin_bp.route("/admin/artist/approve/<artist_id>", methods=["PUT"])
@jwt_required()
def approve_artist(artist_id):
    if _require_admin() is None:
        return jsonify({"error": "Admin access required"}), 403
    try:
        result = artists.update_one(
            {"_id": ObjectId(artist_id)},
            {"$set": {"verification_status": "approved"}},
        )
    except Exception:
        return jsonify({"error": "Invalid artist id"}), 400
    if result.matched_count == 0:
        return jsonify({"error": "Artist not found"}), 404
    return jsonify({"message": "Artist approved"}), 200


# ---------------------------
# REJECT ARTIST (admin only)
# PUT /api/admin/artist/reject/<artist_id>
# ---------------------------
@admin_bp.route("/admin/artist/reject/<artist_id>", methods=["PUT"])
@jwt_required()
def reject_artist(artist_id):
    if _require_admin() is None:
        return jsonify({"error": "Admin access required"}), 403
    try:
        result = artists.update_one(
            {"_id": ObjectId(artist_id)},
            {"$set": {"verification_status": "rejected"}},
        )
    except Exception:
        return jsonify({"error": "Invalid artist id"}), 400
    if result.matched_count == 0:
        return jsonify({"error": "Artist not found"}), 404
    return jsonify({"message": "Artist rejected"}), 200


# ---------------------------
# GOVT ID FILE (admin only — privacy: ID visible only to admin)
# GET /api/admin/artist/<artist_id>/govt-id/<filename>
# ---------------------------
@admin_bp.route("/admin/artist/<artist_id>/govt-id/<filename>", methods=["GET"])
@jwt_required()
def get_govt_id(artist_id, filename):
    if _require_admin() is None:
        return jsonify({"error": "Admin access required"}), 403
    artist = artists.find_one({"_id": ObjectId(artist_id)})
    if not artist or artist.get("govt_id_file") != filename:
        return jsonify({"error": "Not found"}), 404
    return send_from_directory(str(UPLOAD_GOVT_IDS), filename, as_attachment=False)
