import aiohttp
from .config import config

_session = None

def get_shared_session():
    global _session
    if _session is None or _session.closed:
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
        await _session.close()
        _session = None