import asyncio

from aiogram.dispatcher.router import Router
from aiogram.types import Message
from aiogram.utils.formatting import Text

from configuration import logger
from tg.lexicon import lex_messages
from tg.helpers_functions import remove_message


not_match_router: Router = Router()


@not_match_router.message()
async def send_echo_route(message: Message) -> None:
    """
    A function that processes messages that are not processed by other handlers
    :param message: aiogram.types.Message
    :return: None
    """
    logger.info(f'Did not recognize a message from a user with ID={message.from_user.id}: {message.text}')
    msg = await message.answer(Text(lex_messages.notMatch).as_markdown())
    asyncio.create_task(remove_message(msg.bot, message.chat.id, msg.message_id, 600.0))


__all__ = 'not_match_router'
