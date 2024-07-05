from peewee_async import PooledPostgresqlDatabase, Manager
from peewee import ForeignKeyField

from database.lash.defaults import UsersDefault, RegistrationsDefault, SchedulerJobsDefault
from configuration import pgs_conf

db_pool: PooledPostgresqlDatabase = PooledPostgresqlDatabase(
    pgs_conf.name,
    user=pgs_conf.ro.user,
    password=pgs_conf.ro.password,
    host=pgs_conf.ro.host,
    port=pgs_conf.ro.port,
    max_connections=pgs_conf.ro.maxConn
)

objects_ro: Manager = Manager(db_pool)


class UsersRO(UsersDefault):
    """
    The class that describes the connection to the table read-only users
    """
    class Meta:
        schema = 'lash'
        table_name = 'users'
        database = db_pool


class RegistrationsRO(RegistrationsDefault):
    """
    The class that describes the connection to the table read-only registrations

    Attributes:
        user_id: peewee.ForeignKeyField
            foreign key to users table
    """
    user_id = ForeignKeyField(UsersRO, field='tg_id', backref='registrations_user_fk', column_name='user_id',
                              on_delete='restrict', on_update='cascade', null=False)

    class Meta:
        schema = 'lash'
        table_name = 'registrations'
        database = db_pool


class SchedulerJobsRO(SchedulerJobsDefault):
    """
    The class that describes the connection to the table read-only scheduler_jobs

    Attributes:
        user_id: peewee.ForeignKeyField
            foreign key to users table. It links to the 'tg_id' field in the UsersRO table.
            It creates a backreference 'scheduler_jobs_user_fk' in the UsersRO table.
            The column name in the database for this field is 'user_id'.
            On delete, it will restrict the action.
            On update, it will cascade the action.
    """
    user_id = ForeignKeyField(UsersRO, field='tg_id', backref='scheduler_jobs_user_fk', column_name='user_id',
                              on_delete='restrict', on_update='cascade', null=False)

    class Meta:
        schema = 'lash'
        table_name = 'scheduler_jobs'
        database = db_pool


__all__ = (
    'UsersRO',
    'RegistrationsRO',
    'SchedulerJobsRO',
    'objects_ro'
)
