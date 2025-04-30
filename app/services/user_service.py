from app.database import db
from bson import ObjectId

def create_user(user_data: dict):
    result = db.users.insert_one(user_data)
    return str(result.inserted_id)

def get_user(user_id: str):
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
            return user
        return None
    except Exception:
        return None

def update_user(user_id: str, updates: dict):
    try:
        result = db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updates}
        )
        if result.matched_count == 0:
            return None
        return get_user(user_id)
    except Exception:
        return None