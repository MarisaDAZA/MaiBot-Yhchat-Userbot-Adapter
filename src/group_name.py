import json
from os import path
from loguru import logger
from .client_session import get_shared_session
from .proto.yhchat_pb2 import GroupId, GroupInfo

if path.exists('group_names.json'):
    with open('group_names.json', 'r', encoding='utf-8') as f:
        group_names_data = json.load(f)
else:
    group_names_data = {}

async def get_group_info(group_id:str) -> str:
    session = get_shared_session()
    body = GroupId(groupId = group_id)
    async with session.post('https://chat-go.jwzhd.com/v1/group/info', data=body.SerializeToString()) as r:
        string = await r.read()
        groupInfo = GroupInfo()
        groupInfo.ParseFromString(string)
        return groupInfo.group.name

async def get_group_name(group_id:str) -> str:
    if group_id in group_names_data:
        return group_names_data[group_id]
    else:
        name = await get_group_info(group_id)
        logger.info('获取到群聊名字：'+name)
        group_names_data[group_id] = name
        return name

def save_data():
    with open('group_names.json', 'w', encoding='utf-8') as f:
        json.dump(group_names_data, f, indent=4, ensure_ascii=False)
        logger.info('【保存群名数据】')
