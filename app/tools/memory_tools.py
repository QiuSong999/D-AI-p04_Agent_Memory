"""
已经有两个模块：
    - long_term.py：负责将用户记忆保存到 Redis，以及从 Redis 查询记忆。
    - memory_schema.py：规定长期记忆的数据结构。
但是，Agent 不能仅凭这两个模块就自动调用 Redis。

我们需要把 Redis 的读写函数封装成 Agent 能够识别和调用的工具。

这就是 memory_tools.py 的作用。

"""

### 1. 导入依赖
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from memory.long_term import get_user_memory, save_user_memory
from schemas.memory_schema import UserMemory    # 长期记忆的保存模板


### 2. 定义查询用户长期记忆的工具
@tool
def search_user_memory(config: RunnableConfig) -> dict:
    """
    根据当前用户 ID 查询用户保存的长期记忆。
    user_id 从 Agent 的运行时配置中获取。
    """
    user_id = config["configurable"]["user_id"]
    return get_user_memory(user_id)


### 3. 定义保存用户长期记忆的工具
@tool
def save_user_memory_tool(memory: dict, config: RunnableConfig) -> str:
    """
    根据当前用户 ID 保存用户的长期记忆。
    user_id 从 Agent 的运行时配置中获取。
    memory：需要保存的用户资料。
    """

    ### 4. 使用 UserMemory 校验数据
    validated_memory = UserMemory.model_validate(memory)    # 执行长期记忆数据校验

    """
    ⭐⭐⭐模板类.model_validate(被校验的字典)
    .model_validate() 是干啥的？
        Pydantic（V2版）提供的数据校验与清洗方法。把传进来的“野生字典”，按你定义的 Class 模板
        进行校验，最后生成一个标准的 Pydantic 对象。

        核心作用（为什么必须用？）
        - 校验字段：Class 里没定义的字段会根据模型配置处理。
        - 安检：类型不符合要求时，会产生校验错误。
        - 补全：没传的字段，自动按 Class 里的默认值（如 None）补全。
    """

    ### 5. 将校验后的数据转换成字典
    memory_data = validated_memory.model_dump(exclude_none=True)

    ### 6. 保存到 Redis
    user_id = config["configurable"]["user_id"]
    save_user_memory(user_id, memory_data)

    return "用户长期记忆保存成功。"


"""
    agent.py
Agent 根据用户需求决定是否调用工具
            ↓
    memory_tools.py
将查询和保存函数封装成 Agent 工具
            ↓
    long_term.py
    执行 Redis 数据读写
            ↓
         Redis
    实际保存用户长期记忆
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
两种记忆机制对比
对比项                     短期记忆               长期记忆
实现机制                        RedisSaver         Redis Hash
管理者                     LangGraph          我们自己编写的代码
是否注册工具                  不需要                需要
是否需要Agent主动决定读写     不需要                需要
标识                          thread_id          user_id
主要作用                        保存会话上下文            保存跨会话的用户资料

短期记忆是 LangGraph 提供的状态管理能力，长期记忆是我们通过工具赋予 Agent 的外部数据读写能力。
所以，只有两个工具是合理的，不需要再为短期记忆注册工具。
"""