import asyncio
import yhchat_ws
import maibot

async def main():
    await asyncio.gather(yhchat_ws.main(), maibot.run_client())

asyncio.run(main())