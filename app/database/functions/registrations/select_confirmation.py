from datetime import date, time, datetime, timedelta

from configuration import logger
from helpers.work_classes import ReturnEntity
from database.entities import RegistrationRecord, UserRecord
from database.lash import objects_ro, RegistrationsRO


async def select_confirmation(rec_date: date, rec_time: time, per_day: bool) -> ReturnEntity:
    """
    This function selects and returns a list of registration records based on the given parameters.

    :param rec_date: date - The date of the registration records to select.
    :param rec_time: time - The time of the registration records to select.
    :param per_day: bool - A flag indicating whether to select records for a full day or two hours.

    :return: ReturnEntity - An object containing the selected registration records and any error information.

    :raise Exception: If there is an error accessing the database.
    """
    if per_day:
        delta = timedelta(days=1)
    else:
        delta = timedelta(hours=2)
    result: ReturnEntity = ReturnEntity(error=True)
    from_datetime: datetime = datetime(rec_date.year, rec_date.month, rec_date.day, rec_time.hour, rec_time.minute,
                                       rec_time.second) + delta
    to_datetime: datetime = from_datetime + timedelta(minutes=5) + delta
    from_date: date = date(from_datetime.year, from_datetime.month, from_datetime.day)
    from_time: time = time(from_datetime.hour, from_datetime.minute, from_datetime.second)
    to_date: date = date(to_datetime.year, to_datetime.month, to_datetime.day)
    to_time: time = time(to_datetime.hour, to_datetime.minute, to_datetime.second)
    query = RegistrationsRO.select().where(
        (((RegistrationsRO.date == from_date) & (RegistrationsRO.time >= from_time)) |
         ((RegistrationsRO.date == to_date) & (RegistrationsRO.time <= to_time))) &
        (RegistrationsRO.confirmation_day == (not per_day)) & ~RegistrationsRO.confirmation_two_hours
    )
    try:
        records = await objects_ro.execute(query)
        result.entity = [RegistrationRecord(
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
        ) for record in records]
        result.error = False
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result


__all__ = 'select_confirmation'
