from dataclasses import dataclass
from uuid import UUID
from datetime import date, time

from database.entities.users import UserRecord


@dataclass(slots=True)
class RegistrationRecord:
    """
    A class describing the registration entity for convenient use in code

    Arguments:
        id: UUID
        date: date
        time: time
        user: UserRecord
        confirmation_day: bool
        confirmation_two_hours: bool
        notes: str
    """
    id: UUID
    date: date
    time: time
    user: UserRecord
    confirmation_day: bool
    confirmation_two_hours: bool
    notes: str = None
