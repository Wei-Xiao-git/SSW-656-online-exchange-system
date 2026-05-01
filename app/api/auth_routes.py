from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.services.auth_service import register_user, login_user
from app.models.login import LoginRequest
router = APIRouter()


@router.post("/register")
def register(user: User):
    try:
        return register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(request: LoginRequest):
    try:
        return login_user(
            request.username,
            request.password
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))