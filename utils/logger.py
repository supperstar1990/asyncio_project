"""

"""
# utils/logger.py
from loguru import logger
import os
from config.settings import LOG_LEVEL, LOG_FILE

# 移除默认日志处理器
logger.remove()

# 添加控制台输出
logger.add(
    sink=lambda msg: print(msg, end=""),
    level=LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# 添加文件输出（确保data目录存在）
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logger.add(
    sink=LOG_FILE,
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="10 MB",  # 日志文件达到10MB时分割
    retention="7 days"  # 保留7天日志
)

# 导出logger供其他模块使用
__all__ = ["logger"]