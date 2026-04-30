from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


# ─── 请求体 ───
class OTPRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\+?\d{7,15}$", description="手机号（支持国际格式）")


class OTPLoginRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\+?\d{7,15}$")
    otp: str = Field(..., min_length=4, max_length=6)


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=1, max_length=50)
    timezone: Optional[str] = None


# ─── 响应体 ───
class UserResponse(BaseModel):
    id: UUID
    phone: str
    nickname: Optional[str] = None
    role: str
    timezone: str
    is_active: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
