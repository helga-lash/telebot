import asyncio

from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.formatting import Text
from datetime import date, time
from io import BytesIO

from configuration import logger, apl_conf
from tg.lexicon import lex_buttons, lex_messages
from tg.keyboards import Keyboard, AdminCalendar, AdminCalendarCallback, RecordsKeyboard, RecordCallback
from tg.states import FSMUser, FSMRecordNotes, FSMRecordReservation, FSMPhotoDownload
from tg.helpers_functions import remove_message
from database import rec_day, record_update_notes, create_registration
from s3_minio import s3_client

admin_router = Router()


@admin_router.callback_query(F.data == f'{lex_buttons.yes.callback}-adminReg')
async def admin_reg_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the yes button in admin registration
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.update_data(admin=True)
    await callback.message.answer(Text(lex_messages.name).as_markdown())
    await state.set_state(FSMUser.name)


@admin_router.callback_query(F.data == f'{lex_buttons.record.callback}-admin')
@admin_router.callback_query(F.data == f'{lex_buttons.back.callback}-calendar')
async def admin_records_view_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the record button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    keyboard = await AdminCalendar().start_calendar()
    if keyboard.error:
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        await callback.message.answer(Text(lex_messages.recordsWorkerCalendar).as_markdown(),
                                      reply_markup=keyboard.entity)


