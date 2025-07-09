from database import db
from bson import ObjectId, errors
from datetime import datetime

class UserService:
    def create_user(self, user_data):
        created_time = datetime.utcnow().isoformat()
        user_data["created_at"] = created_time
        user_data["updated_at"] = None
        res = db.users.insert_one(user_data)
        return {
            "id": str(res.inserted_id),
            "name": user_data["name"],
            "email": user_data["email"],
            "role": user_data["role"],
            "created_at": created_time,
            "updated_at": None
        }

    def get_user(self, user_id):
     user = db.users.find_one({"_id": ObjectId(user_id)})
     if user:
        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "created_at": str(user.get("created_at", datetime.utcnow().isoformat())),
            "updated_at": str(user.get("updated_at", None)) if user.get("updated_at") else None
        }
     return None

    def update_user(self, user_id, updates):
        updates["updated_at"] = datetime.utcnow().isoformat()
        db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})
        return self.get_user(user_id)

    def get_user_summary(self, user_id: str):
        try:
            object_id = ObjectId(user_id)
        except errors.InvalidId:
            return None  # Or raise HTTPException

        user = db.users.find_one({"_id": object_id}, {"name": 1, "email": 1})
        if not user:
            return None
        return {
            "id": str(user["_id"]),
            "name": user.get("name", ""),
            "email": user.get("email", "")
        }

    def count_users(self):
        return db.users.count_documents({})
