from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.formatting import Text
from datetime import datetime, timedelta
from io import BytesIO

from configuration import logger
from tg.lexicon import lex_buttons, lex_messages
from tg.keyboards import Keyboard
from tg.states import FSMPhotoDownload
from s3_minio import s3_client
from database.entities.scheduler_jobs.work_class import SchedulerJobType, SchedulerJob
from database import create_job

admin_info_router = Router()


@admin_info_router.callback_query(F.data == f'{lex_buttons.info.callback}-admin')
@admin_info_router.callback_query(F.data == f'{lex_buttons.back.callback}-admin')
async def admin_information_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the info button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} in the information section menu')
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
    keyboard = Keyboard(2).create_inline(lex_buttons.addedPhoto, lex_buttons.changeContact)
    msg = await callback.message.answer(Text(lex_messages.infoWorker).as_markdown(), reply_markup=keyboard)
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


@admin_info_router.callback_query(F.data == lex_buttons.changeContact.callback)
async def admin_change_contact_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the change contact button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} selected change contact button in admin menu')
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
    msg = await callback.message.answer(Text('Здесь будет изменение информации о контактах').as_markdown())
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


@admin_info_router.callback_query(F.data == lex_buttons.addedPhoto.callback)
@admin_info_router.callback_query(F.data == f'{lex_buttons.back.callback}-photos', FSMPhotoDownload.waitePhoto)
async def admin_added_photo_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} selected added photo in admin menu')
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
    await state.clear()
    keyboard = Keyboard(2, '-admin').create_inline(lex_buttons.reviews, lex_buttons.trends,
                                                   lex_buttons.naturals, lex_buttons.bulks, lex_buttons.back)
    msg = await callback.message.answer(Text(lex_messages.addedPhoto).as_markdown(), reply_markup=keyboard)
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


@admin_info_router.callback_query(F.data == f'{lex_buttons.trends.callback}-admin')
async def admin_trends_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo in category trends button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} selected added photo in trends')
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
    await state.set_state(FSMPhotoDownload.waitePhoto)
    await state.update_data(bucket='trends')
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    msg = await callback.message.answer(Text(lex_messages.addPhotoTrends).as_markdown(), reply_markup=keyboard)
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


@admin_info_router.callback_query(F.data == f'{lex_buttons.naturals.callback}-admin')
async def admin_naturals_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo in category naturals button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} selected added photo in naturals')
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
    await state.set_state(FSMPhotoDownload.waitePhoto)
    await state.update_data(bucket='naturals')
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    msg = await callback.message.answer(Text(lex_messages.addPhotoNaturals).as_markdown(), reply_markup=keyboard)
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


@admin_info_router.callback_query(F.data == f'{lex_buttons.reviews.callback}-admin')
async def admin_reviews_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo in category reviews button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} selected added photo in reviews')
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
    await state.set_state(FSMPhotoDownload.waitePhoto)
    await state.update_data(bucket='reviews')
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    msg = await callback.message.answer(Text(lex_messages.addPhotoReviews).as_markdown(), reply_markup=keyboard)
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


@admin_info_router.callback_query(F.data == f'{lex_buttons.bulks.callback}-admin')
async def admin_bulks_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the added photo in category bulks button in admin menu
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'The user {callback.message.from_user.id} selected added photo in bulks')
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
    await state.set_state(FSMPhotoDownload.waitePhoto)
    await state.update_data(bucket='bulks')
    keyboard = Keyboard(1, '-photos').create_inline(lex_buttons.back)
    msg = await callback.message.answer(Text(lex_messages.addPhotoBulks).as_markdown(), reply_markup=keyboard)
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


@admin_info_router.message(FSMPhotoDownload.waitePhoto)
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
        msg = await message.answer(Text(lex_messages.addPhotoNotPhoto, reply_markup=keyboard).as_markdown())
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
    job = await create_job(
        message.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=message.chat.id,
            message_id=msg.message_id
        ),
        datetime.now() + timedelta(seconds=5)
    )
    if job.error:
        logger.warning(job.errorText)
        await message.answer(Text(lex_messages.techProblems).as_markdown())
        await state.clear()


__all__ = 'admin_info_router'
