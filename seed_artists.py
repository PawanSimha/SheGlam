"""
Seed Script: Create 10 Professional Artist Profiles
Populates the database with realistic artist accounts for testing
"""
import requests
import json
from pathlib import Path
from io import BytesIO

BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"
AUTH_BASE = f"{BASE_URL}/auth"

# Admin credentials for approval
ADMIN_CREDENTIALS = {
    "email": "pawansimha@gmail.com",
    "password": "Hercules"
}

# 10 realistic artist profiles
ARTISTS = [
    {
        "name": "Priya Sharma",
        "email": "priya.sharma@sheglam.com",
        "phone": "9876543210",
        "password": "artist123",
        "experience_years": 8,
        "specialization": "Bridal, Traditional",
        "location": "Mumbai",
        "price_range": "3000-8000",
        "certificate_link": "https://beautycert.in/priya-sharma",
        "govt_id_type": "Aadhaar"
    },
    {
        "name": "Ananya Reddy",
        "email": "ananya.reddy@sheglam.com",
        "phone": "9876543211",
        "password": "artist123",
        "experience_years": 5,
        "specialization": "Party, HD Makeup",
        "location": "Bangalore",
        "price_range": "2000-6000",
        "certificate_link": "https://beautyacademy.com/ananya",
        "govt_id_type": "Passport"
    },
    {
        "name": "Meera Patel",
        "email": "meera.patel@sheglam.com",
        "phone": "9876543212",
        "password": "artist123",
        "experience_years": 10,
        "specialization": "Bridal, Engagement, Reception",
        "location": "Ahmedabad",
        "price_range": "4000-10000",
        "certificate_link": "https://makeupinstitute.in/meera",
        "govt_id_type": "Voter ID"
    },
    {
        "name": "Kavya Iyer",
        "email": "kavya.iyer@sheglam.com",
        "phone": "9876543213",
        "password": "artist123",
        "experience_years": 3,
        "specialization": "Party, Photoshoot",
        "location": "Chennai",
        "price_range": "1500-4000",
        "certificate_link": "https://glamacademy.com/kavya",
        "govt_id_type": "Aadhaar"
    },
    {
        "name": "Sneha Nair",
        "email": "sneha.nair@sheglam.com",
        "phone": "9876543214",
        "password": "artist123",
        "experience_years": 7,
        "specialization": "Bridal, Traditional, Modern",
        "location": "Thiruvananthapuram",
        "price_range": "2500-7000",
        "certificate_link": "https://beautycert.org/sneha",
        "govt_id_type": "PAN Card"
    },
    {
        "name": "Riya Kapoor",
        "email": "riya.kapoor@sheglam.com",
        "phone": "9876543215",
        "password": "artist123",
        "experience_years": 6,
        "specialization": "HD Makeup, Fashion",
        "location": "Delhi",
        "price_range": "3500-9000",
        "certificate_link": "https://fashionmakeup.in/riya",
        "govt_id_type": "Passport"
    },
    {
        "name": "Divya Singh",
        "email": "divya.singh@sheglam.com",
        "phone": "9876543216",
        "password": "artist123",
        "experience_years": 4,
        "specialization": "Engagement, Party, Corporate",
        "location": "Pune",
        "price_range": "2000-5000",
        "certificate_link": "https://makeupguru.com/divya",
        "govt_id_type": "Aadhaar"
    },
    {
        "name": "Aisha Khan",
        "email": "aisha.khan@sheglam.com",
        "phone": "9876543217",
        "password": "artist123",
        "experience_years": 9,
        "specialization": "Bridal, International Looks",
        "location": "Hyderabad",
        "price_range": "4500-12000",
        "certificate_link": "https://international-makeup.in/aisha",
        "govt_id_type": "Voter ID"
    },
    {
        "name": "Nisha Gupta",
        "email": "nisha.gupta@sheglam.com",
        "phone": "9876543218",
        "password": "artist123",
        "experience_years": 5,
        "specialization": "Party, Casual, Natural Look",
        "location": "Kolkata",
        "price_range": "1800-4500",
        "certificate_link": "https://beautycollege.edu/nisha",
        "govt_id_type": "PAN Card"
    },
    {
        "name": "Simran Kaur",
        "email": "simran.kaur@sheglam.com",
        "phone": "9876543219",
        "password": "artist123",
        "experience_years": 12,
        "specialization": "Bridal, Celebrity Makeup, Airbrush",
        "location": "Chandigarh",
        "price_range": "5000-15000",
        "certificate_link": "https://celebrity-makeup.pro/simran",
        "govt_id_type": "Passport"
    }
]

def create_dummy_image():
    """Create a minimal valid JPG file"""
    # JPEG header for a minimal valid image
    jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    jpeg_data += b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f'
    jpeg_data += b'\x00' * 100  # Padding
    jpeg_data += b'\xff\xd9'  # End of image marker
    return jpeg_data

def headers(token=None):
    """Generate headers with optional JWT token"""
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def signup_artist(artist_data):
    """Register artist account"""
    try:
        resp = requests.post(
            f"{AUTH_BASE}/signup",
            json={
                "name": artist_data["name"],
                "email": artist_data["email"],
                "phone": artist_data["phone"],
                "password": artist_data["password"],
                "role": "artist"
            },
            headers=headers()
        )
        return resp.status_code == 201
    except Exception as e:
        print(f"❌ Signup failed for {artist_data['name']}: {e}")
        return False

