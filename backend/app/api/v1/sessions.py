from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter()

class SessionSchema(BaseModel):
    id: uuid.UUID
    topic_id: uuid.UUID
    status: str
    started_at: datetime

@router.get("/", response_model=List[SessionSchema])
async def list_sessions():
    return []
