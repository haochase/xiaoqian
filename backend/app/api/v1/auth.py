from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import OTPLoginRequest, TokenResponse, UserResponse
from app.services.user_service import login_with_otp, get_user_by_id

router = APIRouter()


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(request: OTPLoginRequest, db: AsyncSession = Depends(get_db)):
    """手机验证码登录（开发阶段固定 123456）"""
    try:
        result = await login_with_otp(db, request.phone, request.otp)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return UserResponse.model_validate(current_user)
