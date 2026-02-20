"""
SheGlam API Test Suite
Comprehensive testing for all backend endpoints
"""
import requests
import json
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"
AUTH_BASE = f"{BASE_URL}/auth"

# Test data
test_user = {
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "password123",
    "phone": "1234567890",
    "role": "user"
}

test_artist = {
    "name": "Test Artist",
    "email": "testartist@example.com",
    "password": "password123",
    "phone": "9876543210",
    "role": "artist"
}

admin_credentials = {
    "email": "pawansimha@gmail.com",
    "password": "Hercules"
}

# Tokens storage
tokens = {
    "user": None,
    "artist": None,
    "admin": None
}

# Created IDs
created_ids = {
    "user_id": None,
    "artist_id": None,
    "booking_id": None
}

def headers(token=None):
    """Generate headers with optional JWT token"""
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def print_test(name, passed, message=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if message:
        print(f"   {message}")

def test_health():
    """Test health check endpoint"""
    try:
        resp = requests.get(f"{API_BASE}/health")
        print_test("Health Check", resp.status_code == 200, f"Status: {resp.status_code}")
        return resp.status_code == 200
    except Exception as e:
        print_test("Health Check", False, str(e))
        return False

def test_user_signup():
    """Test user registration"""
    try:
        resp = requests.post(f"{AUTH_BASE}/signup", json=test_user, headers=headers())
        success = resp.status_code == 201
        print_test("User Signup", success, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("User Signup", False, str(e))
        return False

def test_artist_signup():
    """Test artist registration"""
    try:
        resp = requests.post(f"{AUTH_BASE}/signup", json=test_artist, headers=headers())
        success = resp.status_code == 201
        print_test("Artist Signup", success, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("Artist Signup", False, str(e))
        return False

def test_user_login():
    """Test user login"""
    try:
        resp = requests.post(f"{AUTH_BASE}/login", 
            json={"email": test_user["email"], "password": test_user["password"]},
            headers=headers())
        success = resp.status_code == 200
        if success:
            data = resp.json()
            tokens["user"] = data.get("token")
            print_test("User Login", True, f"Token: {tokens['user'][:20]}...")
        else:
            print_test("User Login", False, f"Status: {resp.status_code}")
        return success
    except Exception as e:
        print_test("User Login", False, str(e))
        return False

def test_artist_login():
    """Test artist login"""
    try:
        resp = requests.post(f"{AUTH_BASE}/login",
            json={"email": test_artist["email"], "password": test_artist["password"]},
            headers=headers())
        success = resp.status_code == 200
        if success:
            data = resp.json()
            tokens["artist"] = data.get("token")
            print_test("Artist Login", True, f"Token: {tokens['artist'][:20]}...")
        else:
            print_test("Artist Login", False, f"Status: {resp.status_code}")
        return success
    except Exception as e:
        print_test("Artist Login", False, str(e))
        return False

def test_admin_login():
    """Test admin login with hardcoded credentials"""
    try:
        resp = requests.post(f"{AUTH_BASE}/login", json=admin_credentials, headers=headers())
        success = resp.status_code == 200
        if success:
            data = resp.json()
            tokens["admin"] = data.get("token")
            print_test("Admin Login", True, f"Email: {admin_credentials['email']}, Token received")
        else:
            print_test("Admin Login", False, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("Admin Login", False, str(e))
        return False

def test_artist_registration():
    """Test artist profile registration with file uploads"""
    try:
        # Create dummy files for testing
        cert_path = Path("test_certificate.jpg")
        govt_path = Path("test_govt_id.jpg")
        
        # Create minimal JPG files (valid header)
        jpeg_header = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        cert_path.write_bytes(jpeg_header + b'\x00' * 100)
        govt_path.write_bytes(jpeg_header + b'\x00' * 100)
        
        files = {
            'certificate': ('test_cert.jpg', open(cert_path, 'rb'), 'image/jpeg'),
            'govt_id': ('test_id.jpg', open(govt_path, 'rb'), 'image/jpeg')
        }
        
        data = {
            'experience_years': '5',
            'specialization': 'Bridal, Party',
            'location': 'Bangalore',
            'price_range': '1000-5000',
            'certificate_link': 'https://example.com/cert',
            'govt_id_type': 'Aadhaar'
        }
        
        h = {"Authorization": f"Bearer {tokens['artist']}"}
        resp = requests.post(f"{API_BASE}/artist/register", data=data, files=files, headers=h)
        
        # Close files
        for f in files.values():
            f[1].close()
        
        # Cleanup
        cert_path.unlink()
        govt_path.unlink()
        
        success = resp.status_code == 201
        print_test("Artist Profile Registration", success, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("Artist Profile Registration", False, str(e))
        return False

def test_get_pending_artists():
    """Test getting pending artist verifications (admin only)"""
    try:
        resp = requests.get(f"{API_BASE}/admin/artists/pending", headers=headers(tokens["admin"]))
        success = resp.status_code == 200
        if success:
            data = resp.json()
            if data and len(data) > 0:
                created_ids["artist_id"] = data[0]["_id"]
                print_test("Get Pending Artists", True, f"Found {len(data)} pending artist(s)")
            else:
                print_test("Get Pending Artists", True, "No pending artists")
        else:
            print_test("Get Pending Artists", False, f"Status: {resp.status_code}")
        return success
    except Exception as e:
        print_test("Get Pending Artists", False, str(e))
        return False

def test_approve_artist():
    """Test approving an artist (admin only)"""
    if not created_ids["artist_id"]:
        print_test("Approve Artist", False, "No artist ID to approve")
        return False
    
    try:
        resp = requests.put(
            f"{API_BASE}/admin/artist/approve/{created_ids['artist_id']}",
            headers=headers(tokens["admin"])
        )
        success = resp.status_code == 200
        print_test("Approve Artist", success, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("Approve Artist", False, str(e))
        return False

def test_get_approved_artists():
    """Test getting list of approved artists (public)"""
    try:
        resp = requests.get(f"{API_BASE}/artists", headers=headers())
        success = resp.status_code == 200
        if success:
            data = resp.json()
            print_test("Get Approved Artists", True, f"Found {len(data)} approved artist(s)")
        else:
            print_test("Get Approved Artists", False, f"Status: {resp.status_code}")
        return success
    except Exception as e:
        print_test("Get Approved Artists", False, str(e))
        return False

def test_create_booking():
    """Test creating a booking (user only)"""
    if not created_ids["artist_id"]:
        print_test("Create Booking", False, "No artist ID to book")
        return False
    
    try:
        booking_data = {
            "artist_id": created_ids["artist_id"],
            "date": "2026-03-15",
            "time": "14:00",
            "requirements": "Bridal makeup for wedding"
        }
        resp = requests.post(f"{API_BASE}/booking", json=booking_data, headers=headers(tokens["user"]))
        success = resp.status_code == 201
        if success:
            data = resp.json()
            created_ids["booking_id"] = data.get("booking_id")
            print_test("Create Booking", True, f"Booking ID: {created_ids['booking_id']}")
        else:
            print_test("Create Booking", False, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("Create Booking", False, str(e))
        return False

def test_get_user_bookings():
    """Test getting user's bookings"""
    try:
        resp = requests.get(f"{API_BASE}/bookings", headers=headers(tokens["user"]))
        success = resp.status_code == 200
        if success:
            data = resp.json()
            print_test("Get User Bookings", True, f"Found {len(data)} booking(s)")
        else:
            print_test("Get User Bookings", False, f"Status: {resp.status_code}")
        return success
    except Exception as e:
        print_test("Get User Bookings", False, str(e))
        return False

def test_get_artist_bookings():
    """Test getting artist's bookings"""
    try:
        resp = requests.get(f"{API_BASE}/bookings", headers=headers(tokens["artist"]))
        success = resp.status_code == 200
        if success:
            data = resp.json()
            print_test("Get Artist Bookings", True, f"Found {len(data)} booking(s)")
        else:
            print_test("Get Artist Bookings", False, f"Status: {resp.status_code}")
        return success
    except Exception as e:
        print_test("Get Artist Bookings", False, str(e))
        return False

def test_accept_booking():
    """Test artist accepting a booking"""
    if not created_ids["booking_id"]:
        print_test("Accept Booking", False, "No booking ID to accept")
        return False
    
    try:
        resp = requests.put(
            f"{API_BASE}/booking/{created_ids['booking_id']}/status",
            json={"status": "accepted"},
            headers=headers(tokens["artist"])
        )
        success = resp.status_code == 200
        print_test("Accept Booking", success, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("Accept Booking", False, str(e))
        return False

def test_complete_booking():
    """Test artist completing a booking"""
    if not created_ids["booking_id"]:
        print_test("Complete Booking", False, "No booking ID to complete")
        return False
    
    try:
        resp = requests.put(
            f"{API_BASE}/booking/{created_ids['booking_id']}/status",
            json={"status": "completed"},
            headers=headers(tokens["artist"])
        )
        success = resp.status_code == 200
        print_test("Complete Booking", success, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("Complete Booking", False, str(e))
        return False

def test_submit_review():
    """Test user submitting a review"""
    if not created_ids["booking_id"]:
        print_test("Submit Review", False, "No booking ID to review")
        return False
    
    try:
        review_data = {
            "booking_id": created_ids["booking_id"],
            "rating": 5,
            "comment": "Excellent service! Highly recommended."
        }
        resp = requests.post(f"{API_BASE}/review", json=review_data, headers=headers(tokens["user"]))
        success = resp.status_code == 201
        print_test("Submit Review", success, f"Status: {resp.status_code}, Response: {resp.json()}")
        return success
    except Exception as e:
        print_test("Submit Review", False, str(e))
        return False

def test_unauthorized_access():
    """Test that users cannot access admin endpoints"""
    try:
        resp = requests.get(f"{API_BASE}/admin/users", headers=headers(tokens["user"]))
        success = resp.status_code == 403
        print_test("Unauthorized Access Prevention", success, f"Status: {resp.status_code} (should be 403)")
        return success
    except Exception as e:
        print_test("Unauthorized Access Prevention", False, str(e))
        return False

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*60)
    print("SheGlam API Test Suite")
    print("="*60 + "\n")
    
    tests = [
        ("Health Check", test_health),
        ("User Signup", test_user_signup),
        ("Artist Signup", test_artist_signup),
        ("User Login", test_user_login),
        ("Artist Login", test_artist_login),
        ("Admin Login", test_admin_login),
        ("Artist Profile Registration", test_artist_registration),
        ("Get Pending Artists", test_get_pending_artists),
        ("Approve Artist", test_approve_artist),
        ("Get Approved Artists", test_get_approved_artists),
        ("Create Booking", test_create_booking),
        ("Get User Bookings", test_get_user_bookings),
        ("Get Artist Bookings", test_get_artist_bookings),
        ("Accept Booking", test_accept_booking),
        ("Complete Booking", test_complete_booking),
        ("Submit Review", test_submit_review),
        ("Unauthorized Access", test_unauthorized_access),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n--- Testing: {name} ---")
        if test_func():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*60 + "\n")
    
    return passed, failed

if __name__ == "__main__":
    run_all_tests()
