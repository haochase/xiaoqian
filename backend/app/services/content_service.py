"""内容生成服务 — LLM 生成聊天大纲和开场白"""
from langchain_openai import ChatOpenAI

from app.core.config import settings


def _get_llm():
    """获取 LLM 实例"""
    return ChatOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_API_BASE_URL,
        model=settings.LLM_MODEL_NAME,
        temperature=0.7,
    )


async def generate_opening(topic_title: str, content_summary: str, history_context: str = "") -> dict:
    """根据检索内容生成聊天开场白和大纲
    
    Args:
        topic_title: 话题标题
        content_summary: 检索到的内容摘要
        history_context: 历史聊天摘要（用于避免重复话题）

    Returns:
        {
            "opening": str,    # 开场白
            "outline": str,    # 聊天大纲（JSON string）
        }
    """
    llm = _get_llm()

    history_block = ""
    if history_context:
        history_block = f"\n最近聊过的内容（请避免重复这些话题）：\n{history_context}"

    prompt = f"""你叫小倩，是一个温暖、贴心的兴趣聊天助手，专门陪伴用户聊天。

话题：{topic_title}

今日检索到的内容：
{content_summary}
{history_block}

请完成以下任务，返回 JSON 格式：

1. 生成一段自然、有温度的开场白：
   - 像朋友聊天一样开口，不要像播报新闻
   - 先聊一两句日常关心，再引出话题
   - 话题内容要口语化转述，不要直接复制新闻标题
   - 结尾留一个开放式问题，邀请用户回应
   - 语言简洁，单次不超过 100 字

2. 生成一个聊天大纲，包含 2-3 个可以深入聊的话题要点。

请严格返回 JSON 格式：
{{"opening": "...", "outline": "聊天大纲内容..."}}"""

    try:
        response = await llm.ainvoke(prompt)
        import json
        # 尝试解析 JSON
        content = response.content.strip()
        # 去掉可能的 markdown 代码块标记
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]

        result = json.loads(content)
        return {
            "opening": result.get("opening", "你好呀，今天过得怎么样？"),
            "outline": result.get("outline", ""),
        }
    except Exception as e:
        # 降级：返回简单开场白
        return {
            "opening": f"嘿～今天想跟你聊聊「{topic_title}」。{content_summary[:50]}...你觉得怎么样？",
            "outline": f"话题要点：\n1. {topic_title}的最新情况\n2. 相关讨论",
        }


async def generate_summary(chat_history: list[dict]) -> str:
    """根据聊天记录生成摘要（用于存入历史向量库）"""
    if not chat_history:
        return ""

    llm = _get_llm()

    # 拼接聊天记录
    dialogue = "\n".join([
        f"{'用户' if m['role'] == 'user' else '小倩'}: {m['content'][:200]}"
        for m in chat_history[-10:]  # 最近 10 条
    ])

    prompt = f"""请用 2-3 句话总结以下聊天对话的核心内容和主题：

{dialogue}

总结："""

    try:
        response = await llm.ainvoke(prompt)
        return response.content.strip()
    except Exception:
        return f"聊了关于 {chat_history[0]['content'][:50]} 的话题"
