"""
Real Estate Property Listings Application
Main Entry Point
Run this file to start the Flask development server
"""

from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Run the development server
    # Debug mode: Auto-reloads on code changes and shows detailed errors
    # WARNING: Never use debug=True in production!
    app.run(debug=True, host='0.0.0.0', port=5000)
