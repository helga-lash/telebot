from aiogram.dispatcher.router import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text
from datetime import datetime, timedelta

from configuration import logger, apl_conf
from database.functions import user_by_id
from database.entities.scheduler_jobs.work_class import SchedulerJobType, SchedulerJob
from database import create_job
from tg.lexicon import lex_commands, lex_buttons, lex_messages
from tg.keyboards import Keyboard
from tg.states import FSMUser
from scheduler import delete_msq_queue


command_router: Router = Router()


@command_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext) -> None:
    """
    Function processing the start command
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user with ID={message.from_user.id} selected the start command')
    job = await create_job(
        message.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=message.chat.id,
            message_id=message.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(message)
    user = await user_by_id(message.from_user.id)
    if user.error:
        logger.warning(user.errorText)
        await message.answer(Text(lex_messages.techProblems).as_markdown())
        return
    if user.entity is None:
        if str(message.from_user.id) not in apl_conf.tgBot.admins:
            keyboard = Keyboard(1, '-registration').create_inline(lex_buttons.no)
            msg_text: str = Text(lex_messages.userNameFirst).as_markdown()
            await state.update_data(admin=False)
            await state.set_state(FSMUser.name)
        else:
            keyboard = Keyboard(1, '-adminReg').create_inline(lex_buttons.yes)
            msg_text: str = Text(lex_messages.admNotRegistered).as_markdown()
    else:
        msg_text: str = Text(lex_commands.start.msg.format(name=f', {user.entity.name}')).as_markdown()
        if user.entity.admin:
            keyboard = Keyboard(2, '-admin').create_inline(lex_buttons.record, lex_buttons.info)
        else:
            keyboard = Keyboard(2).create_inline(lex_buttons.record, lex_buttons.info)
    msg = await message.answer(msg_text, reply_markup=keyboard)
    job = await create_job(
        message.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=message.chat.id,
            message_id=msg.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(msg)


@command_router.message(Command(commands=lex_commands.help.command), StateFilter(default_state))
async def process_help_command(message: Message) -> None:
    """
    Function processing the help command
    :param message: aiogram.types.Message
    :return: None
    """
    logger.debug(f'The user with ID={message.from_user.id} selected the help command')
    job = await create_job(
        message.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=message.chat.id,
            message_id=message.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(message)
    msg = await message.answer(Text(lex_commands.help.msg).as_markdown())
    job = await create_job(
        message.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=message.chat.id,
            message_id=msg.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(msg)


@command_router.message(Command(commands=lex_commands.cancel.command))
async def process_help_command(message: Message, state: FSMContext) -> None:
    """
    Function processing the cancel command
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user with ID={message.from_user.id} selected the cancel command')
    job = await create_job(
        message.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=message.chat.id,
            message_id=message.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(message)
    await state.clear()
    msg = await message.answer(Text(lex_commands.cancel.msg).as_markdown())
    job = await create_job(
        message.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=message.chat.id,
            message_id=msg.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(msg)


__all__ = 'command_router'
