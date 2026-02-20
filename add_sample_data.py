"""
Add Sample Nepal Properties
Populates database with realistic Nepal property listings
"""

from app import create_app, db
from app.models import User, Property
from datetime import datetime

def add_sample_data():
    """Add sample users and Nepal properties"""
    
    app = create_app()
    with app.app_context():
        
        # Check if data already exists
        if User.query.first():
            print("⚠ Database already has data. Skipping...")
            return
        
        print("Adding sample data...")
        
        # Create sample agent
        agent = User(
            username='nepal_agent',
            email='agent@estatehub.np',
            full_name='Ram Sharma',
            phone='+977-9841234567',
            role='agent'
        )
        agent.set_password('password123')
        db.session.add(agent)
        db.session.commit()
        print("✓ Created sample agent: nepal_agent")
        
        # Sample Nepal Properties
        properties = [
            {
                'title': 'Luxury 3BHK Apartment in Lazimpat',
                'description': 'Modern apartment with mountain views, fully furnished, parking available. Perfect for families.',
                'property_type': 'Apartment',
                'address': 'Lazimpat Road',
                'city': 'Kathmandu',
                'state': 'Bagmati',
                'zipcode': '44600',
                'price': 25000000,
                'currency': 'NPR',
                'bedrooms': 3,
                'bathrooms': 2,
                'area': 1500,
                'status': 'available'
            },
            {
                'title': 'Beautiful House in Budhanilkantha',
                'description': 'Spacious house with garden, peaceful neighborhood, close to schools and hospitals.',
                'property_type': 'House',
                'address': 'Budhanilkantha',
                'city': 'Kathmandu',
                'state': 'Bagmati',
                'zipcode': '44600',
                'price': 35000000,
                'currency': 'NPR',
                'bedrooms': 4,
                'bathrooms': 3,
                'area': 2500,
                'status': 'available'
            },
            {
                'title': 'Lake View Villa in Pokhara',
                'description': 'Stunning villa with Phewa Lake view, perfect for tourists and families. Modern amenities.',
                'property_type': 'Villa',
                'address': 'Lakeside',
                'city': 'Pokhara',
                'state': 'Gandaki',
                'zipcode': '33700',
                'price': 40000000,
                'currency': 'NPR',
                'bedrooms': 5,
                'bathrooms': 4,
                'area': 3000,
                'status': 'available'
            },
            {
                'title': 'Commercial Space in New Road',
                'description': 'Prime commercial location, high foot traffic, suitable for retail or office.',
                'property_type': 'Commercial',
                'address': 'New Road',
                'city': 'Kathmandu',
                'state': 'Bagmati',
                'zipcode': '44600',
                'price': 50000000,
                'currency': 'NPR',
                'bedrooms': 0,
                'bathrooms': 2,
                'area': 3000,
                'status': 'available'
            },
            {
                'title': 'Affordable 2BHK in Lalitpur',
                'description': 'Budget-friendly apartment, good for small families or couples. Near Patan Durbar Square.',
                'property_type': 'Apartment',
                'address': 'Jawalakhel',
                'city': 'Lalitpur',
                'state': 'Bagmati',
                'zipcode': '44700',
                'price': 8000000,
                'currency': 'NPR',
                'bedrooms': 2,
                'bathrooms': 1,
                'area': 900,
                'status': 'available'
            },
            {
                'title': 'Land for Sale in Bhaktapur',
                'description': 'Prime land for residential or commercial development. Clear title, road access.',
                'property_type': 'Land',
                'address': 'Suryabinayak',
                'city': 'Bhaktapur',
                'state': 'Bagmati',
                'zipcode': '44800',
                'price': 15000000,
                'currency': 'NPR',
                'bedrooms': 0,
                'bathrooms': 0,
                'area': 5000,
                'status': 'available'
            },
            {
                'title': 'Tourist Hotel in Thamel',
                'description': 'Running hotel business with 15 rooms, restaurant, rooftop. Great investment opportunity.',
                'property_type': 'Hotel',
                'address': 'Thamel',
                'city': 'Kathmandu',
                'state': 'Bagmati',
                'zipcode': '44600',
                'price': 80000000,
                'currency': 'NPR',
                'bedrooms': 15,
                'bathrooms': 15,
                'area': 8000,
                'status': 'available'
            },
            {
                'title': 'Modern Office Space in Durbar Marg',
                'description': 'Premium office space in business district, fully furnished, high-speed internet.',
                'property_type': 'Office Space',
                'address': 'Durbar Marg',
                'city': 'Kathmandu',
                'state': 'Bagmati',
                'zipcode': '44600',
                'price': 30000000,
                'currency': 'NPR',
                'bedrooms': 0,
                'bathrooms': 3,
                'area': 2000,
                'status': 'available'
            }
        ]
        
        # Add properties
        for prop_data in properties:
            prop = Property(
                agent_id=agent.id,
                **prop_data
            )
            db.session.add(prop)
        
        db.session.commit()
        print(f"✓ Added {len(properties)} sample Nepal properties")
        
        # Create sample user
        user = User(
            username='demo_user',
            email='user@example.com',
            full_name='Sita Thapa',
            phone='+977-9851234567',
            role='user'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        print("✓ Created sample user: demo_user")
        
        print("\n✅ Sample data added successfully!")
        print("\n📝 Login Credentials:")
        print("   Agent: nepal_agent / password123")
        print("   User:  demo_user / password123")
        print("\n🏠 Properties added:")
        print(f"   - {len(properties)} Nepal properties with NPR pricing")
        print("   - Cities: Kathmandu, Pokhara, Lalitpur, Bhaktapur")
        print("   - Price range: रू 8,000,000 - रू 80,000,000")

if __name__ == '__main__':
    add_sample_data()
