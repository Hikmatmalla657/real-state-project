"""
Database Reset Script
Deletes old database and creates new one with updated schema
"""

import os
from app import create_app, db

def reset_database():
    """Delete old database and create new one"""
    
    # Path to database file
    db_path = 'instance/realestate.db'
    
    # Delete old database if exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Deleted old database: {db_path}")
    else:
        print("No existing database found")
    
    # Create new database with updated schema
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✓ Created new database with updated schema")
        print("✓ Database now includes 'currency' field for properties")
    
    print("\n✅ Database reset complete!")
    print("You can now run: python run.py")

if __name__ == '__main__':
    reset_database()
