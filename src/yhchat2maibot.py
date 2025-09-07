-import websockets
import asyncio
import json
from uuid import uuid4
from .logger import logger
from maim_message import BaseMessageInfo, UserInfo, GroupInfo,MessageBase, Seg
from .config import config
from .proto.yhchat_pb2 import Msg, PushMessage, ChatType
from .maibot2yhchat import router
from .group_name import get_group_name
from .emoji import get_image_base64


async def login(websocket):
    seq = uuid4().hex
    msg = json.dumps({
        'seq': seq,
        'cmd': 'login',
        'data': {
            'userId': config['yhchat']['userId'],
            'token': config['yhchat']['token'],
            'platform': config['yhchat']['platform'],
            'deviceId': config['yhchat']['deviceid']
        }
    })
    await websocket.send(msg)
    logger.info('【登录云湖】')

async def heartbeat(websocket):
    while True:
        seq = uuid4().hex
        msg = json.dumps({
            'seq': seq,
            'cmd': 'heartbeat',
            'data': {}
        })
        await websocket.send(msg)
        await asyncio.sleep(30)

def check_allow_to_chat(pushMessage):
        '''
        检查是否允许聊天
        Parameters:
            user_id: int: 用户ID
            group_id: int: 群ID
        Returns:
            bool: 是否允许聊天
        '''
        if pushMessage.sender.id == config['yhchat']['userId']:
            logger.warning('收到自己消息，消息被丢弃')
            return False
        if pushMessage.sender.id in config['chat']['ban_user_id']:
            logger.warning('用户在全局黑名单中，消息被丢弃')
            return False
        if config['chat']['ban_bot'] and pushMessage.sender.chatType == ChatType.BOT:
            logger.warning('云湖官方机器人消息拦截已启用，消息被丢弃')
            return False

        if pushMessage.chatType == ChatType.GROUP:
            if config['chat']['group_list_type'] == 'whitelist' and pushMessage.chatId not in config['chat']['group_list']:
                logger.warning('群聊不在聊天白名单中，消息被丢弃')
                return False
            elif config['chat']['group_list_type'] == 'blacklist' and pushMessage.chatId in config['chat']['group_list']:
                logger.warning('群聊在聊天黑名单中，消息被丢弃')
                return False
        elif pushMessage.chatType == ChatType.USER:
            if config['chat']['private_list_type'] == 'whitelist' and pushMessage.sender.id not in config['chat']['private_list']:
                logger.warning('私聊不在聊天白名单中，消息被丢弃')
                return False
            elif config['chat']['private_list_type'] == 'blacklist' and pushMessage.sender.id in config['chat']['private_list']:
                logger.warning('私聊在聊天黑名单中，消息被丢弃')
                return False
        else:
            logger.warning('机器人私聊消息，消息被丢弃')
            return False

        return True

async def receive_from_yhchat(websocket):
    while True:
        string = await websocket.recv()
        msg = Msg()
        msg.ParseFromString(string)

        if msg.header.type == 'push_message':
            pushMessage = PushMessage()
            msg.data.Unpack(pushMessage)
            if check_allow_to_chat(pushMessage):
                await send_to_maimcore(pushMessage)

        elif msg.header.type == 'heartbeat_ack':
            logger.debug('【心跳】')

# 构造并发送要发送给 MaimCore 的消息
async def send_to_maimcore(pushMessage):
    '''根据平台事件构造标准 MessageBase'''
    if pushMessage.contentType == 1:
        logger.info('【收到消息】'pushMessage.sender.id)
        message_segment = Seg('text', pushMessage.content.text)
    elif pushMessage.contentType == 2:
        logger.info('【收到图片】'pushMessage.content.imageUrl)
        message_segment = Seg('image', get_image_base64(pushMessage.content.imageUrl))
    elif pushMessage.contentType == 7:
        logger.info('【收到表情】'pushMessage.content.imageUrl)
        message_segment = Seg('emoji', get_image_base64(pushMessage.content.imageUrl))
    else:
        return
    user_info = UserInfo(platform='yhchat', user_id=pushMessage.sender.id, user_nickname=pushMessage.sender.nickname)
    if pushMessage.chatType == ChatType.GROUP:
        group_name = await get_group_name(pushMessage.chatId)
        group_info = GroupInfo(platform='yhchat', group_id=pushMessage.chatId, group_name=group_name)
    else:
        group_info = None
    format_info = {'content_format': ['text'], 'accept_format': ['text']}
    message_info = BaseMessageInfo(
        platform='yhchat',
        message_id=pushMessage.message_id, # 平台消息的原始ID
        time=pushMessage.time/1000, # 当前时间戳
        user_info=user_info,
        group_info=group_info,
        format_info=format_info
    )
    message_segment = Seg('text', pushMessage.content.text)
    msg_to_send = MessageBase(message_info=message_info, message_segment=message_segment)
    # logger.debug(msg_to_send)
    await router.send_message(msg_to_send)

async def yhchat():
    while True:
        try:
            async with websockets.connect('wss://chat-ws-go.jwzhd.com/ws') as websocket:
                await login(websocket)
                await asyncio.gather(heartbeat(websocket), receive_from_yhchat(websocket))
        except Exception as e:
            logger.exception(e)
            retry_wait = config['yhchat']['retry_wait']
            logger.error(f'【与云湖的连接断开】将在{retry_wait}秒后重试')
            await asyncio.sleep(retry_wait)
