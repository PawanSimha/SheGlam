import os
from pathlib import Path

from pymongo import MongoClient

from config import MONGODB_URI, MONGODB_DB_NAME, UPLOAD_CERTIFICATES, UPLOAD_GOVT_IDS

# MongoDB connection
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

# Collections
users_collection = db["users"]
artists = db["artists"]
bookings = db["bookings"]
reviews = db["reviews"]


def ensure_upload_dirs():
    """Create upload directories if they don't exist (files hidden from public via .gitignore)."""
    for d in (UPLOAD_CERTIFICATES, UPLOAD_GOVT_IDS):
        d.mkdir(parents=True, exist_ok=True)


def test_db_connection():
    users_collection.insert_one({"status": "db connected"})
    return list(users_collection.find())
