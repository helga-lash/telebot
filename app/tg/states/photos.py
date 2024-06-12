from aiogram.filters.state import State, StatesGroup


class FSMPhotoDownload(StatesGroup):
    """
    A class used to represent a finite state machine for photo download process.

    Attributes
    ----------
        waitePhoto : State
            Represents the state for handling review photos.
    """
    waitePhoto: State = State()
