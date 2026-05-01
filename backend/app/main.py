from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager
import os

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

# 挂载路由（两个前缀：/api/v1 供外部 API 调用，/api 供前端直连）
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["话题"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["会话"])
app.include_router(ws.router, prefix="/ws", tags=["WebSocket"])

# 前端直连兼容（无 Vite 代理时）
app.include_router(auth.router, prefix="/api/auth")
app.include_router(topics.router, prefix="/api/topics")
app.include_router(sessions.router, prefix="/api/sessions")

# 前端静态文件
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")


@app.get("/")
async def root():
    if os.path.isfile(os.path.join(FRONTEND_DIR, "index.html")):
        return FileResponse(
            os.path.join(FRONTEND_DIR, "index.html"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    return {"message": "欢迎使用小倩 API", "version": settings.VERSION, "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# SPA 兜底：Vue Router history 模式
@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(
            index_path,
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    return JSONResponse(status_code=404, content={"detail": "Not Found"})
