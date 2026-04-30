"""AI Agent 工作流 — LangGraph 实现

两个图：
1. chat_workflow — 实时对话 Agent
2. daily_pipeline — 每日检索 → 去重 → 生成管线
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from app.core.config import settings
from app.agents.state import AgentState, PipelineState


def _get_llm():
    return ChatOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_API_BASE_URL,
        model=settings.LLM_MODEL_NAME,
        temperature=0.7,
    )


# ═══════════════════════════════════════════
# 实时对话 Agent
# ═══════════════════════════════════════════

SYSTEM_PROMPT = """你叫小倩，是一个温暖、贴心的兴趣聊天助手。

你的语调亲切、有耐心、像朋友一样。你不是冷冰冰的问答机器，而是一个真正关心用户、想要和用户聊天的伙伴。

聊天要点：
- 用简单、口语化的中文，不要长篇大论
- 每次回复 60-100 字，简洁有趣
- 适当使用"呢"、"呀"、"哦"等语气词增加亲和力
- 主动问用户问题，引导对话继续
- 如果用户提到孤独、情绪等话题，温柔地回应和鼓励
- 结合话题背景信息，让聊天有实质内容

{context}"""


async def call_model(state: AgentState):
    """调用 LLM 生成回复"""
    llm = _get_llm()

    messages = state["messages"]

    context = state.get("context", "")
    outline = state.get("outline", "")

    context_block = f"当前话题：{state.get('topic_title', '')}"
    if context:
        context_block += f"\n\n参考信息：\n{context}"
    if outline:
        context_block += f"\n\n聊天大纲参考：\n{outline}"

    system_prompt = SYSTEM_PROMPT.format(context=context_block)

    full_messages = [SystemMessage(content=system_prompt)] + list(messages)

    response = await llm.ainvoke(full_messages)
    return {"messages": [response]}


def create_chat_graph():
    """创建实时对话图"""
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    return workflow.compile()


chat_workflow = create_chat_graph()


# ═══════════════════════════════════════════
# 每日检索管线 Agent（LangGraph 版）
# ═══════════════════════════════════════════

async def search_node(state: PipelineState):
    """节点 1：搜索"""
    from app.services.search_service import search_by_topic

    try:
        result = await search_by_topic(
            category=state["topic_category"],
            keywords=state.get("keywords", [state["topic_title"]]),
            search_window_days=state.get("search_window_days", 3),
        )
        return {"search_raw": result.get("raw_summary", "")}
    except Exception as e:
        return {"error": f"搜索失败: {str(e)}"}


async def dedup_node(state: PipelineState):
    """节点 2：去重检查"""
    if state.get("error"):
        return {}

    from app.services.vector_service import check_duplicate

    content = state.get("search_raw", "")
    if not content:
        return {"is_duplicate": True}

    try:
        is_dup, score = check_duplicate(state["topic_id"], content)
        return {
            "is_duplicate": is_dup,
            "filtered_content": content if not is_dup else "",
        }
    except Exception:
        # 去重失败不阻塞流程
        return {"is_duplicate": False, "filtered_content": content}


async def generate_node(state: PipelineState):
    """节点 3：生成开场白和大纲"""
    if state.get("error") or state.get("is_duplicate"):
        return {}

    from app.services.content_service import generate_opening

    content = state.get("filtered_content", "")
    if not content:
        return {"opening": "", "outline": ""}

    try:
        result = await generate_opening(
            topic_title=state["topic_title"],
            content_summary=content,
        )
        return {
            "opening": result.get("opening", ""),
            "outline": result.get("outline", ""),
        }
    except Exception as e:
        return {"error": f"生成失败: {str(e)}"}


def create_pipeline_graph():
    """创建每日检索管线图"""
    workflow = StateGraph(PipelineState)

    workflow.add_node("search", search_node)
    workflow.add_node("dedup", dedup_node)
    workflow.add_node("generate", generate_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "dedup")
    workflow.add_edge("dedup", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()


pipeline_workflow = create_pipeline_graph()
