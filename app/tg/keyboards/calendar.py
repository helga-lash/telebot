import calendar
from datetime import datetime, timedelta
from enum import Enum

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

from configuration import logger


class LexWeekDay(Enum):
    mon: str = 'Пн'
    tue: str = 'Вт'
    wed: str = 'Ср'
    thu: str = 'Чт'
    fri: str = 'Пт'
    sat: str = 'Сб'
    sun: str = 'Вс'


class LexMonthRed(Enum):
    jan: str = 'Янв'
    feb: str = 'Фев'
    mar: str = 'Мар'
    apr: str = 'Апр'
    may: str = 'Май'
    jun: str = 'Июнь'
    jul: str = 'Июль'
    aug: str = 'Авг'
    sep: str = 'Сен'
    oct: str = 'Окт'
    nov: str = 'Ноя'
    dec: str = 'Дек'


class CalendarCallback(CallbackData, prefix='calendar'):
    act: str
    year: int
    month: int
    day: int


class SimpleCalendar:

    @staticmethod
    def month(month: int = datetime.now().month) -> str:
        logger.error(f"!!!!{month}!!!!\n!!!!{calendar.month_abbr[month].lower()}!!!!")
        return eval(f"str(LexMonthRed.{calendar.month_abbr[month].lower()}.value)")

    async def start_calendar(self, year: int = datetime.now().year,
                             month: int = datetime.now().month) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []
        ignore_callback = CalendarCallback(act="IGNORE", year=year, month=month, day=0)  # for buttons with no answer
        # First row - Month and Year
        buttons.append(InlineKeyboardButton(text="<<", callback_data=CalendarCallback(act="PREV-YEAR",
                                                                                      year=year, month=month,
                                                                                      day=1).pack()))
        buttons.append(InlineKeyboardButton(text=f'{self.month(month)} {str(year)}',
                                            callback_data=ignore_callback.pack()))
        buttons.append(InlineKeyboardButton(text=">>", callback_data=CalendarCallback(act="NEXT-YEAR",
                                                                                      year=year, month=month,
                                                                                      day=1).pack()))
        # Second row - Week Days
        for day in LexWeekDay:
            buttons.append(InlineKeyboardButton(text=day.value, callback_data=ignore_callback.pack()))
        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            for day in week:
                if day == 0:
                    buttons.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback.pack()))
                    continue
                buttons.append(InlineKeyboardButton(text=str(day),
                                                    callback_data=CalendarCallback(act="DAY",
                                                                                   year=year, month=month,
                                                                                   day=day).pack()))
        # Last row - Buttons
        buttons.append(InlineKeyboardButton(text="<",
                                            callback_data=CalendarCallback(act="PREV-MONTH",
                                                                           year=year, month=month,
                                                                           day=day).pack()))
        buttons.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback.pack()))
        buttons.append(InlineKeyboardButton(text=">",
                                            callback_data=CalendarCallback(act="NEXT-MONTH",
                                                                           year=year, month=month,
                                                                           day=day).pack()))
        kb_builder.row(*buttons)
        kb_builder.adjust(3, 7)
        return kb_builder.as_markup()

    async def process_selection(self, query: CallbackQuery, data: CalendarCallback) -> tuple:
        """
        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by calendar_callback
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """
        return_data = (False, None)
        temp_date = datetime(data.year, data.month, 1)
        # processing empty buttons, answering with no action
        if data.act == "IGNORE":
            await query.answer(cache_time=60)
        # user picked a day button, return date
        if data.act == "DAY":
            await query.message.delete_reply_markup()  # removing inline keyboard
            return_data = True, datetime(data.year, data.month, data.day)
        # user navigates to previous year, editing message with new calendar
        if data.act == "PREV-YEAR":
            prev_date = datetime(data.year - 1, data.month, 1)
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(prev_date.year),
                                                                                         int(prev_date.month)))
        # user navigates to next year, editing message with new calendar
        if data.act == "NEXT-YEAR":
            next_date = datetime(data.year + 1, data.month, 1)
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(next_date.year),
                                                                                         int(next_date.month)))
        # user navigates to previous month, editing message with new calendar
        if data.act == "PREV-MONTH":
            prev_date = temp_date - timedelta(days=1)
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(prev_date.year),
                                                                                         int(prev_date.month)))
        # user navigates to next month, editing message with new calendar
        if data.act == "NEXT-MONTH":
            next_date = temp_date + timedelta(days=31)
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(next_date.year),
                                                                                         int(next_date.month)))
        # at some point user clicks DAY button, returning date
        return return_data


__all__ = (
    'SimpleCalendar',
    'CalendarCallback'
)
