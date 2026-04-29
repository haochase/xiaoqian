# 小倩 · 兴趣聊天助手 — 完整开发设计文档

> 版本：v1.0 | 日期：2026-04-29

---

## 一、产品定位与商业可行性分析

### 1.1 核心价值主张

**一句话定位**：小倩是一款"主动式兴趣聊天伴侣"——不等你问，定时主动发起话题，像一个真正关心你的朋友。

这与市场上所有现有 AI 助手（豆包、Siri、小爱同学）形成本质差异：

| 维度 | 传统AI助手 | 小倩 |
|------|-----------|------|
| 交互模式 | 被动响应（你问我答） | 主动发起（我找话题聊你） |
| 内容来源 | 实时回答 | 定时检索 + 去重 + 编排 |
| 情感属性 | 工具感 | 陪伴感 |
| 目标用户 | 效率导向 | 情感/成长导向 |
| 知识更新 | 用户主动触发 | 系统自动驱动 |

### 1.2 目标用户画像

**主要用户（情感型）**
- 60岁+ 独居/行动不便老人，子女不在身边
- 一人在家，缺乏社交刺激，看电视已麻木
- 不擅长智能设备操作，无法主动搜索信息

**次要用户（成长型）**
- 25-40岁上班族，下班疲惫但仍想自我提升
- 通勤、午饭、遛弯时间碎片化学习需求
- 不想花时间收集信息，只想"被喂知识"

### 1.3 商业可行性评估

**✅ 支撑点**

1. **痛点真实且强烈**：中国独居老人超 2600 万（2023年），孤独感已被WHO列为全球性健康危机
2. **AI能力高度匹配**：检索 + 摘要 + 拟人化对话，正是LLM最擅长的
3. **差异化壁垒清晰**：无竞品在做"主动定时聊天"这一模式
4. **MVP成本极低**：用现有API（搜索+LLM+TTS）可在2周内跑起原型
5. **家庭付费逻辑成立**：子女为父母购买 → 情感价值驱动付费意愿高

**⚠️ 风险点**

| 风险 | 等级 | 应对策略 |
|------|------|---------|
| 老人设备门槛 | 高 | 先做微信小程序（老人已熟悉微信），后做独立App |
| LLM生成内容质量不稳定 | 中 | 增加内容审核层 + 用户反馈机制 |
| 搜索API成本 | 中 | 按话题数量控制检索频次，免费版限3个话题 |
| 隐私与数据安全 | 中 | 话题数据本地化选项，明确隐私政策 |
| 用户留存 | 中 | 核心在于内容新鲜感 + 对话质量，需持续迭代 |

**商业化路径**

```
免费版（1-3个话题）
    → 家庭版（月付/年付，5-10个话题，家人管理后台）
        → 企业版（养老院、社区健康中心批量采购）
            → 数据变现（脱敏兴趣图谱，广告精准投放）
```

---

## 二、系统整体架构

### 2.1 架构总览

```
┌─────────────────────────────────────────────────────────┐
│                      用户端（前端）                        │
│   微信小程序 / Web App / 未来独立App                       │
│   话题配置 | 聊天界面 | 历史记录 | 家人管理后台              │
└────────────────┬────────────────────────────────────────┘
                 │ HTTPS / WebSocket
┌────────────────▼────────────────────────────────────────┐
│                      API 网关层                           │
│           FastAPI（REST + WebSocket）                     │
│     认证/鉴权 | 限流 | 路由 | 日志                         │
└──────┬──────────────────────────┬───────────────────────┘
       │                          │
┌──────▼──────┐         ┌─────────▼────────┐
│  业务服务层  │         │   AI Agent 层     │
│             │         │                  │
│ 用户服务    │         │ 话题调度 Agent    │
│ 话题服务    │         │ 内容检索 Agent    │
│ 聊天服务    │         │ 去重 Agent       │
│ 通知服务    │         │ 对话生成 Agent    │
└──────┬──────┘         └─────────┬────────┘
       │                          │
┌──────▼──────────────────────────▼───────────────────────┐
│                      数据层                               │
│  PostgreSQL（用户/话题/聊天记录）                           │
│  Redis（会话缓存/任务队列）                                 │
│  向量数据库 Chroma（历史内容去重）                           │
└─────────────────────────────────────────────────────────┘
```

