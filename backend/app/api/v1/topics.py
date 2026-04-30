from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.topic import TopicCreate, TopicUpdate, TopicResponse, TopicListItem
from app.services import topic_service

router = APIRouter()


@router.get("", response_model=List[TopicListItem])
async def list_topics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topics = await topic_service.list_topics(db, current_user.id)
    return [TopicListItem.model_validate(t) for t in topics]


@router.post("", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic_in: TopicCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = await topic_service.create_topic(db, current_user.id, topic_in)
    return TopicResponse.model_validate(topic)


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    import uuid
    topic = await topic_service.get_topic(db, uuid.UUID(topic_id), current_user.id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="话题不存在")
    return TopicResponse.model_validate(topic)


@router.put("/{topic_id}", response_model=TopicResponse)
async def update_topic(
    topic_id: str,
    topic_in: TopicUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    import uuid
    topic = await topic_service.update_topic(db, uuid.UUID(topic_id), current_user.id, topic_in)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="话题不存在")
    return TopicResponse.model_validate(topic)


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(
    topic_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    import uuid
    deleted = await topic_service.delete_topic(db, uuid.UUID(topic_id), current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="话题不存在")
