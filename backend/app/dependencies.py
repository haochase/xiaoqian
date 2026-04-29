import os
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from jose import JWTError
from app.core.security import decode_access_token
from app.core.database import get_db
from app.models.user import User

async def get_current_user(token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)) -> User:
    """解析 JWT 并返回对应的 User 实例。若 token 无效或用户不存在则抛出 401。"""
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    result = await db.execute("SELECT * FROM users WHERE id = :uid", {"uid": user_id})
    user_row = result.fetchone()
    if not user_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_row[0]
