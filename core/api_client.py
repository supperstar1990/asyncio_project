"""
"""
# core/api_client.py
import aiohttp
import asyncio
from config.settings import API_BASE_URL, TIMEOUT
from core.concurrency import limited_concurrency
from utils.logger import logger

async def fetch_api(session, endpoint, params=None):
    """
    单个API请求的异步函数
    :param session: aiohttp.ClientSession对象（复用连接，提升性能）
    :param endpoint: API端点（如/posts/1）
    :param params: 请求参数
    :return: API返回的JSON数据
    """
    url = f"{API_BASE_URL}{endpoint}"
    try:
        async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as response:
            response.raise_for_status()  # 抛出HTTP错误（如404/500）
            data = await response.json()
            logger.info(f"成功调用API: {url}，状态码: {response.status}")
            return data
    except aiohttp.ClientError as e:
        logger.error(f"API调用失败 {url}: {str(e)}")
        return None

async def batch_api_calls(endpoints, params_list=None):
    """
    批量API调用（带并发控制）
    :param endpoints: API端点列表
    :param params_list: 每个端点对应的参数列表（可选）
    :return: 所有API调用结果的列表
    """
    if params_list is None:
        params_list = [None] * len(endpoints)
    
    # 校验输入长度
    if len(endpoints) != len(params_list):
        raise ValueError("endpoints和params_list长度必须一致")
    
    # 创建复用的ClientSession（推荐做法，减少连接开销）
    async with aiohttp.ClientSession() as session:
        # 构建任务列表（通过limited_concurrency控制并发）
        tasks = [
            limited_concurrency(fetch_api, session, endpoint, params)
            for endpoint, params in zip(endpoints, params_list)
        ]
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=False)
        logger.info(f"批量API调用完成，共执行 {len(results)} 个请求")
        return results
