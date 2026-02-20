# Nepal Property Setup Guide - EstateHub

## Overview
Your EstateHub project now supports Nepalese properties with NPR (Nepalese Rupees) pricing and multi-currency support for international users.

## Features Added

### 1. **Currency Support**
- **Primary Currency**: NPR (Nepalese Rupees) - रू
- **Additional Currencies**: USD, EUR, GBP, INR
- **Exchange Rates**: Built-in conversion (update rates in `currency_helper.py`)

### 2. **Nepal-Specific Features**
- **Nepal Cities**: Pre-populated with major cities (Kathmandu, Pokhara, Lalitpur, etc.)
- **Property Types**: Common Nepal property types (House, Apartment, Land, Commercial, etc.)
- **Price Format**: Indian numbering system (Lakhs and Crores)

### 3. **International User Support**
- Currency converter shows prices in user's preferred currency
- Session-based currency preference
- Easy currency switching

## How to Use

### For Property Agents (Adding Properties):

1. **Login as Agent**
2. **Go to "Add Property"**
3. **Fill Property Details**:
   - Title: e.g., "Modern 3BHK Apartment in Kathmandu"
   - City: Select from Nepal cities dropdown
   - Price: Enter in NPR (e.g., 15000000 for 1.5 Crore)
   - Currency: Select NPR (default)

### Example Property Listings:

**Budget Properties:**
- 1BHK Apartment: रू 3,000,000 - 5,000,000 (30-50 Lakhs)
- 2BHK Apartment: रू 5,000,000 - 8,000,000 (50-80 Lakhs)

**Mid-Range Properties:**
- 3BHK Apartment: रू 10,000,000 - 20,000,000 (1-2 Crore)
- House: रू 15,000,000 - 30,000,000 (1.5-3 Crore)

**Luxury Properties:**
- Villa: रू 50,000,000+ (5+ Crore)
- Commercial: रू 100,000,000+ (10+ Crore)

### For International Users:

1. **Browse Properties** - Prices shown in NPR by default
2. **Currency Converter** - Automatic conversion to USD/EUR/GBP
3. **Affordable Booking** - Contact agents directly through inquiry form

## Database Migration

Since we added a new `currency` field to the Property model, you need to:

### Option 1: Fresh Start (Recommended for Development)
```bash
# Delete the old database
rm instance/realestate.db

# Run the application (it will create new database)
python run.py
```

### Option 2: Keep Existing Data
```python
# Run this in Python shell
from app import create_app, db
from app.models import Property

app = create_app()
with app.app_context():
    # Add currency column with default NPR
    db.session.execute('ALTER TABLE properties ADD COLUMN currency VARCHAR(10) DEFAULT "NPR"')
    db.session.commit()
```

## Sample Property Data for Nepal

### Kathmandu Properties:
1. **Luxury Apartment - Lazimpat**
   - Price: रू 25,000,000 (2.5 Crore)
   - 3 Bed, 2 Bath, 1500 sqft

2. **Modern House - Budhanilkantha**
   - Price: रू 35,000,000 (3.5 Crore)
   - 4 Bed, 3 Bath, 2500 sqft

3. **Commercial Space - New Road**
   - Price: रू 50,000,000 (5 Crore)
   - Office, 3000 sqft

### Pokhara Properties:
1. **Lake View Villa**
   - Price: रू 40,000,000 (4 Crore)
   - 5 Bed, 4 Bath, 3000 sqft

2. **Tourist Hotel**
   - Price: रू 80,000,000 (8 Crore)
   - 15 Rooms, Commercial

## Currency Exchange Rates (Approximate)

- 1 USD = रू 133
- 1 EUR = रू 145
- 1 GBP = रू 170
- 1 INR = रू 1.60

**Note**: Update rates regularly in `app/currency_helper.py`

## For Foreign Tourists/Buyers:

### Affordable Options:
- **Short-term Rentals**: रू 20,000 - 50,000/month ($150-375/month)
- **Long-term Rentals**: रू 15,000 - 40,000/month ($112-300/month)
- **Purchase**: Starting from रू 3,000,000 ($22,500)

### Popular Areas for Foreigners:
1. **Thamel, Kathmandu** - Tourist hub
2. **Lakeside, Pokhara** - Scenic views
3. **Patan, Lalitpur** - Cultural area
4. **Boudha** - Peaceful neighborhood

## Features for International Users:

✅ **Multi-Currency Display** - See prices in your currency
✅ **English Interface** - Easy to navigate
✅ **Direct Agent Contact** - Inquiry system
✅ **Property Photos** - Visual browsing
✅ **Detailed Information** - Full property specs
✅ **Favorite Properties** - Save for later

## Next Steps:

1. **Add Sample Properties** - Create listings with Nepal cities and NPR prices
2. **Test Currency Conversion** - Verify prices display correctly
3. **Add Property Images** - Upload photos of Nepal properties
4. **Customize Exchange Rates** - Update to current rates

## Support:

For questions about Nepal property market or technical issues, refer to:
- Nepal Real Estate Association
- Current NPR exchange rates: Nepal Rastra Bank website

---

**Your EstateHub is now ready for Nepal property listings! 🏠🇳🇵**
