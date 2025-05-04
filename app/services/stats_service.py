from datetime import datetime
from bson import ObjectId

from app.services.book_service import BookService
from app.services.user_service import UserService
from app.services.loan_service import LoanService

class StatisticsService:
    def __init__(self):
        self.book_service = BookService()
        self.user_service = UserService()
        self.loan_service = LoanService()

    def get_most_borrowed_books(self):
        pipeline = self.loan_service.get_borrowed_books_pipeline()
        results = self.loan_service.aggregate_loans(pipeline)
        books = []
        for item in results:
            book = self.book_service.get_book_summary(item["_id"])
            if book:
                books.append({
                    "book_id": book["id"],
                    "title": book["title"],
                    "author": book["author"],
                    "borrow_count": item["borrow_count"]
                })
        return books

    def get_most_active_users(self):
        pipeline = self.loan_service.get_active_users_pipeline()
        results = self.loan_service.aggregate_loans(pipeline)
        users = []
        for item in results:
            user = self.user_service.get_user_summary(item["_id"])
            if user:
                current_borrows = self.loan_service.count_active_loans(item["_id"])
                users.append({
                    "user_id": user["id"],
                    "name": user["name"],
                    "books_borrowed": item["books_borrowed"],
                    "current_borrows": current_borrows
                })
        return users

    def get_system_overview(self):
        available_sum = self.book_service.count_available_books()
        books_borrowed = self.loan_service.count_active_loans()
        total_books = available_sum + books_borrowed  # ✅ total = available + borrowed

        total_users = self.user_service.count_users()
        overdue = self.loan_service.count_overdue_loans()  # ✅ only those not returned

        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        loans_today = self.loan_service.count_loans_since(today_start)
        returns_today = self.loan_service.count_returns_since(today_start)

        return {
            "total_books": total_books,
            "total_users": total_users,
            "books_available": available_sum,
            "books_borrowed": books_borrowed,
            "overdue_loans": overdue,
            "loans_today": loans_today,
            "returns_today": returns_today
        }
