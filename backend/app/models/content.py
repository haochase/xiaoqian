import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base


class TopicContent(Base):
    """每次检索到的原始内容缓存"""
    __tablename__ = "topic_contents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    raw_content: Mapped[str | None] = mapped_column(Text)        # 原始检索结果
    summary: Mapped[str | None] = mapped_column(Text)            # LLM 摘要
    chroma_id: Mapped[str | None] = mapped_column(String(100))   # Chroma 向量 ID（用于去重）
    source_urls: Mapped[dict | None] = mapped_column(JSONB)      # 来源 URL 列表
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    used: Mapped[bool] = mapped_column(Boolean, default=False)   # 是否已用于聊天

    topic: Mapped["Topic"] = relationship("Topic", back_populates="contents")


class TopicHistorySummary(Base):
    """每次聊天结束后存储的历史摘要，用于下次去重"""
    __tablename__ = "topic_history_summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    chroma_id: Mapped[str | None] = mapped_column(String(100))   # Chroma 向量 ID
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    topic: Mapped["Topic"] = relationship("Topic", back_populates="history_summaries")
