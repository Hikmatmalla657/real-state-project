"""
Application Routes (URL Handlers)
Defines all the pages and their functionality
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Property, Inquiry
from app.currency_helper import format_price, convert_currency, get_price_display, NEPAL_CITIES, NEPAL_PROPERTY_TYPES
from werkzeug.utils import secure_filename
import os

# Create Blueprint
main = Blueprint('main', __name__)

# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============= PUBLIC ROUTES (No login required) =============

@main.route('/')
def home():
    """
    Home Page - Shows featured properties
    """
    # Get latest 6 properties for featured section
    featured_properties = Property.query.filter_by(status='available').order_by(Property.created_at.desc()).limit(6).all()
    
    # Get property statistics
    total_properties = Property.query.filter_by(status='available').count()
    total_agents = User.query.filter_by(role='agent').count()
    
    return render_template('home.html', 
                         featured_properties=featured_properties,
                         total_properties=total_properties,
                         total_agents=total_agents)


@main.route('/properties')
def properties():
    """
    Properties Listing Page - Shows all available properties with search/filter
    """
    # Get user's preferred currency from session (default: NPR)
    user_currency = session.get('currency', 'NPR')
    
    # Get filter parameters from URL
    search_query = request.args.get('search', '')
    property_type = request.args.get('type', '')
    city = request.args.get('city', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    bedrooms = request.args.get('bedrooms', type=int)
    
    # Start with base query
    query = Property.query.filter_by(status='available')
    
    # Apply filters
    if search_query:
        query = query.filter(Property.title.contains(search_query) | Property.description.contains(search_query))
    
    if property_type:
        query = query.filter_by(property_type=property_type)
    
    if city:
        query = query.filter_by(city=city)
    
    if min_price:
        query = query.filter(Property.price >= min_price)
    
    if max_price:
        query = query.filter(Property.price <= max_price)
    
    if bedrooms:
        query = query.filter(Property.bedrooms >= bedrooms)
    
    # Execute query and get results
    all_properties = query.order_by(Property.created_at.desc()).all()
    
    # Get unique cities (prioritize Nepal cities)
    cities = NEPAL_CITIES
    
    # Get property types
    property_types = NEPAL_PROPERTY_TYPES
    
    return render_template('properties.html', 
                         properties=all_properties,
                         cities=cities,
                         property_types=property_types,
                         user_currency=user_currency)


@main.route('/property/<int:property_id>')
def property_detail(property_id):
    """
    Property Detail Page - Shows detailed information about a specific property
    """
    property_item = Property.query.get_or_404(property_id)
    
    # Get similar properties (same type and city)
    similar_properties = Property.query.filter(
        Property.id != property_id,
        Property.property_type == property_item.property_type,
        Property.city == property_item.city,
        Property.status == 'available'
    ).limit(3).all()
    
    return render_template('property_detail.html', 
                         property=property_item,
                         similar_properties=similar_properties)


# ============= AUTHENTICATION ROUTES =============

@main.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration Page
    Handles both displaying the form (GET) and processing registration (POST)
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        role = request.form.get('role', 'user')  # Default to 'user'
        
        # Server-side validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists.')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            role=role
        )
        new_user.set_password(password)  # Hash the password
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login Page
    Handles authentication and session creation
    """
    if current_user.is_authenticated:
        # Redirect to appropriate dashboard based on role
        if current_user.role == 'agent':
            return redirect(url_for('main.agent_dashboard'))
        else:
            return redirect(url_for('main.user_dashboard'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Log in the user (creates session)
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.full_name or user.username}!', 'success')
            
            # Redirect to appropriate dashboard
            if user.role == 'agent':
                return redirect(url_for('main.agent_dashboard'))
            else:
                return redirect(url_for('main.user_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    """
    Logout - Destroys user session
    """
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.home'))


# ============= USER DASHBOARD ROUTES =============

@main.route('/user/dashboard')
@login_required
def user_dashboard():
    """
    User Dashboard - For property buyers/renters
    Shows saved favorites and inquiries
    """
    if current_user.role != 'user':
        flash('Access denied. Agents should use the agent dashboard.', 'warning')
        return redirect(url_for('main.agent_dashboard'))
    
    # Get user's favorite properties
    favorites = current_user.favorite_properties.all()
    
    # Get user's inquiries
    inquiries = Inquiry.query.filter_by(user_id=current_user.id).order_by(Inquiry.created_at.desc()).all()
    
    return render_template('user_dashboard.html', 
                         favorites=favorites,
                         inquiries=inquiries)


@main.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """
    User Profile Page - Edit user information
    """
    if request.method == 'POST':
        # Update user information
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        current_user.email = request.form.get('email')
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.user_profile'))
    
    return render_template('profile.html')


@main.route('/user/favorite/<int:property_id>', methods=['POST'])
@login_required
def toggle_favorite(property_id):
    """
    Add or remove property from favorites
    AJAX endpoint
    """
    if current_user.role != 'user':
        return jsonify({'success': False, 'message': 'Only users can save favorites'}), 403
    
    property_item = Property.query.get_or_404(property_id)
    
    # Check if already in favorites
    if property_item in current_user.favorite_properties:
        # Remove from favorites
        current_user.favorite_properties.remove(property_item)
        db.session.commit()
        return jsonify({'success': True, 'action': 'removed', 'message': 'Removed from favorites'})
    else:
        # Add to favorites
        current_user.favorite_properties.append(property_item)
        db.session.commit()
        return jsonify({'success': True, 'action': 'added', 'message': 'Added to favorites'})


@main.route('/user/inquiry/<int:property_id>', methods=['POST'])
@login_required
def submit_inquiry(property_id):
    """
    Submit inquiry about a property
    """
    if current_user.role != 'user':
        flash('Only users can submit inquiries.', 'warning')
        return redirect(url_for('main.property_detail', property_id=property_id))
    
    property_item = Property.query.get_or_404(property_id)
    
    # Get form data
    message = request.form.get('message')
    contact_phone = request.form.get('contact_phone')
    
    # Validate
    if not message:
        flash('Please enter a message.', 'danger')
        return redirect(url_for('main.property_detail', property_id=property_id))
    
    # Create inquiry
    inquiry = Inquiry(
        user_id=current_user.id,
        property_id=property_id,
        message=message,
        contact_phone=contact_phone
    )
    
    db.session.add(inquiry)
    db.session.commit()
    
    flash('Your inquiry has been submitted successfully!', 'success')
    return redirect(url_for('main.property_detail', property_id=property_id))


# ============= AGENT DASHBOARD ROUTES =============

@main.route('/agent/dashboard')
@login_required
def agent_dashboard():
    """
    Agent Dashboard - For property agents/listers
    Shows their properties and inquiries
    """
    if current_user.role != 'agent':
        flash('Access denied. Only agents can access this page.', 'warning')
        return redirect(url_for('main.user_dashboard'))
    
    # Get agent's properties
    agent_properties = Property.query.filter_by(agent_id=current_user.id).order_by(Property.created_at.desc()).all()
    
    # Get inquiries for agent's properties
    property_ids = [p.id for p in agent_properties]
    inquiries = Inquiry.query.filter(Inquiry.property_id.in_(property_ids)).order_by(Inquiry.created_at.desc()).all()
    
    # Statistics
    total_properties = len(agent_properties)
    available_properties = len([p for p in agent_properties if p.status == 'available'])
    total_inquiries = len(inquiries)
    pending_inquiries = len([i for i in inquiries if i.status == 'pending'])
    
    return render_template('agent_dashboard.html',
                         properties=agent_properties,
                         inquiries=inquiries,
                         stats={
                             'total': total_properties,
                             'available': available_properties,
                             'inquiries': total_inquiries,
                             'pending': pending_inquiries
                         })


@main.route('/agent/property/add', methods=['GET', 'POST'])
@login_required
def add_property():
    """
    Add New Property Listing
    """
    if current_user.role != 'agent':
        flash('Only agents can add properties.', 'warning')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        property_type = request.form.get('property_type')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        price = request.form.get('price', type=float)
        currency = request.form.get('currency', 'NPR')
        bedrooms = request.form.get('bedrooms', type=int)
        bathrooms = request.form.get('bathrooms', type=int)
        area = request.form.get('area', type=float)
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to make filename unique
                import time
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join('app/static/uploads', filename))
                image_filename = filename
        
        # Create new property
        new_property = Property(
            agent_id=current_user.id,
            title=title,
            description=description,
            property_type=property_type,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            price=price,
            currency=currency,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area=area,
            image_filename=image_filename
        )
        
        db.session.add(new_property)
        db.session.commit()
        
        flash('Property listed successfully!', 'success')
        return redirect(url_for('main.agent_dashboard'))
    
    return render_template('add_property.html', 
                         cities=NEPAL_CITIES,
                         property_types=NEPAL_PROPERTY_TYPES)


@main.route('/agent/property/edit/<int:property_id>', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    """
    Edit Existing Property
    """
    property_item = Property.query.get_or_404(property_id)
    
    # Check if user is the owner
    if property_item.agent_id != current_user.id:
        flash('You can only edit your own properties.', 'danger')
        return redirect(url_for('main.agent_dashboard'))
    
    if request.method == 'POST':
        # Update property data
        property_item.title = request.form.get('title')
        property_item.description = request.form.get('description')
        property_item.property_type = request.form.get('property_type')
        property_item.address = request.form.get('address')
        property_item.city = request.form.get('city')
        property_item.state = request.form.get('state')
        property_item.zipcode = request.form.get('zipcode')
        property_item.price = request.form.get('price', type=float)
        property_item.bedrooms = request.form.get('bedrooms', type=int)
        property_item.bathrooms = request.form.get('bathrooms', type=int)
        property_item.area = request.form.get('area', type=float)
        property_item.status = request.form.get('status')
        
        # Handle new image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                import time
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join('app/static/uploads', filename))
                property_item.image_filename = filename
        
        db.session.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('main.agent_dashboard'))
    
    return render_template('edit_property.html', property=property_item)


@main.route('/agent/property/delete/<int:property_id>', methods=['POST'])
@login_required
def delete_property(property_id):
    """
    Delete Property
    """
    property_item = Property.query.get_or_404(property_id)
    
    # Check if user is the owner
    if property_item.agent_id != current_user.id:
        flash('You can only delete your own properties.', 'danger')
        return redirect(url_for('main.agent_dashboard'))
    
    # Delete the property (cascades to inquiries)
    db.session.delete(property_item)
    db.session.commit()
    
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('main.agent_dashboard'))


@main.route('/agent/inquiry/<int:inquiry_id>/status', methods=['POST'])
@login_required
def update_inquiry_status(inquiry_id):
    """
    Update inquiry status (pending, replied, closed)
    """
    if current_user.role != 'agent':
        return jsonify({'success': False, 'message': 'Only agents can update inquiry status'}), 403
    
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    
    # Check if property belongs to agent
    if inquiry.property.agent_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    new_status = request.form.get('status')
    if new_status in ['pending', 'replied', 'closed']:
        inquiry.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'message': 'Status updated'})
    
    return jsonify({'success': False, 'message': 'Invalid status'}), 400


@main.route('/set-currency/<currency_code>')
def set_currency(currency_code):
    """
    Set user's preferred currency in session
    """
    allowed_currencies = ['NPR', 'USD', 'EUR', 'GBP', 'INR']
    if currency_code in allowed_currencies:
        session['currency'] = currency_code
        flash(f'Currency changed to {currency_code}', 'success')
    return redirect(request.referrer or url_for('main.home'))
