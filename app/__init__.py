"""EstateHub application factory."""
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFError, CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get("SECRET_KEY"), SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///realestate.db"), SQLALCHEMY_TRACK_MODIFICATIONS=False, UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER", os.path.join(app.root_path, "static", "uploads")), MAX_CONTENT_LENGTH=int(os.environ.get("MAX_UPLOAD_BYTES", 16 * 1024 * 1024)))
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY must be set in the environment before EstateHub can start.")
    db.init_app(app); login_manager.init_app(app); csrf.init_app(app); limiter.init_app(app)
    login_manager.login_view = "main.login"; login_manager.login_message = "Please log in to access this page."; login_manager.login_message_category = "info"
    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        if request.accept_mimetypes.best == "application/json" or request.is_json:
            return jsonify(success=False, message="Your form session expired. Please refresh and try again."), 400
        return error.description, 400
    @app.errorhandler(413)
    def upload_too_large(_error): return "Uploaded image is too large. The maximum size is 16 MB.", 413
    from app.currency_helper import convert_currency, format_price
    from app.image_helper import get_property_image
    from app.routes import main
    app.register_blueprint(main)
    app.jinja_env.filters["format_price"] = format_price; app.jinja_env.filters["convert_price"] = convert_currency; app.jinja_env.globals["property_image"] = get_property_image
    with app.app_context():
        db.create_all(); os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    return app
