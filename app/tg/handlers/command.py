from aiogram.dispatcher.router import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text

from configuration import logger
from database.functions import user_by_id
from tg.lexicon import lex_commands, lex_buttons, lex_messages
from tg.keyboards import Keyboard


command_router: Router = Router()


@command_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message) -> None:
    """
    Function processing the start command
    :param message: aiogram.types.Message
    :return: None
    """
    logger.debug(f'The user with ID={message.from_user.id} selected the start command')
    user = await user_by_id(message.from_user.id)
    if user.error:
        logger.warning(user.errorText)
        await message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        keyboard = Keyboard(2).create_inline(lex_buttons.record, lex_buttons.info)
        if user.entity is None:
            await message.answer(Text(lex_commands.start.msg.format(name='')).as_markdown(), reply_markup=keyboard)
        else:
            await message.answer(Text(lex_commands.start.msg.format(name=f', {user.entity.name}')).as_markdown(),
                                 reply_markup=keyboard)


@command_router.message(Command(commands=lex_commands.help.command), StateFilter(default_state))
async def process_help_command(message: Message) -> None:
    """
    Function processing the help command
    :param message: aiogram.types.Message
    :return: None
    """
    logger.debug(f'The user with ID={message.from_user.id} selected the help command')
    await message.answer(Text(lex_commands.help.msg).as_markdown())


@command_router.message(Command(commands=lex_commands.cancel.command))
async def process_help_command(message: Message, state: FSMContext) -> None:
    """
    Function processing the cancel command
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user with ID={message.from_user.id} selected the cancel command')
    await state.clear()
    await message.answer(Text(lex_commands.cancel.msg).as_markdown())


__all__ = 'command_router'
