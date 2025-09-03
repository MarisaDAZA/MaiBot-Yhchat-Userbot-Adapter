import websockets
import asyncio
from uuid import uuid4
from json import dumps
from yhchat_pb2 import Msg, PushMessage
from yhchat_config import userId, token, deviceid
from maibot import send_to_maimcore

async def login(websocket):
    seq = uuid4().hex
    msg = dumps({
        'seq': seq,
        'cmd': 'login',
        'data': {
            'userId': userId,
            'token': token,
            'platform': 'android',
            'deviceId': deviceid
        }
    })
    await websocket.send(msg)

async def heartbeat(websocket):
    while True:
        seq = uuid4().hex
        msg = dumps({
            'seq': seq,
            'cmd': 'heartbeat',
            'data': {}
        })
        await websocket.send(msg)
        await asyncio.sleep(30)

async def receive(websocket):
    while True:
        string = await websocket.recv()
        msg = Msg()
        msg.ParseFromString(string)

        if msg.header.type == 'push_message':
            pushMessage = PushMessage()
            msg.data.Unpack(pushMessage)
            print('【收到消息】')
            await send_to_maimcore(pushMessage)
            
        elif msg.header.type == 'heartbeat_ack':
            print('【心跳】') #msg.header.id
        else:
            print('【'+msg.header.type+'】')

async def main():
    # while True:
    #     try:
            async with websockets.connect('wss://chat-ws-go.jwzhd.com/ws') as websocket:
                await login(websocket)
                await asyncio.gather(heartbeat(websocket), receive(websocket))
        # except Exception as e:
        #     print('【错误】',e)
        #     await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())