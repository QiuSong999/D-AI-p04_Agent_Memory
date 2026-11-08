### 0. 导入依赖
from langchain.agents import create_agent
from core.llm import llm

# search_user_memory：查询长期记忆。save_user_memory_tool：保存长期记忆。两个工具
from tools.memory_tools import search_user_memory, save_user_memory_tool

from memory.short_term import get_checkpointer
from contextlib import contextmanager


### 1. 创建工具列表
tools = [search_user_memory, save_user_memory_tool]     #两个工具

### 2. 定义 Agent 获取函数
@contextmanager
def get_agent():
    with get_checkpointer() as checkpointer:
        agent = create_agent(
            model=llm,
            tools=tools,
            checkpointer=checkpointer,
            system_prompt="""
            你是一个具有长期记忆能力的 AI 助手。

            1. 当用户明确要求你记住某项个人信息时，
               调用 save_user_memory_tool，将信息保存到当前用户的长期记忆。

            2. 当用户询问之前保存的个人信息时，
               调用 search_user_memory 查询当前用户的长期记忆，
               根据查询结果回答。

            3. 不要声称已经保存信息，除非保存工具调用成功。

            4. 临时编号、验证码、一次性数字以及当前任务中的临时信息，
               只保留在短期记忆中，不得调用 save_user_memory_tool 保存到长期记忆。

            5. 只有用户明确要求保存长期有效的个人信息，
               例如姓名、宠物、兴趣、职业目标时，才调用长期记忆保存工具。

            6. 不得为了保存不符合字段含义的信息，
               将其强行写入 name、pet、interest 或 career_goal 字段。

            7. 用户身份由系统运行配置提供，
               不得自行编造或修改用户 ID。
            """
        )
        yield agent
"""
    执行过程如下：
1. 进入 get_agent()
   执行 with get_checkpointer()，获取 RedisSaver。建立并保持 Redis 连接。
        ↓
2. 创建 Agent
   将 checkpointer 传给 create_agent()。让 Agent 具备短期记忆能力。
        ↓
3. 执行 yield agent
   将创建好的 Agent 交给外部的 with 语句使用。
    此时，get_agent() 暂停执行，但内部的 with get_checkpointer() 并没有退出，
    因此 RedisSaver 的连接资源仍然保持开启。
        ↓
4. 外部执行 agent.invoke()
    Agent 使用 Checkpointer 读取和保存当前会话的短期记忆。
        ↓
5. 退出外部 with
   外部代码执行完毕后，get_agent() 从 yield agent 暂停的位置继续执行，
   随后退出内部的 with get_checkpointer()，释放 RedisSaver 的连接资源。


~~~~~~~~~~~~~~~~~~~~~
这里配置@contextmanager 是为了后续调用：
    with get_agent() as agent:
        result = agent.invoke(...)
        
如果不配置，定义为普通函数：
    def get_agent():
        with get_checkpointer() as checkpointer:
            agent = create_agent(
                model=llm,
                tools=tools,
                checkpointer=checkpointer,
                system_prompt="..."
            )
            return agent
问题在于：执行 return agent 时，函数立即退出。因此，内部的：
    with get_checkpointer() as checkpointer:
    也会立即退出，RedisSaver 的上下文资源随之关闭。
    但我们返回的 Agent 还需要使用这个 Checkpointer。
    这样就可能导致 Agent 使用 Checkpointer 时，底层连接资源已经关闭。
~~~~~~~~~~~~~~~~~~~

"""