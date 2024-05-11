from peewee_async import PooledPostgresqlDatabase, Manager
from peewee import ForeignKeyField

from database.lash.defaults import UsersDefault, RegistrationsDefault
from configuration import pgs_conf

db_pool: PooledPostgresqlDatabase = PooledPostgresqlDatabase(
    pgs_conf.name,
    user=pgs_conf.rw.user,
    password=pgs_conf.rw.password,
    host=pgs_conf.rw.host,
    port=pgs_conf.rw.port,
    max_connections=pgs_conf.rw.maxConn
)

objects_rw: Manager = Manager(db_pool)


class UsersRW(UsersDefault):
    """
    The class that describes the connection to the table write-only users
    """
    class Meta:
        schema = 'lash'
        table_name = 'users'
        database = db_pool


class RegistrationsRW(RegistrationsDefault):
    """
    The class that describes the connection to the table write-only registrations

    Attributes:
        user_id: peewee.ForeignKeyField
            foreign key to users table
    """
    user_id = ForeignKeyField(UsersRW, field='tg_id', backref='registrations_user_fk', column_name='user_id',
                              on_delete='restrict', on_update='cascade')

    class Meta:
        schema = 'lash'
        table_name = 'registrations'
        database = db_pool


__all__ = (
    'UsersRW',
    'RegistrationsRW',
    'objects_rw'
)
