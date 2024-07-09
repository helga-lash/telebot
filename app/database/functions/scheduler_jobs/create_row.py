from datetime import datetime

from database.lash import objects_rw, SchedulerJobsRW
from database.entities import SchedulerJobsRecord, UserRecord, SchedulerJob
from helpers.work_classes import ReturnEntity
from configuration import logger


async def create_job(user: int, job: SchedulerJob, exec_time: datetime) -> ReturnEntity:
    """
    This function creates a new job record in the database.

    :param user: The ID of the user who created the job.
    :type user: int
    :param job: The job to be created.
    :type job: SchedulerJob
    :param exec_time: The execution time of the job.
    :type exec_time: datetime
    :return: A ReturnEntity object indicating whether the job was created successfully and any error messages.
    :rtype: ReturnEntity
    """
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_rw.create(
            SchedulerJobsRW,
            execute_time=exec_time,
            data=job.to_dict(),
            user_id=str(user)
        )
        result.entity = SchedulerJobsRecord(
            id=record.id,
            executeTime=record.execute_time,
            data=SchedulerJob.from_dict(record.data),
            user=UserRecord(
                tg_id=record.user_id.tg_id,
                name=record.user_id.name,
                surname=record.user_id.surname,
                phone_number=record.user_id.phone_number,
                notes=record.user_id.notes
            ),
            createdAt=record.created_at,
            updatedAt=record.updated_at,
            lock=record.lock,
            done=record.done
        )
        result.error = False
        logger.debug(f'Added job record with id={result.entity.id}')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result


__all__ = 'create_job'
