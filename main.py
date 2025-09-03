import asyncio
from src.yhchat2maibot import yhchat
from src.maibot2yhchat import maibot
from src.logger import logger

async def main():
    await asyncio.gather(yhchat(), maibot())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("用户中断")