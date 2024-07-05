from aiogram.dispatcher.router import Router
from aiogram.types import Message
from aiogram.utils.formatting import Text
from datetime import datetime, timedelta

from configuration import logger
from tg.lexicon import lex_messages
from database.entities.scheduler_jobs.work_class import SchedulerJobType, SchedulerJob
from database import create_job


not_match_router: Router = Router()


@not_match_router.message()
async def send_echo_route(message: Message) -> None:
    """
    A function that processes messages that are not processed by other handlers
    :param message: aiogram.types.Message
    :return: None
    """
    logger.info(f'Did not recognize a message from a user with ID={message.from_user.id}: {message.text}')
    msg = await message.answer(Text(lex_messages.notMatch).as_markdown())
    job = await create_job(
        message.from_user.id,
        SchedulerJob(
            type=SchedulerJobType.REMOVE_MESSAGE,
            chat_id=message.chat.id,
            message_id=msg.message_id
        ),
        datetime.now() + timedelta(minutes=2)
    )
    if job.error:
        logger.warning(job.errorText)
        await message.answer(Text(lex_messages.techProblems).as_markdown())


__all__ = 'not_match_router'
