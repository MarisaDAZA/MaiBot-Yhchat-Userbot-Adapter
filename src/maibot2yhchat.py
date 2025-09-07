import asyncio
import aiohttp
from uuid import uuid4
from .logger import logger
from maim_message import MessageBase, Router, RouteConfig, TargetConfig
from .config import config
from . import http.session
from .proto.yhchat_pb2 import ChatType, SendMessage
from .emoji import get_emoji_url

# 定义连接目标 (例如 MaimCore)
route_config = RouteConfig(
    route_config={
        'yhchat': TargetConfig(
            url=f'ws://{config['maibot']['host']}:{config['maibot']['port']}/ws',
        )
    }
)
# 创建 Router 实例
router = Router(route_config)

async def send_to_yhchat(chat_id:str, chat_type:int, content_type:str, content:str):
    body = SendMessage(
        messageId = uuid4().hex,
        chatId = chat_id,
        chatType = chat_type,
    )
    if content_type = 'text':
        body.contentType = 1
        body.content.text = content
        logger.info(f'【发送消息】{text}')
    elif content_type = 'emoji':
        body.contentType = 7
        emoji_url = get_emoji_url(content)
        body.content.emojiUrl = emoji_url
        logger.info(f'【发送表情】{emoji_url}')
    else:
        logger.warning(f'MaimCore 返回不支持的消息类型：{message.message_segment.type}')
        return
    await http.session.post('https://chat-go.jwzhd.com/v1/msg/send-message', data=body.SerializeToString())

async def receive_from_maimcore(message_dict: dict):
    '''
    定义如何处理从 MaimCore 收到的消息
    '''
    try:
        message=MessageBase.from_dict(message_dict)
        if message.message_info.group_info:
            await send_to_yhchat(message.message_info.group_info.group_id, ChatType.GROUP, message.message_segment.type, message.message_segment.data)
        else:
            await send_to_yhchat(message.message_info.user_info.user_id, ChatType.USER, message.message_segment.type, message.message_segment.data)
    except Exception as e: # byd不加这玩意出错了根本不报错
        logger.exception(e)

# 注册消息处理器
# Router 会自动将从对应 platform 收到的消息传递给注册的处理器
router.register_class_handler(receive_from_maimcore)
