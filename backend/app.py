import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, send_from_directory, render_template
from flask_jwt_extended import JWTManager

from config import (
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_SECRET_KEY,
    SECRET_KEY,
)
from database.db import ensure_upload_dirs

# Blueprints
# Blueprints
from routes.auth import auth_bp
from routes.artist import artist_bp
from routes.review import review_bp
from routes.booking import booking_bp
from routes.admin import admin_bp

# Paths: run from project root or backend/
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend"
TEMPLATES = FRONTEND / "templates"
STATIC = FRONTEND / "static"

# -------------------
# CREATE APP
# -------------------
app = Flask(
    __name__,
    template_folder=str(TEMPLATES),
    static_folder=str(STATIC),
    static_url_path="/static",
)

# -------------------
# LOGGING CONFIG
# -------------------
if not app.debug:
    # Ensure logs directory exists
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    
    file_handler = RotatingFileHandler(
        log_dir / "sheglam.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('SheGlam startup')

app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
JWTManager(app)

# -------------------
# REGISTER BLUEPRINTS
# -------------------
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(artist_bp, url_prefix="/api")
app.register_blueprint(review_bp, url_prefix="/api")
app.register_blueprint(booking_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")

# -------------------
# UPLOAD DIRS
# -------------------
ensure_upload_dirs()


# -------------------
# FRONTEND ROUTES (serve HTML pages)
# -------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register-user")
def register_user_page():
    return render_template("register_user.html")


@app.route("/register-artist")
def register_artist_page():
    return render_template("register_artist.html")


@app.route("/user-dashboard")
def user_dashboard_page():
    return render_template("user_dashboard.html")


@app.route("/artist-dashboard")
def artist_dashboard_page():
    return render_template("artist_dashboard.html")


@app.route("/artists")
def artists_page():
    return render_template("artist_list.html")


@app.route("/artist/<artist_id>")
def artist_profile_page(artist_id):
    return render_template("artist_profile.html")


@app.route("/admin-dashboard")
def admin_dashboard_page():
    return render_template("admin_dashboard.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/offers")
def offers_page():
    return render_template("offers.html")


@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(str(STATIC), "robots.txt")


@app.route("/sitemap.xml")
def sitemap_xml():
    return send_from_directory(str(STATIC), "sitemap.xml")


# -------------------
# HEALTH CHECK (API)
# -------------------
@app.route("/api/health")
def health():
    return {"status": "ok", "message": "SheGlam Backend is running"}


# -------------------
# RUN SERVER
# -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
