from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup


async def send_message(bot: Bot, user_id: int, message: str, keyboard: InlineKeyboardMarkup or None = None) -> None:
    """
    Function that sends a message to the admins
    :param bot: aiogram.Bot
    :param user_id: int
    :param message: str
    :param keyboard: aiogram.types.InlineKeyboardMarkup or None, default None
    :return: None
    """
    if keyboard is None:
        await bot.send_message(chat_id=user_id, text=message)
    else:
        await bot.send_message(chat_id=user_id, text=message, reply_markup=keyboard)


__all__ = 'send_message'
