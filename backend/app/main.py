from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1 import auth, topics, sessions, ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动
    from app.core.database import init_db
    await init_db()

    # 启动定时调度器
    from app.tasks.scheduler import init_scheduler
    init_scheduler()

    yield

    # 关闭
    from app.tasks.scheduler import shutdown_scheduler
    shutdown_scheduler()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="小倩 · 主动式兴趣聊天助手 API",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["话题"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["会话"])
app.include_router(ws.router, prefix="/ws", tags=["WebSocket"])


@app.get("/")
async def root():
    return {"message": "欢迎使用小倩 API", "version": settings.VERSION, "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
