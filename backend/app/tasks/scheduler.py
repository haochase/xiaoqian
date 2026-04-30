"""定时任务 — 每日话题检索与聊天生成"""
import asyncio
import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.services.topic_service import get_topics_due_today
from app.services.chat_service import create_session
from app.agents.chat_agent import pipeline_workflow


async def run_daily_pipeline():
    """执行每日检索管线：处理所有今日到期的话题"""
    db: AsyncSession = AsyncSessionLocal()

    try:
        # 1. 查询今天需要触发的话题
        topics = await get_topics_due_today(db)
        if not topics:
            print(f"[Scheduler] 今日无到期话题")
            return

        print(f"[Scheduler] 今日到期话题: {len(topics)} 个")

        # 2. 逐个处理
        for topic in topics:
            try:
                await process_topic(db, topic)
            except Exception as e:
                print(f"[Scheduler] 话题 {topic.title} 处理失败: {e}")

        await db.commit()
    finally:
        await db.close()


async def process_topic(db: AsyncSession, topic):
    """处理单个话题的完整管线"""
    keywords = (topic.keywords or {}).get("words", [topic.title])
    search_window = (topic.keywords or {}).get("search_window_days", 3)

    print(f"[Pipeline] 开始处理: {topic.title} (id={topic.id})")

    # 执行 Agent 管线
    state = {
        "topic_id": str(topic.id),
        "topic_title": topic.title,
        "topic_category": topic.category,
        "keywords": keywords,
        "search_window_days": search_window,
        "search_raw": None,
        "is_duplicate": False,
        "filtered_content": None,
        "opening": None,
        "outline": None,
        "session_created": False,
        "error": None,
    }

    result = await pipeline_workflow.ainvoke(state)

    if result.get("error"):
        print(f"[Pipeline] {topic.title} 失败: {result['error']}")
        return

    if result.get("is_duplicate"):
        print(f"[Pipeline] {topic.title} 内容与历史重复，跳过")
        return

    opening = result.get("opening", "")
    if not opening:
        print(f"[Pipeline] {topic.title} 未生成有效内容，跳过")
        return

    # 创建聊天会话
    session = await create_session(
        db,
        user_id=topic.user_id,
        topic_id=topic.id,
        outline=result.get("outline", ""),
        opening=opening,
    )

    # 更新话题的最后聊天时间
    from app.models.topic import Topic
    topic.last_chat_at = datetime.now(timezone.utc)

    print(f"[Pipeline] {topic.title} 完成，会话 id={session.id}")
    print(f"[Pipeline] 开场白: {opening[:80]}...")


# ═══════════════════════════════════════════
# APScheduler 调度器
# ═══════════════════════════════════════════

_scheduler = None


def init_scheduler():
    """初始化并启动 APScheduler"""
    global _scheduler

    try:
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
    except ImportError:
        print("[Scheduler] APScheduler 未安装，跳过定时任务")
        return

    _scheduler = AsyncIOScheduler()

    hour = getattr(settings, "DAILY_TRIGGER_HOUR", 8)
    minute = getattr(settings, "DAILY_TRIGGER_MINUTE", 30)

    _scheduler.add_job(
        run_daily_pipeline,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="daily_pipeline",
        name="每日话题检索管线",
        replace_existing=True,
    )

    _scheduler.start()
    print(f"[Scheduler] 定时任务已启动，每日 {hour:02d}:{minute:02d} 执行")


def shutdown_scheduler():
    """关闭调度器"""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
