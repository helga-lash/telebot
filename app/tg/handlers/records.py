from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram import F

from tg.lexicon import lex_buttons, lex_messages
from tg.keyboards import Keyboard, SimpleCalendar, CalendarCallback
from configuration import logger, apl_conf

records_router: Router = Router()


@records_router.callback_query(F.data == lex_buttons.record.callback)
async def record(callback: CallbackQuery):
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the record button')
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer('На какой день хотите записаться\?',
                                  reply_markup=await SimpleCalendar().start_calendar())


@records_router.callback_query(CalendarCallback.filter())
async def process_simple_calendar(callback: CallbackQuery, callback_data: CalendarCallback):
    selected, date = await SimpleCalendar().process_selection(callback, callback_data)
    if selected:
        await callback.message.answer(
            f'You selected {date.strftime("%Y\-%m\-%d")}',
            reply_markup=callback.message.reply_markup
        )


__all__ = 'records_router'
