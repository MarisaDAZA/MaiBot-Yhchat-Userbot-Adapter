import aiohttp
from loguru import logger
from .config import config

_session = None

def get_shared_session():
    global _session
    if _session or _session.closed:
        logger.debug('新建 Client Session')
        _session = aiohttp.ClientSession()
        _session.headers.update({
            'User-Agent': 'android 1.4.89',
            'Accept': 'application/x-protobuf',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-protobuf',
            'Token': config['yhchat']['token']
        })
    return _session

async def close_shared_session():
    global _session
    if _session and not _session.closed:
        logger.debug('关闭 Client Session')
        await _session.close()
