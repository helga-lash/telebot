from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.formatting import Text
from datetime import datetime, timedelta

from configuration import logger
from tg.lexicon import lex_buttons, lex_messages
from tg.states import FSMUser
from database.entities.scheduler_jobs.work_class import SchedulerJobType, SchedulerJob
from database import create_job
from scheduler import delete_msq_queue

admin_registration_router = Router()


@admin_registration_router.callback_query(F.data == f'{lex_buttons.yes.callback}-adminReg')
async def admin_reg_route(callback: CallbackQuery, state: FSMContext) -> None:
    """
    A function that processes the returned data from the yes button in admin registration
    :param callback: aiogram.types.CallbackQuery
    :param state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await callback.answer()
    await callback.message.delete_reply_markup()
    logger.debug(f'User {callback.message.from_user.id} wants to register as admin')
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
        await delete_msq_queue.put(callback.message)
    await state.update_data(admin=True)
    msg = await callback.message.answer(Text(lex_messages.name).as_markdown())
    await state.set_state(FSMUser.name)
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
        await delete_msq_queue.put(msg)


__all__ = 'admin_registration_router'
