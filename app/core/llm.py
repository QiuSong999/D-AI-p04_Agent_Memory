### 1. 导入依赖
from langchain_openai import ChatOpenAI
from core.config import (       # 从config.py文件中读取配置
        dashscope_api_key,
        llm_model,
        llm_base_url
      )


### 2. 创建大模型对象
llm = ChatOpenAI(
    model=llm_model,
    base_url=llm_base_url,
    api_key=dashscope_api_key,  # 3个参数都是从config.py导入
)