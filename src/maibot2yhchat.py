import asyncio
import aiohttp
from uuid import uuid4
from loguru import logger
from maim_message import MessageBase, Router, RouteConfig, TargetConfig
from .config import config
from .proto.yhchat_pb2 import ChatType, SendMessage
from .client_session import session, set_global_session

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

async def send_to_yhchat(chat_id:str, chat_type:int, text:str):
    body = SendMessage(
        messageId = uuid4().hex,
        chatId = chat_id,
        chatType = chat_type,
        contentType = 1
    )
    body.content.text = text
    await session.post('https://chat-go.jwzhd.com/v1/msg/send-message', data=body.SerializeToString())
    logger.info('【发送消息】'+text)

async def receive_from_maimcore(message_dict: dict):
    '''
    定义如何处理从 MaimCore 收到的消息
    '''
    try:
        message=MessageBase.from_dict(message_dict)
        logger.info(f'收到来自 MaimCore ({message.message_info.platform}) 的回复: {message.message_segment}')
        if message.message_info.group_info:
            await send_to_yhchat(message.message_info.group_info.group_id, ChatType.GROUP, message.message_segment.data)
        else:
            await send_to_yhchat(message.message_info.user_info.user_id, ChatType.USER, message.message_segment.data)
    except Exception as e: # byd不加这玩意出错了根本不报错
        logger.exception(e)     
# 注册消息处理器
# Router 会自动将从对应 platform 收到的消息传递给注册的处理器
router.register_class_handler(receive_from_maimcore)
