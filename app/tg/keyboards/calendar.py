import calendar
from datetime import datetime, timedelta, time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

from configuration import logger
from helpers_functions import check_month, check_day


class CalendarCallback(CallbackData, prefix='calendar'):
    act: str
    year: int
    month: int
    day: int


class SimpleCalendar:

    @staticmethod
    def __month(month: int = datetime.now().month) -> str:
        match month:
            case 1:
                return 'Янв'
            case 2:
                return 'Фев'
            case 3:
                return 'Мар'
            case 4:
                return 'Апр'
            case 5:
                return 'Май'
            case 6:
                return 'Июнь'
            case 7:
                return 'Июль'
            case 8:
                return 'Авг'
            case 9:
                return 'Сен'
            case 10:
                return 'Окт'
            case 11:
                return 'Ноя'
            case 12:
                return 'Дек'

    async def start_calendar(self, year: int = datetime.now().year,
                             month: int = datetime.now().month) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: InlineKeyboardMarkup object with the calendar.
        """
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []
        ignore_callback = CalendarCallback(act="IGNORE", year=year, month=month, day=0)  # for buttons with no answer
        # First row - Month and Year
        first_row = await check_month(month)
        if not first_row['previous']:
            buttons.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback.pack()))
        else:
            buttons.append(InlineKeyboardButton(text="<<", callback_data=CalendarCallback(act="PREV-MONTH",
                                                                                          year=year, month=month,
                                                                                          day=1).pack()))
        buttons.append(InlineKeyboardButton(text=f'{self.__month(month)} {str(year)}',
                                            callback_data=ignore_callback.pack()))
        if not first_row['next']:
            buttons.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback.pack()))
        else:
            buttons.append(InlineKeyboardButton(text=">>", callback_data=CalendarCallback(act="NEXT-MONTH",
                                                                                          year=year, month=month,
                                                                                          day=1).pack()))
        # Second row - Week Days
        for day_week in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
            buttons.append(InlineKeyboardButton(text=day_week, callback_data=ignore_callback.pack()))
        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            for day in week:
                ver_day = await check_day(year, month, day)
                if ver_day['cb']:
                    buttons.append(InlineKeyboardButton(text=ver_day['text'],
                                                        callback_data=CalendarCallback(act="DAY",
                                                                                       year=year, month=month,
                                                                                       day=day).pack()))
                else:
                    buttons.append(InlineKeyboardButton(text=ver_day['text'], callback_data=ignore_callback.pack()))
        # Last row - Button
        buttons.append(InlineKeyboardButton(text="❌ - нет свободных окошек",
                                            callback_data=ignore_callback.pack()))

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
