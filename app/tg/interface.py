from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from configuration import logger, apl_conf
from tg.handlers import command_router, info_router, records_router, not_match_router, admin_router, confirmation_router
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
        self.bot: Bot = Bot(token=token, default=DefaultBotProperties(parse_mode='MarkdownV2'))
        self.dispatcher: Dispatcher = Dispatcher(storage=storage)
        self.__create_photo_path()

    @staticmethod
    def __create_photo_path(photo_path: Path = apl_conf.tgBot.photoPath) -> None:
        """
        Static method to create photo path

        Parameters:
            photo_path (Path): The path to the photo directory.

        Returns:
            None
        """
        logger.debug(f'Create path "{str(photo_path)} if not exist"')
        photo_path.mkdir(parents=True, exist_ok=True)

    async def run(self):
        logger.debug('Run telebot')
        self.__create_photo_path()
        await set_menu(self.bot)
        self.dispatcher.include_router(command_router)
        self.dispatcher.include_router(records_router)
        self.dispatcher.include_router(info_router)
        self.dispatcher.include_router(admin_router)
        self.dispatcher.include_router(confirmation_router)
        self.dispatcher.include_router(not_match_router)
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dispatcher.start_polling(self.bot)
