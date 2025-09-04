import asyncio
from loguru import logger
from src.yhchat2maibot import yhchat
from src.maibot2yhchat import router
from src.group_name import save_data
from src.client_session import close_shared_session

async def main():
    await asyncio.gather(router.run(), yhchat())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        close_shared_session()
        save_data()
        logger.warning('【用户中断】')