from aiogram.filters.state import State, StatesGroup


class FSMRecord(StatesGroup):
    """
    A class describing the state machine for recording a procedure

    Arguments:
        date: aiogram.filters.state.State
            recording date selection status
        time: aiogram.filters.state.State
            recording time selection status
        user: aiogram.filters.state.State
            user registration status
        confirmation: aiogram.filters.state.State
            write confirmation status
    """
    date: State = State()
    time: State = State()
    user: State = State()
    confirmation: State = State()


__all__ = 'FSMRecord'
