from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.utils.formatting import Text

from tg.lexicon import lex_buttons, lex_messages
from tg.keyboards import Keyboard
from configuration import logger

info_router: Router = Router()


@info_router.callback_query(F.data == lex_buttons.info.callback)
async def info_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the info button
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the info button')
    keyboard = Keyboard(3).create_inline(lex_buttons.works, lex_buttons.reviews, lex_buttons.contacts)
    await callback.message.delete_reply_markup()
    await callback.message.answer(Text(lex_messages.info).as_markdown(), reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.works.callback)
async def works_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the works button
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the works button')
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(3).create_inline(lex_buttons.trends, lex_buttons.naturals, lex_buttons.bulks)
    await callback.message.answer(Text(lex_messages.works).as_markdown(), reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.trends.callback)
async def works_trends_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the treads button
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the trends button')
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(2).create_inline(lex_buttons.record, lex_buttons.info,
                                         lex_buttons.works, lex_buttons.next)
    await callback.message.answer('Здесь будут фотографии работ', reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.naturals.callback)
async def works_naturals_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the naturals button
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the naturals button')
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(2).create_inline(lex_buttons.record, lex_buttons.info,
                                         lex_buttons.works, lex_buttons.next)
    await callback.message.answer('Здесь будут фотографии работ', reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.bulks.callback)
async def works_bulk_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the bulks button
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the bulks button')
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(2).create_inline(lex_buttons.record, lex_buttons.info,
                                         lex_buttons.works, lex_buttons.next)
    await callback.message.answer('Здесь будут фотографии работ', reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.reviews.callback)
async def reviews_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the reviews button
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the reviews button')
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(2).create_inline(lex_buttons.record,
                                         lex_buttons.info, lex_buttons.next)
    await callback.message.answer('Здесь будут скриншеты отзывов', reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.contacts.callback)
async def contacts_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the contacts button
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the contacts button')
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(2).create_inline(lex_buttons.record, lex_buttons.info)
    await callback.message.answer('Здесь будут контакты', reply_markup=keyboard)


__all__ = 'info_router'
