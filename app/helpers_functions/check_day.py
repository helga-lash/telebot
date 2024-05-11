from datetime import datetime

from configuration import logger, apl_conf


async def check_day(year: int, month: int, day: int) -> dict:
    """
    A function that checks whether it is possible to sign up for a procedure on this day.
    :param year: year in integer format
    :param month: month in integer format
    :param day: month day in integer format
    :return: dictionary containing the following key-value: text-string, cb-boolean
    """
    apl_conf.tgBot.recordTime.sort()
    result: dict = dict(text='', cb=False)
    dt_now: datetime = datetime.now()
    last_time = apl_conf.tgBot.recordTime[-2]
    if day == 0:
        result.update(text=' ')
        return result
    if year == dt_now.year and month == dt_now.month:
        if ((day == dt_now.day) and (dt_now.time() > last_time)) or (day < dt_now.day):
            result.update(text=f'{str(day)}❌')
            return result
    result.update(text=str(day), cb=True)
    return result
