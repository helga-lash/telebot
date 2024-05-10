from peewee_async import PooledPostgresqlDatabase, Manager
from peewee import ForeignKeyField

from database.lash.defaults import UsersDefault, RegistrationsDefault
from configuration import pgs_conf

db_pool: PooledPostgresqlDatabase = PooledPostgresqlDatabase(
    pgs_conf.name,
    user=pgs_conf.ro.user,
    password=pgs_conf.ro.password,
    host=pgs_conf.ro.host,
    port=pgs_conf.ro.port,
    max_connections=5
)

objects_ro: Manager = Manager(db_pool)


class UsersRO(UsersDefault):
    class Meta:
        schema = 'lash'
        table_name = 'users'
        database = db_pool


class RegistrationsRO(RegistrationsDefault):
    user_id = ForeignKeyField(UsersRO, field='tg_id', backref='registrations_user_fk', column_name='user_id',
                              on_delete='restrict', on_update='cascade')

    class Meta:
        schema = 'lash'
        table_name = 'registrations'
        database = db_pool


__all__ = (
    'UsersRO',
    'RegistrationsRO',
    'objects_ro'
)
