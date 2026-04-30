"""Agent 状态定义 — 支持完整的多 Agent 管线"""
from typing import Annotated, List, TypedDict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Agent 工作流共享状态"""
    # 消息历史
    messages: Annotated[List[BaseMessage], add_messages]

    # 当前话题 ID
    topic_id: str

    # 话题信息
    topic_title: str
    topic_category: str

    # 检索到的原始内容（search_service 输出）
    search_results: Optional[str]

    # 去重后的内容（过滤已聊过的）
    filtered_content: Optional[str]

    # 生成的聊天大纲和开场白
    outline: str
    opening: str

    # 对话上下文
    context: str


class PipelineState(TypedDict):
    """每日检索管线状态"""
    topic_id: str
    topic_title: str
    topic_category: str
    keywords: list[str]
    search_window_days: int

    # 管线各阶段输出
    search_raw: Optional[str]
    is_duplicate: bool
    filtered_content: Optional[str]
    opening: Optional[str]
    outline: Optional[str]

    # 结果
    session_created: bool
    error: Optional[str]
