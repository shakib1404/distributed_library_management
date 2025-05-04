from app.database import db
from bson import ObjectId
from datetime import datetime, timedelta

from app.services.book_service import BookService
from app.services.user_service import UserService

class LoanService:
    def __init__(self):
        self.book_service = BookService()
        self.user_service = UserService()

    @staticmethod
    def parse_loan_document(doc, include_extensions=False):
        result = {
            "id": str(doc["_id"]),
            "user_id": doc["user_id"],
            "book_id": doc["book_id"],
            "issue_date": doc["issue_date"],
            "due_date": doc["due_date"],
            "return_date": doc.get("return_date"),
            "status": doc["status"]
        }
        if include_extensions:
            result["extensions_count"] = doc.get("extensions_count", 0)
        return result

    def issue_book(self, data):
        data["issue_date"] = datetime.utcnow()
        data["status"] = "ACTIVE"
        data["extensions_count"] = 0
        result = db.loans.insert_one(data)
        self.book_service.decrement_available_copy(data["book_id"])
        loan = db.loans.find_one({"_id": result.inserted_id})
        return self.parse_loan_document(loan)

    def return_book(self, loan_id):
        db.loans.update_one(
            {"_id": ObjectId(loan_id)},
            {"$set": {"return_date": datetime.utcnow(), "status": "RETURNED"}}
        )
        loan = db.loans.find_one({"_id": ObjectId(loan_id)})
        self.book_service.increment_available_copy(loan["book_id"])
        return self.parse_loan_document(loan)

    def get_loan_by_id(self, loan_id):
        loan = db.loans.find_one({"_id": ObjectId(loan_id)})
        if loan:
            return self.parse_loan_document(loan)
        return None

    def get_loans_by_user(self, user_id):
        cursor = db.loans.find({"user_id": user_id})
        result = []
        for loan in cursor:
            book = self.book_service.get_book_summary(loan["book_id"])
            result.append({
                "id": str(loan["_id"]),
                "book": book,
                "issue_date": loan["issue_date"],
                "due_date": loan["due_date"],
                "return_date": loan.get("return_date"),
                "status": loan["status"]
            })
        return result

    def get_overdue_loans(self):
        today = datetime.utcnow()
        cursor = db.loans.find({"due_date": {"$lt": today}, "status": "ACTIVE"})
        result = []
        for loan in cursor:
            user = self.user_service.get_user_summary(loan["user_id"])
            book = self.book_service.get_book_summary(loan["book_id"])
            result.append({
                "id": str(loan["_id"]),
                "user": user,
                "book": book,
                "issue_date": loan["issue_date"],
                "due_date": loan["due_date"],
                "days_overdue": (today - loan["due_date"]).days
            })
        return result

    def extend_loan(self, loan_id: str, extension_days: int):
        loan = db.loans.find_one({"_id": ObjectId(loan_id)})
        if not loan:
            return None
        new_due_date = loan["due_date"] + timedelta(days=extension_days)
        updated = db.loans.find_one_and_update(
            {"_id": ObjectId(loan_id)},
            {"$set": {"due_date": new_due_date}, "$inc": {"extensions_count": 1}},
            return_document=True
        )
        return self.parse_loan_document(updated, include_extensions=True)

    def get_borrowed_books_pipeline(self):
        return [
            {"$group": {"_id": "$book_id", "borrow_count": {"$sum": 1}}},
            {"$sort": {"borrow_count": -1}},
            {"$limit": 10}
        ]

    def get_active_users_pipeline(self):
        return [
            {"$group": {"_id": "$user_id", "books_borrowed": {"$sum": 1}}},
            {"$sort": {"books_borrowed": -1}},
            {"$limit": 10}
        ]

    def aggregate_loans(self, pipeline):
        return db.loans.aggregate(pipeline)

    def count_active_loans(self, user_id=None):
        query = {"status": "ACTIVE"}
        if user_id:
            query["user_id"] = user_id
        return db.loans.count_documents(query)

   

    def count_overdue_loans(self):
     now = datetime.utcnow()
     return db.loans.count_documents({
        "due_date": {"$lt": now},
        "returned_at": None  # only those not returned
      })


    def count_loans_since(self, since_time):
        return db.loans.count_documents({"issue_date": {"$gte": since_time}})

    def count_returns_since(self, since_time):
        return db.loans.count_documents({"return_date": {"$gte": since_time}})
