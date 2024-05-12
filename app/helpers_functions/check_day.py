from datetime import datetime

from configuration import logger, apl_conf
from database import num_rec_day
from helpers.work_classes import ReturnEntity


async def check_day(year: int, month: int, day: int) -> ReturnEntity:
    """
    A function that checks whether it is possible to sign up for a procedure on this day.
    :param year: year in integer format
    :param month: month in integer format
    :param day: month day in integer format
    :return: ReturnEntity where entity is tuple where first value - button text, second value - callback boolean
    """
    apl_conf.tgBot.recordTime.sort()
    result: ReturnEntity = ReturnEntity(error=False, entity=('', False))
    dt_now: datetime = datetime.now()
    last_time = apl_conf.tgBot.recordTime[-2]
    if day == 0:
        result.entity = (' ', False)
        return result
    if year == dt_now.year and month == dt_now.month:
        if ((day == dt_now.day) and (dt_now.time() > last_time)) or (day < dt_now.day):
            logger.debug(f'The day {year}-{month}-{day} that passed')
            result.entity = (f'{str(day)}❌', False)
            return result
    count_record: ReturnEntity = await num_rec_day(year, month, day)
    if count_record.error:
        logger.debug(count_record.errorText)
        result.error = True
        result.error_text_append(count_record.errorText)
        return result
    if count_record.entity >= len(apl_conf.tgBot.recordTime):
        logger.debug(f'No availability per day {year}-{month}-{day}')
        result.entity = (f'{str(day)}❌', False)
        return result
    logger.debug(f'There are places available for the day {year}-{month}-{day}')
    result.entity = (str(day), True)
    return result
