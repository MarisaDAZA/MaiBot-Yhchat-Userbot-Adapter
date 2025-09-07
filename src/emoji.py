import json
import base64
import hashlib
import filetype
from . import http

async def get_image_base64(url: str) -> str:
    """获取图片/表情包的Base64"""
    async with http.session.get(url) as r:
        image_bytes = await r.read()
    return base64.b64encode(image_bytes).decode()

def get_emoji_url(image_base64: str) -> str:
    image_bytes = base64.b64decode(image_base64)
    md5 = hashlib.md5(image_bytes).hexdigest()
    ext = filetype.guess(image_bytes).extension
    return f'expression/{md5}.{ext}'
