"""
Real Estate Property Listings Application
Main Entry Point
Run this file to start the Flask development server
"""

import os
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Run the development server
    # Debug mode: Auto-reloads on code changes and shows detailed errors
    # WARNING: Never use debug=True in production!
    debug = os.environ.get('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes'}
    app.run(debug=debug, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