def login_artist(artist_data):
    """Login and get JWT token"""
    try:
        resp = requests.post(
            f"{AUTH_BASE}/login",
            json={
                "email": artist_data["email"],
                "password": artist_data["password"]
            },
            headers=headers()
        )
        if resp.status_code == 200:
            return resp.json().get("token")
        return None
    except Exception as e:
        print(f"❌ Login failed for {artist_data['name']}: {e}")
        return None

def create_artist_profile(artist_data, token):
    """Create artist profile with files"""
    try:
        # Prepare files
        cert_data = create_dummy_image()
        govt_data = create_dummy_image()
        
        files = {
            'certificate': (f'{artist_data["name"]}_cert.jpg', BytesIO(cert_data), 'image/jpeg'),
            'govt_id': (f'{artist_data["name"]}_id.jpg', BytesIO(govt_data), 'image/jpeg')
        }
        
        form_data = {
            'experience_years': str(artist_data['experience_years']),
            'specialization': artist_data['specialization'],
            'location': artist_data['location'],
            'price_range': artist_data['price_range'],
            'certificate_link': artist_data['certificate_link'],
            'govt_id_type': artist_data['govt_id_type']
        }
        
        h = {"Authorization": f"Bearer {token}"}
        resp = requests.post(
            f"{API_BASE}/artist/register",
            data=form_data,
            files=files,
            headers=h
        )
        
        return resp.status_code == 201
    except Exception as e:
        print(f"❌ Profile creation failed for {artist_data['name']}: {e}")
        return False

def get_admin_token():
    """Login as admin"""
    try:
        resp = requests.post(
            f"{AUTH_BASE}/login",
            json=ADMIN_CREDENTIALS,
            headers=headers()
        )
        if resp.status_code == 200:
            return resp.json().get("token")
        return None
    except Exception as e:
        print(f"❌ Admin login failed: {e}")
        return None

def get_pending_artists(admin_token):
    """Get pending artists"""
    try:
        resp = requests.get(
            f"{API_BASE}/admin/artists/pending",
            headers=headers(admin_token)
        )
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception as e:
        print(f"❌ Failed to get pending artists: {e}")
        return []

def approve_artist(artist_id, admin_token):
    """Approve an artist"""
    try:
        resp = requests.put(
            f"{API_BASE}/admin/artist/approve/{artist_id}",
            headers=headers(admin_token)
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"❌ Approval failed: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("SheGlam Artist Profile Seeder")
    print("Creating 10 professional artist accounts...")
    print("="*70 + "\n")
    
    created_count = 0
    
    # Step 1: Create all artist accounts and profiles
    for i, artist in enumerate(ARTISTS, 1):
        print(f"\n[{i}/10] Processing: {artist['name']}")
        print("-" * 50)
        
        # Signup
        print(f"  ⏳ Signing up...")
        if not signup_artist(artist):
            print(f"  ⚠️  Skipping (probably already exists)")
            continue
        
        print(f"  ✅ Signed up successfully")
        
        # Login
        print(f"  ⏳ Logging in...")
        token = login_artist(artist)
        if not token:
            print(f"  ❌ Login failed")
            continue
        
        print(f"  ✅ Logged in")
        
        # Create profile
        print(f"  ⏳ Creating profile...")
        if create_artist_profile(artist, token):
            print(f"  ✅ Profile created")
            print(f"  📍 Location: {artist['location']}")
            print(f"  💼 Specialization: {artist['specialization']}")
            print(f"  📊 Experience: {artist['experience_years']} years")
            print(f"  💰 Price: ₹{artist['price_range']}")
            created_count += 1
        else:
            print(f"  ❌ Profile creation failed")
    
    print("\n" + "="*70)
    print(f"Created {created_count} artist profiles")
    print("="*70 + "\n")
    
    # Step 2: Auto-approve all pending artists
    print("⏳ Logging in as admin to approve artists...")
    admin_token = get_admin_token()
    
    if admin_token:
        print("✅ Admin logged in")
        print("⏳ Fetching pending artists...")
        
        pending = get_pending_artists(admin_token)
        print(f"✅ Found {len(pending)} pending artist(s)")
        
        if pending:
            print("\n⏳ Approving artists...")
            approved_count = 0
            
            for artist in pending:
                artist_name = artist.get('business_name', artist.get('user_id', 'Unknown'))
                if approve_artist(artist['_id'], admin_token):
                    print(f"  ✅ Approved: {artist_name}")
                    approved_count += 1
                else:
                    print(f"  ❌ Failed to approve: {artist_name}")
            
            print(f"\n✅ Approved {approved_count}/{len(pending)} artists")
        else:
            print("ℹ️  No pending artists to approve")
    else:
        print("❌ Admin login failed - artists remain pending")
    
    print("\n" + "="*70)
    print("✨ Seeding Complete!")
    print(f"📊 Total artists created: {created_count}")
    print("🌐 View them at: http://localhost:5000/artists")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
