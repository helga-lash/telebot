import asyncio

from aiogram import Bot

from configuration import logger, apl_conf
from database import update_job, delete_jobs, select_jobs_for_work
from database.entities.scheduler_jobs.work_class import SchedulerJobType
from database.lash import objects_ro, objects_rw


async def schedule(bot: Bot) -> None:
    while apl_conf.run:
        await asyncio.sleep(30)
        del_rows = await delete_jobs()
        if del_rows.error:
            logger.warning('Unable to delete old jobs')
            continue
        logger.info(f'Deleted {del_rows.entity} old jobs')
        records = await select_jobs_for_work()
        if records.error:
            logger.warning('Skipping a loop iteration')
            continue
        for record in records.entity:
            lock = await update_job(record.id, True)
            if lock.error:
                logger.warning(f'Unable to lock record ID={record.id}')
                continue
            match record.data.type:
                case SchedulerJobType.REMOVE_MESSAGE:
                    try:
                        await bot.delete_message(chat_id=record.data.chat_id, message_id=record.data.message_id)
                    except Exception as error:
                        logger.warning(f'Unable to delete message ID={record.data.message_id}: {error}')
                case SchedulerJobType.SEND_MESSAGE:
                    await bot.send_message(chat_id=record.data.chat_id, text=record.data.text,
                                           reply_markup=record.data.keyboard)
                case _:
                    logger.warning(f'Unknown job type {record.data.type}, record ID={record.id}')
                    continue
            done = await update_job(record.id, False)
            if done.error:
                logger.warning(f'Unable to unlock record ID={record.id}')
    await objects_rw.close()
    await objects_ro.close()
    logger.info("Closed database connections")


__all__ = 'schedule'
