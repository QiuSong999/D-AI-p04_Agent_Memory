# P04 Agent Memory 多用户多会话记忆系统

## 一、项目简介

本项目基于 LangChain、LangGraph 和 Redis 实现一个支持多用户、多会话的 AI Agent 记忆系统。

通过短期记忆和长期记忆相结合，使 Agent 能够在不同会话中恢复历史对话，并跨会话记住用户的个人信息。

项目使用 FastAPI 提供聊天接口，支持通过 `user_id` 区分用户，通过 `thread_id` 区分会话。

## 二、技术栈

- Python 3.12
- FastAPI
- Pydantic
- LangChain
- LangGraph
- Redis
- RedisSaver
- ChatOpenAI
- DashScope（通义千问）

## 三、核心功能

### 1. 短期记忆（Short-term Memory）

使用 LangGraph Checkpointer 实现短期记忆持久化。

- 使用 RedisSaver 保存 Agent 执行过程中的状态。
- 使用 thread_id 区分不同会话。
- 相同 thread_id 可以恢复当前会话的历史状态。
- 不同 thread_id 的短期记忆相互隔离。

### 2. 长期记忆（Long-term Memory）

使用 Redis Hash 实现用户长期记忆存储。

Redis Key 格式：
user_memory:{user_id}

长期记忆包含以下字段：

- `name`：用户姓名
- `pet`：宠物信息
- `interest`：兴趣爱好
- `career_goal`：职业目标

通过 Agent Tools 实现长期记忆的查询和保存：

- `search_user_memory`：查询用户长期记忆。
- `save_user_memory_tool`：保存用户长期记忆。

### 3. 多用户、多会话隔离

通过 `user_id` 和 `thread_id` 实现用户与会话的区分：

- 相同 `user_id`、不同 `thread_id`：共享长期记忆，短期记忆相互隔离。
- 不同 `user_id`：长期记忆相互隔离。
- 相同 `thread_id`：可以继续之前的对话。

### 4. FastAPI 接口

使用 FastAPI 提供聊天接口。

聊天请求包含：

- `user_id`：用户标识
- `thread_id`：会话标识
- `message`：用户消息

提供 API 文档页面，方便接口测试。

## 四、项目结构

p04_Agent_Memory/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── llm.py
│   │
│   ├── agents/
│   │   └── agent.py
│   │
│   ├── memory/
│   │   ├── short_term.py
│   │   └── long_term.py
│   │
│   ├── tools/
│   │   └── memory_tools.py
│   │
│   ├── schemas/
│   │   ├── chat_schema.py
│   │   └── memory_schema.py
│   │
│   └── api/
│       └── chat.py
│
├── .env
├── .gitignore
└── README.md


## 五、运行方式

### 1. 配置环境变量

在项目根目录创建 .env 文件，配置 DashScope API Key：
env
dashscope_api_key=你的API_KEY


### 2. 启动 Redis

确保 Redis 服务正常运行，并在项目配置文件中设置正确的 Redis 连接地址。

### 3. 启动项目

使用 PyCharm 运行：
app/main.py


### 4. 访问接口文档

项目启动后访问：
http://127.0.0.1:8000/docs


通过 Swagger UI 测试聊天接口。

## 六、项目收获

通过本项目，掌握了：

1. LangGraph Checkpointer 的工作机制。
2. 使用 RedisSaver 实现 Agent 短期记忆持久化。
3. 使用 Redis Hash 实现用户长期记忆存储。
4. 使用 LangChain Tools 实现记忆查询与保存。
5. 使用 `user_id` 和 `thread_id` 实现多用户、多会话记忆隔离。
6. 使用 FastAPI 封装 Agent 服务接口。
7. 理解短期记忆与长期记忆在 Agent 应用中的区别。

## 七、项目地址

GitHub：https://github.com/QiuSong999/D-AI-p04_Agent_Memory