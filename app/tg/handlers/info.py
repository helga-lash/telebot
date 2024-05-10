from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram import F

from tg.lexicon import lex_buttons, lex_messages
from tg.keyboards import Keyboard
from configuration import logger


info_router: Router = Router()


@info_router.callback_query(F.data == lex_buttons.info.callback)
async def info(callback: CallbackQuery):
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the info button')
    keyboard = Keyboard.create_inline(3, '', lex_buttons.works,
                                      lex_buttons.reviews, lex_buttons.contacts)
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer(lex_messages.info, reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.works.callback)
async def works(callback: CallbackQuery):
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the works button')
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    keyboard = Keyboard.create_inline(3, '', lex_buttons.trends,
                                      lex_buttons.naturals, lex_buttons.bulks)
    await callback.message.answer(lex_messages.works, reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.trends.callback)
async def works(callback: CallbackQuery):
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the trends button')
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    keyboard = Keyboard.create_inline(2, '', lex_buttons.record, lex_buttons.info,
                                      lex_buttons.works, lex_buttons.next)
    await callback.message.answer('Здесь будут фотографии работ', reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.naturals.callback)
async def works(callback: CallbackQuery):
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the naturals button')
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    keyboard = Keyboard.create_inline(2, '', lex_buttons.record, lex_buttons.info,
                                      lex_buttons.works, lex_buttons.next)
    await callback.message.answer('Здесь будут фотографии работ', reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.bulks.callback)
async def works(callback: CallbackQuery):
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the bulks button')
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    keyboard = Keyboard.create_inline(2, '', lex_buttons.record, lex_buttons.info,
                                      lex_buttons.works, lex_buttons.next)
    await callback.message.answer('Здесь будут фотографии работ', reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.reviews.callback)
async def works(callback: CallbackQuery):
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the reviews button')
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    keyboard = Keyboard.create_inline(2, '', lex_buttons.record,
                                      lex_buttons.info, lex_buttons.next)
    await callback.message.answer('Здесь будут скриншеты отзывов', reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.contacts.callback)
async def works(callback: CallbackQuery):
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the contacts button')
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer('Здесь будут контакты')


__all__ = 'info_router'
