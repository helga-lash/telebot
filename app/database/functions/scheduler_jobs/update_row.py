from datetime import datetime
from uuid import UUID

from database.lash import objects_rw, SchedulerJobsRW
from database.entities import SchedulerJobsRecord, UserRecord, SchedulerJob
from helpers.work_classes import ReturnEntity
from configuration import logger


async def update_job(record_id: UUID, lock: bool) -> ReturnEntity:
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_rw.get(SchedulerJobsRW, id=record_id)
        if lock:
            record.lock = True
        else:
            record.done = True
            record.lock = False
        record.updatedAt = datetime.now()
        await objects_rw.update(record)
        result.entity = SchedulerJobsRecord(
            id=record.id,
            executeTime=record.execute_time,
            data=SchedulerJob.from_dict(record.data),
            user=UserRecord(
                tg_id=record.user_id.tg_id,
                name=record.user_id.name,
                surname=record.user_id.surname,
                phone_number=record.user_id.phone_number,
                notes=record.user_id.notes,
                admin=record.user_id.admin
            ),
            createdAt=record.created_at,
            updatedAt=record.updated_at,
            lock=record.lock,
            done=record.done
        )
        result.error = False
        logger.debug(f'Updated job record with id={result.entity.id}')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result


__all__ = 'update_job'
