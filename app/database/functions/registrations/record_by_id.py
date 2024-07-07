from peewee import DoesNotExist
from uuid import UUID

from configuration import logger
from helpers.work_classes import ReturnEntity
from database.entities import RegistrationRecord, UserRecord
from database.lash import objects_ro, RegistrationsRO


async def record_by_id(record_id: UUID) -> ReturnEntity:
    """
    Method to get the record by id
    :param record_id: uuid of record
    :return: ReturnEntity where entity is RegistrationRecord or None
    """
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_ro.get(RegistrationsRO, id=record_id)
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
        logger.debug(f'Found record with ID={record_id}')
    except DoesNotExist:
        logger.debug(f'Record with ID={record_id} not found in database')
        result.error_text_append(f'Record with ID={record_id} not found in database')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result


__all__ = 'record_by_id'
