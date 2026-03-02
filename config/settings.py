"""
全局文件配置
"""
import os

MAX_CONCURRENCY = 10
TIMEOUT = 30

#API配置
API_BASE_URL = "https://jsonplaceholder.typicode.com"
API_ENDPOINTS = {
    "posts":"\nposts"
}

# 爬虫配置（示例：测试目标）
CRAWL_TARGETS = [
    "https://httpbin.org/get?page=1",
    "https://httpbin.org/get?page=2",
    "https://httpbin.org/get?page=3",
    # 可扩展更多目标
]

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "app.log")