### 2.2 技术选型

| 层次 | 技术 | 理由 |
|------|------|------|
| 后端框架 | FastAPI + Python 3.11 | 异步支持好，AI生态完善 |
| 任务调度 | APScheduler / Celery Beat | 定时任务，每日触发内容检索 |
| AI编排 | LangGraph | 多Agent协作，状态管理清晰 |
| LLM | DashScope (qwen-max) / OpenAI | 支持中文，成本可控 |
| 搜索 | Tavily API / Bing Search API | 实时网络检索 |
| TTS | 阿里云TTS / 火山引擎TTS | 中文效果好，支持情感音色 |
| STT | FunASR / Whisper | 支持普通话方言，老人语速适应 |
| 向量DB | Chroma (本地) / Qdrant (云) | 内容去重向量存储 |
| 关系DB | PostgreSQL + SQLAlchemy | 成熟稳定 |
| 缓存/队列 | Redis | 会话状态 + 任务队列 |
| 前端 | Vue 3 + Vite（Web） / 微信小程序 | 双端覆盖 |
| 部署 | Docker Compose（MVP）→ K8s（规模化） | 分阶段扩展 |

---

## 三、数据模型设计

### 3.1 核心数据表

```sql
-- 用户表
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone       VARCHAR(20) UNIQUE,
    nickname    VARCHAR(50),
    role        VARCHAR(20) DEFAULT 'elder',  -- elder | family | admin
    timezone    VARCHAR(50) DEFAULT 'Asia/Shanghai',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 家庭关联表（子女绑定老人账号）
CREATE TABLE family_links (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    elder_id    UUID REFERENCES users(id),
    family_id   UUID REFERENCES users(id),
    relation    VARCHAR(20),  -- son | daughter | spouse | other
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 话题表
CREATE TABLE topics (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID REFERENCES users(id),
    title        VARCHAR(100) NOT NULL,
    category     VARCHAR(30) NOT NULL,           -- price | celebrity | news | weather | custom
    keywords     JSONB,                          -- ["猪肉", "生猪", "肉价"]
    schedule     JSONB,                          -- {"days": ["mon","wed","fri"], "time": "09:00"}
    is_active    BOOLEAN DEFAULT TRUE,
    last_chat_at TIMESTAMPTZ,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- 检索内容缓存表
CREATE TABLE topic_contents (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id     UUID REFERENCES topics(id),
    raw_content  TEXT,
    summary      TEXT,
    embedding    VECTOR(1536),                   -- 用于去重
    source_urls  JSONB,
    retrieved_at TIMESTAMPTZ DEFAULT NOW(),
    used         BOOLEAN DEFAULT FALSE
);

-- 聊天会话表
CREATE TABLE chat_sessions (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID REFERENCES users(id),
    topic_id     UUID REFERENCES topics(id),
    outline      TEXT,
    status       VARCHAR(20) DEFAULT 'active',  -- active | completed | abandoned
    started_at   TIMESTAMPTZ DEFAULT NOW(),
    ended_at     TIMESTAMPTZ
);

-- 聊天消息表
CREATE TABLE chat_messages (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id   UUID REFERENCES chat_sessions(id),
    role         VARCHAR(10),                    -- user | assistant
    content      TEXT,
    audio_url    VARCHAR(500),                   -- TTS生成的语音URL（Phase 2）
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- 话题历史摘要表（用于去重）
CREATE TABLE topic_history_summaries (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id     UUID REFERENCES topics(id),
    summary      TEXT,
    embedding    VECTOR(1536),
    created_at   TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 四、AI Agent 设计

### 4.1 Agent 工作流（LangGraph）

```
每日定时触发
     │
     ▼
[话题调度 Agent]
  - 查询当天需要执行的话题列表
  - 为每个话题创建独立任务
     │
     ▼
[内容检索 Agent]
  - 根据话题关键词调用搜索API
  - 获取最新相关内容（新闻/价格/天气）
  - 清洗和结构化原始数据
     │
     ▼
[去重过滤 Agent]
  - 对新内容生成embedding
  - 与历史摘要向量做相似度比较（阈值0.85）
  - 过滤已聊过的内容，保留新鲜内容
     │
     ▼
