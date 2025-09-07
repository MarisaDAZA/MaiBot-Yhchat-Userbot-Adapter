import aiohttp
from loguru import logger
from .config import config

async def setup_session():
    global session
    logger.debug('新建 Http Session')
    session = aiohttp.ClientSession()
    session.headers.update({
        'Token': config['yhchat']['token'],
        'Referer': 'http://myapp.jwznb.com'
    })

async def close_session():
    global session
    logger.debug('关闭 Http Session')
    await session.close()
