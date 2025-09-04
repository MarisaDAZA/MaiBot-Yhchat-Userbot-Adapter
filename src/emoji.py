import json
from os import path
from loguru import logger
import base64
from .client_session import get_image_session

if path.exists('emoji_base64.json'):
    with open('emoji_base64.json', 'r', encoding='utf-8') as f:
        emoji_base64 = json.load(f)
else:
    emoji_base64 = {}

async def get_image_base64(url: str) -> str:
    """获取图片/表情包的Base64"""
    session = get_image_session
    async with session.get(url) as r:
        image_bytes = r.read()
    return base64.b64encode(image_bytes).decode()