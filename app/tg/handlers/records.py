import re

from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.formatting import Text

from datetime import date, time, datetime, timedelta

from tg.lexicon import lex_buttons, lex_messages, lex_commands
from tg.keyboards import Keyboard, SimpleCalendar, SimpleCalendarCallback
from tg.states import FSMRecord, FSMUser
from configuration import logger, apl_conf
from database.functions import rec_day, user_by_id, create_user, create_registration
from database.entities.scheduler_jobs.work_class import SchedulerJobType, SchedulerJob
from database import create_job
from scheduler import delete_msq_queue


records_router: Router = Router()


@records_router.callback_query(F.data == lex_buttons.record.callback)
@records_router.callback_query(FSMRecord.confirmation, F.data == f'{lex_buttons.no.callback}-record')
async def record_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the records button and state
    FSMRecord.confirmation + data from the no button
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await state.clear()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the record button')
    await callback.message.delete_reply_markup()
    keyboard = await SimpleCalendar().start_calendar()
    if keyboard.error:
        logger.warning(keyboard.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        await state.clear()
    else:
        await callback.message.answer(Text(lex_messages.recordCalendar).as_markdown(), reply_markup=keyboard.entity)
        await state.set_state(FSMRecord.date)


@records_router.callback_query(SimpleCalendarCallback.filter(), FSMRecord.date)
async def process_simple_calendar_route(callback: CallbackQuery,
                                        callback_data: SimpleCalendarCallback, state: FSMContext) -> None:
    """
    A function that processes the returned data from the calendar in state FSMRecord.date
    :param callback: aiogram.types.CallbackQuery
    :param callback_data: tg.keyboards.SimpleCalendarCallback
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    selected_date = await SimpleCalendar().process_selection(callback, callback_data)
    if selected_date.error:
        logger.warning(selected_date.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        await state.clear()
    else:
        if callback_data.act == 'DAY':
            day: date = date(selected_date.entity.year, selected_date.entity.month, selected_date.entity.day)
            records = await rec_day(day)
            if records.error:
                logger.warning(records.errorText)
                await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
                await state.clear()
            else:
                if len(records.entity) == len(apl_conf.tgBot.recordTime):
                    keyboard = await SimpleCalendar().start_calendar(callback_data.year, callback_data.month)
                    if keyboard.error:
                        logger.warning(keyboard.errorText)
                        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
                        await state.clear()
                    else:
                        await callback.answer(Text(
                            lex_messages.recordCalendarSorry.format(date=f'{callback_data.year}-{callback_data.month}-'
                                                                         f'{callback_data.day}')
                        ).as_markdown(), reply_markup=keyboard.entity)
                else:
                    await state.update_data(date=day)
                    buttons = []
                    for tm in apl_conf.tgBot.recordTime:
                        if (
                                tm not in [x.time for x in records.entity]
                        ) and (
                                tm > time(datetime.now().hour, datetime.now().minute, datetime.now().second)
                        ):
                            buttons.append(f'{str(tm).split(':')[0]}:{str(tm).split(':')[1]}')
                    keyboard = Keyboard(3).create_inline(*buttons)
                    await callback.message.answer(Text(lex_messages.recordTime).as_markdown(), reply_markup=keyboard)
                    await state.set_state(FSMRecord.time)


@records_router.callback_query(FSMRecord.time)
async def record_time_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes state FSMRecord.time
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.update_data(time=time(*[int(x) for x in callback.data.split(':')]))
    user = await user_by_id(callback.from_user.id)
    if user.error:
        logger.warning(user.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        await state.clear()
    else:
        if user.entity is not None:
            await state.update_data(user=user.entity.tg_id)
            await state.set_state(FSMRecord.confirmation)
            data = await state.get_data()
            keyboard = Keyboard(2, '-record').create_inline(lex_buttons.yes, lex_buttons.no)
            await callback.message.answer(
                Text(lex_messages.recordConfirm.format(
                    day=data['date'].strftime("%d-%m-%Y"),
                    tm=data['time'].strftime("%H:%M")
                )).as_markdown(),
                reply_markup=keyboard
            )
        else:
            keyboard = Keyboard(1, '-registration').create_inline(lex_buttons.no)
            await state.update_data(admin=False)
            await callback.message.answer(Text(lex_messages.userName).as_markdown(), reply_markup=keyboard)
            await state.set_state(FSMRecord.user)


@records_router.callback_query(F.data == f'{lex_buttons.no.callback}-registration')
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


@records_router.message(FSMRecord.user)
@records_router.message(FSMUser.name)
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


@records_router.message(FSMUser.surname)
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


@records_router.message(FSMUser.phone_number)
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


@records_router.callback_query(FSMUser.confirmation, F.data == f'{lex_buttons.no.callback}-user-reg')
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


@records_router.callback_query(FSMUser.confirmation, F.data == f'{lex_buttons.yes.callback}-user-reg')
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


@records_router.callback_query(FSMRecord.confirmation, F.data == f'{lex_buttons.yes.callback}-record')
async def create_record_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes state FSMRecord.confirmation and returned data from the yes
    button for confirmation user data
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    data = await state.get_data()
    create = await create_registration(data['date'], data['time'], callback.from_user.id)
    if create.error:
        logger.warning(create.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        await callback.message.answer(Text(lex_messages.recordOk.format(name=create.entity.user.name)).as_markdown())
        day_confirm = True
        record_datetime = datetime(
                data['date'].year, data['date'].month, data['date'].day,
                data['time'].hour, data['time'].minute, data['time'].second
            )
        if (record_datetime - datetime.now()) < timedelta(hours=2):
            day_confirm = False
            two_hours_confirm_datetime = datetime.now()
        else:
            two_hours_confirm_datetime = record_datetime - timedelta(hours=2)
        job_two_hours_confirm = await create_job(
            callback.from_user.id,
            SchedulerJob(
                type=SchedulerJobType.SEND_MESSAGE,
                chat_id=callback.from_user.id,
                text=Text(lex_messages.confirmationDay.format(
                    date=create.entity.date.strftime("%d-%m-%Y"),
                    time=create.entity.time.strftime("%H:%M"),
                    name=create.entity.user.name
                )).as_markdown(),
                keyboard=Keyboard(
                    2, f'-confirmation_two_hours:{create.entity.id}'
                ).create_inline(lex_buttons.yes, lex_buttons.no)
            ),
            two_hours_confirm_datetime
        )
        if job_two_hours_confirm.error:
            logger.warning(job_two_hours_confirm.errorText)
            await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
            await state.clear()
        if day_confirm:
            if record_datetime - datetime.now() < timedelta(days=1):
                day_confirm_datetime = datetime.now()
            else:
                day_confirm_datetime = record_datetime - timedelta(days=1)
            job_day_confirm = await create_job(
                callback.from_user.id,
                SchedulerJob(
                    type=SchedulerJobType.SEND_MESSAGE,
                    chat_id=callback.from_user.id,
                    text=Text(lex_messages.confirmationDay.format(
                        date=create.entity.date.strftime("%d-%m-%Y"),
                        time=create.entity.time.strftime("%H:%M"),
                        name=create.entity.user.name
                    )).as_markdown(),
                    keyboard=Keyboard(
                        2, f'-confirmation_day:{create.entity.id}'
                    ).create_inline(lex_buttons.yes, lex_buttons.no)
                ),
                day_confirm_datetime
            )
            if job_day_confirm.error:
                logger.warning(job_day_confirm.errorText)
                await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
                await state.clear()
        for admin in apl_conf.tgBot.admins:
            job = await create_job(
                admin,
                SchedulerJob(
                    type=SchedulerJobType.SEND_MESSAGE,
                    chat_id=int(admin),
                    text=Text(lex_messages.adminRecordOkNotify.format(
                        date=create.entity.date.strftime("%d-%m-%Y"),
                        time=create.entity.time.strftime("%H:%M"),
                        name=create.entity.user.name,
                        surname=create.entity.user.surname,
                        phone=create.entity.user.phone_number
                    )).as_markdown()
                ),
                datetime.now()
            )
            if job.error:
                logger.warning(job.errorText)
                await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    await state.clear()


__all__ = 'records_router'
