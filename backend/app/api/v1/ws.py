from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.agents.chat_agent import chat_workflow
from langchain_core.messages import HumanMessage
import json

router = APIRouter()

@router.websocket("/chat/{topic_id}")
async def websocket_endpoint(websocket: WebSocket, topic_id: str):
    await websocket.accept()
    try:
        while True:
            # 接收前端消息
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_input = message_data.get("content", "")
            
            # 调用 LangGraph 工作流
            # 初始化状态
            initial_state = {
                "messages": [HumanMessage(content=user_input)],
                "topic_id": topic_id,
                "context": "",
                "outline": ""
            }
            
            # 执行工作流
            result = await chat_workflow.ainvoke(initial_state)
            
            # 获取最后一条消息（AI 回复）
            ai_message = result["messages"][-1]
            
            # 发送回前端
            await websocket.send_json({
                "id": str(ai_message.id) if hasattr(ai_message, 'id') else "ai-msg",
                "role": "assistant",
                "content": ai_message.content
            })
            
    except WebSocketDisconnect:
        print(f"Client disconnected from topic {topic_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
