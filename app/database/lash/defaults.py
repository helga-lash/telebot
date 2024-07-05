from peewee import Model, CharField, TextField, UUIDField, DateField, TimeField, BooleanField, DateTimeField
from playhouse.postgres_ext import JSONField
from uuid import uuid4
from datetime import datetime


class UsersDefault(Model):
    """
    A class describing unrelated fields for the users table

    Attributes:
        tg_id: peewee.CharField(50)
            user ID in telegram
        name: peewee.CharField(10)
            username
        surname: peewee.CharField(10)
            user surname
        phone_number: peewee.CharField(20)
            user phone number
        notes: peewee.TextField
            notes about the user
    """
    tg_id = CharField(column_name='tg_id', max_length=50, unique=True, null=False, primary_key=True)
    name = CharField(column_name='name', max_length=10, null=False)
    surname = CharField(column_name='surname', max_length=10, null=False)
    phone_number = CharField(column_name='phone_number', max_length=20, unique=True, null=False)
    notes = TextField(column_name='notes')
    admin = BooleanField(column_name='admin', null=False, default=False)


class RegistrationsDefault(Model):
    """
    A class describing unrelated fields for the registrations table

    Attributes:
        id: peewee.UUIDField
            recording ID
        date: peewee.DateField
            recording date
        time: peewee.TimeField
            recording time
        confirmation_day: peewee.BooleanField
            confirmation per day
        confirmation_two_hours: peewee.BooleanField
            confirmation in two hours
        notes: peewee.TextField
            notes about the record
    """
    id = UUIDField(column_name='id', unique=True, primary_key=True, default=lambda: uuid4())
    date = DateField(column_name='date', null=False)
    time = TimeField(column_name='time', null=False)
    confirmation_day = BooleanField(column_name='confirmation_day', null=False, default=False)
    confirmation_two_hours = BooleanField(column_name='confirmation_two_hours', null=False, default=False)
    lock = BooleanField(column_name='lock', null=False, default=False)
    notes = TextField(column_name='notes')


class SchedulerJobsDefault(Model):
    """
    A class representing a job in the scheduler.

    Attributes:
        id : UUIDField
            The unique identifier for the job.
        execute_time : DateTimeField
            The time when the job should be executed.
        data : JSONField
            The data associated with the job.
        created_at : DateTimeField
            The time when the job was created.
        updated_at : DateTimeField
            The time when the job was last updated.
        lock : BooleanField
            A flag indicating whether the job is locked.
        done : BooleanField
            A flag indicating whether the job is done.
    """
    id = UUIDField(column_name='id', unique=True, primary_key=True, default=lambda: uuid4())
    execute_time = DateTimeField(column_name='execute_time', null=False)
    data = JSONField(column_name='data', null=False)
    created_at = DateTimeField(column_name='created_at', null=False, default=lambda: datetime.now())
    updated_at = DateTimeField(column_name='updated_at', null=False, default=lambda: datetime.now())
    lock = BooleanField(column_name='lock', null=False, default=False)
    done = BooleanField(column_name='done', null=False, default=False)
