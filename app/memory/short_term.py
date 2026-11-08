# ★★短期记忆持久化，要存进Redis★★

### 1. 导入依赖
from contextlib import contextmanager
from langgraph.checkpoint.redis import RedisSaver
# RedisSaver：Checkpointer 的 Redis 实现，负责将这些状态持久化到 Redis。
from core.config import redis_url


### 2. 创建短期记忆 Checkpointer
@contextmanager     #⭐把自己定义的函数get_checkpointer具备 with 上下文管理器的使用方式。目的是让
                    # agent.py文件中的 with get_checkpointer() as checkpointer: 可以使用本函数
def get_checkpointer():
    with RedisSaver.from_conn_string(redis_url) as checkpointer:
        #RedisSaver.from_conn_string(redis_url) 返回的对象本身就支持上下文管理协议。
        #⭐根据Redis地址创建RedisSaver对象。

        checkpointer.setup()    #⭐初始化 Redis Checkpointer 所需的存储结构
        yield checkpointer      #⭐把创建好的 checkpointer 返回给外部使用，同时暂停函数执行（换成return就是结束函数了）
#⭐⭐⭐RedisSaver.from_conn_string()是LangGraph提供的一个类方法，用来根据Redis连接地址创建 RedisSaver 对象
#⭐Agent 使用 checkpointer 期间，RedisSaver 必须保持开启，所以使用yield而不是return
"""
⭐⭐⭐
之前学的
    with open("a.txt", "rb") as src_f:
        data = src_f.read()
        
这里的 open() 是 Python 已经提供的函数，它本身就支持 with
但是：get_checkpointer() 是我们自己写的普通函数。普通函数默认不能直接放在 with 后面。
所以我们使用 @contextmanager，让自己写的函数也能支持 with。
"""

"""
api/chat.py
    │
    │ 接收 user_id、thread_id
    ▼
组合 checkpoint_thread_id
    │
    ▼
agent.py
    │
    │ 创建 Agent，传入 checkpointer
    ▼
RedisSaver
    │
    │ 根据 thread_id 读取、保存状态
    ▼
Redis
"""