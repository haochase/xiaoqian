from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# ─── 话题关键词 ───
class KeywordsSchema(BaseModel):
    """话题检索关键词"""
    words: list[str] = Field(default_factory=list, description="搜索关键词列表")
    search_window_days: int = Field(default=3, ge=1, le=30, description="检索窗口天数")


# ─── 话题时间安排 ───
class ScheduleSchema(BaseModel):
    """话题触发时间安排"""
    days: list[str] = Field(default_factory=lambda: ["mon", "tue", "wed", "thu", "fri"],
                            description="触发日期 (mon/tue/wed/thu/fri/sat/sun)")
    time: str = Field(default="09:00", description="触发时间 (HH:MM)")


# ─── 请求体 ───
class TopicCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="话题标题")
    category: str = Field(..., description="话题类别: price | celebrity | news | weather | custom")
    keywords: Optional[KeywordsSchema] = None
    schedule: Optional[ScheduleSchema] = None
    is_active: bool = True


class TopicUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = None
    keywords: Optional[KeywordsSchema] = None
    schedule: Optional[ScheduleSchema] = None
    is_active: Optional[bool] = None


# ─── 响应体 ───
class TopicResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    category: str
    keywords: Optional[dict] = None
    schedule: Optional[dict] = None
    is_active: bool
    last_chat_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TopicListItem(BaseModel):
    id: UUID
    title: str
    category: str
    is_active: bool
    last_chat_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}
