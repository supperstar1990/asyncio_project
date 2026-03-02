"""
"""
# core/async_crawler.py
import aiohttp
import asyncio
from config.settings import TIMEOUT
from core.concurrency import limited_concurrency
from utils.logger import logger

async def crawl_url(session, url):
    """
    单个URL的异步爬取函数
    :param session: aiohttp.ClientSession对象
    :param url: 要爬取的URL
    :return: 爬取的响应数据
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as response:
            response.raise_for_status()
            # 示例：返回文本数据（可根据需求改为JSON/二进制等）
            data = await response.text()
            logger.info(f"成功爬取URL: {url}，响应长度: {len(data)} 字符")
            return {
                "url": url,
                "status": response.status,
                "data": data[:200]  # 只保留前200字符，避免数据过大
            }
    except aiohttp.ClientError as e:
        logger.error(f"爬取URL失败 {url}: {str(e)}")
        return {
            "url": url,
            "status": None,
            "error": str(e)
        }

async def async_crawl(urls):
    """
    异步批量爬取URL（带并发控制）
    :param urls: 要爬取的URL列表
    :return: 所有爬取结果的列表
    """
    async with aiohttp.ClientSession() as session:
        # 构建任务列表（通过limited_concurrency控制并发）
        tasks = [
            limited_concurrency(crawl_url, session, url)
            for url in urls
        ]
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=False)
        logger.info(f"异步爬虫完成，共爬取 {len(results)} 个URL")
        return results