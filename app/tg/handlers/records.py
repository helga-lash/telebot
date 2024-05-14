from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.formatting import Text

from datetime import date, time

from tg.lexicon import lex_buttons, lex_messages, lex_commands
from tg.keyboards import Keyboard, SimpleCalendar, CalendarCallback
from tg.states import FSMRecord, FSMUser
from configuration import logger, apl_conf
from database.functions import rec_day, user_by_id, create_user, create_registration

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


@records_router.callback_query(CalendarCallback.filter(), FSMRecord.date)
async def process_simple_calendar_route(callback: CallbackQuery,
                                        callback_data: CalendarCallback, state: FSMContext) -> None:
    """
    A function that processes the returned data from the calendar in state FSMRecord.date
    :param callback: aiogram.types.CallbackQuery
    :param callback_data: tg.keyboards.CalendarCallback
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
                        if tm not in [x.time for x in records.entity]:
                            buttons.append(str(tm))
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
                    day=data['date'],
                    tm=data['time']
                )).as_markdown(),
                reply_markup=keyboard
            )
        else:
            keyboard = Keyboard(1, '-registration').create_inline(lex_buttons.no)
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
    await state.update_data(name=message.text)
    await state.set_state(FSMUser.surname)
    await message.answer(Text(lex_messages.userSurname).as_markdown())


@records_router.message(FSMUser.surname)
async def user_surname_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMUser.surname
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await state.update_data(surname=message.text)
    await state.set_state(FSMUser.phone_number)
    await message.answer(Text(lex_messages.userPhone).as_markdown())


@records_router.message(FSMUser.phone_number)
async def user_phone_route(message: Message, state: FSMContext) -> None:
    """
    A function that processes state FSMUser.phone_number
    :param message: aiogram.types.Message
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await state.update_data(phone_number=message.text)
    await state.set_state(FSMUser.confirmation)
    data = await state.get_data()
    keyboard = Keyboard(2, '-user-reg').create_inline(lex_buttons.yes, lex_buttons.no)
    await message.answer(Text(lex_messages.userConfirm.format(
        surname=data['surname'],
        name=data['name'],
        phone=data['phone_number']
    )).as_markdown(), reply_markup=keyboard)


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
    await state.set_state(FSMUser.name)
    keyboard = Keyboard(1, '-registration').create_inline(lex_buttons.no)
    await callback.message.answer(Text(lex_messages.userName).as_markdown(), reply_markup=keyboard)


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
    data = await state.get_data()
    create = await create_user(callback.from_user.id, data['name'], data['surname'], data['phone_number'])
    if create.error:
        logger.warning(create.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        await state.clear()
    else:
        await state.update_data(user=create.entity.tg_id)
        await state.set_state(FSMRecord.confirmation)
        keyboard = Keyboard(2, '-record').create_inline(lex_buttons.yes, lex_buttons.no)
        await callback.message.answer(
            Text(lex_messages.recordConfirm.format(
                day=data['date'],
                tm=data['time']
            )).as_markdown(),
            reply_markup=keyboard
        )


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
    await state.set_state()


__all__ = 'records_router'
