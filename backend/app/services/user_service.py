"""用户业务逻辑"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import create_access_token


async def get_or_create_user(db: AsyncSession, phone: str) -> User:
    """根据手机号查找用户，不存在则创建"""
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            id=uuid.uuid4(),
            phone=phone,
            nickname=f"用户_{phone[-4:]}",
            role="elder",
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)

    return user


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def login_with_otp(db: AsyncSession, phone: str, otp: str) -> dict:
    """短信验证码登录，返回 token + user"""
    # 开发阶段：固定验证码 123456
    if otp != "123456":
        raise ValueError("验证码错误")

    user = await get_or_create_user(db, phone)
    access_token = create_access_token(subject=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "phone": user.phone,
            "nickname": user.nickname,
            "role": user.role,
            "timezone": user.timezone,
            "is_active": user.is_active,
        },
    }
