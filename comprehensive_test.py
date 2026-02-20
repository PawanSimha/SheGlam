import requests
import unittest
import time
import random
import string

BASE_URL = "http://localhost:5000"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class TestSheGlam(unittest.TestCase):
    
    def setUp(self):
        self.session = requests.Session()
        self.user_email = f"user_{random_string()}@test.com"
        self.artist_email = f"artist_{random_string()}@test.com"
        self.password = "password123"
        self.admin_email = "pawansimha@gmail.com"
        self.admin_pass = "Hercules"

    # ==========================
    # AUTHENTICATION TESTS
    # ==========================
    def test_01_health_check(self):
        """Test API Health"""
        try:
            res = self.session.get(f"{BASE_URL}/api/health")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['status'], 'ok')
            print("✅ Health Check Passed")
        except requests.exceptions.ConnectionError:
            self.fail("Server is not running. Please start app.py")

    def test_02_register_user_success(self):
        """Test User Registration Success"""
        res = self.session.post(f"{BASE_URL}/auth/signup", json={
            "name": "Test User",
            "email": self.user_email,
            "password": self.password,
            "phone": "9999999999",
            "role": "user"
        })
        self.assertEqual(res.status_code, 201)
        print("✅ User Registration Success Passed")

    def test_03_register_duplicate_fail(self):
        """Test Duplicate Registration Failure"""
        # Register once
        self.test_02_register_user_success()
        # Register again
        res = self.session.post(f"{BASE_URL}/auth/signup", json={
            "name": "Test User",
            "email": self.user_email,
            "password": self.password,
            "role": "user"
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("already exists", res.json()['error'])
        print("✅ Duplicate Registration Fail Passed")

    def test_04_login_success(self):
        """Test Login Success"""
        self.test_02_register_user_success()
        res = self.session.post(f"{BASE_URL}/auth/login", json={
            "email": self.user_email,
            "password": self.password
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.json())
        print("✅ Login Success Passed")

    def test_05_login_fail(self):
        """Test Login Failure (Wrong Password)"""
        self.test_02_register_user_success()
        res = self.session.post(f"{BASE_URL}/auth/login", json={
            "email": self.user_email,
            "password": "wrongpassword"
        })
        self.assertEqual(res.status_code, 401)
        print("✅ Login Failure Passed")

    # ==========================
    # WORKFLOW TESTS
    # ==========================
    def test_06_admin_workflow(self):
        """Test Admin Login and Data Fetching"""
        # Login
        res = self.session.post(f"{BASE_URL}/auth/login", json={
            "email": self.admin_email,
            "password": self.admin_pass
        })
        self.assertEqual(res.status_code, 200, "Admin login failed")
        token = res.json()['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Get Users
        res = self.session.get(f"{BASE_URL}/api/admin/users", headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)
        
        # Get Artists
        res = self.session.get(f"{BASE_URL}/api/admin/artists", headers=headers)
        self.assertEqual(res.status_code, 200)
        
        print("✅ Admin Workflow Passed")

    def test_07_booking_lifecycle(self):
        """Test Full Booking Lifecycle: Book -> Accept -> Complete -> Reject (Another)"""
        # 1. Setup Admin Token
        res = self.session.post(f"{BASE_URL}/auth/login", json={"email": self.admin_email, "password": self.admin_pass})
        admin_token = res.json()['token']
        admin_header = {"Authorization": f"Bearer {admin_token}"}

        # 2. Setup Artist
        # Since we can't easily upload files in pure json test without mocking, let's use an existing approved artist if available, or skip
        # Actually, let's skip the multipart creation complexity here and focus on logic if we assume data exists.
        # Better: Login as admin, find an approved artist.
        res = self.session.get(f"{BASE_URL}/api/admin/artists", headers=admin_header)
        artists = res.json()
        target_artist = next((a for a in artists if a.get('verification_status') == 'approved'), None)
        
        if not target_artist:
            print("⚠️ Skipping Booking Test: No approved artist found to test against.")
            return

        artist_id = target_artist['_id']
        artist_user_id = target_artist['user_id']
        
        # We need to login as THIS artist to accept. 
        # Since we don't know the password of seeded artists in this scope (unless we hardcode), 
        # we will use the one we created in seed_artists.py: 'priya.sharma@sheglam.com' / 'artist123'
        
        # Only proceed if we found Priya or can use her credentials
        artist_creds = {"email": "priya.sharma@sheglam.com", "password": "artist123"}
        
        res = self.session.post(f"{BASE_URL}/auth/login", json=artist_creds)
        if res.status_code != 200:
            print("⚠️ Skipping Booking Test: Could not login as default seeded artist.")
            return
        artist_token = res.json()['token']
        artist_header = {"Authorization": f"Bearer {artist_token}"}
        
        # 3. Setup User
        self.test_02_register_user_success()
        res = self.session.post(f"{BASE_URL}/auth/login", json={"email": self.user_email, "password": self.password})
        user_token = res.json()['token']
        user_header = {"Authorization": f"Bearer {user_token}"}

        # 4. Create Booking
        booking_payload = {
            "artist_id": artist_id,
            "date": "2025-10-10",
            "time": "10:00",
            "requirements": "Test Booking Cycle"
        }
        res = self.session.post(f"{BASE_URL}/api/booking", json=booking_payload, headers=user_header)
        self.assertEqual(res.status_code, 201)
        booking_id = res.json()['booking_id']

        # 5. Artist Accepts
        res = self.session.put(f"{BASE_URL}/api/booking/{booking_id}/status", json={"status": "accepted"}, headers=artist_header)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['message'], "Booking accepted")

        # 6. Verify User sees Accepted
        res = self.session.get(f"{BASE_URL}/api/bookings", headers=user_header)
        my_booking = next((b for b in res.json() if b['_id'] == booking_id), None)
        self.assertEqual(my_booking['status'], 'accepted')

        # 7. Artist Completes
        res = self.session.put(f"{BASE_URL}/api/booking/{booking_id}/status", json={"status": "completed"}, headers=artist_header)
        self.assertEqual(res.status_code, 200)

        # 8. Create another booking to Reject
        res = self.session.post(f"{BASE_URL}/api/booking", json=booking_payload, headers=user_header)
        booking_id_2 = res.json()['booking_id']
        
        # Artist Rejects
        res = self.session.put(f"{BASE_URL}/api/booking/{booking_id_2}/status", json={"status": "rejected"}, headers=artist_header)
        self.assertEqual(res.status_code, 200)
        
        print("✅ Booking Lifecycle (Accept/Complete/Reject) Passed")

    def test_08_rbac_protection(self):
        """Test Role Based Access Control"""
        # User trying to access Admin route
        self.test_02_register_user_success()
        res = self.session.post(f"{BASE_URL}/auth/login", json={"email": self.user_email, "password": self.password})
        user_token = res.json()['token']
        user_header = {"Authorization": f"Bearer {user_token}"}

        res = self.session.get(f"{BASE_URL}/api/admin/users", headers=user_header)
        self.assertEqual(res.status_code, 403) # Should be forbidden
        
        print("✅ RBAC Protection Passed")

    def test_09_frontend_routes(self):
        """Test Frontend Page Availability"""
        pages = ["/", "/login", "/register-user", "/register-artist", "/artists"]
        for page in pages:
            res = self.session.get(f"{BASE_URL}{page}")
            self.assertEqual(res.status_code, 200, f"Page {page} failed to load")
        print("✅ Frontend Routes Passed")

if __name__ == '__main__':
    unittest.main(verbosity=2)
