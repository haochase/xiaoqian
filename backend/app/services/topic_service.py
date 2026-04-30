"""话题 CRUD 业务逻辑"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicUpdate


async def list_topics(db: AsyncSession, user_id: uuid.UUID) -> list[Topic]:
    result = await db.execute(
        select(Topic)
        .where(Topic.user_id == user_id)
        .order_by(Topic.created_at.desc())
    )
    return list(result.scalars().all())


async def get_topic(db: AsyncSession, topic_id: uuid.UUID, user_id: uuid.UUID) -> Topic | None:
    result = await db.execute(
        select(Topic).where(Topic.id == topic_id, Topic.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_topic(db: AsyncSession, user_id: uuid.UUID, data: TopicCreate) -> Topic:
    topic = Topic(
        id=uuid.uuid4(),
        user_id=user_id,
        title=data.title,
        category=data.category,
        keywords=data.keywords.model_dump() if data.keywords else None,
        schedule=data.schedule.model_dump() if data.schedule else None,
        is_active=data.is_active,
    )
    db.add(topic)
    await db.flush()
    await db.refresh(topic)
    return topic


async def update_topic(
    db: AsyncSession, topic_id: uuid.UUID, user_id: uuid.UUID, data: TopicUpdate
) -> Topic | None:
    topic = await get_topic(db, topic_id, user_id)
    if not topic:
        return None

    update_data = data.model_dump(exclude_unset=True)
    if "keywords" in update_data and update_data["keywords"] is not None:
        update_data["keywords"] = update_data["keywords"].model_dump() if hasattr(update_data["keywords"], "model_dump") else update_data["keywords"]
    if "schedule" in update_data and update_data["schedule"] is not None:
        update_data["schedule"] = update_data["schedule"].model_dump() if hasattr(update_data["schedule"], "model_dump") else update_data["schedule"]

    for field, value in update_data.items():
        setattr(topic, field, value)

    await db.flush()
    await db.refresh(topic)
    return topic


async def delete_topic(db: AsyncSession, topic_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    topic = await get_topic(db, topic_id, user_id)
    if not topic:
        return False
    await db.delete(topic)
    await db.flush()
    return True


async def get_topics_due_today(db: AsyncSession) -> list[Topic]:
    """查询今天需要触发的所有活跃话题"""
    import calendar
    now = datetime.now(timezone.utc)
    weekday = calendar.day_abbr[now.weekday()].lower()  # mon, tue, ...

    result = await db.execute(
        select(Topic).where(Topic.is_active == True)
    )
    all_active = result.scalars().all()

    # 按 schedule 过滤：今天的日期在 days 列表中
    due = []
    for topic in all_active:
        schedule = topic.schedule or {}
        days = schedule.get("days", ["mon", "tue", "wed", "thu", "fri"])
        if weekday in days:
            due.append(topic)
    return due
