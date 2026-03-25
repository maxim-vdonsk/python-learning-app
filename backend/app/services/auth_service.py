"""
Authentication service - handles user registration and login.
"""
import random
import string
import asyncio
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, hash_password, create_access_token
from app.schemas.user import UserCreate, Token, UserOut


def _generate_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, user_data: UserCreate) -> Token:
        """Register a new user and send welcome email."""
        existing = await self.user_repo.get_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже зарегистрирован"
            )

        existing_username = await self.user_repo.get_by_username(user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя пользователя уже занято"
            )

        hashed = hash_password(user_data.password)
        user = await self.user_repo.create(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed,
        )

        # Send welcome email in background (don't block registration)
        asyncio.create_task(self._send_welcome(user_data.email, user_data.username, user_data.password))

        token = create_access_token({"sub": str(user.id)})
        return Token(
            access_token=token,
            user=UserOut.model_validate(user)
        )

    async def login(self, email: str, password: str) -> Token:
        """Authenticate user and return JWT token."""
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = create_access_token({"sub": str(user.id)})
        return Token(
            access_token=token,
            user=UserOut.model_validate(user)
        )

    async def forgot_password(self, email: str) -> None:
        """Generate new password and send it to user's email."""
        user = await self.user_repo.get_by_email(email)
        if not user:
            # Don't reveal whether email exists
            return

        new_password = _generate_password()
        hashed = hash_password(new_password)
        await self.user_repo.update_password(user.id, hashed)

        asyncio.create_task(self._send_reset(user.email, user.username, new_password))

    @staticmethod
    async def _send_welcome(email: str, username: str, password: str) -> None:
        try:
            from app.services.email_service import send_welcome_email
            await send_welcome_email(email, username, password)
        except Exception:
            pass

    @staticmethod
    async def _send_reset(email: str, username: str, new_password: str) -> None:
        try:
            from app.services.email_service import send_reset_password_email
            await send_reset_password_email(email, username, new_password)
        except Exception:
            pass
