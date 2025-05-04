from app.database import db
from bson import ObjectId
from datetime import datetime

def create_book(data):
    data["available_copies"] = data.get("copies", 0)
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    result = db.books.insert_one(data)
    return str(result.inserted_id)

def get_book(book_id):
    book = db.books.find_one({"_id": ObjectId(book_id)})
    if book:
        book["id"] = str(book["_id"])
        del book["_id"]
        return book
    return None

def update_book(book_id, updates):
    updates["updated_at"] = datetime.utcnow()
    db.books.update_one({"_id": ObjectId(book_id)}, {"$set": updates})
    book = db.books.find_one({"_id": ObjectId(book_id)})
    if book:
        book["id"] = str(book["_id"])
        del book["_id"]
        return {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "isbn": book["isbn"],
            "copies": book["copies"],
            "available_copies": book["available_copies"],
            "created_at": book["created_at"].isoformat() + "Z",
            "updated_at": book["updated_at"].isoformat() + "Z"
        }
    return None


def delete_book(book_id):
    db.books.delete_one({"_id": ObjectId(book_id)})


def search_books(query):
    cursor = db.books.find({"$or": [
        {"title": {"$regex": query, "$options": "i"}},
        {"author": {"$regex": query, "$options": "i"}},
        {"isbn": {"$regex": query, "$options": "i"}},
    ]})
    result = []
    for book in cursor:
        book["id"] = str(book["_id"])
        del book["_id"]
        result.append(book)
    return result


