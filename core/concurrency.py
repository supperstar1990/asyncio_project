"""
"""
# core/concurrency.py
import asyncio
from config.settings import MAX_CONCURRENCY
from utils.logger import logger

# 创建信号量对象，控制最大并发数
semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

async def limited_concurrency(func, *args, **kwargs):
    """
    带并发限制的函数执行装饰器/工具函数
    :param func: 要执行的异步函数
    :param args: 函数参数
    :param kwargs: 函数关键字参数
    :return: 函数执行结果
    """
    async with semaphore:  # 自动获取/释放信号量，控制并发数
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"执行函数 {func.__name__} 出错: {str(e)}")
            raise e
        