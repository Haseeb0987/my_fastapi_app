from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.auth_model import User
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest
from app.common.api_response import APIResponse
from app.utils.security import hash_password
from app.utils.utils import generate_user_id

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):

    stmt = select(User).where(User.email == payload.email)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        user_id=generate_user_id(),
        email=payload.email,
        password_hash=hash_password(payload.password),  # ✅ NO encode
        is_active=True
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return APIResponse(
        success=True,
        data={"user_id": user.user_id, "email": user.email},
        message="User registered successfully"
    ).to_dict()



@router.post("/login", response_model=dict)
async def login_user(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        service = AuthService(db)
        token = await service.authenticate_user(payload.email, payload.password)

        return APIResponse(
            success=True,
            data={
                "access_token": token,
                "token_type": "bearer",
                "expires_in": 1800
            },
            message="Login successful"
        ).to_dict()

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.get("/me")
async def get_current_user(current_user: User = Depends(AuthService.get_current_user)):
    """Get current authenticated user"""
    return APIResponse(
        success=True,
        data={"user_id": current_user.user_id, "email": current_user.email},
        message="Current user retrieved successfully"
    ).to_dict()

