import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    # category: price | celebrity | news | weather | custom
    keywords: Mapped[dict | None] = mapped_column(JSONB)
    # e.g. {"words": ["猪肉", "生猪价格"], "search_window_days": 3}
    schedule: Mapped[dict | None] = mapped_column(JSONB)
    # e.g. {"days": ["mon","wed","fri"], "time": "09:00"}
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_chat_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 关联
    user: Mapped["User"] = relationship("User", back_populates="topics")
    contents: Mapped[list["TopicContent"]] = relationship(
        "TopicContent", back_populates="topic", cascade="all, delete-orphan"
    )
    history_summaries: Mapped[list["TopicHistorySummary"]] = relationship(
        "TopicHistorySummary", back_populates="topic", cascade="all, delete-orphan"
    )
    sessions: Mapped[list["ChatSession"]] = relationship("ChatSession", back_populates="topic")
