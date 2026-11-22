
### 1. 导入依赖
from fastapi import APIRouter
from agents.agent import get_agent
from schemas.chat_schema import ChatRequest


### 2. 创建路由对象
router = APIRouter()
#APIRouter的核心用途——把路由拆分到不同文件
#创建 router后，路由函数就可以写在其他文件（如主应用app写在main.py文件中，而路由函数写在chat.py）里了，并用 @router 装饰。

### 3. 定义聊天接口
@router.get("/")
def hello():
    return "welcome, 请访问[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)"

@router.post("/chat")
def chat(request: ChatRequest):     # ChatRequest上传格式要求
    #request是先经过 FastAPI 和 Pydantic 的解析、校验，然后转换成 ChatRequest 对象，才传入 chat() 函数
    #如： request = ChatRequest(
    #                           message="你好",
    #                           thread_id="session_001"
    #                           )

    ### 4. 组合用户 ID 和会话 ID
    checkpoint_thread_id = f"{request.user_id}:{request.thread_id}"
    # checkpoint_thread_id：决定读取哪一份短期记忆。
    # user_id：决定读取哪一份长期记忆。


    ### 5. 获取 Agent
    with get_agent() as agent:

        ### 6. 调用 Agent
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.message      #request为ChatRequest对象
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": checkpoint_thread_id,
                    "user_id": request.user_id
                }
            }
        )
        # thread_id区分短期会话
        # user_id区分长期记忆所属用户
        print("Agent 完整返回结果：", result["messages"])

        ### 7. 返回 AI 回复
        return {
            "answer": result["messages"][-1].content
        }

"""
客户端发送 POST /chat
        │
        ▼
FastAPI 接收 JSON
        │
        ▼
ChatRequest 校验数据
        │
        ▼
chat() 获取 user_id、message 和 thread_id
        │
        ▼
get_agent() 获取 Agent
        │
        ▼
agent.invoke()
        │
        ├── RedisSaver 恢复短期记忆
        │
        ├── Agent 根据需要调用长期记忆工具
        │
        └── LLM 生成回答
        │
        ▼
返回 JSON 响应
"""


