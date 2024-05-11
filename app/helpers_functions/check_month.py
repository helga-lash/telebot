from datetime import datetime, timedelta

from configuration import logger, apl_conf


async def check_month(month: int) -> dict:
    """
    Function checking month for calendar
    :param month: month being checked
    :return: a dictionary containing two keys ('next', 'previous') with boolean values
    """
    result: dict = dict(next=True, previous=True)
    dt_now: datetime = datetime.now()
    if month <= dt_now.month:
        logger.debug('Can not get previous month')
        result.update(previous=False)
    if month >= (dt_now + timedelta(days=(apl_conf.tgBot.recordMonth - 1) * 31)).month:
        logger.debug('Can not get next month')
        result.update(next=False)
    return result


__all__ = 'check_month'
