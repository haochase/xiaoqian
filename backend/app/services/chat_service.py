"""聊天会话与消息业务逻辑"""
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.chat import ChatSession, ChatMessage
from app.models.topic import Topic


async def create_session(
    db: AsyncSession,
    user_id: uuid.UUID,
    topic_id: uuid.UUID,
    outline: Optional[str] = None,
    opening: Optional[str] = None,
) -> ChatSession:
    """创建新的聊天会话"""
    session = ChatSession(
        id=uuid.uuid4(),
        user_id=user_id,
        topic_id=topic_id,
        outline=outline,
        opening=opening,
        status="active",
    )
    db.add(session)
    await db.flush()
    await db.refresh(session)
    return session


async def get_session(
    db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID
) -> Optional[ChatSession]:
    """获取会话（含消息 + 话题标题）"""
    result = await db.execute(
        select(ChatSession)
        .options(joinedload(ChatSession.messages), joinedload(ChatSession.topic))
        .where(ChatSession.id == session_id, ChatSession.user_id == user_id)
    )
    return result.unique().scalar_one_or_none()


async def list_sessions(
    db: AsyncSession, user_id: uuid.UUID, limit: int = 20
) -> list[ChatSession]:
    """获取用户最近的会话列表"""
    result = await db.execute(
        select(ChatSession)
        .options(joinedload(ChatSession.topic))
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.started_at.desc())
        .limit(limit)
    )
    return list(result.unique().scalars().all())


async def add_message(
    db: AsyncSession,
    session_id: uuid.UUID,
    role: str,
    content: str,
    audio_url: Optional[str] = None,
) -> ChatMessage:
    """往会话中添加一条消息"""
    msg = ChatMessage(
        id=uuid.uuid4(),
        session_id=session_id,
        role=role,
        content=content,
        audio_url=audio_url,
    )
    db.add(msg)
    await db.flush()
    await db.refresh(msg)
    return msg


async def end_session(db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """结束会话"""
    session = await get_session(db, session_id, user_id)
    if not session:
        return False
    session.status = "completed"
    session.ended_at = datetime.now(timezone.utc)
    await db.flush()
    return True


async def get_active_session(
    db: AsyncSession, user_id: uuid.UUID, topic_id: uuid.UUID
) -> Optional[ChatSession]:
    """获取用户某个话题下的活跃会话"""
    result = await db.execute(
        select(ChatSession)
        .where(
            ChatSession.user_id == user_id,
            ChatSession.topic_id == topic_id,
            ChatSession.status == "active",
        )
        .order_by(ChatSession.started_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()
