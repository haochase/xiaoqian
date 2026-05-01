from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.chat import ChatSessionResponse, ChatSessionListItem
from app.services import chat_service

router = APIRouter()


def _format_session(session) -> dict:
    """格式化会话为响应格式"""
    topic_title = session.topic.title if session.topic else None
    messages = [
        {
            "id": m.id,
            "session_id": m.session_id,
            "role": m.role,
            "content": m.content,
            "audio_url": m.audio_url,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in (session.messages or [])
    ]
    return {
        "id": session.id,
        "user_id": session.user_id,
        "topic_id": session.topic_id,
        "topic_title": topic_title,
        "outline": session.outline,
        "opening": session.opening,
        "status": session.status,
        "started_at": session.started_at,
        "ended_at": session.ended_at,
        "messages": messages,
    }


@router.get("", response_model=List[ChatSessionListItem])
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sessions = await chat_service.list_sessions(db, current_user.id)
    return [
        {
            "id": s.id,
            "topic_id": s.topic_id,
            "topic_title": s.topic.title if s.topic else None,
            "status": s.status,
            "started_at": s.started_at,
            "ended_at": s.ended_at,
        }
        for s in sessions
    ]


@router.get("/{session_id}", response_model=ChatSessionResponse)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    import uuid
    session = await chat_service.get_session(db, uuid.UUID(session_id), current_user.id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="会话不存在")
    return _format_session(session)


@router.get("/{session_id}/messages")
async def get_session_messages(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取会话消息列表 — 支持 session ID 或 topic ID"""
    import uuid
    session = await chat_service.get_session(db, uuid.UUID(session_id), current_user.id)
    if not session:
        session = await chat_service.get_active_session(db, current_user.id, uuid.UUID(session_id))
    if not session:
        return []
    messages = getattr(session, 'messages', []) or []
    return [
        {
            "id": str(m.id),
            "session_id": str(m.session_id),
            "role": m.role,
            "content": m.content,
            "audio_url": m.audio_url,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in messages
    ]


@router.post("/{session_id}/end")
async def end_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    import uuid
    ok = await chat_service.end_session(db, uuid.UUID(session_id), current_user.id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="会话不存在")
    return {"status": "completed"}
