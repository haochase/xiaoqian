# 小倩 (XiaoQian) · 主动式兴趣聊天助手

🌸 一个基于大语言模型的智能聊天助手，专为老年用户和对特定话题感兴趣的学习者设计。通过主动推送定制化话题、实时 WebSocket 对话，让知识获取变得像聊天一样自然。

## ✨ 核心特性

- 🎯 **话题定制** — 支持天气、财经、科技、体育、娱乐等多类别话题订阅
- 💬 **实时对话** — WebSocket 驱动，秒级响应的自然语言聊天
- 🔍 **智能检索** — 集成 Tavily Search API 与和风天气 API，自动获取最新资讯
- 🧠 **AI Agent 管线** — LangGraph 驱动的搜索→去重→生成三阶段智能管线
- 📅 **定时推送** — APScheduler 每日自动检索话题最新动态并生成开场白
- 🎨 **小清新 UI** — 磨砂玻璃 + 柔和渐变，适配老年用户的大字体优雅界面

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI (Python 3.11+) |
| AI 引擎 | LangChain + LangGraph + OpenAI 兼容 API |
| 数据库 | PostgreSQL 16 + SQLAlchemy 2.0 (async) |
| 缓存 / 队列 | Redis |
| 向量存储 | ChromaDB (嵌入式模式) |
| 消息网关 | Feishu / WebSocket 直连 |
| 前端 | Vue 3 + TypeScript + Vite |
| 部署 | Docker + Cloudflare Tunnel |

## 📁 项目结构

```
xiaoqian/
├── backend/
│   └── app/
│       ├── agents/          # LangGraph AI Agent
│       ├── api/v1/          # REST + WebSocket 端点
│       ├── core/            # 配置、数据库、安全
│       ├── models/          # ORM 模型
│       ├── schemas/         # Pydantic 数据模型
│       ├── services/        # 业务逻辑
│       └── tasks/           # 定时任务调度
├── frontend/
│   └── web/                 # Vue 3 SPA
│       └── src/
│           ├── views/       # 页面组件
│           ├── store/       # Pinia 状态管理
│           └── api/         # Axios HTTP 客户端
├── docker-compose.yml       # 基础设施编排
└── pyproject.toml           # Python 依赖管理
```

## 🚀 快速开始

### 前置条件

- Docker & Docker Compose
- Python 3.11+
- Node.js 20+ (仅开发前端时需要)

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 LLM API Key 等
```

### 2. 启动基础设施

```bash
docker compose up -d db redis
```

### 3. 启动后端

```bash
cd backend
pip install -e ..
uvicorn app.main:app --host 0.0.0.0 --port 8081
```

### 4. 构建前端

```bash
cd frontend
docker build --target builder -t xiaoqian-build .
docker create --name tmp xiaoqian-build
docker cp tmp:/app/dist ./dist
docker rm tmp
```

### 5. 访问

打开浏览器访问 `http://localhost:8081`

## 🧪 AI Agent 管线

```
用户订阅话题 → 定时触发 → 搜索最新资讯 → 向量去重 → LLM 生成开场白 → WebSocket 推送
```

详见 [Agent 架构说明](#)。

## 📄 License

MIT
