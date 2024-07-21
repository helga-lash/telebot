import re

from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.formatting import Text

from datetime import datetime, timedelta

from tg.lexicon import lex_buttons, lex_messages, lex_commands
from tg.keyboards import Keyboard
from tg.states import FSMRecord, FSMUser
from configuration import logger, apl_conf
from database.functions import create_user
from database.entities.scheduler_jobs.work_class import SchedulerJobType, SchedulerJob
from database import create_job
from scheduler import delete_msq_queue


user_registration_router: Router = Router()


@user_registration_router.callback_query(F.data == f'{lex_buttons.no.callback}-registration')
async def not_registration_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the no button for user registration
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.clear()
    await callback.message.answer(Text(lex_commands.help.msg).as_markdown())


@user_registration_router.message(FSMRecord.user)
@user_registration_router.message(FSMUser.name)
async def username_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes states FSMRecord.user and FSMUser.name
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user ID={message.from_user.id} sent name')
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
    if re.compile(r'^[А-Я][а-я]{1,9}$').match(message.text):
        await state.update_data(name=message.text)
        await state.set_state(FSMUser.surname)
        msg = await message.answer(Text(lex_messages.userSurname).as_markdown())
    else:
        msg = await message.answer(Text(lex_messages.userNameNotValid).as_markdown())
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


@user_registration_router.message(FSMUser.surname)
async def user_surname_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMUser.surname
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user ID={message.from_user.id} sent surname')
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
    if re.compile(r'^[А-Я][а-я]{1,9}$').match(message.text):
        await state.update_data(surname=message.text)
        await state.set_state(FSMUser.phone_number)
        msg = await message.answer(Text(lex_messages.userPhone).as_markdown())
    else:
        msg = await message.answer(Text(lex_messages.userSurnameNotValid).as_markdown())
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


@user_registration_router.message(FSMUser.phone_number)
async def user_phone_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMUser.phone_number
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user ID={message.from_user.id} sent phone number')
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
    if re.compile(r'^7\d{10}$').match(message.text):
        await state.update_data(phone_number=message.text)
        await state.set_state(FSMUser.confirmation)
        data = await state.get_data()
        keyboard = Keyboard(2, '-user-reg').create_inline(lex_buttons.yes, lex_buttons.no)
        msg = await message.answer(Text(lex_messages.userConfirm.format(
            surname=data['surname'],
            name=data['name'],
            phone=data['phone_number']
        )).as_markdown(), reply_markup=keyboard)
    else:
        msg = await message.answer(Text(lex_messages.userPhoneNotValid).as_markdown())
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


@user_registration_router.callback_query(FSMUser.confirmation, F.data == f'{lex_buttons.no.callback}-user-reg')
async def not_registration_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes state FSMUser.confirmation and returned data from the no button for confirmation user data
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user ID={callback.from_user.id} did not confirm his details')
    job = await create_job(
        callback.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(callback.message)
    await state.set_state(FSMUser.name)
    msg = await callback.message.answer(Text(lex_messages.name).as_markdown())
    job = await create_job(
        callback.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=callback.message.chat.id,
            message_id=msg.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(msg)


@user_registration_router.callback_query(FSMUser.confirmation, F.data == f'{lex_buttons.yes.callback}-user-reg')
async def create_user_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes state FSMUser.confirmation and returned data from the yes
    button for confirmation user data
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user ID={callback.from_user.id} confirm his details')
    job = await create_job(
        callback.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(callback.message)
    data = await state.get_data()
    create = await create_user(callback.from_user.id, data['name'], data['surname'],
                               data['phone_number'], data['admin'])
    if create.error:
        logger.warning(create.errorText)
        msg = await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        await state.clear()
    else:
        if ((str(callback.from_user.id) not in apl_conf.tgBot.admins) and
                (data.get('date') is not None) and (data.get('time') is not None)):
            await state.update_data(user=create.entity.tg_id)
            await state.set_state(FSMRecord.confirmation)
            keyboard = Keyboard(2, '-record').create_inline(lex_buttons.yes, lex_buttons.no)
            msg = await callback.message.answer(
                Text(lex_messages.recordConfirm.format(
                    day=data['date'].strftime("%d-%m-%Y"),
                    tm=data['time'].strftime("%H:%M")
                )).as_markdown(),
                reply_markup=keyboard
            )
        else:
            await state.clear()
            msg = await callback.message.answer(Text(lex_messages.userOk).as_markdown())
    job = await create_job(
        callback.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=callback.message.chat.id,
            message_id=msg.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await delete_msq_queue.put(msg)


__all__ = 'user_registration_router'
