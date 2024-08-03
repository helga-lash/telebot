from datetime import date, time

from database.lash import objects_rw, RegistrationsRW
from database.entities import RegistrationRecord, UserRecord
from helpers.work_classes import ReturnEntity
from configuration import logger


async def create_registration(dt: date, tm: time, user_id: int, notes: str = None) -> ReturnEntity:
    """
    A function that adds an entry to the registration table
    :param dt: date
    :param tm: time
    :param user_id: telegram user ID
    :param notes: notes for the user record
    :return: ReturnEntity where entity is database.entities.RegistrationRecord
    """
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_rw.create(
            RegistrationsRW,
            date=dt,
            time=tm,
            user_id=str(user_id),
            notes=notes
        )
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
            confirmation_two_hours=record.confirmation_two_hours
        )
        result.error = False
        logger.debug(f'Added user record with id={result.entity.user.tg_id} on {result.entity.date} '
                     f'at {result.entity.time}')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result
