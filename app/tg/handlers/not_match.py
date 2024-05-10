from aiogram.dispatcher.router import Router
from aiogram.types import Message

from configuration import logger
from tg.lexicon import lex_messages


not_match_router: Router = Router()


@not_match_router.message()
async def send_echo(message: Message):
    logger.info(f'Did not recognize a message from a user with ID={message.from_user.id}: {message.text}')
    await message.answer(lex_messages.notMatch)


__all__ = 'not_match_router'
