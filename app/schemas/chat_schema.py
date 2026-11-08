
from pydantic import BaseModel, Field


### 1. 定义聊天请求模型
# 定义一个 Pydantic 数据模型，专门描述客户端发送聊天请求时需要提供的数据。
class ChatRequest(BaseModel):
    """定义客户端发送的聊天请求。"""

    user_id: str = Field(
        min_length=1,
        description="当前用户的唯一 ID"
    )

    message: str = Field(
        min_length=1,
        description="用户本轮发送的消息"
    )

    thread_id: str = Field(
        min_length=1,
        description="当前对话的会话 ID"
    )
