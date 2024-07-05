from peewee import DoesNotExist
from uuid import UUID

from database.lash import objects_rw, RegistrationsRW
from database.entities import RegistrationRecord, UserRecord
from helpers.work_classes import ReturnEntity
from configuration import logger


async def lock_reg_row(record_id: UUID) -> ReturnEntity:
    """
    Method to lock a record in the database
    :param record_id: UUID
    :return: ReturnEntity
    """
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_rw.get(RegistrationsRW, id=record_id)
        record.lock = True
        await objects_rw.update(record)
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
            lock=record.lock,
            notes=record.notes
        )
        result.error = False
    except DoesNotExist:
        logger.debug(f'Record with ID={record_id} not found in database')
        result.error_text_append(f'Record with ID={record_id} not found in database')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result
