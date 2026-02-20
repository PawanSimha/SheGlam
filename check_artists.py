import requests

try:
    resp = requests.get('http://localhost:5000/api/artists')
    artists = resp.json()
    
    print(f"\n{'='*70}")
    print(f"Total Approved Artists: {len(artists)}")
    print(f"{'='*70}\n")
    
    for i, artist in enumerate(artists, 1):
        name = artist.get('business_name') or artist.get('user_id', 'Unknown')
        location = artist.get('location', 'Unknown')
        spec = artist.get('specialization', [])
        if isinstance(spec, list):
            spec = ', '.join(spec)
        exp = artist.get('experience_years', 0)
        rating = artist.get('rating', 0)
        price = artist.get('price_range', 'N/A')
        
        print(f"{i}. {name}")
        print(f"   📍 {location} | ⭐ {rating} | 📊 {exp} years exp")
        print(f"   💄 {spec}")
        print(f"   💰 ₹{price}")
        print()
        
except Exception as e:
    print(f"Error: {e}")
