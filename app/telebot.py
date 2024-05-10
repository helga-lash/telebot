import asyncio
import os


from tg import TelegramInterface


tg: TelegramInterface = TelegramInterface()

asyncio.run(tg.run())
