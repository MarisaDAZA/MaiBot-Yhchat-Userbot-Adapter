from aiohttp import ClientSession
from uuid import uuid4
from yhchat_pb2 import SendMessage, MessageSent
from yhchat_config import token

async def send_message(chatId, chatType, text):
    async with ClientSession() as session:
        session.headers.update({
            'User-Agent': 'android 1.4.83',
            'Accept': 'application/x-protobuf',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-protobuf',
            'Token': token
        })
        body = SendMessage(
            message_id = uuid4().hex,
            chatId = chatId,
            chatType = chatType,
            contentType = 1
        )
        body.content.text = text
        async with session.post('https://chat-go.jwzhd.com/v1/msg/send-message', data=body.SerializeToString()) as r:
            string = await r.read()
            messageSent = MessageSent()
            messageSent.ParseFromString(string)
            print('【发送消息】', messageSent.msg)
        