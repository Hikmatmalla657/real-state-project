"""
Currency Helper Functions
Handles currency conversion and formatting for Nepal and international users
"""

# Exchange rates (approximate - update regularly for production)
EXCHANGE_RATES = {
    'NPR': 1.0,        # Nepalese Rupee (base currency)
    'USD': 0.0075,     # 1 NPR = 0.0075 USD (approx 133 NPR = 1 USD)
    'EUR': 0.0069,     # 1 NPR = 0.0069 EUR
    'GBP': 0.0059,     # 1 NPR = 0.0059 GBP
    'INR': 0.60,       # 1 NPR = 0.60 INR
}

CURRENCY_SYMBOLS = {
    'NPR': 'रू',       # Nepalese Rupee symbol
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'INR': '₹',
}

def convert_currency(amount, from_currency='NPR', to_currency='USD'):
    """
    Convert amount from one currency to another
    
    Args:
        amount: The amount to convert
        from_currency: Source currency code (default: NPR)
        to_currency: Target currency code (default: USD)
    
    Returns:
        Converted amount
    """
    if from_currency == to_currency:
        return amount
    
    # Convert to NPR first (base currency)
    amount_in_npr = amount / EXCHANGE_RATES.get(from_currency, 1.0)
    
    # Convert from NPR to target currency
    converted_amount = amount_in_npr * EXCHANGE_RATES.get(to_currency, 1.0)
    
    return round(converted_amount, 2)

def format_price(amount, currency='NPR', show_symbol=True):
    """
    Format price with proper currency symbol and formatting
    
    Args:
        amount: The price amount
        currency: Currency code (default: NPR)
        show_symbol: Whether to show currency symbol (default: True)
    
    Returns:
        Formatted price string
    """
    symbol = CURRENCY_SYMBOLS.get(currency, currency)
    
    # Format with commas for thousands
    if currency == 'NPR' or currency == 'INR':
        # Indian numbering system (lakhs and crores)
        formatted = format_indian_number(amount)
    else:
        # Western numbering system
        formatted = "{:,.0f}".format(amount)
    
    if show_symbol:
        if currency == 'NPR':
            return f"{symbol} {formatted}"
        else:
            return f"{symbol}{formatted}"
    
    return formatted

def format_indian_number(number):
    """
    Format number in Indian numbering system (lakhs, crores)
    Example: 1,00,000 (1 lakh), 10,00,000 (10 lakhs), 1,00,00,000 (1 crore)
    """
    s = str(int(number))
    if len(s) <= 3:
        return s
    
    # Last 3 digits
    result = s[-3:]
    s = s[:-3]
    
    # Add commas every 2 digits for the rest
    while s:
        if len(s) <= 2:
            result = s + ',' + result
            break
        result = s[-2:] + ',' + result
        s = s[:-2]
    
    return result

def get_price_display(property_obj, user_currency='NPR'):
    """
    Get price display for a property in user's preferred currency
    
    Args:
        property_obj: Property model instance
        user_currency: User's preferred currency (default: NPR)
    
    Returns:
        Dictionary with original and converted prices
    """
    original_price = property_obj.price
    original_currency = property_obj.currency
    
    result = {
        'original_price': original_price,
        'original_currency': original_currency,
        'original_formatted': format_price(original_price, original_currency),
    }
    
    # If user wants different currency, add conversion
    if user_currency != original_currency:
        converted_price = convert_currency(original_price, original_currency, user_currency)
        result['converted_price'] = converted_price
        result['converted_currency'] = user_currency
        result['converted_formatted'] = format_price(converted_price, user_currency)
    
    return result

# Popular Nepal cities for property listings
NEPAL_CITIES = [
    'Kathmandu',
    'Pokhara',
    'Lalitpur',
    'Bhaktapur',
    'Biratnagar',
    'Birgunj',
    'Dharan',
    'Bharatpur',
    'Janakpur',
    'Hetauda',
    'Butwal',
    'Dhangadhi',
    'Itahari',
    'Nepalgunj',
    'Tulsipur',
]

# Property types common in Nepal
NEPAL_PROPERTY_TYPES = [
    'House',
    'Apartment',
    'Villa',
    'Land',
    'Commercial',
    'Office Space',
    'Shop',
    'Warehouse',
    'Hotel',
    'Resort',
]
