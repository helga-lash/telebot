from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from tg.lexicon.button_classes import Button


class Keyboard:
    """
    Class that allows you to create keyboards

    Methods:
        create_inline: creates an inline keyboard
        create_reply: creates a reply keyboard
    Arguments:
        width: int
            number of buttons in one line
        cb_pref: str
            prefix added to callback
    """

    def __init__(self, width, cb_pref: str = ''):
        self.width = width
        self.cb_pref = cb_pref

    def create_inline(self, *args: str or Button, **kwargs: str) -> InlineKeyboardMarkup:
        """
        Method that creates a keyboard in a message
        :param args: stings or tg.lexicon.button_classes.Button
        :param kwargs: callback_data=text
        :return: aiogram.utils.keyboard.InlineKeyboardMarkup
        """
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []
        if args:
            for button in args:
                if type(button) is str:
                    buttons.append(InlineKeyboardButton(text=button, callback_data=f'{button}{self.cb_pref}'))
                elif type(button) is Button:
                    buttons.append(InlineKeyboardButton(text=button.text,
                                                        callback_data=f'{button.callback}{self.cb_pref}'))
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(text=text, callback_data=f'{button}{self.cb_pref}'))
        kb_builder.row(*buttons, width=self.width)
        return kb_builder.as_markup()

    def create_reply(self, *args: str, one_time_keyboard: bool = True) -> ReplyKeyboardMarkup:
        """
        Method that creates a keyboard in a message
        :param args: stings or tg.lexicon.button_classes.Button
        :param one_time_keyboard: boolean, default True
        :return: aiogram.utils.keyboard.InlineKeyboardMarkup
        """
        kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = []
        if args:
            for button in args:
                buttons.append(KeyboardButton(text=button))
        kb_builder.row(*buttons, width=self.width)
        return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


__all__ = 'Keyboard'
