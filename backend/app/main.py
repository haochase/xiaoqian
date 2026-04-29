from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, topics, sessions, ws

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="小千 · 主动式兴趣聊天助手 API"
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
# app.include_router(topics.router, prefix="/api/v1/topics", tags=["话题"])
# app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["会话"])
app.include_router(ws.router, prefix="/ws", tags=["WebSocket"])

@app.get("/")
async def root():
    return {"message": "Welcome to XiaoQian API", "status": "running"}
