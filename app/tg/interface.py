from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from configuration import logger, apl_conf
from tg.handlers import command_router, info_router, records_router, not_match_router
from tg.keyboards import set_menu


class TelegramInterface:
    """
    Class describing telegram interface

    Methods:
        run: run telegram interface
    """
    def __init__(self, token: str = apl_conf.tgBot.token):
        logger.debug(f'Initialization of class TelegramInterface with token = {token}')
        storage: MemoryStorage = MemoryStorage()
        self.bot: Bot = Bot(token=token, parse_mode='MarkdownV2')
        self.dispatcher: Dispatcher = Dispatcher(storage=storage)

    async def run(self):
        logger.debug('Run telebot')
        await set_menu(self.bot)
        self.dispatcher.include_router(command_router)
        self.dispatcher.include_router(records_router)
        self.dispatcher.include_router(info_router)
        self.dispatcher.include_router(not_match_router)
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dispatcher.start_polling(self.bot)
