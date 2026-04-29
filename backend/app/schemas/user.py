from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    phone: str = Field(..., regex=r"^\+?\d{7,15}$", description="国际化手机号")
    nickname: Optional[str] = None
    # 实际发送 OTP 的方式在 auth 路由中实现，这里仅接受手机号

class UserRead(BaseModel):
    id: str
    phone: str
    nickname: Optional[str] = None
    role: str
    timezone: str
    created_at: str

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
