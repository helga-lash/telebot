from datetime import date

from helpers.work_classes import ReturnEntity
from configuration import logger
from database.lash import RegistrationsRO, objects_ro
from database.entities import UserRecord, RegistrationRecord


async def rec_day(day: date) -> ReturnEntity:
    """
    A function that returns records on a specific day.
    :param day: datetime.date - check day
    :return: ReturnEntity where entity is list of records on a specific day
    """
    result: ReturnEntity = ReturnEntity(error=True, entity=[])
    try:
        records = await objects_ro.execute(RegistrationsRO.select().where(RegistrationsRO.date == day))
        for record in records:
            result.entity.append(RegistrationRecord(
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
            ))
        result.error = False
        logger.debug(f'Records received for {day}')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result
