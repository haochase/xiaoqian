from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# ─── 消息 ───
class ChatMessageCreate(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1)


class ChatMessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    audio_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── 会话 ───
class ChatSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    topic_id: UUID
    topic_title: Optional[str] = None
    outline: Optional[str] = None
    opening: Optional[str] = None
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    messages: list[ChatMessageResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class ChatSessionListItem(BaseModel):
    id: UUID
    topic_id: UUID
    topic_title: Optional[str] = None
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── WebSocket 消息 ───
class WSMessageIn(BaseModel):
    """前端发来的 WebSocket 消息"""
    content: str = Field(..., min_length=1)


class WSMessageOut(BaseModel):
    """后端返回的 WebSocket 消息"""
    id: str
    role: str
    content: str
