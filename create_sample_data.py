"""
Sample Data Generator
Run this script to populate the database with sample users and properties for testing
"""

from app import create_app, db
from app.models import User, Property, Inquiry
from datetime import datetime

def create_sample_data():
    """Create sample users and properties for testing"""
    
    app = create_app()
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        print("Creating sample users...")
        
        # Create sample users (buyers)
        user1 = User(
            username='john_doe',
            email='john1@example.com',
            full_name='John Doe',
            phone='+977 123-456-7890',
            role='user'
        )
        user1.set_password('password123')
        
        user2 = User(
            username='Hikmat_smith',
            email='jane2@example.com',
            full_name='Jane Smith',
            phone='+977 987-654-3210',
            role='user'
        )
        user2.set_password('password123')
        
        # Create sample agents
        agent1 = User(
            username='mike_agent',
            email='mike@estatehub3.com',
            full_name='Mike Johnson',
            phone='+977 555-1234',
            role='agent'
        )
        agent1.set_password('agent123')
        
        agent2 = User(
            username='sarah_agent',
            email='sarah@estatehub.com',
            full_name='Sarah Williams',
            phone='+977 555-5678',
            role='agent'
        )
        agent2.set_password('agent123')
        
        # Add users to database
        db.session.add_all([user1, user2, agent1, agent2])
        db.session.commit()
        
        print("Creating sample properties...")
        
        # Sample properties for agent1
        property1 = Property(
            agent_id=agent1.id,
            title='Luxury Villa with Garden in Bakhundole',
            description='Modern luxury villa with 4 bedrooms, private garden, parking space, and beautiful mountain views. Located in a peaceful residential area.',
            property_type='Villa',
            address='Bakhundole',
            city='Lalitpur',
            state='Bagmati',
            zipcode='44600',
            price=450000,
            bedrooms=4,
            bathrooms=3,
            area=3500,
            status='available'
)
        
        
        property2 = Property(
            agent_id=agent1.id,
            title='Modern Apartment in Jawalakhel',
            description='2-bedroom apartment with lift, parking, gym, and 24/7 security. Perfect for city living with easy access to shops and offices.',
            property_type='Apartment',
            address='Jawalakhel',
            city='Lalitpur',
            state='Bagmati',
            zipcode='44700',
            price=180000,
            bedrooms=2,
            bathrooms=2,
            area=1200,
            status='available'
)
        
        property3 = Property(
            agent_id=agent1.id,
            title='Family House in Bhaktapur',
            description='Comfortable 3-bedroom house with courtyard and traditional design. Suitable for families looking for a peaceful environment.',
            property_type='House',
            address='Bhaktapur Durbar Area',
            city='Bhaktapur',
            state='Bagmati',
            zipcode='44800',
            price=250000,
            bedrooms=3,
            bathrooms=2,
            area=2000,
            status='available'
)
        
        # Sample properties for agent2
        property4 = Property(
            agent_id=agent2.id,
            title='Premium Condo with Lake View',
            description='Luxury condo near Phewa Lake with modern interior, balcony, and stunning Himalayan views.',
            property_type='Condo',
            address='Lakeside',
            city='Pokhara',
            state='Gandaki',
            zipcode='33700',
            price=320000,
            bedrooms=3,
            bathrooms=2,
            area=1800,
            status='available'
)
        
        
        property5 = Property(
            agent_id=agent2.id,
            title='Commercial Space in New Road',
            description='Prime commercial space suitable for shops, offices, or restaurants. Located in a high-traffic business area.',
            property_type='Commercial',
            address='New Road',
            city='Kathmandu',
            state='Bagmati',
            zipcode='44600',
            price=600000,
            area=2500,
            status='available'
)
        
        
        property6 = Property(
            agent_id=agent2.id,
            title='Spacious Family Home in Thimi',
            description='Large 5-bedroom house with garden, parking, and rooftop terrace. Ideal for big families.',
            property_type='House',
            address='Madhyapur Thimi',
            city='Bhaktapur',
            state='Bagmati',
            zipcode='44800',
            price=380000,
            bedrooms=5,
            bathrooms=4,
            area=4000,
            status='available'
)
        property7 = Property(
            agent_id=agent1.id,
            title='Affordable Apartment in Baneshwor',
            description='1-bedroom budget apartment with basic facilities. Great for students or first-time buyers.',
            property_type='Apartment',
            address='Baneshwor',
            city='Kathmandu',
            state='Bagmati',
            zipcode='44600',
            price=95000,
            bedrooms=1,
            bathrooms=1,
            area=650,
            status='available'
)
        
        property8 = Property(
            agent_id=agent2.id,
            title='Residential Land in Chitwan',
            description='5000 sq ft land suitable for building a house. Peaceful area with road access and clear ownership.',
            property_type='Land',
            address='Bharatpur',
            city='Chitwan',
            state='Bagmati',
            zipcode='44200',
            price=75000,
            area=5000,
            status='available'
)
        
        # Add properties to database
        db.session.add_all([property1, property2, property3, property4, property5, property6, property7, property8])
        db.session.commit()
        
        print("Creating sample inquiries...")
        
        # Sample inquiries
        inquiry1 = Inquiry(
            user_id=user1.id,
            property_id=property1.id,
            message="I'm very interested in this villa. Could we schedule a viewing this weekend?",
            contact_phone=user1.phone,
            status='pending'
        )
        
        inquiry2 = Inquiry(
            user_id=user2.id,
            property_id=property2.id,
            message="Is the apartment still available? I'd like more information about the monthly maintenance fees.",
            contact_phone=user2.phone,
            status='pending'
        )
        
        inquiry3 = Inquiry(
            user_id=user1.id,
            property_id=property4.id,
            message="Beautiful property! Can you provide more details about the amenities?",
            contact_phone=user1.phone,
            status='replied'
        )
        
        db.session.add_all([inquiry1, inquiry2, inquiry3])
        
        # Add some favorites
        user1.favorite_properties.append(property1)
        user1.favorite_properties.append(property4)
        user2.favorite_properties.append(property2)
        
        db.session.commit()
        
        print("\n✅ Sample data created successfully!")
        print("\n📊 Summary:")
        print(f"   Users (Buyers): 2")
        print(f"   Agents: 2")
        print(f"   Properties: 8")
        print(f"   Inquiries: 3")
        print("\n🔑 Login Credentials:")
        print("\n   User Account:")
        print("   Username: john_doe")
        print("   Password: password123")
        print("\n   Agent Account:")
        print("   Username: mike_agent")
        print("   Password: agent123")
        print("\n🚀 Run 'python run.py' to start the application!")

if __name__ == '__main__':
    create_sample_data()
