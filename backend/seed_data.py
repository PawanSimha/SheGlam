"""
Seed script: 10 approved artists and 5 normal users for testing.
Run from backend directory: python seed_data.py
"""
from datetime import datetime

import bcrypt
from pymongo import MongoClient

from config import MONGODB_URI, MONGODB_DB_NAME, INDIAN_CITIES

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]
users_collection = db["users"]
artists_collection = db["artists"]

# Do not overwrite admin
ADMIN_EMAIL = "pawansimha@gmail.com"


def _hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def seed():
    password = "Test@123"
    cities = [c for c in INDIAN_CITIES if c != "Other"][:15]
    specializations = [
        ["Bridal", "Party"],
        ["Bridal", "Engagement"],
        ["Party", "Festival"],
        ["Bridal"],
        ["Party", "Corporate"],
        ["Bridal", "Party", "Editorial"],
        ["Party"],
        ["Bridal", "Engagement", "Party"],
        ["Corporate", "Party"],
        ["Bridal", "Party"],
    ]
    # Targeted cities from user request
    target_cities = ["Bangalore", "Mumbai", "Chennai", "Thiruvananthapuram", "Hyderabad", "Telangana", "Delhi", "Kochi", "Pune", "Kolkata"]
    
    # Realistic names
    names = [
        "Aarav Sharma", "Diya Patel", "Ishaan Gupta", "Ananya Singh", "Vihaan Kumar",
        "Aditi Verma", "Arjun Reddy", "Kavya Nair", "Rohan Iyer", "Meera Joshi",
        "Saanvi Malhotra", "Aryan Das", "Priya Rao", "Kabir Mehta", "Riya Jain",
        "Vivaan Choudhury", "Nisha Saxena", "Aditya Mishra", "Pooja Hegde", "Rahul Krishnan"
    ]
    
    cities_len = len(target_cities)
    
    # Create 20 artists
    for i in range(20):
        email = f"artist{i+1}@sheglam.com"
        name = names[i] if i < len(names) else f"Artist {i+1}"
        
        # 1. Create User
        if not users_collection.find_one({"email": email}):
            users_collection.insert_one({
                "name": name,
                "email": email,
                "password_hash": _hash(password),
                "role": "artist",
                "phone": f"98765{i:05d}",
                "created_at": datetime.utcnow(),
            })
            print(f"Created user: {name} ({email})")
            
        # 2. Create Artist Profile
        if artists_collection.find_one({"user_id": email}):
            continue
            
        city = target_cities[i % cities_len]
        rating = round(3.0 + (i % 20) * 0.1 + (0.5 if i % 3 == 0 else 0), 1) # Randomish rating 3.0 - 5.0
        if rating > 5.0: rating = 5.0
        
        artists_collection.insert_one({
            "user_id": email,
            "business_name": name + " Makeovers",
            "experience_years": (i % 10) + 1,
            "specialization": specializations[i % len(specializations)],
            "location": city,
            "price_range": f"₹{2000 + i*500} - ₹{5000 + i*1000}",
            "certificate_file": "seed_cert.jpg",
            "certificate_link": "",
            "govt_id_type": "Aadhaar",
            "govt_id_file": "seed_id.jpg",
            "verification_status": "approved",
            "rating": rating,
            "total_services": i * 5,
            "created_at": datetime.utcnow(),
        })
        print(f"Created artist profile: {name} in {city} (Rating: {rating})")
        print("Created artist profile:", email, "in", city)

    print("Seed done. User/artist password:", password)


if __name__ == "__main__":
    seed()
