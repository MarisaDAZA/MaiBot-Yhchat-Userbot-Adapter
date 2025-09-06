import asyncio
from loguru import logger
from src.yhchat2maibot import yhchat
from src.maibot2yhchat import router
from src.group_name import save_data
from src.client_session import setup_session, close_session

async def main():
    try:
        await setup_session()
    	await asyncio.gather(router.run(), yhchat())
    except asyncio.CancelledError:
        await close_shared_session()
        save_data()
        logger.warning('【用户中断】')

if __name__ == '__main__':
    asyncio.run(main())
