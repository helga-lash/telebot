from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.formatting import Text
from aiogram.fsm.context import FSMContext
from uuid import UUID
from enum import Enum

from database.entities import RegistrationRecord
from database import record_by_id, record_update_notes
from tg.lexicon import lex_messages, lex_buttons
from tg.states import FSMRecordNotes
from configuration import logger, apl_conf


class RecordActions(Enum):
    """
    Class describe actions for a record

    Attributes:
        view: str = 'view'
        replace: str ='replace'
        delete: str = 'delete'
        add: str = 'add'
    """
    view: str = 'view'
    replace: str = 'replace'
    delete: str = 'delete'
    add: str = 'add'


class RecordCallback(CallbackData, prefix='record'):
    """
    Class that allows you to create a callback for the record button

    Attributes:
        id: UUID
        action: RecordActions
    """
    id: UUID
    action: RecordActions


class RecordsKeyboard:
    """
    Class that allows you to create a keyboard for the record button

    Methods:
        start: create an inline keyboard for the record buttons
    """
    @staticmethod
    async def start(records: list[RegistrationRecord]) -> InlineKeyboardMarkup:
        """
        Method to create an inline keyboard for record buttons
        :param records: list[RegistrationRecord]
        :return: InlineKeyboardMarkup
        """
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []
        for record in records:
            buttons.append(InlineKeyboardButton(
                text=record.time.strftime('%H:%M'),
                callback_data=RecordCallback(
                    id=record.id,
                    action=RecordActions.view).pack()
            ))
        if len(records) < len(apl_conf.tgBot.recordTime):
            buttons.append(InlineKeyboardButton(
                text=lex_buttons.timeReserve.text,
                callback_data=lex_buttons.timeReserve.callback))
        width = 3
        if len(buttons) > width:
            width = 2
        kb_builder.row(*buttons, width=width)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    async def process(query: CallbackQuery, data: RecordCallback, state: FSMContext) -> None:
        """
        Method to process the returned data from the record button
        :param query: aiogram.types.CallbackQuery
        :param data: RecordCallback
        :param state: aiogram.fsm.context.FSMContext
        :return: None
        """
        match data.action:
            case RecordActions.view:
                record = await record_by_id(data.id)
                if record.error:
                    logger.warning(record.errorText)
                    await query.message.answer(Text(lex_messages.techProblems).as_markdown())
                msg_text: str = (f'Дата: {record.entity.date.strftime("%Y-%m-%d")}\n'
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
                kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
                buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(
                    text='Заменить заметки',
                    callback_data=RecordCallback(
                        id=data.id,
                        action=RecordActions.replace).pack(
                    )), InlineKeyboardButton(
                    text='Удалить заметки',
                    callback_data=RecordCallback(
                        id=data.id,
                        action=RecordActions.delete).pack(
                    )), InlineKeyboardButton(
                    text='Добавить запись в заметки',
                    callback_data=RecordCallback(
                        id=data.id,
                        action=RecordActions.add).pack(
                    ))]
                await query.message.answer(Text(msg_text).as_markdown(),
                                           reply_markup=kb_builder.row(*buttons).as_markup())
            case RecordActions.delete:
                record = await record_update_notes(data.id)
                if record.error:
                    logger.warning(record.errorText)
                    await query.message.answer(Text(lex_messages.techProblems).as_markdown())
                msg_text: str = (f'Дата: {record.entity.date.strftime("%Y-%m-%d")}\n'
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
                await query.message.answer(Text(msg_text).as_markdown())
            case RecordActions.add:
                record = await record_by_id(data.id)
                if record.error:
                    logger.warning(record.errorText)
                    await query.message.answer(Text(lex_messages.techProblems).as_markdown())
                await state.update_data(id=data.id, notes=record.entity.notes)
                await state.set_state(FSMRecordNotes.add)
                await query.message.answer(Text(lex_messages.addNotes).as_markdown())
            case RecordActions.replace:
                await state.update_data(id=data.id)
                await state.set_state(FSMRecordNotes.replace)
                await query.message.answer(Text(lex_messages.replaceNotes).as_markdown())


__all__ = ('RecordsKeyboard', 'RecordCallback')
