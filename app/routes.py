"""Application routes."""
import os
import uuid
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image, UnidentifiedImageError
from sqlalchemy import case, func
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from app import db, limiter
from app.currency_helper import EXCHANGE_RATES, KATHMANDU_VALLEY_AREAS, NEPAL_CITIES, NEPAL_PROPERTY_TYPES
from app.models import Inquiry, Property, User, favorites

main = Blueprint("main", __name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_CURRENCIES = tuple(EXCHANGE_RATES)
def allowed_file(file_storage):
    filename = file_storage.filename or ""
    if "." not in filename or filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS: return False
    try:
        image = Image.open(file_storage.stream); image.verify(); file_storage.stream.seek(0); return True
    except (UnidentifiedImageError, OSError): file_storage.stream.seek(0); return False
def save_image(file_storage):
    if not allowed_file(file_storage): raise ValueError("Please upload a valid PNG, JPG, GIF, or WebP image.")
    extension = secure_filename(file_storage.filename).rsplit(".", 1)[1].lower(); filename = f"{uuid.uuid4().hex}.{extension}"
    file_storage.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename)); return filename
def remove_image(filename):
    if filename:
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], os.path.basename(filename))
        if os.path.isfile(path): os.remove(path)
def price_in_npr(): return Property.price / case(*[(Property.currency == code, rate) for code, rate in EXCHANGE_RATES.items()], else_=1.0)
def property_form_context(**kwargs): return {"cities": NEPAL_CITIES, "property_types": NEPAL_PROPERTY_TYPES, "currencies": ALLOWED_CURRENCIES, "neighborhoods": KATHMANDU_VALLEY_AREAS, **kwargs}

def dashboard_redirect():
    """Return the correct dashboard for the authenticated user's server-side role."""
    if current_user.role == "agent": return redirect(url_for("main.agent_dashboard"))
    if current_user.role == "admin": return redirect(url_for("main.admin_dashboard"))
    return redirect(url_for("main.user_dashboard"))

@main.route("/")
def home():
    available = Property.query.filter_by(status="available")
    featured_properties = available.order_by(Property.is_featured.desc(), Property.created_at.desc()).limit(6).all()
    return render_template("home.html", featured_properties=featured_properties, total_properties=available.count(), total_rentals=available.filter_by(listing_type="rent").count(), total_sales=available.filter_by(listing_type="sale").count(), total_agents=User.query.filter_by(role="agent").count())
@main.route("/properties")
def properties():
    user_currency = session.get("currency", "NPR"); search_query = request.args.get("search", "").strip(); property_type = request.args.get("type", ""); listing_type = request.args.get("listing_type", ""); city = request.args.get("city", ""); neighborhood = request.args.get("neighborhood", "").strip(); sort = request.args.get("sort", "newest"); min_price = request.args.get("min_price", type=float); max_price = request.args.get("max_price", type=float); bedrooms = request.args.get("bedrooms", type=int)
    query = Property.query.filter_by(status="available")
    if search_query: query = query.filter(Property.title.contains(search_query) | Property.description.contains(search_query))
    if property_type: query = query.filter_by(property_type=property_type)
    if listing_type in {"sale", "rent"}: query = query.filter_by(listing_type=listing_type)
    if city: query = query.filter_by(city=city)
    if neighborhood: query = query.filter(Property.neighborhood.ilike(f"%{neighborhood}%"))
    if min_price is not None: query = query.filter(price_in_npr() >= min_price / EXCHANGE_RATES[user_currency])
    if max_price is not None: query = query.filter(price_in_npr() <= max_price / EXCHANGE_RATES[user_currency])
    if bedrooms is not None: query = query.filter(Property.bedrooms >= bedrooms)
    sort_orders = {"price_asc": price_in_npr().asc(), "price_desc": price_in_npr().desc(), "oldest": Property.created_at.asc(), "newest": Property.created_at.desc()}
    pagination = query.order_by(sort_orders.get(sort, sort_orders["newest"])).paginate(page=request.args.get("page", 1, type=int), per_page=12, error_out=False)
    areas_query = db.session.query(Property.neighborhood).filter(Property.neighborhood.isnot(None), Property.neighborhood != "")
    if city: areas_query = areas_query.filter(Property.city == city)
    available_areas = [area for (area,) in areas_query.distinct().order_by(Property.neighborhood).all()]
    return render_template("properties.html", properties=pagination.items, pagination=pagination, total_results=pagination.total, cities=NEPAL_CITIES, property_types=NEPAL_PROPERTY_TYPES, available_areas=available_areas, user_currency=user_currency)
@main.route("/property/<int:property_id>")
def property_detail(property_id):
    property_item = Property.query.get_or_404(property_id)
    similar_properties = Property.query.filter(Property.id != property_id, Property.property_type == property_item.property_type, Property.city == property_item.city, Property.status == "available").limit(3).all()
    return render_template("property_detail.html", property=property_item, similar_properties=similar_properties)
