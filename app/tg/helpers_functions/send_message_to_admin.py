from aiogram import Bot

from configuration import apl_conf


async def admin_send_message(bot: Bot, message: str) -> None:
    """
    Function that sends a message to the admins
    :param bot: aiogram.Bot
    :param message: str
    :return: None
    """
    for admin_id in apl_conf.tgBot.admins:
        await bot.send_message(chat_id=admin_id, text=message)


__all__ = 'admin_send_message'
