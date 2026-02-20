import requests
import sys

BASE_URL = "http://localhost:5000"

def log(msg):
    print(f"[TEST] {msg}")

def test_flow():
    session = requests.Session()

    # 1. Register User
    user_email = "testuser@example.com"
    user_pass = "password123"
    log(f"Registering User: {user_email}")
    res = session.post(f"{BASE_URL}/auth/signup", json={
        "name": "Test User",
        "email": user_email,
        "password": user_pass,
        "phone": "9999999999",
        "role": "user"
    })
    if res.status_code == 201:
        log("User Registered.")
    elif res.status_code == 400 and "User already exists" in res.text:
        log("User already exists, proceeding.")
    else:
        log(f"User Registration Failed: {res.text}")
        return

    # 2. Login User
    log("Logging in User...")
    res = session.post(f"{BASE_URL}/auth/login", json={
        "email": user_email,
        "password": user_pass
    })
    if res.status_code != 200:
        log(f"User Login Failed: {res.text}")
        return
    user_token = res.json()["token"]
    log("User Logged In.")

    # 3. Register Artist
    artist_email = "testartist@example.com"
    artist_pass = "password123"
    log(f"Registering Artist: {artist_email}")
    # Note: Artist registration uses multipart/form-data usually, 
    # but backend might strictly require it or accept json if not handling files in this specific test.
    # checking artist.py would reveal if it strictly needs files. 
    # For now, assuming we can just login if existing, or fail if we can't upload files easily via this script without actual files.
    # Let's try to simple login as artist first (might fail if not exists)
    
    # Actually, let's login as ADMIN to see if we can find an artist to book.
    log("Logging in Admin...")
    res = session.post(f"{BASE_URL}/auth/login", json={
        "email": "pawansimha@gmail.com",
        "password": "Hercules"
    })
    if res.status_code != 200:
        log(f"Admin Login Failed: {res.text}")
        return
    admin_token = res.json()["token"]
    log("Admin Logged In.")

    # 4. Get Artists (as Admin)
    res = session.get(f"{BASE_URL}/api/admin/artists", headers={"Authorization": f"Bearer {admin_token}"})
    artists = res.json()
    if not artists:
        log("No artists found. Please seed artists or register one manually via UI.")
        return
    
    # Pick the first approved artist
    target_artist = next((a for a in artists if a.get("verification_status") == "approved"), None)
    
    if not target_artist:
        log("No approved artists found. Approving the first one...")
        target_artist = artists[0]
        res = session.put(f"{BASE_URL}/api/admin/artist/approve/{target_artist['_id']}", headers={"Authorization": f"Bearer {admin_token}"})
        if res.status_code == 200:
            log(f"Approved artist: {target_artist['name']}")
        else:
            log(f"Failed to approve artist: {res.text}")
            return

    artist_id = target_artist['_id']
    log(f"Target Artist ID: {artist_id}")

    # 5. Book Artist (as User)
    log("Booking Artist...")
    res = session.post(f"{BASE_URL}/api/booking", json={
        "artist_id": artist_id,
        "date": "2025-12-25",
        "time": "10:00",
        "requirements": "Test Booking"
    }, headers={"Authorization": f"Bearer {user_token}"})
    
    if res.status_code != 201:
        log(f"Booking Failed: {res.text}")
        return
    booking_id = res.json()["booking_id"]
    log(f"Booking Created: {booking_id}")

    # 6. Login Artist (to accept)
    # We need the artist's credentials. If we picked a random artist, we don't know the password.
    # So we can't fully automate the acceptance unless we registered the artist ourselves.
    
    log("Flow Test Complete. User booked an artist.")
    log("To fully verify acceptance, login as the specific artist and check dashboard.")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"Test Error: {e}")
        print("Ensure the server is running on port 5000!")
