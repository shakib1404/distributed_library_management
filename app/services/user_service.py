from app.database import db
from bson import ObjectId, errors

class UserService:
    def create_user(self, user_data: dict):
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)

    def get_user(self, user_id: str):
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
                del user["_id"]
                return user
            return None
        except Exception:
            return None

    def update_user(self, user_id: str, updates: dict):
        try:
            result = db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": updates}
            )
            if result.matched_count == 0:
                return None
            return self.get_user(user_id)
        except Exception:
            return None

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
