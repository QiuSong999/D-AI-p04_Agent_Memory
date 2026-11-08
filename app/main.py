
### 1. 导入依赖
from fastapi import FastAPI
from api.chat import router

import uvicorn


### 2. 创建 FastAPI 应用
app = FastAPI(
        title="P04 Agent Memory API",                   # API 项目名称
        description="具有短期记忆和长期记忆能力的 Agent",    # API 项目描述
        version="1.0.0"     #API 版本号
    )
#⭐这三个参数都是用于描述 API 项目的，都会显示在自动生成的接口文档页面 /docs 上


### 3. 注册聊天路由
app.include_router(router)  #括号内的router是从chat.py文件中导入的。#将 router 中定义的接口添加到 app 主应用中。
# include_router(...)是FastAPI 提供的方法。理解成：把一个 router 加入到这个 FastAPI 应用中。

### 4. 启动 FastAPI 服务
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )

"""
  main.py
FastAPI 主应用 app
    ↓
app.include_router(router)
注册路由
    ↓
chat.py
APIRouter 对象 router
    ↓
POST /chat
聊天接口
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                  客户端
                    │
                    ▼
               FastAPI API
                    │
           接收 user_id、thread_id
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     短期记忆标识          长期记忆标识
          │                   │
   user_id:thread_id        user_id
          │                   │
          ▼                   ▼
      RedisSaver           Agent Tools
          │                   │
          ▼                   ▼
    Redis Checkpoint       Redis Hash
          │                   │
          ▼                   ▼
     会话历史记录          用户长期资料
"""