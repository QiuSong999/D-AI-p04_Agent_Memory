#定义长期记忆的数据结构

### 1. 导入依赖
from pydantic import BaseModel, Field, ConfigDict


### 2. 定义用户长期记忆的数据结构
class UserMemory(BaseModel):
    """保存用户的长期记忆。"""

    model_config = ConfigDict(extra="forbid")
    # ⭐⭐ 拒绝未定义的字段

    name: str | None = Field(
                                default=None,
                                description="用户的姓名或称呼"
                            )

    pet: str | None = Field(
                                default=None,
                                description="用户的宠物信息，例如宠物种类和名字"
                            )

    interest: str | None = Field(
                                default=None,
                                description="用户长期的兴趣、爱好或技术方向"
                            )

    career_goal: str | None = Field(
                                default=None,
                                description="用户的职业目标或长期发展方向"
                            )

"""
模块	                    负责什么
memory_schema.py	规定长期记忆的数据结构，并提供数据校验
long_term.py	    将长期记忆写入 Redis，或从 Redis 读取
"""