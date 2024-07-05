import asyncio
import os

os.environ['CFG_PTH'] = '/work/git/github/helga_lash/telebot/dev-conf.yaml'

from tg import TelegramInterface
from scheduler import schedule


async def main():
    tg: TelegramInterface = TelegramInterface()
    bot_task = tg.run()
    scheduler_task = asyncio.create_task(schedule(tg.bot))
    await asyncio.gather(bot_task, scheduler_task)

asyncio.run(main())
