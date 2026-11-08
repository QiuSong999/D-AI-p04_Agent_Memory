### 1. 导入依赖
import os
from pathlib import Path
from dotenv import load_dotenv


### 2. 获取项目根目录
base_dir = Path(__file__).resolve().parent.parent.parent
# 第一个 .parent：返回 core/。第二个 .parent：返回 app/。第三个 .parent：返回 p04_Agent_Memory/

### 3. 加载 .env 文件
env_path = base_dir / ".env"    # 获取env文件的目录
load_dotenv(env_path)           # 加载

### 4. 获取dashscope_api_key API key
dashscope_api_key = os.getenv("dashscope_api_key")

if not dashscope_api_key:
    raise ValueError("没有读取到 dashscope_api_key，请检查 .env 文件。")


### 5. 定义模型配置
llm_model = "qwen-plus"

llm_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"


### 6. 定义 Redis 配置
redis_url = "redis://192.168.88.130:6379"