from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Optional
from aiogram.types import InlineKeyboardMarkup
from enum import Enum


class SchedulerJobType(Enum):
    """
    Enum class representing different types of scheduler jobs
    """
    SEND_MESSAGE = 'send message'
    REMOVE_MESSAGE = 'remove message'


def decode_keyboard(keyboard: dict) -> InlineKeyboardMarkup or None:
    if not isinstance(keyboard, dict):
        return None
    else:
        return InlineKeyboardMarkup.model_validate(keyboard)


def encode_keyboard(keyboard: InlineKeyboardMarkup) -> dict or None:
    if not isinstance(keyboard, InlineKeyboardMarkup):
        return None
    else:
        return keyboard.model_dump()


@dataclass_json
@dataclass(slots=True)
class SchedulerJob:
    type: SchedulerJobType = field(metadata=config(encoder=lambda x: x.value))
    chat_id: int
    message_id: Optional[int] = None
    text: Optional[str] = None
    keyboard: Optional[InlineKeyboardMarkup] = field(
        default=None,
        metadata=config(
            encoder=encode_keyboard,
            decoder=decode_keyboard
        )
    )


__all__ = (
    'SchedulerJobType',
    'SchedulerJob'
)

