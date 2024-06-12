import asyncio

from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F
from aiogram.utils.formatting import Text
from aiogram.fsm.context import FSMContext
from random import randint
from pathlib import Path

from tg.lexicon import lex_buttons, lex_messages
from tg.keyboards import Keyboard
from tg.helpers_functions import remove_message
from configuration import logger
from s3_minio import s3_client

info_router: Router = Router()


@info_router.callback_query(F.data == lex_buttons.info.callback)
async def info_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the info button
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await state.clear()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the info button')
    keyboard = Keyboard(3).create_inline(lex_buttons.works, lex_buttons.reviews, lex_buttons.contacts)
    await callback.message.delete_reply_markup()
    await callback.message.answer(Text(lex_messages.info).as_markdown(), reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.works.callback)
async def works_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the works button
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await state.clear()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the works button')
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(3).create_inline(lex_buttons.trends, lex_buttons.naturals, lex_buttons.bulks)
    await callback.message.answer(Text(lex_messages.works).as_markdown(), reply_markup=keyboard)


@info_router.callback_query(F.data == lex_buttons.trends.callback)
@info_router.callback_query(F.data == lex_buttons.naturals.callback)
@info_router.callback_query(F.data == lex_buttons.bulks.callback)
@info_router.callback_query(F.data == lex_buttons.reviews.callback)
@info_router.callback_query(F.data == lex_buttons.next.callback)
async def photos_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the treads button
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    logger.debug(f'The user with the ID={callback.from_user.id} clicked the {callback.data} button')
    await callback.message.delete_reply_markup()
    keyboard = Keyboard(2).create_inline(lex_buttons.record, lex_buttons.info,
                                         lex_buttons.works, lex_buttons.next)
    data = await state.get_data()
    if data.get('photo_type') is None:
        await state.update_data(photo_type=callback.data)
        photo_type = callback.data
    else:
        photo_type = data.get('photo_type')
    photos_list = await s3_client.return_photo_names(photo_type)
    if photos_list.error:
        logger.warning(photos_list.errorText)
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
        return
    for _ in range(3):
        filename = photos_list.entity.pop(randint(0, len(photos_list.entity) - 1))
        file_path = await s3_client.download(photo_type, filename)
        if file_path.error:
            logger.warning(file_path.errorText)
            await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
            return
        msg = await callback.message.answer_photo(FSInputFile(file_path.entity))
        Path(file_path.entity).unlink(missing_ok=True)
        asyncio.create_task(remove_message(msg.bot, callback.message.chat.id, msg.message_id, 3600.0))
    await callback.message.answer('Здесь будут фотографии работ', reply_markup=keyboard)


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
