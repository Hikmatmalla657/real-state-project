# EstateHub - Installation & Setup Guide

This guide will help you set up and run the EstateHub Real Estate Platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version` or `python3 --version`

2. **pip** (Python package installer)
   - Usually comes with Python
   - Verify: `pip --version` or `pip3 --version`

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/downloads

## Step-by-Step Installation

### Step 1: Get the Project Files

**Option A: If you have the ZIP file**
```bash
# Extract the ZIP file to a folder
# Navigate to the extracted folder
cd real_estate_project
```

**Option B: If cloning from GitHub**
```bash
git clone https://github.com/yourusername/estatehub.git
cd estatehub
```

### Step 2: Create a Virtual Environment (Recommended)

A virtual environment keeps your project dependencies isolated.

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-Login (user authentication)
- Werkzeug (security utilities)

### Step 4: Initialize the Database

You have two options:

**Option A: Create Empty Database**
```bash
python run.py
```
The database will be created automatically on first run.
Then create your own admin account through the registration page.

**Option B: Load Sample Data (Recommended for Testing)**
```bash
python create_sample_data.py
```

This creates:
- 2 sample users (buyers)
- 2 sample agents
- 8 sample properties
- 3 sample inquiries

**Sample Login Credentials:**
- **User Account:** 
  - Username: `john_doe`
  - Password: `password123`
  
- **Agent Account:**
  - Username: `mike_agent`
  - Password: `agent123`

### Step 5: Run the Application

```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 6: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

## Testing the Application

### As a User (Property Buyer/Renter):

1. **Register a new account:**
   - Click "Register" in the navigation bar
   - Fill in your details
   - Choose "Find Property" as your role
   - Click "Create Account"

2. **Or login with sample account:**
   - Username: `john_doe`
   - Password: `password123`

3. **Test Features:**
   - Browse properties on the Properties page
   - Use search and filters
   - Click on a property to see details
   - Save properties to favorites (heart icon)
   - Submit an inquiry to an agent
   - View your dashboard

### As an Agent (Property Lister):

1. **Login with sample agent account:**
   - Username: `mike_agent`
   - Password: `agent123`

2. **Test Features:**
   - View your agent dashboard
   - Click "Add New Property"
   - Fill in property details
   - Upload an image (optional)
   - Submit the form
   - Edit your properties
   - View and manage inquiries
   - Update inquiry status

## Project Structure Overview

```
real_estate_project/
├── app/                      # Main application package
│   ├── __init__.py          # App initialization & configuration
│   ├── models.py            # Database models (User, Property, Inquiry)
│   ├── routes.py            # URL routes and view functions
│   ├── static/              # Static files (CSS, JS, images)
│   │   ├── css/
│   │   │   └── style.css   # Custom styles
│   │   ├── js/
│   │   │   └── main.js     # JavaScript functionality
│   │   └── uploads/        # User-uploaded property images
│   └── templates/           # HTML templates (Jinja2)
│       ├── base.html       # Base template with navbar & footer
│       ├── home.html       # Homepage
│       ├── properties.html # Property listings
│       └── ... (other pages)
├── instance/
│   └── realestate.db       # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── run.py                  # Application entry point
├── create_sample_data.py   # Sample data generator
└── README.md               # Documentation
```

## Common Issues & Solutions

### Issue 1: "Python not found"
**Solution:** Make sure Python is installed and added to your system PATH.

### Issue 2: "pip not found"
**Solution:** 
```bash
python -m pip --version
# or
python -m ensurepip --upgrade
```

### Issue 3: "Address already in use"
**Solution:** Port 5000 is already being used. Either:
- Stop the other application using port 5000
- Or modify `run.py` to use a different port:
```python
app.run(debug=True, port=5001)
```

### Issue 4: Database errors
**Solution:** Delete the database and recreate:
```bash
# Delete instance/realestate.db
# Then run:
python create_sample_data.py
```

### Issue 5: Images not uploading
**Solution:** Check that the `app/static/uploads` folder exists and has write permissions.

## Stopping the Application

Press `Ctrl+C` in the terminal where the application is running.

## Deactivating Virtual Environment

When you're done:
```bash
deactivate
```

## Next Steps

1. **Customize the Application:**
   - Modify colors in `app/static/css/style.css`
   - Update the logo and branding
   - Add more property types
   - Customize email templates

2. **Deploy to Production:**
   - See the README.md for deployment guides
   - Options include: PythonAnywhere, Heroku, Railway

3. **Add Features:**
   - Email notifications
   - Payment integration
   - Advanced search with maps
   - Property comparisons

## Need Help?

- Check the README.md for more detailed documentation
- Review the code comments for understanding
- Test the sample data to see how everything works

## Security Note

⚠️ **Important:** The current configuration uses a simple secret key and is set to debug mode. 

**For production deployment:**
1. Change the `SECRET_KEY` in `app/__init__.py` to a random, secure value
2. Set `debug=False` in `run.py`
3. Use a production-grade database (PostgreSQL, MySQL)
4. Enable HTTPS
5. Set up proper error logging

---

**Happy Coding! 🚀**

If you encounter any issues not covered here, please check the project documentation or create an issue on GitHub.
