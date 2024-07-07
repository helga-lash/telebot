from uuid import UUID

from configuration import logger
from helpers.work_classes import ReturnEntity
from database.entities import RegistrationRecord, UserRecord
from database.lash import objects_rw, RegistrationsRW


async def delete_record(record_id: UUID) -> ReturnEntity:
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_rw.get(RegistrationsRW, id=record_id)
        await objects_rw.delete(record)
        result.entity = RegistrationRecord(
            id=record.id,
            date=record.date,
            time=record.time,
            user=UserRecord(
                tg_id=record.user_id.tg_id,
                name=record.user_id.name,
                surname=record.user_id.surname,
                phone_number=record.user_id.phone_number,
                notes=record.user_id.notes
            ),
            confirmation_day=record.confirmation_day,
            confirmation_two_hours=record.confirmation_two_hours,
            notes=record.notes
        )
        result.error = False
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result


__all__ = 'delete_record'
