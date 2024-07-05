import asyncio
import os

os.environ['CFG_PTH'] = '/work/git/github/helga_lash/telebot/dev-conf.yaml'

from tg import TelegramInterface
from scheduler import schedule


async def main():
    tg: TelegramInterface = TelegramInterface()
    asyncio.create_task(schedule(tg.bot))
    await tg.run()

asyncio.run(main())
