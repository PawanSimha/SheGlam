from datetime import datetime

def artist_document(data):
    return {
        "user_id": data["user_id"],
        "experience_years": data["experience_years"],
        "specialization": data["specialization"],
        "location": data["location"],
        "price_range": data["price_range"],

        "certificate_file": data["certificate_file"],
        "certificate_link": data["certificate_link"],

        "govt_id_type": data["govt_id_type"],
        "govt_id_file": data["govt_id_file"],

        "verification_status": "pending",
        "rating": 0,
        "total_services": 0,

        "created_at": datetime.utcnow()
    }

def booking_document(data):
    return {
        "user_id": data["user_id"],
        "artist_id": data["artist_id"],
        "date": data["date"],
        "time": data["time"],
        "requirements": data["requirements"],
        "status": "requested"
    }


def review_document(data):
    return {
        "user_id": data["user_id"],
        "artist_id": data["artist_id"],
        "booking_id": data["booking_id"],
        "rating": int(data["rating"]),   # 1 to 5
        "comment": data["comment"],
        "created_at": datetime.utcnow()
    }
