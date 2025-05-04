from fastapi import APIRouter
from app.services.stats_service import StatisticsService

router = APIRouter(prefix="/api/stats", tags=["Statistics"])
stats_service = StatisticsService()

@router.get("/books/popular")
def get_popular_books():
    return stats_service.get_most_borrowed_books()

@router.get("/users/active")
def get_active_users():
    return stats_service.get_most_active_users()

@router.get("/overview")
def get_system_overview():
    return stats_service.get_system_overview()
