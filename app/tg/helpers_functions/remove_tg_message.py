import asyncio

from aiogram import Bot


async def remove_message(bot: Bot, chat_id: int, message_id: int, delay: float) -> None:
    """
    Function that deletes a message after a delay
    :param bot: aiogram.Bot
    :param chat_id: int
    :param message_id: int
    :param delay: float
    :return: None
    """
    await asyncio.sleep(delay)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


__all__ = 'remove_message'
