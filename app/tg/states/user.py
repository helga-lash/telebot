from aiogram.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    name: State = State()
    surname: State = State()
    phone_number: State = State()
    confirmation: State = State()


__all__ = 'FSMUser'
