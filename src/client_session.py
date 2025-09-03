import aiohttp
from .config import config

session = None

async def set_global_session():
    session = aiohttp.ClientSession()
    session.headers.update({
        'User-Agent': 'android 1.4.89',
        'Accept': 'application/x-protobuf',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-protobuf',
        'Token': config['yhchat']['token']
    })