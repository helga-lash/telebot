from datetime import datetime, timedelta

from database.entities import SchedulerJobsRecord, UserRecord, SchedulerJob
from database.lash import objects_ro, SchedulerJobsRO
from helpers.work_classes import ReturnEntity
from configuration import logger


async def select_jobs_for_work() -> ReturnEntity:
    result: ReturnEntity = ReturnEntity(error=True)
    from_time = datetime.now() - timedelta(minutes=5)
    to_time = datetime.now() + timedelta(minutes=5)
    try:
        records = await objects_ro.execute(
            SchedulerJobsRO.select().where(
                ((SchedulerJobsRO.execute_time >= from_time) | (SchedulerJobsRO.execute_time <= to_time)) &
                ~SchedulerJobsRO.lock & ~SchedulerJobsRO.done
            ))
        result.entity = [
            SchedulerJobsRecord(
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
            ) for record in records
        ]
        result.error = False
        logger.debug(f'Selecting {len(result.entity)} scheduler jobs')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result


__all__ = 'select_jobs_for_work'
