import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Flask
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-in-prod")
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 86400))  # 24 hours
JWT_TOKEN_LOCATION = ["cookies", "headers"]
JWT_COOKIE_SECURE = False  # Set to True in production with HTTPS
JWT_COOKIE_CSRF_PROTECT = True
JWT_ACCESS_COOKIE_PATH = "/"
JWT_COOKIE_SAMESITE = "Lax"

# Admin
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@sheglam.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "sheglam_db")

# File uploads (general: png, jpg, jpeg, pdf)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
# Artist registration: certificate and government ID — jpg, png only
ALLOWED_EXTENSIONS_ARTIST = {"jpg", "png"}
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_CERTIFICATES = BASE_DIR / "frontend" / "static" / "uploads" / "certificates"
UPLOAD_GOVT_IDS = BASE_DIR / "frontend" / "static" / "uploads" / "govt_ids"

# Government ID options for artist registration
GOVT_ID_OPTIONS = ["Aadhaar", "Passport", "Voter ID", "PAN Card"]

# Indian cities for location dropdown
INDIAN_CITIES = [
    "Bangalore", "Mumbai", "Chennai", "Thiruvananthapuram", "Hyderabad", "Telangana",
    "Delhi", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur",
    "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Patna", "Vadodara",
    "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot",
    "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Allahabad",
    "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Jodhpur",
    "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubli",
    "Tiruchirappalli", "Bareilly", "Mysore", "Tiruppur", "Gurgaon", "Noida",
    "Greater Noida", "Kochi", "Other",
]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_artist(filename):
    """Certificate and government ID: jpg, png only."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS_ARTIST
