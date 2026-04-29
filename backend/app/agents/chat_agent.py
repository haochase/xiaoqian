from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from app.core.config import settings
from app.agents.state import AgentState

# 初始化 LLM
llm = ChatOpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_API_BASE_URL,
    model=settings.LLM_MODEL_NAME,
    temperature=0.7
)

async def call_model(state: AgentState):
    """调用 LLM 生成回复"""
    messages = state["messages"]
    
    # 构建系统提示词
    system_prompt = (
        "你叫小倩，是一个温暖、贴心的兴趣聊天助手，专门陪伴用户聊天。"
        "你的语气应该是亲切、有耐心且富有情感色彩的。"
        "如果提供了背景信息，请结合背景信息进行对话。"
    )
    
    # 如果有背景上下文，添加到提示词中
    if state.get("context"):
        system_prompt += f"\n\n背景信息：\n{state['context']}"
        
    response = await llm.ainvoke([SystemMessage(content=system_prompt)] + messages)
    return {"messages": [response]}

def create_chat_graph():
    """创建聊天流程图"""
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("agent", call_model)
    
    # 设置入口
    workflow.set_entry_point("agent")
    
    # 简单的线性流程，目前只有 agent 节点
    workflow.add_edge("agent", END)
    
    return workflow.compile()

# 导出编译后的图形
chat_workflow = create_chat_graph()
