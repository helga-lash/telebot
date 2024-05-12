import asyncio
import os

os.environ['CFG_PTH'] = '/work/git/github/helga_lash/telebot/dev-conf.yaml'

from tg import TelegramInterface


tg: TelegramInterface = TelegramInterface()

asyncio.run(tg.run())
