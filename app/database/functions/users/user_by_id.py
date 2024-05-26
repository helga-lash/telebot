from peewee import DoesNotExist

from configuration import logger
from helpers.work_classes import ReturnEntity
from database.entities import UserRecord
from database.lash import objects_ro, UsersRO


async def user_by_id(tg_id: int) -> ReturnEntity:
    """
    Function searching for a user in the database.
    :param tg_id: telegram user ID
    :return: ReturnEntity where entity is database.entities.UserRecord or None
    """
    result: ReturnEntity = ReturnEntity(error=True)
    try:
        record = await objects_ro.get(UsersRO, tg_id=str(tg_id))
        result.entity = UserRecord(
            tg_id=record.tg_id,
            name=record.name,
            surname=record.surname,
            phone_number=record.phone_number,
            notes=record.notes,
            admin=record.admin
        )
        result.error = False
        logger.debug(f'Found user named {record.surname} {record.name}')
    except DoesNotExist:
        logger.debug(f'User with ID={tg_id} not found in database')
        result.error = False
    except Exception as error:
        logger.warning(error)
        result.error_text_append('Database access error')
    return result
