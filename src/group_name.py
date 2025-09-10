from .logger import logger
from . import http
from .proto.yhchat_pb2 import GroupId, GroupInfo

group_names_data = {}

async def get_group_info(group_id:str) -> str:
    body = GroupId(groupId = group_id)
    async with http.session.post('https://chat-go.jwzhd.com/v1/group/info', data=body.SerializeToString()) as r:
        string = await r.read()
        groupInfo = GroupInfo()
        groupInfo.ParseFromString(string)
        return groupInfo.group.name

async def get_group_name(group_id:str) -> str:
    if group_id in group_names_data:
        return group_names_data[group_id]
    else:
        name = await get_group_info(group_id)
        logger.debug(f'获取到群聊名字：{name}')
        group_names_data[group_id] = name
        return name
