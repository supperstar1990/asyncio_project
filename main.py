"""
"""
# main.py
import asyncio
from config.settings import API_ENDPOINTS, CRAWL_TARGETS
from core.api_client import batch_api_calls
from core.async_crawler import async_crawl
from utils.logger import logger

async def main():
    """
    主函数：演示批量API调用 + 异步爬虫 + 并发控制
    """
    logger.info("===== 开始执行异步任务 =====")
    
    # 1. 演示批量API调用
    logger.info("\n--- 第一步：批量API调用 ---")
    # 构造API端点列表（示例：调用/posts/1 到 /posts/5）
    api_endpoints = [f"{API_ENDPOINTS['posts']}/{i}" for i in range(1, 6)]
    api_results = await batch_api_calls(api_endpoints)
    # 打印部分结果
    for i, result in enumerate(api_results[:2]):
        if result:
            logger.info(f"API结果示例 {i+1}: {result.get('title', '无标题')}")
    
    # 2. 演示异步爬虫
    logger.info("\n--- 第二步：异步爬虫 ---")
    crawl_results = await async_crawl(CRAWL_TARGETS)
    # 打印部分结果
    for result in crawl_results:
        if result.get("status") == 200:
            logger.info(f"爬虫结果示例: URL={result['url']}，响应片段={result['data'][:50]}...")
    
    logger.info("\n===== 所有异步任务执行完成 =====")

if __name__ == "__main__":
    # 解决Windows下asyncio的事件循环问题（跨平台兼容）
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            # 备用事件循环启动方式
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())