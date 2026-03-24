"""
Authentication service - handles user registration and login.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, hash_password, create_access_token
from app.schemas.user import UserCreate, Token, UserOut


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, user_data: UserCreate) -> Token:
        """Register a new user."""
        # Check if email already exists
        existing = await self.user_repo.get_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже зарегистрирован"
            )

        # Check username
        existing_username = await self.user_repo.get_by_username(user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя пользователя уже занято"
            )

        # Create user
        hashed = hash_password(user_data.password)
        user = await self.user_repo.create(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed,
        )

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
