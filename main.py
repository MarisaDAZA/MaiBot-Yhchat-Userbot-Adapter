import asyncio
from loguru import logger
from src.yhchat2maibot import yhchat
from src.maibot2yhchat import router
from src.client_session import set_global_session
from src.group_name import save_data

async def main():
    await asyncio.gather(set_global_session(), router.run(), yhchat())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        save_data()
        logger.warning('【用户中断】')