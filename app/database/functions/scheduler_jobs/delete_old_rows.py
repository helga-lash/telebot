from datetime import datetime, timedelta

from database.lash import objects_rw, SchedulerJobsRW, objects_ro, SchedulerJobsRO
from helpers.work_classes import ReturnEntity
from configuration import logger


async def delete_jobs() -> ReturnEntity:
    """
    This function deletes old job records from the database.

    :return: A ReturnEntity object indicating whether the jobs were deleted successfully and any error messages.
    :rtype: ReturnEntity
    """
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        count = await objects_ro.count(SchedulerJobsRO.select().where(
            SchedulerJobsRO.updated_at <= datetime.now() - timedelta(days=92)
        ))
        if count > 0:
            await objects_rw.execute(SchedulerJobsRW.delete().where(
                SchedulerJobsRO.updated_at <= datetime.now() - timedelta(days=92)
            ))

        result.entity = count
        result.error = False
        logger.debug(f'Deleted {count} old jobs')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result


__all__ = 'delete_jobs'
