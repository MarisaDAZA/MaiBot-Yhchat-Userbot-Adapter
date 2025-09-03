import asyncio
from yhchat_pb2 import ChatType
from yhchat_send import send_message
from maim_message import (
    BaseMessageInfo, UserInfo, GroupInfo, MessageBase, Seg,
    Router, RouteConfig, TargetConfig
)

# 1. 定义连接目标 (例如 MaimCore)
route_config = RouteConfig(
    route_config={
        "yhchat": TargetConfig(
            url="ws://127.0.0.1:51400/ws"
        )
    }
)

# 2. 创建 Router 实例
router = Router(route_config)

# 3. 定义如何处理从 MaimCore 收到的消息
async def handle_response_from_maimcore(message_dict: dict):
    try:
        message=MessageBase.from_dict(message_dict)
        print(f"收到来自 MaimCore ({message.message_info.platform}) 的回复: {message.message_segment}")
        if message.message_info.group_info:
            await send_message(message.message_info.group_info.group_id, ChatType.GROUP, message.message_segment.data)
        else:
            await send_message(message.message_info.user_info.user_id, ChatType.USER, message.message_segment.data)
    except Exception as e:
        print(e)
        

# 4. 注册消息处理器
# Router 会自动将从对应 platform 收到的消息传递给注册的处理器
router.register_class_handler(handle_response_from_maimcore)

# 5. 构造并发送要发送给 MaimCore 的消息
async def send_to_maimcore(pushMessage):
    """根据平台事件构造标准 MessageBase"""
    user_info = UserInfo(platform="yhchat", user_id=pushMessage.sender.id, user_nickname=pushMessage.sender.nickname)
    if pushMessage.chatType == ChatType.GROUP:
        return
        # group_info = GroupInfo(platform="yhchat", group_id=pushMessage.chatId)
    else:
        group_info = None
    format_info = {"content_format": ["text"], "accept_format": ["text"]}
    message_info = BaseMessageInfo(
        platform="yhchat",
        message_id=pushMessage.message_id, # 平台消息的原始ID
        time=pushMessage.time/1000, # 当前时间戳
        user_info=user_info,
        group_info=group_info,
        format_info=format_info
    )
    message_segment = Seg("text", pushMessage.content.text)
    msg_to_send = MessageBase(message_info=message_info, message_segment=message_segment)
    await router.send_message(msg_to_send)

# 6. 运行并发送消息
async def run_client():
    # 启动 Router (它会自动尝试连接所有配置的目标，并开始接收消息)
    # run() 通常是异步阻塞的，需要 create_task
    router_task = asyncio.create_task(router.run())
    print("Router 正在启动并尝试连接...")

    # 等待连接成功 (实际应用中需要更健壮的连接状态检查)
    await asyncio.sleep(2)
    print("连接应该已建立...")

    try:
        await router_task
    except asyncio.CancelledError:
        print("Router 任务已被取消。")

if __name__ == "__main__":
    try:
        asyncio.run(run_client())
    except KeyboardInterrupt:
        print("用户中断。")
    # 注意：实际适配器中，Router 的启动和消息发送/接收会集成到适配器的主事件循环中。