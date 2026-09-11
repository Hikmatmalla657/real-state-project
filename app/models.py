"""Database models."""
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager
def utc_now(): return datetime.now(timezone.utc)
@login_manager.user_loader
def load_user(user_id): return db.session.get(User, int(user_id))
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True); username = db.Column(db.String(80), unique=True, nullable=False); email = db.Column(db.String(120), unique=True, nullable=False); password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100)); phone = db.Column(db.String(20)); whatsapp_number = db.Column(db.String(20)); role = db.Column(db.String(20), default="user", nullable=False); created_at = db.Column(db.DateTime(timezone=True), default=utc_now)
    properties = db.relationship("Property", backref="agent", lazy=True, cascade="all, delete-orphan"); inquiries = db.relationship("Inquiry", backref="user", lazy=True, cascade="all, delete-orphan"); favorite_properties = db.relationship("Property", secondary="favorites", backref="favorited_by", lazy="dynamic")
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
favorites = db.Table("favorites", db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True), db.Column("property_id", db.Integer, db.ForeignKey("properties.id"), primary_key=True), db.Column("added_at", db.DateTime(timezone=True), default=utc_now))
class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True); agent_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False); title = db.Column(db.String(200), nullable=False); description = db.Column(db.Text, nullable=False); property_type = db.Column(db.String(50), nullable=False); listing_type = db.Column(db.String(10), default="sale", nullable=False); address = db.Column(db.String(200), nullable=False); city = db.Column(db.String(100), nullable=False); neighborhood = db.Column(db.String(100)); state = db.Column(db.String(100)); zipcode = db.Column(db.String(20)); price = db.Column(db.Float, nullable=False); currency = db.Column(db.String(10), default="NPR", nullable=False); bedrooms = db.Column(db.Integer); bathrooms = db.Column(db.Integer); area = db.Column(db.Float); status = db.Column(db.String(20), default="available"); is_featured = db.Column(db.Boolean, default=False, nullable=False); image_filename = db.Column(db.String(200)); created_at = db.Column(db.DateTime(timezone=True), default=utc_now); updated_at = db.Column(db.DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    inquiries = db.relationship("Inquiry", backref="property", lazy=True, cascade="all, delete-orphan")
class Inquiry(db.Model):
    __tablename__ = "inquiries"
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False); property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False); message = db.Column(db.Text, nullable=False); contact_phone = db.Column(db.String(20)); status = db.Column(db.String(20), default="pending"); created_at = db.Column(db.DateTime(timezone=True), default=utc_now)
