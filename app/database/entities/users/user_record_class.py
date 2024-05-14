from dataclasses import dataclass


@dataclass(slots=True)
class UserRecord:
    """
    A class describing the user entity for convenient use in code

    Arguments:
        tg_id: str
        name: str
        surname: str
        phone_number: str
        notes: str
    """
    tg_id: str
    name: str
    surname: str
    phone_number: str
    notes: str = None
