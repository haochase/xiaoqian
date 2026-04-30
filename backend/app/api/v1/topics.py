from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
import uuid

router = APIRouter()

class TopicBase(BaseModel):
    title: str
    category: str
    is_active: bool = True

class TopicCreate(TopicBase):
    pass

class TopicSchema(TopicBase):
    id: uuid.UUID

@router.get("", response_model=List[TopicSchema])
async def list_topics():
    return [
        {"id": uuid.uuid4(), "title": "今日猪肉价格", "category": "price", "is_active": True},
        {"id": uuid.uuid4(), "title": "本地天气预报", "category": "weather", "is_active": True}
    ]

@router.post("", response_model=TopicSchema)
async def create_topic(topic_in: TopicCreate):
    new_topic = TopicSchema(
        id=uuid.uuid4(),
        **topic_in.dict()
    )
    return new_topic

