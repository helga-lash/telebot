from peewee import Model, CharField, TextField, UUIDField, DateField, TimeField, BooleanField
from uuid import uuid4


class UsersDefault(Model):
    tg_id = CharField(column_name='tg_id', max_length=50, unique=True, null=False, primary_key=True)
    name = CharField(column_name='name', max_length=50, null=False)
    surname = CharField(column_name='surname', max_length=50, null=False)
    phone_number = CharField(column_name='phone_number', max_length=20, unique=True, null=False)
    description = TextField(column_name='description')


class RegistrationsDefault(Model):
    id = UUIDField(column_name='id', unique=True, primary_key=True, default=lambda: uuid4())
    date = DateField(column_name='date', null=False)
    time = TimeField(column_name='time', null=False)
    confirmation_day = BooleanField(column_name='confirmation_day', null=False, default=False)
    confirmation_two_hours = BooleanField(column_name='confirmation_two_hours', null=False, default=False)
    description = TextField(column_name='description')