@main.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per hour")
def register():
    if current_user.is_authenticated: return redirect(url_for("main.home"))
    if request.method == "POST":
        username = (request.form.get("username") or "").strip(); email = (request.form.get("email") or "").strip().lower(); password = request.form.get("password") or ""; errors = []
        if len(username) < 3: errors.append("Username must be at least 3 characters long.")
        if "@" not in email: errors.append("Please enter a valid email address.")
        if len(password) < 8: errors.append("Password must be at least 8 characters long.")
        if password != request.form.get("confirm_password"): errors.append("Passwords do not match.")
        if username and User.query.filter_by(username=username).first(): errors.append("Username already exists.")
        if email and User.query.filter_by(email=email).first(): errors.append("Email already registered.")
        if errors:
            for error in errors: flash(error, "danger")
            return render_template("register.html")
        role = request.form.get("role", "user")
        if role not in {"user", "agent"}: role = "user"
        user = User(username=username, email=email, full_name=request.form.get("full_name"), phone=request.form.get("phone"), role=role); user.set_password(password); db.session.add(user); db.session.commit(); flash("Registration successful! Please log in.", "success"); return redirect(url_for("main.login"))
    return render_template("register.html")
@main.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def login():
    if current_user.is_authenticated: return dashboard_redirect()
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user and user.check_password(request.form.get("password") or ""):
            login_user(user, remember=bool(request.form.get("remember"))); flash(f"Welcome back, {user.full_name or user.username}!", "success"); return dashboard_redirect()
        flash("Invalid username or password.", "danger")
    return render_template("login.html")
@main.route("/logout")
@login_required
def logout(): logout_user(); flash("You have been logged out successfully.", "info"); return redirect(url_for("main.home"))
@main.route("/user/dashboard")
@login_required
def user_dashboard():
    if current_user.role != "user": return dashboard_redirect()
    return render_template("user_dashboard.html", favorites=current_user.favorite_properties.all(), inquiries=Inquiry.query.filter_by(user_id=current_user.id).order_by(Inquiry.created_at.desc()).all())
@main.route("/user/profile", methods=["GET", "POST"])
@login_required
def user_profile():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower(); existing = User.query.filter(User.email == email, User.id != current_user.id).first()
        if not email or "@" not in email: flash("Please enter a valid email address.", "danger")
        elif existing: flash("That email address is already registered.", "danger")
        else:
            current_user.full_name = request.form.get("full_name"); current_user.phone = request.form.get("phone"); current_user.whatsapp_number = request.form.get("whatsapp_number"); current_user.email = email
            if request.form.get("new_password"): current_user.set_password(request.form["new_password"])
            db.session.commit(); flash("Profile updated successfully!", "success"); return redirect(url_for("main.user_profile"))
    return render_template("profile.html")
@main.route("/user/favorite/<int:property_id>", methods=["POST"])
@login_required
def toggle_favorite(property_id):
    if current_user.role != "user": return jsonify(success=False, message="Only users can save favorites"), 403
    property_item = Property.query.get_or_404(property_id)
    if property_item in current_user.favorite_properties: current_user.favorite_properties.remove(property_item); action = "removed"
    else: current_user.favorite_properties.append(property_item); action = "added"
    db.session.commit(); return jsonify(success=True, action=action, message=f"{action.title()} {'from' if action == 'removed' else 'to'} favorites")
@main.route("/user/inquiry/<int:property_id>", methods=["POST"])
@login_required
def submit_inquiry(property_id):
    if current_user.role != "user": flash("Only users can submit inquiries.", "warning"); return redirect(url_for("main.property_detail", property_id=property_id))
    message = (request.form.get("message") or "").strip()
    if not message: flash("Please enter a message.", "danger"); return redirect(url_for("main.property_detail", property_id=property_id))
    Property.query.get_or_404(property_id); db.session.add(Inquiry(user_id=current_user.id, property_id=property_id, message=message, contact_phone=request.form.get("contact_phone"))); db.session.commit(); flash("Your inquiry has been submitted successfully!", "success"); return redirect(url_for("main.property_detail", property_id=property_id))
@main.route("/agent/dashboard")
@login_required
def agent_dashboard():
    if current_user.role != "agent": return dashboard_redirect()
    base_properties = Property.query.filter_by(agent_id=current_user.id); inquiries_query = Inquiry.query.join(Property).filter(Property.agent_id == current_user.id)
    properties_pagination = base_properties.options(joinedload(Property.favorited_by)).order_by(Property.created_at.desc()).paginate(page=request.args.get("page", 1, type=int), per_page=10, error_out=False); inquiries_pagination = inquiries_query.order_by(Inquiry.created_at.desc()).paginate(page=request.args.get("inquiry_page", 1, type=int), per_page=10, error_out=False)
    property_likes = {property_item.id: property_item.favorited_by for property_item in properties_pagination.items}
    return render_template("agent_dashboard.html", properties=properties_pagination.items, property_likes=property_likes, inquiries=inquiries_pagination.items, properties_pagination=properties_pagination, inquiries_pagination=inquiries_pagination, stats={"total": base_properties.count(), "available": base_properties.filter_by(status="available").count(), "inquiries": inquiries_query.count(), "pending": inquiries_query.filter_by(status="pending").count()})

