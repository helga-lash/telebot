from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from tg.lexicon.button_classes import Button


class Keyboard:
    """
    Class that allows you to create keyboards

    Methods:
        create_inline: creates an inline keyboard
        create_reply: creates a reply keyboard
    """

    @staticmethod
    def create_inline(width: int, cb_pref: str = '', *args: str or Button, **kwargs: str) -> InlineKeyboardMarkup:
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []
        if args:
            for button in args:
                if type(button) is str:
                    buttons.append(InlineKeyboardButton(text=button, callback_data=f'{button}{cb_pref}'))
                elif type(button) is Button:
                    buttons.append(InlineKeyboardButton(text=button.text, callback_data=f'{button.callback}{cb_pref}'))
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(text=text, callback_data=f'{button}{cb_pref}'))
        kb_builder.row(*buttons, width=width)
        return kb_builder.as_markup()

    @staticmethod
    def create_reply(width: int, *args: str, one_time_keyboard: bool = True) -> ReplyKeyboardMarkup:
        kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = []
        if args:
            for button in args:
                buttons.append(KeyboardButton(text=button))
        kb_builder.row(*buttons, width=width)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


__all__ = 'Keyboard'
