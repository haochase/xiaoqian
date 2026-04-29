from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.core.security import create_access_token
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

router = APIRouter()

class OTPLoginRequest(BaseModel):
    phone: str
    otp: str

@router.post("/verify-otp")
async def verify_otp(request: OTPLoginRequest, db: AsyncSession = Depends(get_db)):
    # 模拟验证码：123456
    if request.otp != "123456":
        raise HTTPException(status_code=400, detail="验证码错误")
    
    # 查找或创建用户
    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            id=uuid.uuid4(),
            phone=request.phone,
            nickname=f"用户_{request.phone[-4:]}",
            role="elder"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    # 生成 JWT
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_me():
    # 这里应该用 get_current_user 依赖，目前先返回 mock
    return {"id": "mock-id", "phone": "13800138000", "nickname": "小倩用户"}
