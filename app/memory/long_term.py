# 长期记忆的存储与读取
# 不同会话可以共享同一个用户的长期记忆。
### 1. 导入依赖

import redis

from core.config import redis_url
#⭐⭐⭐短期记忆通过 Checkpointer 接入 Agent；长期记忆通过 Tools 接入 Agent。

### 2. 创建 Redis 连接对象
redis_client = redis.Redis.from_url(
    redis_url,      #从config文件中导入的redis_url = "redis://192.168.88.130:6379"
    decode_responses=True   #读取 Redis 数据时，自动将字节数据解码为字符串。
)
    #⭐⭐⭐redis.Redis.from_url()：根据 Redis 连接地址创建 Redis 客户端对象。
"""
两种创建 Redis 连接对象的方式:
    1、通过 host、port 等参数创建
        redis_client = redis.Redis(
                            host="192.168.88.130",
                            port=6379,
                            decode_responses=True,
                        )
    2、通过 Redis URL 创建
        redis_client = redis.Redis.from_url(
                            redis_url,
                            decode_responses=True
                        )
两种方式的联系
    1. 都是使用 redis.Redis 创建 Redis 客户端对象。
    2. 都可以连接同一个 Redis 服务器。
    3. 都可以通过创建的客户端对象执行 Redis 操作，例如 hset()、hgetall()、set()、get()。
    4. 都可以设置 decode_responses=True，让返回结果自动解码为字符串

对比	        redis.Redis()	    redis.Redis.from_url()
创建方式	    直接指定连接参数	    解析 Redis URL
主机地址	    host 参数	        URL 中的主机地址
端口	        port 参数	        URL 中的端口
配置位置	    可以直接写在代码中	    可以统一放在配置文件中
适用场景	    连接参数简单、固定	    需要统一管理连接配置

本项目中选择 from_url()，是为了让长期记忆模块和短期记忆模块共用config.py中的 redis_url，统一管理 Redis 连接配置。
"""

### 3. 保存用户长期记忆
#目前只要求传入一个字典，并没有明确规定字典中应该有哪些字段、每个字段应该是什么类型。定义数据类型在memory_schema.py文件中
def save_user_memory(user_id: str, memory: dict):
    key = f"p04long_memory:{user_id}"  # user_id：用户唯一标识，key：Redis Hash 的键，例如 user_memory:1001。
    redis_client.hset(key, mapping=memory)     # memory：需要保存的用户资料，例如 {"name": "小张", "interest": "学习 Python"}
    # .hset()：将用户资料保存到 Redis Hash 中
    """
    ⭐
    r.hset() 是 Redis Python 客户端提供的方法，用于向 Redis Hash 中写入数据。
    里面有2个参数:
        1、key
            表示 Redis Hash 的键，也就是存储数据的名称。
        2、mapping
            表示要写入的字段和值，类型是字典。
        如
            user_memory:1001                #也就是key
                name       → 小张
                interest   → 学习 Python
    """



### 4. 读取用户长期记忆
def get_user_memory(user_id: str):
    key = f"p04long_memory:{user_id}"
    memory = redis_client.hgetall(key)     #r.hgetall(key)：读取指定 Redis Hash 中的所有字段和值。
    return memory               #将读取到的用户资料返回