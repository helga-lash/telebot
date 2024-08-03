from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.formatting import Text
from datetime import time, datetime, timedelta

from configuration import logger, apl_conf
from tg.lexicon import lex_buttons, lex_messages
from tg.keyboards import Keyboard, AdminCalendar, RecordsKeyboard, RecordCallback
from tg.states import FSMRecordNotes, FSMRecordReservation, FSMPhotoDownload
from database import rec_day, record_update_notes, create_registration
from database.entities.scheduler_jobs.work_class import SchedulerJobType, SchedulerJob
from database import create_job

admin_records_router = Router()


@admin_records_router.callback_query(F.data == lex_buttons.timeReserve.callback)
async def admin_time_reserve_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the time reserve button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
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
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        return
    day = (await state.get_data())['date']
    logger.debug(f'User: {callback.message.from_user.id} open records on {day} for time reservation')
    records = await rec_day(day)
    if records.error:
        logger.warning(records.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    buttons = []
    for tm in apl_conf.tgBot.recordTime:
        if tm not in [x.time for x in records.entity]:
            buttons.append(f'{str(tm).split(':')[0]}:{str(tm).split(':')[1]}')
    keyboard = Keyboard(3).create_inline(*buttons)
    await state.set_state(FSMRecordReservation.time)
    msg = await callback.message.answer(Text(lex_messages.reserveTime).as_markdown(), reply_markup=keyboard)
    job = await create_job(
        callback.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=msg.chat.id,
            message_id=msg.message_id
        ),
        datetime.now() + timedelta(minutes=10)
    )
    if job.error:
        logger.warning(job.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())


@admin_records_router.callback_query(FSMRecordReservation.time)
async def admin_notes_reserve_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes state FSMRecordReservation.time
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} has selected a time to reserve')
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
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        return
    await state.update_data(time=time(*[int(x) for x in callback.data.split(':')]))
    await state.set_state(FSMRecordReservation.notes)
    msg = await callback.message.answer(
        Text(lex_messages.reserveNotes).as_markdown())
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
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())


@admin_records_router.message(FSMRecordReservation.notes)
async def admin_record_reserve_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMRecordReservation.time
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user {message.from_user.id} has selected a time to reserve')
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
        await message.answer(Text(lex_messages.techProblems).as_markdown())
        return
    await state.update_data(notes=message.text)
    await state.set_state(FSMRecordReservation.confirmation)
    data = await state.get_data()
    keyboard = Keyboard(2, '-admin-record').create_inline(lex_buttons.yes, lex_buttons.no)
    msg = await message.answer(
        Text(lex_messages.recordReserved.format(
            day=data['date'],
            tm=data['time'],
            notes=data['notes']
        )).as_markdown(),
        reply_markup=keyboard
    )
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
        await message.answer(Text(lex_messages.techProblems).as_markdown())


@admin_records_router.callback_query(F.data == f'{lex_buttons.no.callback}-admin-record',
                                     FSMRecordReservation.confirmation)
async def not_reservation_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the no button for reserve time
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.clear()
    logger.debug(f'The user {callback.message.from_user.id} did not confirm the selected time and date')
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
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        return
    keyboard = await AdminCalendar().start_calendar()
    if keyboard.error:
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        msg = await callback.message.answer(Text(lex_messages.recordsWorkerCalendar).as_markdown(),
                                            reply_markup=keyboard.entity)
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
            await callback.message.answer(Text(lex_messages.techProblems).as_markdown())


@admin_records_router.callback_query(F.data == f'{lex_buttons.yes.callback}-admin-record',
                                     FSMRecordReservation.confirmation)
async def reservation_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the yes button for reserve time
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} confirm the selected time and date')
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
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    data = await state.get_data()
    create = await create_registration(data['date'], data['time'], callback.from_user.id, data['notes'])
    if create.error:
        logger.warning(create.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        msg = await callback.message.answer(Text(lex_messages.reservedOk.format(name=create.entity.user.name
                                                                                )).as_markdown())
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
            await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    await state.set_state()


@admin_records_router.callback_query(RecordCallback.filter())
async def admin_record_view_route(callback: CallbackQuery, callback_data: RecordCallback, state: FSMContext) -> None:
    """
    A function that processes the returned data from the record button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param callback_data: tg.keyboards.RecordCallback
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} view the selected record')
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
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    await RecordsKeyboard().process(callback, callback_data, state)


@admin_records_router.message(FSMRecordNotes.replace)
async def admin_record_replace_notes_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMRecordNotes.replace
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user {message.from_user.id} replace the notes')
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
        await message.answer(Text(lex_messages.techProblems).as_markdown())
    data = await state.get_data()
    record = await record_update_notes(data['id'], message.text)
    if record.error:
        logger.warning(record.errorText)
        await message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        await state.clear()
        msg_text = (f'Заметки изменены!\n'
                    f'Дата: {record.entity.date.strftime("%d-%m-%Y")}\n'
                    f'Время: {record.entity.time.strftime("%H:%M")}\n'
                    f'Заметки: {record.entity.notes}\n'
                    f'Имя: {record.entity.user.name}\n'
                    f'Фамилия: {record.entity.user.surname}\n'
                    f'Телефон: {record.entity.user.phone_number}\n'
                    f'Заметки о пользователе: {record.entity.user.notes}\n')
        if record.entity.confirmation_day:
            msg_text += f'Подтверждение за сутки: Да\n'
        else:
            msg_text += f'Подтверждение за сутки: Нет\n'
        if record.entity.confirmation_two_hours:
            msg_text += f'Подтверждение за два часа: Да\n'
        else:
            msg_text += f'Подтверждение за два часа: Нет\n'
        keyboard = Keyboard(1, '-admin-calendar').create_inline(lex_buttons.back)
        msg = await message.answer(Text(msg_text).as_markdown(), reply_markup=keyboard)
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
            await message.answer(Text(lex_messages.techProblems).as_markdown())


@admin_records_router.message(FSMRecordNotes.add)
async def admin_record_add_notes_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMRecordNotes.add
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'The user {message.from_user.id} add the notes')
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
        await message.answer(Text(lex_messages.techProblems).as_markdown())
    data = await state.get_data()
    record = await record_update_notes(data['id'], f'{data["notes"]} | {message.text}')
    if record.error:
        logger.warning(record.errorText)
        await message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        await state.clear()
        msg_text = (f'Заметка добавлена!\n'
                    f'Дата: {record.entity.date.strftime("%d-%m-%Y")}\n'
                    f'Время: {record.entity.time.strftime("%H:%M")}\n'
                    f'Заметки: {record.entity.notes}\n'
                    f'Имя: {record.entity.user.name}\n'
                    f'Фамилия: {record.entity.user.surname}\n'
                    f'Телефон: {record.entity.user.phone_number}\n'
                    f'Заметки о пользователе: {record.entity.user.notes}\n')
        if record.entity.confirmation_day:
            msg_text += f'Подтверждение за сутки: Да\n'
        else:
            msg_text += f'Подтверждение за сутки: Нет\n'
        if record.entity.confirmation_two_hours:
            msg_text += f'Подтверждение за два часа: Да\n'
        else:
            msg_text += f'Подтверждение за два часа: Нет\n'
        keyboard = Keyboard(1, '-admin-calendar').create_inline(lex_buttons.back)
        msg = await message.answer(Text(msg_text).as_markdown(), reply_markup=keyboard)
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
            await message.answer(Text(lex_messages.techProblems).as_markdown())


__all__ = 'admin_records_router'
