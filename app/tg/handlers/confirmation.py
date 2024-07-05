from uuid import UUID
from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.utils.formatting import Text

from tg.lexicon import lex_buttons, lex_messages
from tg.helpers_functions import send_message
from database import update_confirmation, delete_record
from configuration import logger, apl_conf


confirmation_router: Router = Router()


@confirmation_router.callback_query(F.data.startswith(f'{lex_buttons.yes.callback}-confirmation_day'))
async def yes_confirmation_day_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the yes button in confirmation day
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    confirm = await update_confirmation(UUID(callback.data.split(':')[-1]), True)
    if confirm.error:
        logger.warning(f'Unable to confirm record ID={confirm.entity.id}')
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        await callback.message.delete_reply_markup()
        for admin in apl_conf.tgBot.admins:
            await send_message(
                callback.bot,
                admin,
                Text(lex_messages.adminConfirmation.format(
                    name=confirm.entity.user.name,
                    surname=confirm.entity.user.surname,
                    date=confirm.entity.date.strftime("%d-%m-%Y"),
                    time=confirm.entity.time.strftime("%H:%M")
                )).as_markdown()
            )


@confirmation_router.callback_query(F.data.startswith(f'{lex_buttons.yes.callback}-confirmation_two_hours'))
async def yes_confirmation_day_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the yes button in confirmation day
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    confirm = await update_confirmation(UUID(callback.data.split(':')[-1]), False)
    if confirm.error:
        logger.warning(f'Unable to confirm record ID={confirm.entity.id}')
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        await callback.message.delete_reply_markup()
        for admin in apl_conf.tgBot.admins:
            await send_message(
                callback.bot,
                admin,
                Text(lex_messages.adminConfirmation.format(
                    name=confirm.entity.name,
                    surname=confirm.entity.surname,
                    date=confirm.entity.date.strftime("%d-%m-%Y"),
                    time=confirm.entity.time.strftime("%H:%M")
                )).as_markdown()
            )


@confirmation_router.callback_query(F.data.startswith(f'{lex_buttons.no.callback}-confirmation'))
async def no_confirmation_route(callback: CallbackQuery) -> None:
    """
    A function that processes the returned data from the yes button in confirmation day
    :param callback: aiogram.types.CallbackQuery
    :return: None
    """
    await callback.answer()
    delete = await delete_record(UUID(callback.data.split(':')[-1]))
    if delete.error:
        logger.warning(f'Unable to confirm record ID={delete.entity.id}')
        await callback.message.answer(Text(lex_messages.techProblems).as_markdown())
    else:
        await callback.message.delete_reply_markup()
        for admin in apl_conf.tgBot.admins:
            await send_message(
                callback.bot,
                admin,
                Text(lex_messages.adminRecordDelete.format(
                    name=delete.entity.user.name,
                    surname=delete.entity.user.surname,
                    date=delete.entity.date.strftime("%d-%m-%Y"),
                    time=delete.entity.time.strftime("%H:%M")
                )).as_markdown()
            )


__all__ = 'confirmation_router'