@admin_router.callback_query(AdminCalendarCallback.filter())
async def admin_calendar_route(callback: CallbackQuery, callback_data: AdminCalendarCallback,
                               state: FSMContext) -> None:
    """
    A function that processes the returned data from the calendar button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param callback_data: tg.keyboards.AdminCalendarCallback
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
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
                await callback.message.answer(Text(msg_text).as_markdown(), reply_markup=keyboard)


@admin_router.callback_query(F.data == lex_buttons.timeReserve.callback)
async def admin_time_reserve_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the time reserve button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    day = (await state.get_data())['date']
    records = await rec_day(day)
    if records.error:
        logger.warning(records.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    buttons = []
    for tm in apl_conf.tgBot.recordTime:
        if tm not in [x.time for x in records.entity]:
            buttons.append(f'{str(tm).split(':')[0]}:{str(tm).split(':')[1]}')
    keyboard = Keyboard(3).create_inline(*buttons)
    await callback.message.answer(Text(lex_messages.reserveTime).as_markdown(), reply_markup=keyboard)
    await state.set_state(FSMRecordReservation.time)


@admin_router.callback_query(FSMRecordReservation.time)
async def admin_record_reserve_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes state FSMRecordReservation.time
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.update_data(time=time(*[int(x) for x in callback.data.split(':')]))
    await state.set_state(FSMRecordReservation.confirmation)
    data = await state.get_data()
    keyboard = Keyboard(2, '-record').create_inline(lex_buttons.yes, lex_buttons.no)
    await callback.message.answer(
        Text(lex_messages.recordReserved.format(
            day=data['date'],
            tm=data['time']
        )).as_markdown(),
        reply_markup=keyboard
    )


@admin_router.callback_query(F.data == f'{lex_buttons.no.callback}-record', FSMRecordReservation.confirmation)
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
    keyboard = await AdminCalendar().start_calendar()
    if keyboard.error:
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        await callback.message.answer(Text(lex_messages.recordsWorkerCalendar).as_markdown(),
                                      reply_markup=keyboard.entity)


@admin_router.callback_query(F.data == f'{lex_buttons.yes.callback}-record', FSMRecordReservation.confirmation)
async def reservation_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the yes button for reserve time
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
        await callback.message.answer(Text(lex_messages.reservedOk.format(name=create.entity.user.name)).as_markdown())
    await state.set_state()


@admin_router.callback_query(RecordCallback.filter())
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
    await RecordsKeyboard().process(callback, callback_data, state)


@admin_router.message(FSMRecordNotes.replace)
async def admin_record_replace_notes_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMRecordNotes.replace
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
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
        keyboard = await Keyboard(1, '-calendar').create_inline(lex_buttons.back)
        await message.answer(Text(msg_text).as_markdown(), reply_markup=keyboard)


@admin_router.message(FSMRecordNotes.add)
async def admin_record_add_notes_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMRecordNotes.add
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
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
        keyboard = await Keyboard(1, '-calendar').create_inline(lex_buttons.back)
        await message.answer(Text(msg_text).as_markdown(), reply_markup=keyboard)


@admin_router.callback_query(F.data == f'{lex_buttons.info.callback}-admin')
@admin_router.callback_query(F.data == f'{lex_buttons.back.callback}-admin')
async def admin_info_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the info button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(2).create_inline(lex_buttons.addedPhoto, lex_buttons.changeContact)
    await callback.message.answer(Text(lex_messages.infoWorker).as_markdown(), reply_markup=keyboard)


@admin_router.callback_query(F.data == lex_buttons.changeContact.callback)
async def admin_change_contact_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the change contact button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await callback.message.answer(Text('Здесь будет изменение информации о контактах').as_markdown())


@admin_router.callback_query(F.data == lex_buttons.addedPhoto.callback)
@admin_router.callback_query(F.data == f'{lex_buttons.back.callback}-photos', FSMPhotoDownload.waitePhoto)
async def admin_added_photo_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.clear()
    keyboard = Keyboard(2, '-admin').create_inline(lex_buttons.reviews, lex_buttons.trends,
                                                   lex_buttons.naturals, lex_buttons.bulks, lex_buttons.back)
    await callback.message.answer(Text(lex_messages.addedPhoto).as_markdown(), reply_markup=keyboard)


@admin_router.callback_query(F.data == f'{lex_buttons.trends.callback}-admin')
async def admin_reviews_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo in category trends button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.set_state(FSMPhotoDownload.waitePhoto)
    await state.update_data(bucket='trends')
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    await callback.message.answer(Text(lex_messages.addPhotoTrends).as_markdown(), reply_markup=keyboard)


@admin_router.callback_query(F.data == f'{lex_buttons.naturals.callback}-admin')
async def admin_reviews_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo in category naturals button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.set_state(FSMPhotoDownload.waitePhoto)
    await state.update_data(bucket='naturals')
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    await callback.message.answer(Text(lex_messages.addPhotoNaturals).as_markdown(), reply_markup=keyboard)


@admin_router.callback_query(F.data == f'{lex_buttons.reviews.callback}-admin')
async def admin_reviews_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo in category reviews button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.set_state(FSMPhotoDownload.waitePhoto)
    await state.update_data(bucket='reviews')
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    await callback.message.answer(Text(lex_messages.addPhotoReviews).as_markdown(), reply_markup=keyboard)


@admin_router.callback_query(F.data == f'{lex_buttons.bulks.callback}-admin')
async def admin_reviews_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo in category bulks button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    await state.set_state(FSMPhotoDownload.waitePhoto)
    await state.update_data(bucket='bulks')
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    await callback.message.answer(Text(lex_messages.addPhotoBulks).as_markdown(), reply_markup=keyboard)


@admin_router.message(FSMPhotoDownload.waitePhoto)
async def admin_download_photo_route(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    data = BytesIO()
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    if message.photo:
        await message.bot.download(file=message.photo[-1].file_id, destination=data)
        filename = f'{message.photo[-1].file_id}.jpg'
        file_size = message.photo[-1].file_size
    elif message.document:
        await message.bot.download(file=message.document.file_id, destination=data)
        filename = f'{message.document.file_id}.jpg'
        file_size = message.document.file_size
    else:
        await message.answer(Text(lex_messages.addPhotoNotPhoto, reply_markup=keyboard).as_markdown())
        return
    data.seek(0)
    upload = await s3_client.upload(
        state_data['bucket'],
        filename,
        data,
        file_size
    )
    if upload.error:
        logger.warning(upload.errorText)
        await message.answer(Text(lex_messages.techProblems).as_markdown())
        await state.clear()
        await message.delete()
        return
    msg = await message.answer(Text(lex_messages.addedPhotoOk).as_markdown(), show_alert=True)
    await message.delete()
    asyncio.create_task(remove_message(msg.bot, message.chat.id, msg.message_id, 5.0))


__all__ = 'admin_router'
