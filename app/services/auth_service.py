from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.auth_model import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token, verify_token
from app.utils.utils import generate_user_id
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.db.base import get_db

class AuthService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, email: str, password: str):
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        if result.scalars().first():
            raise ValueError("Email already registered")

        user = User(
            user_id=generate_user_id(),
            email=email,
            password_hash=hash_password(password),
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def authenticate_user(self, email: str, password: str):
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalars().first()

        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise PermissionError("User inactive")

        user.last_login_at = datetime.utcnow()
        await self.db.commit()

        token = create_access_token({"sub": user.user_id})
        return token

    async def get_current_user(
        self, 
        credentials: HTTPBearer = Depends(HTTPBearer()),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        """Get current user from JWT token"""
        token = credentials.credentials
        
        try:
            payload = verify_token(token)
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        # Fetch user from database
        stmt = select(User).where(User.user_id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive"
            )

        return user
