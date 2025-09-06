import aiohttp
from loguru import logger
from .config import config

session = None

async def setup_session():
    global session
    logger.debug('新建 Client Session')
    session = aiohttp.ClientSession()
    session.headers.update({
        'User-Agent': 'android 1.4.89',
        'Accept': 'application/x-protobuf',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-protobuf',
        'Token': config['yhchat']['token']
    })

async def close_session():
    global session
    logger.debug('关闭 Client Session')
    await session.close()
