from database.lash import objects_rw, UsersRW
from database.entities import UserRecord
from helpers.work_classes import ReturnEntity
from configuration import logger


async def create_user(tg_id: int, name: str, surname: str, phone: str, admin: bool) -> ReturnEntity:
    """
    Function that creates a new user in the database
    :param tg_id: telegram user ID
    :param name: username
    :param surname: user surname
    :param phone: user phone number
    :param admin: user status
    :return: ReturnEntity where entity is database.entities.UserRecord
    """
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_rw.create(UsersRW, tg_id=str(tg_id), name=name, surname=surname,
                                         phone_number=phone, admin=admin)
        result.entity = UserRecord(
            tg_id=record.tg_id,
            name=record.name,
            surname=record.surname,
            phone_number=record.phone_number,
            admin=record.admin
        )
        result.error = False
        logger.debug(f'A user has been added with the following data: id={result.entity.tg_id}, '
                     f'name={result.entity.name}, surname={result.entity.surname}, phone={result.entity.phone_number},'
                     f'admin={result.entity.admin}')
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result