[聊天编排 Agent]
  - 基于新内容生成今日聊天大纲
  - 设计对话开场白（有温度，不干巴巴）
  - 准备2-3个引导性追问
     │
     ▼
[推送触发]
  - 向用户推送今日开场消息
  - 等待用户回复，进入实时对话模式
     │
     ▼
[实时对话 Agent]
  - 维护对话上下文
  - 根据大纲引导话题，自然延伸
  - 会话结束后生成摘要，存入历史
```

### 4.2 对话生成 Prompt 设计

**开场白生成 Prompt**

```
你是一个温暖、亲切的聊天伙伴，用户是一位老人，你要用简单、口语化的中文和他/她聊天。

今天检索到的话题内容：
{topic_content}

历史聊天摘要（避免重复）：
{history_summaries}

请根据以上内容，生成一段自然的开场白，要求：
1. 像朋友聊天一样开口，不要像播报新闻
2. 先聊一两句日常关心，再引出话题
3. 话题内容要口语化转述，不要直接复制新闻标题
4. 结尾留一个开放式问题，邀请用户回应
5. 语言简洁，单次不超过100字
```

**实时对话 Prompt**

```
你是{user_nickname}的聊天伙伴，正在聊关于"{topic_title}"的话题。

今日聊天大纲：
{outline}

历史对话：
{chat_history}

用户说：{user_message}

请自然地回复，引导话题继续深入，适时插入大纲中的下一个要点。
回复要求：简洁口语，不超过80字，像朋友聊天。
```

### 4.3 话题类别处理策略

| 类别 | 检索策略 | 内容新鲜度 |
|------|---------|-----------|
| price（价格） | 每日检索，关键词含"今日/本周" | 必须是最新 |
| weather（天气） | 调用天气API，无需搜索 | 实时 |
| celebrity（明星） | 检索近7天新闻 | 近期即可 |
| news（资讯） | 检索近3天行业动态 | 近期即可 |
| custom（自定义） | 用户可设置检索窗口 | 灵活配置 |

---

## 五、API 接口设计

### 5.1 用户与认证

```
POST   /api/v1/auth/send-otp          # 发送手机验证码
POST   /api/v1/auth/verify-otp        # 验证并登录/注册
POST   /api/v1/auth/refresh           # 刷新Token
GET    /api/v1/users/me               # 获取当前用户信息
PUT    /api/v1/users/me               # 更新用户信息
POST   /api/v1/family/bind            # 子女绑定老人账号
GET    /api/v1/family/members         # 获取家庭成员列表
```

### 5.2 话题管理

```
GET    /api/v1/topics                 # 获取话题列表
POST   /api/v1/topics                 # 创建话题
GET    /api/v1/topics/{id}            # 获取话题详情
PUT    /api/v1/topics/{id}            # 更新话题
DELETE /api/v1/topics/{id}            # 删除话题
POST   /api/v1/topics/{id}/trigger    # 手动触发一次检索+聊天
PUT    /api/v1/topics/{id}/schedule   # 修改时间安排
```

### 5.3 聊天

```
GET    /api/v1/sessions               # 获取聊天历史列表
GET    /api/v1/sessions/{id}          # 获取会话详情（含消息）
WS     /api/v1/ws/chat/{session_id}   # WebSocket实时聊天
POST   /api/v1/sessions/{id}/end      # 主动结束会话
```

### 5.4 语音（Phase 2）

```
POST   /api/v1/voice/tts              # 文字转语音
POST   /api/v1/voice/stt              # 语音转文字
WS     /api/v1/ws/voice/{session_id}  # 实时语音对话流
```

---

## 六、前端设计

### 6.1 微信小程序页面结构

```
pages/
├── index/          # 首页（今日聊天入口 + 话题列表）
├── chat/           # 聊天页面（文字/语音切换）
├── topics/
│   ├── list/       # 话题列表
│   ├── add/        # 添加话题（选类别+填关键词+设时间）
│   └── schedule/   # 时间安排编辑
├── history/        # 历史聊天记录
├── family/         # 家人管理
└── profile/        # 个人设置
```

### 6.2 Web管理端（家人后台）

```
pages/
├── Dashboard       # 概览（老人今日聊天状态）
├── Topics          # 话题配置与管理
├── Schedule        # 时间安排管理
├── ChatHistory     # 聊天记录查看
└── Settings        # 账号与通知设置
```

### 6.3 适老化设计规范

- 字体：最小18px，重要内容24px+
- 按钮：最小触控区域 48×48px
- 颜色：高对比度，避免依赖颜色区分信息（色盲友好）
- 操作：核心功能不超过3步完成
- 反馈：每个操作有明确的视觉/声音反馈

---

## 七、部署架构

### 7.1 MVP阶段（单机 Docker Compose）

```yaml
services:
  api:        FastAPI 后端
  worker:     Celery 任务队列（定时检索）
  scheduler:  APScheduler 定时触发器
  postgres:   PostgreSQL 数据库
  redis:      Redis 缓存+队列
  chroma:     向量数据库
  nginx:      反向代理

