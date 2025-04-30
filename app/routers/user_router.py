from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def register_user(user: UserCreate):
    user_dict = user.dict()
    user_id = user_service.create_user(user_dict)
    return {**user_dict, "id": user_id}

@router.get("/{user_id}", response_model=UserOut)
def fetch_user(user_id: str):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user: UserUpdate):
    print("DEBUG BODY RECEIVED:", user)
    updated = user_service.update_user(user_id, user.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated