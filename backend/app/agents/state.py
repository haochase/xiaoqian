from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # 消息历史，使用 add_messages 允许自动合并新消息
    messages: Annotated[List[BaseMessage], add_messages]
    # 当前话题 ID
    topic_id: str
    # 检索到的相关背景信息
    context: str
    # 对话大纲（如果生成了的话）
    outline: str
