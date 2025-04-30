from app.database import db
from bson import ObjectId, errors
from datetime import datetime, timedelta

def get_most_borrowed_books():
    pipeline = [
        {"$group": {"_id": "$book_id", "borrow_count": {"$sum": 1}}},
        {"$sort": {"borrow_count": -1}},
        {"$limit": 10}
    ]
    results = db.loans.aggregate(pipeline)
    books = []
    for item in results:
        try:
            book = db.books.find_one({"_id": ObjectId(item["_id"])})
        except errors.InvalidId:
            continue
        if book:
            books.append({
                "book_id": str(book["_id"]),
                "title": book["title"],
                "author": book["author"],
                "borrow_count": item["borrow_count"]
            })
    return books

def get_most_active_users():
    pipeline = [
        {"$group": {"_id": "$user_id", "books_borrowed": {"$sum": 1}}},
        {"$sort": {"books_borrowed": -1}},
        {"$limit": 10}
    ]
    results = db.loans.aggregate(pipeline)
    users = []
    for item in results:
        try:
            user = db.users.find_one({"_id": ObjectId(item["_id"])})
        except errors.InvalidId:
            continue
        if user:
            current_borrows = db.loans.count_documents({"user_id": item["_id"], "status": "ACTIVE"})
            users.append({
                "user_id": str(user["_id"]),
                "name": user["name"],
                "books_borrowed": item["books_borrowed"],
                "current_borrows": current_borrows
            })
    return users

def get_system_overview():
    available_agg = db.books.aggregate([{"$group": {"_id": None, "sum": {"$sum": "$available_copies"}}}])
    try:
        available_sum = next(available_agg)["sum"]
    except StopIteration:
        available_sum = 0

    return {
        "total_books": db.books.count_documents({}),
        "total_users": db.users.count_documents({}),
        "books_available": available_sum,
        "books_borrowed": db.loans.count_documents({"status": "ACTIVE"}),
        "overdue_loans": db.loans.count_documents({"due_date": {"$lt": datetime.utcnow()}, "status": "ACTIVE"}),
        "loans_today": db.loans.count_documents({"issue_date": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)}}),
        "returns_today": db.loans.count_documents({"return_date": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)}})
    }
