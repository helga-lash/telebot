from aiogram.filters.state import State, StatesGroup


class FSMRecord(StatesGroup):
    date: State = State()
    time: State = State()
    user: State = State()
    confirmation: State = State()


__all__ = 'FSMRecord'
