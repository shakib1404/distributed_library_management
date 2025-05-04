from app.database import db
from bson import ObjectId, errors
from datetime import datetime

class BookService:
    def create_book(self, data):
        data["available_copies"] = data.get("copies", 0)
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = db.books.insert_one(data)
        return str(result.inserted_id)

    def get_book(self, book_id):
        book = db.books.find_one({"_id": ObjectId(book_id)})
        if book:
            book["id"] = str(book["_id"])
            del book["_id"]
            return book
        return None

    def update_book(self, book_id, updates):
        updates["updated_at"] = datetime.utcnow()
        db.books.update_one({"_id": ObjectId(book_id)}, {"$set": updates})
        return self.get_book(book_id)

    def delete_book(self, book_id):
        db.books.delete_one({"_id": ObjectId(book_id)})

    def search_books(self, query):
        cursor = db.books.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}},
                {"isbn": {"$regex": query, "$options": "i"}},
            ]
        })
        result = []
        for book in cursor:
            book["id"] = str(book["_id"])
            del book["_id"]
            result.append(book)
        return result

    def decrement_available_copy(self, book_id):
        return db.books.update_one(
            {"_id": ObjectId(book_id), "available_copies": {"$gt": 0}},
            {"$inc": {"available_copies": -1}}
        )

    def increment_available_copy(self, book_id):
        return db.books.update_one(
            {"_id": ObjectId(book_id)},
            {"$inc": {"available_copies": 1}}
        )

    def get_book_summary(self, book_id):
        try:
            object_id = ObjectId(book_id)
        except errors.InvalidId:
            return None

        book = db.books.find_one({"_id": object_id}, {"title": 1, "author": 1})
        if not book:
            return None
        return {
            "id": str(book["_id"]),
            "title": book.get("title", ""),
            "author": book.get("author", "")
        }

    def count_books(self):
        return db.books.count_documents({})

    def count_available_books(self):
        agg = db.books.aggregate([{"$group": {"_id": None, "sum": {"$sum": "$available_copies"}}}])
        try:
            return next(agg)["sum"]
        except StopIteration:
            return 0
