"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, Token
from app.services.auth_service import AuthService

router = APIRouter()


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user and return JWT token."""
    service = AuthService(db)
    return await service.register(user_data)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login with email/password and return JWT token."""
    service = AuthService(db)
    return await service.login(form_data.username, form_data.password)


@router.post("/login/json", response_model=Token)
async def login_json(user_data: dict, db: AsyncSession = Depends(get_db)):
    """Login with JSON body (for frontend)."""
    service = AuthService(db)
    return await service.login(user_data["email"], user_data["password"])


@router.post("/forgot-password")
async def forgot_password(
    body: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send new password to user's email."""
    service = AuthService(db)
    await service.forgot_password(body.email)
    return {"message": "Если такой email зарегистрирован — новый пароль отправлен на почту"}
