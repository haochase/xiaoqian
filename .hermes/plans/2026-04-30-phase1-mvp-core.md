# Phase 1: MVP 核心功能实施计划

> **For Hermes:** 按 Task 顺序逐个实现，每完成一个 Task 提交一次。

**目标:** 让「小倩」跑通核心流程：用户创建话题 → 定时检索 → 去重 → 生成聊天开场 → 推送/对话

**状态:** 数据模型 ✅ | API 路由骨架 ✅ | 业务逻辑 ❌ | Agent 管线 ❌ | 定时任务 ❌

---

## 第一阶段：后端服务层（让 API 不再是 mock）

### Task 1: 修复 schemas — 创建完整的 Pydantic 模型

**目标:** 补充缺失的 Pydantic schemas，支撑 API 输入输出

**文件:**
- Create: `backend/app/schemas/topic.py`
- Create: `backend/app/schemas/chat.py`
- Modify: `backend/app/schemas/user.py` (补充完整)

### Task 2: 实现用户服务

**目标:** 用户注册/登录/查询，替换 mock 的 `/api/v1/auth`

**文件:**
- Create: `backend/app/services/user_service.py`
- Modify: `backend/app/api/v1/auth.py`

### Task 3: 实现话题 CRUD 服务

**目标:** 话题创建/查询/更新/删除，关键词+定时配置存储

**文件:**
- Create: `backend/app/services/topic_service.py`
- Modify: `backend/app/api/v1/topics.py`

### Task 4: 实现会话与消息服务

**目标:** 创建会话、存储消息、查询历史

**文件:**
- Create: `backend/app/services/chat_service.py`
- Modify: `backend/app/api/v1/sessions.py`

### Task 5: 修复 WebSocket 聊天 — 接入真实 DB 和会话管理

**目标:** WebSocket 聊天能创建/恢复会话、存储消息到 DB

**文件:**
- Modify: `backend/app/api/v1/ws.py`

---

## 第二阶段：AI Agent 管线（搜索 → 去重 → 生成）

### Task 6: 搜索集成 — Tavily + 和风天气

**目标:** 根据话题分类调用对应搜索 API，返回结构化内容

**文件:**
- Create: `backend/app/services/search_service.py`

### Task 7: 向量去重 — Chroma 集成

**目标:** 对检索结果生成 embedding，与历史做相似度比较，过滤重复内容

**文件:**
- Create: `backend/app/services/vector_service.py`

### Task 8: 内容生成服务 — 聊天大纲 + 开场白

**目标:** 基于去重后的内容，调用 LLM 生成有温度的聊天大纲和开场白

**文件:**
- Create: `backend/app/services/content_service.py`

### Task 9: 完善 LangGraph Agent 管线

**目标:** 将搜索 → 去重 → 生成串成完整 Agent 工作流

**文件:**
- Modify: `backend/app/agents/chat_agent.py`
- Modify: `backend/app/agents/state.py`

---

## 第三阶段：定时任务调度

### Task 10: 定时调度器 — APScheduler 集成

**目标:** 每天按话题 schedule 触发检索+生成流程

**文件:**
- Create: `backend/app/tasks/scheduler.py`
- Modify: `backend/app/main.py` (启动时加载调度器)

### Task 11: 每日检索管线任务

**目标:** 单个话题的完整检索 → 去重 → 生成 → 创建会话 → 推送通知流程

**文件:**
- Create: `backend/app/tasks/daily_pipeline.py`

---

## 第四阶段：前端对接

### Task 12: 前端 API 层对接

**目标:** 前端 axios 实例配置，对接真实 API

**文件:**
- Modify: `frontend/web/src/api/index.ts`

### Task 13: 登录页面对接

**目标:** 手机号+验证码登录完整流程

**文件:**
- Modify: `frontend/web/src/views/Login.vue`

### Task 14: 话题管理页面对接

**目标:** 话题列表展示 + 创建话题表单

**文件:**
- Modify: `frontend/web/src/views/TopicList.vue`

### Task 15: 聊天页面对接

**目标:** WebSocket 实时聊天 + 消息展示

**文件:**
- Modify: `frontend/web/src/views/Chat.vue`
