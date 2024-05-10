from aiogram.dispatcher.router import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from peewee import DoesNotExist

from configuration import logger
from database.lash import objects_ro, UsersRO
from tg.lexicon import lex_commands, lex_buttons, lex_messages
from tg.keyboards import Keyboard


command_router: Router = Router()


@command_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    logger.debug(f'Getting started with a bot user with ID={message.from_user.id} '
                 f'and name={message.from_user.first_name}')
    keyboard = Keyboard.create_inline(2, '', lex_buttons.record, lex_buttons.info)
    try:
        user = await objects_ro.get(UsersRO, tg_id=message.from_user.id)
        logger.debug(f'Found user named {user.surname} {user.name}')
        await message.answer(lex_commands.start.msg.format(name=f', {user.name}'), reply_markup=keyboard)
    except DoesNotExist:
        logger.info('User not found in database')
        await message.answer(lex_commands.start.msg.format(name=''), reply_markup=keyboard)
    except Exception as error:
        logger.warning(error)
        await message.answer(lex_messages.techProblems)


@command_router.message(Command(commands=lex_commands.help.command), StateFilter(default_state))
async def process_help_command(message: Message):
    logger.debug(f'Getting started with a bot user with ID={message.from_user.id} '
                 f'and name {message.from_user.first_name}')
    await message.answer(lex_commands.help.msg)


__all__ = 'command_router'
