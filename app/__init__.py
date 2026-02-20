"""
Real Estate Property Listings Web Application
Main Application Factory
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """
    Application Factory Pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    
    # Application Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # Change this in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///realestate.db'  # SQLite database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'main.login'  # Redirect to login page if not authenticated
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import and register blueprints (routes)
    from app.routes import main
    app.register_blueprint(main)
    
    # Register template filters for currency
    from app.currency_helper import format_price, convert_currency, get_price_display
    
    @app.template_filter('format_price')
    def format_price_filter(amount, currency='NPR'):
        return format_price(amount, currency)
    
    @app.template_filter('convert_price')
    def convert_price_filter(amount, from_curr='NPR', to_curr='USD'):
        return convert_currency(amount, from_curr, to_curr)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app
