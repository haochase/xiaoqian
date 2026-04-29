from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
import uuid

router = APIRouter()

class TopicSchema(BaseModel):
    id: uuid.UUID
    title: str
    category: str
    is_active: bool

@router.get("", response_model=List[TopicSchema])
async def list_topics():
    return [
        {"id": uuid.uuid4(), "title": "今日猪肉价格", "category": "price", "is_active": True},
        {"id": uuid.uuid4(), "title": "本地天气预报", "category": "weather", "is_active": True}
    ]

@router.post("")
async def create_topic(topic: TopicSchema):
    return topic
