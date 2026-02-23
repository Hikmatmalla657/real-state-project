# EstateHub - Real Estate Property Listings Platform

![EstateHub](https://img.shields.io/badge/EstateHub-Real%20Estate-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.3-red)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

A professional, full-stack real estate property listings website built with Flask, SQLAlchemy, and Bootstrap. This project enables users to browse properties, save favorites, and contact agents, while agents can manage their property listings.

## 🌟 Features

### For Property Buyers/Renters (Users)
- 🏠 Browse extensive property listings
- 🔍 Advanced search and filtering (type, location, price, bedrooms)
- ❤️ Save favorite properties
- 📧 Send inquiries to property agents
- 👤 Personal dashboard to manage favorites and inquiries
- 📱 Fully responsive design for mobile, tablet, and desktop

### For Property Agents
- ➕ Add new property listings with images
- ✏️ Edit and update existing properties
- 🗑️ Delete property listings
- 📊 View property statistics and insights
- 📬 Manage inquiries from potential buyers
- 📈 Track property status (available, sold, rented)

### Technical Features
- 🔐 Secure user authentication with password hashing
- 🎨 Professional, colorful, and modern UI design
- 📦 RESTful API architecture
- 💾 SQLite database with SQLAlchemy ORM
- 🔄 CRUD operations for all entities
- ✅ Client-side and server-side form validation
- 🎭 Session management with Flask-Login
- 📸 Image upload functionality
- 🎯 One-to-Many and Many-to-Many database relationships

## 🚀 Live Demo

[Add your deployment URL here]

## 📸 Screenshots

### Homepage
![Homepage](screenshots/homepage.png)

### Property Listings
![Properties](screenshots/properties.png)

### User Dashboard
![User Dashboard](screenshots/user_dashboard.png)

### Agent Dashboard
![Agent Dashboard](screenshots/agent_dashboard.png)

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask 2.3** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **Werkzeug** - Password hashing and security

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with CSS variables
- **Bootstrap 5.3** - Responsive framework
- **JavaScript (ES6+)** - Client-side interactivity
- **Font Awesome** - Icons
- **Google Fonts** - Typography (Playfair Display, DM Sans)

### Database
- **SQLite** - Development database
- **SQLAlchemy ORM** - Database abstraction

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/estatehub.git
cd estatehub
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

The application will start on `http://localhost:5000`

## 📁 Project Structure

```
real_estate_project/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models (User, Property, Inquiry)
│   ├── routes.py            # URL routes and view functions
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom styles
│   │   ├── js/
│   │   │   └── main.js      # JavaScript functionality
│   │   ├── images/          # Static images
│   │   └── uploads/         # User-uploaded images
│   └── templates/
│       ├── base.html        # Base template
│       ├── home.html        # Homepage
│       ├── properties.html  # Property listings
│       ├── property_detail.html
│       ├── register.html    # User registration
│       ├── login.html       # User login
│       ├── user_dashboard.html
│       ├── agent_dashboard.html
│       ├── add_property.html
│       ├── edit_property.html
│       └── profile.html
├── instance/
│   └── realestate.db        # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # Project documentation
```

## 🗄️ Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `full_name`
- `phone`
- `role` (user/agent)
- `created_at`

### Properties Table
- `id` (Primary Key)
- `agent_id` (Foreign Key → Users)
- `title`
- `description`
- `property_type`
- `address`, `city`, `state`, `zipcode`
- `price`
- `bedrooms`, `bathrooms`, `area`
- `status` (available/sold/rented)
- `image_filename`
- `created_at`, `updated_at`

### Inquiries Table
- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `property_id` (Foreign Key → Properties)
- `message`
- `contact_phone`
- `status` (pending/replied/closed)
- `created_at`

### Favorites Table (Association)
- `user_id` (Foreign Key → Users)
- `property_id` (Foreign Key → Properties)
- `added_at`

## 🎯 Usage Guide

### Creating an Account

1. Navigate to the **Register** page
2. Choose your role:
   - **Find Property** - For buyers/renters
   - **List Property** - For agents
3. Fill in your details
4. Click **Create Account**

### For Users

1. **Browse Properties**: Visit the Properties page to see all listings
2. **Search & Filter**: Use filters to narrow down your search
3. **View Details**: Click on any property to see full details
4. **Save Favorites**: Click the heart icon to save properties
5. **Send Inquiry**: Fill out the inquiry form on property detail pages
6. **Dashboard**: View your saved properties and sent inquiries

### For Agents

1. **Add Property**: Click "Add New Property" from your dashboard
2. **Upload Image**: Add property photos (JPG, PNG, GIF, WebP)
3. **Manage Listings**: Edit or delete properties from your dashboard
4. **Handle Inquiries**: View and respond to buyer inquiries
5. **Update Status**: Mark properties as available, sold, or rented

## 🔐 Security Features

- Password hashing using Werkzeug
- Session-based authentication with Flask-Login
- CSRF protection
- Input validation (client-side and server-side)
- Secure file uploads with type validation
- Protected routes requiring authentication

## 🎨 Design Features

- Modern, colorful gradient-based design
- Distinctive typography (Playfair Display + DM Sans)
- Smooth animations and transitions
- Responsive layout for all devices
- Accessible form design
- Professional color scheme

## 🧪 Testing

### Manual Testing Checklist

- [ ] User registration works correctly
- [ ] User login and logout work
- [ ] Users can browse properties
- [ ] Search and filter functionality works
- [ ] Users can save/unsave favorites
- [ ] Users can submit inquiries
- [ ] Agents can add properties
- [ ] Agents can edit properties
- [ ] Agents can delete properties
- [ ] Image upload works correctly
- [ ] Responsive design on mobile devices
- [ ] Form validation works properly

## 🚀 Deployment

### Deploy to PythonAnywhere

1. Create account on [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your project files
3. Create virtual environment
4. Install dependencies
5. Configure WSGI file
6. Set up static files
7. Reload web app

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

## 📝 Future Enhancements

- [ ] Email notifications for inquiries
- [ ] Advanced search with map integration
- [ ] Property comparison feature
- [ ] User reviews and ratings
- [ ] Payment gateway integration
- [ ] Admin panel for site management
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Property analytics for agents
- [ ] Social media sharing

## 👥 Contributors

- **Your Name** - Initial work - [Your GitHub](https://github.com/yourusername)

## 📄 License

This project is developed for educational purposes as part of the Web Technology (BIT233) course assignment.

## 🙏 Acknowledgments

- Texas College of Management & IT
- Mr. Ashish Gautam (Course Instructor)
- Bootstrap team for the excellent framework
- Font Awesome for beautiful icons
- Unsplash for placeholder images

## 📞 Contact

For questions or support, please contact:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

**Developed with ❤️ for Web Technology Assignment**
#   r e a l - s t a t e  
 # r e a l - s t a t e - p r o j e c t  
 