# 推荐配置
服务器：2核4G（约60元/月）
存储：50GB SSD
```

### 7.2 成长阶段（微服务化，用户量1000+）

- API服务水平扩展（2-3实例）
- 任务队列独立部署
- 数据库读写分离
- CDN 加速语音文件
- 成本预估：约500-1000元/月

---

## 八、分阶段开发计划

### Phase 1：文字版 MVP（2-3 周）

**目标**：核心流程跑通，可供测试用户试用

- [ ] 用户注册/登录（手机验证码）
- [ ] 话题创建与管理（支持4种类别）
- [ ] 定时任务：每日检索 + 去重 + 生成大纲
- [ ] WebSocket 实时文字聊天
- [ ] 基础Web界面（话题配置 + 聊天）
- [ ] 聊天历史存储与查看

### Phase 2：语音版（6-8 周）

**目标**：支持实时语音对话，适老化体验

- [ ] TTS 集成（阿里云/火山引擎，多音色选择）
- [ ] STT 集成（FunASR，支持普通话/方言）
- [ ] 实时语音流 WebSocket
- [ ] 微信小程序版本
- [ ] 家人管理后台
- [ ] 适老化UI优化

### Phase 3：智能扩展（3个月+）

**目标**：话题自动扩展，个性化增强

- [ ] 话题关联图谱（LLM自动扩展相关话题）
- [ ] 用户兴趣分析（基于聊天历史）
- [ ] 情绪感知（识别用户情绪，调整对话风格）
- [ ] 多语言/方言支持

---

## 九、成本估算

### 月度运营成本（MVP阶段，约100用户）

| 项目 | 费用/月 |
|------|---------|
| 云服务器（2核4G） | 60元 |
| LLM API（qwen-max） | 约200元 |
| 搜索API（Tavily） | 约100元 |
| TTS（Phase2） | 约50元 |
| 短信验证码 | 约30元 |
| **合计** | **约440元/月** |

### 商业化定价建议

| 版本 | 价格 | 权益 |
|------|------|------|
| 免费版 | 0元 | 1个话题，每周3次 |
| 家庭版 | 39元/月 | 10个话题，每日触发，家人后台 |
| 年付 | 299元/年 | 家庭版全部权益，省169元 |

---

## 十、关键风险与应对

| 风险 | 应对方案 |
|------|---------|
| 老人不会用小程序 | 家人代配置，老人只需会点"开始聊天"一个按钮 |
| LLM内容出现不当信息 | 增加内容过滤层，用户反馈一键屏蔽 |
| 搜索结果质量差 | 多源检索（至少3个来源），LLM交叉验证 |
| 用户忘记与AI聊天 | 微信服务号推送提醒 |
| 对话突然中断 | 会话状态持久化，支持随时续聊 |
| 用户数据隐私 | 话题和聊天内容加密存储，明确不用于训练第三方模型 |

---

## 十一、项目目录结构

```
xiaoqian/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI路由
│   │   ├── agents/         # LangGraph Agent
│   │   ├── models/         # SQLAlchemy模型
│   │   ├── schemas/        # Pydantic Schema
│   │   ├── services/       # 业务逻辑
│   │   ├── tasks/          # Celery定时任务
│   │   └── core/           # 配置、安全、数据库
│   ├── migrations/         # Alembic迁移文件
│   └── pyproject.toml
├── frontend/
│   ├── web/                # Vue 3 管理后台
│   └── miniprogram/        # 微信小程序
├── docker-compose.yml
└── README.md
```
