from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.formatting import Text
from datetime import date, datetime, timedelta

from configuration import logger
from tg.lexicon import lex_buttons, lex_messages
from tg.keyboards import AdminCalendar, AdminCalendarCallback, RecordsKeyboard
from database import rec_day
from database.entities.scheduler_jobs.work_class import SchedulerJobType, SchedulerJob
from database import create_job

admin_calendar_router = Router()


@admin_calendar_router.callback_query(F.data == f'{lex_buttons.record.callback}-admin')
@admin_calendar_router.callback_query(F.data == f'{lex_buttons.back.callback}-admin-calendar')
async def admin_records_view_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the record button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'User: {callback.message.from_user.id} open admin calendar')
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
        msg = await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        msg = await callback.message.answer(Text(lex_messages.recordsWorkerCalendar).as_markdown(),
                                            reply_markup=keyboard.entity)
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


@admin_calendar_router.callback_query(AdminCalendarCallback.filter())
async def admin_calendar_route(callback: CallbackQuery, callback_data: AdminCalendarCallback,
                               state: FSMContext) -> None:
    """
    A function that processes the returned data from the calendar button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param callback_data: tg.keyboards.AdminCalendarCallback
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    logger.debug(f'User: {callback.message.from_user.id} working on admin calendar')
    selected_date = await AdminCalendar().process_selection(callback, callback_data)
    if selected_date.error:
        logger.warning(selected_date.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        if callback_data.act == 'DAY':
            day: date = date(selected_date.entity.year, selected_date.entity.month, selected_date.entity.day)
            records = await rec_day(day)
            if records.error:
                logger.warning(records.errorText)
                await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
            else:
                msg_text: str = ''
                for record in (sorted(records.entity, key=lambda x: x.time)):
                    msg_text += (f'{record.time.strftime("%H:%M")} - {record.user.surname} {record.user.name} '
                                 f'{record.user.phone_number}\n')
                if len(records.entity) > 0:
                    msg_text += 'Для получения дополнительной информации о записи нажмите кнопку со временем.\n'
                if date.today() <= day:
                    msg_text += f'Для резервирования времени нажмите кнопку "{lex_buttons.timeReserve.text}"'
                if msg_text == '':
                    msg_text += f'{day.strftime("%d-%m-%Y")} не было записей.'
                keyboard = await RecordsKeyboard().start(records.entity, day)
                await state.update_data(date=day)
                msg = await callback.message.answer(Text(msg_text).as_markdown(), reply_markup=keyboard)
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


__all__ = 'admin_calendar_router'
