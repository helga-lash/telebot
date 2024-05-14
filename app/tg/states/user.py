from aiogram.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    """
    A class describing the state machine for user registration

    Arguments:
        name: aiogram.filters.state.State
            username wait state
        surname: aiogram.filters.state.State
            user surname wait state
        phone_number: aiogram.filters.state.State
            user phone number waiting state
        confirmation: aiogram.filters.state.State
            state of waiting for confirmation of user data
    """
    name: State = State()
    surname: State = State()
    phone_number: State = State()
    confirmation: State = State()


__all__ = 'FSMUser'
