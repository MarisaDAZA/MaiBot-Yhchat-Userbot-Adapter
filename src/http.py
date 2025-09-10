import aiohttp
from loguru import logger
from .config import config

async def setup_session():
    global session
    logger.debug('新建 Http Session')
    session = aiohttp.ClientSession()

async def close_session():
    global session
    logger.debug('关闭 Http Session')
    await session.close()