@main.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin": return dashboard_redirect()
    status_counts = dict(db.session.query(Property.status, func.count(Property.id)).group_by(Property.status).all())
    like_counts = db.session.query(favorites.c.property_id.label("property_id"), func.count(favorites.c.user_id).label("like_count")).group_by(favorites.c.property_id).subquery()
    top_liked_properties = db.session.query(Property, func.coalesce(like_counts.c.like_count, 0).label("like_count")).outerjoin(like_counts, Property.id == like_counts.c.property_id).order_by(func.coalesce(like_counts.c.like_count, 0).desc(), Property.created_at.desc()).limit(10).all()
    return render_template("admin_dashboard.html", stats={"users": User.query.filter_by(role="user").count(), "agents": User.query.filter_by(role="agent").count(), "properties": Property.query.count(), "inquiries": Inquiry.query.count()}, status_counts=status_counts, top_liked_properties=top_liked_properties, recent_properties=Property.query.order_by(Property.created_at.desc()).limit(20).all())

@main.route("/admin/property/<int:property_id>/featured", methods=["POST"])
@login_required
def toggle_featured(property_id):
    if current_user.role != "admin": return dashboard_redirect()
    property_item = Property.query.get_or_404(property_id)
    property_item.is_featured = not property_item.is_featured
    db.session.commit()
    flash(f"'{property_item.title}' is {'now' if property_item.is_featured else 'no longer'} featured.", "success")
    return redirect(url_for("main.admin_dashboard"))
def populate_property(property_item):
    for field in ("title", "description", "property_type", "address", "city", "neighborhood", "state", "zipcode", "status"):
        if field in request.form: setattr(property_item, field, request.form.get(field))
    property_item.listing_type = request.form.get("listing_type", ""); property_item.price = request.form.get("price", type=float); property_item.currency = request.form.get("currency", "NPR"); property_item.bedrooms = request.form.get("bedrooms", type=int); property_item.bathrooms = request.form.get("bathrooms", type=int); property_item.area = request.form.get("area", type=float)
    if property_item.listing_type not in {"sale", "rent"}: raise ValueError("Choose whether this listing is for sale or rent.")
    if property_item.currency not in ALLOWED_CURRENCIES or property_item.price is None or property_item.price < 0: raise ValueError("Enter a non-negative price and a supported currency.")
@main.route("/agent/property/add", methods=["GET", "POST"])
@login_required
def add_property():
    if current_user.role != "agent": return redirect(url_for("main.home"))
    if request.method == "POST":
        property_item = Property(agent_id=current_user.id)
        try:
            populate_property(property_item); file = request.files.get("image")
            if file and file.filename: property_item.image_filename = save_image(file)
        except ValueError as error: flash(str(error), "danger"); return render_template("add_property.html", **property_form_context())
        db.session.add(property_item); db.session.commit(); flash("Property listed successfully!", "success"); return redirect(url_for("main.agent_dashboard"))
    return render_template("add_property.html", **property_form_context())
@main.route("/agent/property/edit/<int:property_id>", methods=["GET", "POST"])
@login_required
def edit_property(property_id):
    property_item = Property.query.get_or_404(property_id)
    if current_user.role != "agent" or property_item.agent_id != current_user.id: flash("You can only edit your own properties.", "danger"); return redirect(url_for("main.agent_dashboard"))
    if request.method == "POST":
        old_filename = property_item.image_filename
        try:
            populate_property(property_item); file = request.files.get("image")
            if file and file.filename: property_item.image_filename = save_image(file)
        except ValueError as error: flash(str(error), "danger"); return render_template("edit_property.html", **property_form_context(property=property_item))
        db.session.commit()
        if property_item.image_filename != old_filename: remove_image(old_filename)
        flash("Property updated successfully!", "success"); return redirect(url_for("main.agent_dashboard"))
    return render_template("edit_property.html", **property_form_context(property=property_item))
@main.route("/agent/property/delete/<int:property_id>", methods=["POST"])
@login_required
def delete_property(property_id):
    property_item = Property.query.get_or_404(property_id)
    if current_user.role != "agent" or property_item.agent_id != current_user.id: return jsonify(success=False, message="You can only delete your own properties."), 403
    filename = property_item.image_filename; db.session.delete(property_item); db.session.commit(); remove_image(filename); return jsonify(success=True, message="Property deleted successfully.")
@main.route("/agent/inquiry/<int:inquiry_id>/status", methods=["POST"])
@login_required
def update_inquiry_status(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    if current_user.role != "agent" or inquiry.property.agent_id != current_user.id: return jsonify(success=False, message="Unauthorized"), 403
    status = request.form.get("status")
    if status not in {"pending", "replied", "closed"}: return jsonify(success=False, message="Invalid status"), 400
    inquiry.status = status; db.session.commit(); return jsonify(success=True, message="Status updated")
@main.route("/set-currency/<currency_code>")
def set_currency(currency_code):
    if currency_code in ALLOWED_CURRENCIES: session["currency"] = currency_code; flash(f"Currency changed to {currency_code}", "success")
    return redirect(request.referrer or url_for("main.home"))
