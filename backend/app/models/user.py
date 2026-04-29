import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    nickname: Mapped[str | None] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(20), default="elder")  # elder | family | admin
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Shanghai")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 关联
    topics: Mapped[list["Topic"]] = relationship("Topic", back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[list["ChatSession"]] = relationship("ChatSession", back_populates="user")
    elder_links: Mapped[list["FamilyLink"]] = relationship(
        "FamilyLink", foreign_keys="FamilyLink.elder_id", back_populates="elder"
    )
    family_links: Mapped[list["FamilyLink"]] = relationship(
        "FamilyLink", foreign_keys="FamilyLink.family_id", back_populates="family_member"
    )


class FamilyLink(Base):
    __tablename__ = "family_links"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    elder_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    family_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    relation: Mapped[str | None] = mapped_column(String(20))  # son | daughter | spouse | other
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    elder: Mapped["User"] = relationship("User", foreign_keys=[elder_id], back_populates="elder_links")
    family_member: Mapped["User"] = relationship("User", foreign_keys=[family_id], back_populates="family_links")
