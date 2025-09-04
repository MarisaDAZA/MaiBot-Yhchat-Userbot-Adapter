import aiohttp
from loguru import logger
from .config import config

_protobuf_session = None
_image_session = None

def get_protobuf_session():
    global _protobuf_session
    if _protobuf_session is None or _protobuf_session.closed:
        _protobuf_session = aiohttp.ClientSession()
        _protobuf_session.headers.update({
            'User-Agent': 'android 1.4.89',
            'Accept': 'application/x-protobuf',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-protobuf',
            'Token': config['yhchat']['token']
        })
    return _protobuf_session

def get_image_session():
    global _image_session
    if _image_session is None or _image_session.closed:
        _image_session = aiohttp.ClientSession()
        _image_session.headers.update({
            'User-Agent': 'Dart/3.9 (dart:io)',
            'Accept-Encoding': 'gzip',
            'Referer': 'http://myapp.jwznb.com'
        })
    return _image_session

async def close_sessions():
    global _protobuf_session
    if _protobuf_session and not _protobuf_session.closed:
        await _protobuf_session.close()
        logger('已关闭 protobuf session')
    if _image_session and not _image_session.closed:
        await _image_session.close()
        logger('已关闭 image session')
    