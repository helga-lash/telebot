from datetime import date

from database.lash import RegistrationsRO, objects_ro
from helpers.work_classes import ReturnEntity
from configuration import logger


async def num_rec_day(year: int, month: int, day: int) -> ReturnEntity:
    """
    The function determines the number of records on a specific day
    :param year: year
    :param month: month
    :param day: day
    :return: ReturnEntity where entity is number of records on a specific day
    """
    dt = date(year, month, day)
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        result.entity = await objects_ro.count(RegistrationsRO.select().where(RegistrationsRO.date == dt))
        result.error = False
        logger.debug(f'Received number of records for {year}-{month}-{day} in the amount of {result.entity}')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result
