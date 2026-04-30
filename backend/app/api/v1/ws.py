"""WebSocket 实时聊天端点"""
import json
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import decode_access_token
from app.services.user_service import get_user_by_id
from app.services.chat_service import (
    create_session,
    get_active_session,
    add_message,
    get_session,
)
from app.services.topic_service import get_topic
from app.agents.chat_agent import chat_workflow
from langchain_core.messages import HumanMessage

router = APIRouter()


@router.websocket("/chat/{topic_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    topic_id: str,
    token: str = Query(...),
):
    """WebSocket 聊天连接
    
    参数:
        topic_id: 话题 UUID
        token: JWT access token (query param)
    """
    # 1. 验证 token
    user_id_str = decode_access_token(token)
    if not user_id_str:
        await websocket.close(code=4001, reason="Invalid token")
        return

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        await websocket.close(code=4001, reason="Invalid token payload")
        return

    await websocket.accept()

    db: AsyncSession = AsyncSessionLocal()

    try:
        # 2. 验证用户和话题存在
        user = await get_user_by_id(db, user_id)
        if not user:
            await websocket.close(code=4004, reason="User not found")
            return

        topic = await get_topic(db, uuid.UUID(topic_id), user_id)
        if not topic:
            await websocket.close(code=4004, reason="Topic not found")
            return

        # 3. 查找或创建活跃会话
        session = await get_active_session(db, user_id, uuid.UUID(topic_id))
        if not session:
            session = await create_session(db, user_id, uuid.UUID(topic_id))

        # 4. 发送历史消息（如果有）
        if session.messages:
            for msg in session.messages:
                await websocket.send_json({
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content,
                })
        elif session.opening:
            # 发送开场白
            await websocket.send_json({
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": session.opening,
            })

        # 5. 消息循环
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_input = message_data.get("content", "")

            if not user_input.strip():
                continue

            # 保存用户消息到 DB
            await add_message(db, session.id, "user", user_input)

            # 构建对话上下文
            history = []
            for msg in (session.messages or []):
                if msg.role == "user":
                    history.append(HumanMessage(content=msg.content))
                else:
                    from langchain_core.messages import AIMessage
                    history.append(AIMessage(content=msg.content))

            # 调用 LLM
            initial_state = {
                "messages": history + [HumanMessage(content=user_input)],
                "topic_id": topic_id,
                "context": f"话题: {topic.title}",
                "outline": session.outline or "",
            }

            result = await chat_workflow.ainvoke(initial_state)
            ai_message = result["messages"][-1]

            # 保存 AI 回复到 DB
            saved_msg = await add_message(db, session.id, "assistant", ai_message.content)

            # 发送回前端
            await websocket.send_json({
                "id": str(saved_msg.id),
                "role": "assistant",
                "content": ai_message.content,
            })

            await db.commit()

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"role": "system", "content": f"出错了: {str(e)}"})
        except Exception:
            pass
    finally:
        await db.close()
