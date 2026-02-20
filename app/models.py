"""
Database Models
Defines the structure of database tables using SQLAlchemy ORM
"""

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Load user by ID for session management
    Required by Flask-Login
    """
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """
    User Model - Stores user account information
    Supports two roles: 'user' (buyers) and 'agent' (property listers)
    """
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # User Information
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    # User Role: 'user' or 'agent'
    role = db.Column(db.String(20), default='user', nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    # One-to-Many: One user can have many properties (if agent)
    properties = db.relationship('Property', backref='agent', lazy=True, cascade='all, delete-orphan')
    
    # One-to-Many: One user can make many inquiries
    inquiries = db.relationship('Inquiry', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Many-to-Many: Users can save favorite properties
    favorite_properties = db.relationship('Property', secondary='favorites', backref='favorited_by', lazy='dynamic')
    
    def set_password(self, password):
        """
        Hash and store password securely
        Never store plain text passwords!
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify password against stored hash
        Returns True if password matches
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


# Association table for Many-to-Many relationship between Users and Properties (Favorites)
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'), primary_key=True),
    db.Column('added_at', db.DateTime, default=datetime.utcnow)
)


class Property(db.Model):
    """
    Property Model - Stores real estate property listings
    Each property is posted by an agent (user with role='agent')
    """
    __tablename__ = 'properties'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key - Links to User (agent)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Property Details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)  # House, Apartment, Villa, etc.
    
    # Location
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(20))
    
    # Property Specifications
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='NPR', nullable=False)  # NPR, USD, EUR, etc.
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    area = db.Column(db.Float)  # Square feet
    
    # Listing Status
    status = db.Column(db.String(20), default='available')  # available, sold, rented
    
    # Image
    image_filename = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # One-to-Many: One property can have many inquiries
    inquiries = db.relationship('Inquiry', backref='property', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Property {self.title}>'


class Inquiry(db.Model):
    """
    Inquiry Model - Stores inquiries/messages from users about properties
    Links users to properties they're interested in
    """
    __tablename__ = 'inquiries'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    
    # Inquiry Details
    message = db.Column(db.Text, nullable=False)
    contact_phone = db.Column(db.String(20))
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, replied, closed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Inquiry {self.id} for Property {self.property_id}>'
