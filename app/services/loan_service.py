
from app.database import db
from bson import ObjectId
from datetime import datetime, timedelta

class LoanService:
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
        db.books.update_one(
            {"_id": ObjectId(data["book_id"]), "available_copies": {"$gt": 0}},
            {"$inc": {"available_copies": -1}}
        )
        loan = db.loans.find_one({"_id": result.inserted_id})
        return self.parse_loan_document(loan)

    def return_book(self, loan_id):
        db.loans.update_one(
            {"_id": ObjectId(loan_id)},
            {"$set": {"return_date": datetime.utcnow(), "status": "RETURNED"}}
        )
        loan = db.loans.find_one({"_id": ObjectId(loan_id)})
        db.books.update_one(
            {"_id": ObjectId(loan["book_id"])},
            {"$inc": {"available_copies": 1}}
        )
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
            book = db.books.find_one({"_id": ObjectId(loan["book_id"])})
            result.append({
                "id": str(loan["_id"]),
                "book": {
                    "id": str(book["_id"]),
                    "title": book["title"],
                    "author": book["author"]
                },
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
            user = db.users.find_one({"_id": ObjectId(loan["user_id"])})
            book = db.books.find_one({"_id": ObjectId(loan["book_id"])})
            result.append({
                "id": str(loan["_id"]),
                "user": {
                    "id": str(user["_id"]),
                    "name": user["name"],
                    "email": user["email"]
                },
                "book": {
                    "id": str(book["_id"]),
                    "title": book["title"],
                    "author": book["author"]
                },
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
