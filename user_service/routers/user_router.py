from fastapi import APIRouter, HTTPException
from schemas.user_schema import UserCreate, UserOut, UserUpdate
from services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["Users"])
user_service = UserService()

@router.post("/", response_model=UserOut)
def create(user: UserCreate):
    return user_service.create_user(user.dict())


@router.get("/{user_id}", response_model=UserOut)
def fetch_user(user_id: str):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user: UserUpdate):
    updated = user_service.update_user(user_id, user.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
