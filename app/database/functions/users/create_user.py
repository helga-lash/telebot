from database.lash import objects_rw, UsersRW
from database.entities import UserRecord
from helpers.work_classes import ReturnEntity
from configuration import logger


async def create_user(tg_id: int, name: str, surname: str, phone: str) -> ReturnEntity:
    """

    :param tg_id: telegram user ID
    :param name: username
    :param surname: user surname
    :param phone: user phone number
    :return: ReturnEntity where entity is database.entities.UserRecord
    """
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_rw.create(UsersRW, tg_id=str(tg_id), name=name, surname=surname, phone_number=phone)
        result.entity = UserRecord(
            tg_id=record.tg_id,
            name=record.name,
            surname=record.surname,
            phone_number=record.phone_number
        )
        result.error = False
        logger.debug(f'A user has been added with the following data: id={result.entity.tg_id}, '
                     f'name={result.entity.name}, surname={result.entity.surname}, phone={result.entity.phone_number}')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result
