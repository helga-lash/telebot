import calendar
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

from configuration import logger
from helpers_functions import check_month, check_day
from helpers.work_classes import ReturnEntity


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
                             month: int = datetime.now().month) -> ReturnEntity:
        """
        Creates an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: ReturnEntity where entity is InlineKeyboardMarkup object with the calendar.
        """
        result: ReturnEntity = ReturnEntity(error=False, entity=InlineKeyboardBuilder())
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
                ver_day: ReturnEntity = await check_day(year, month, day)
                if ver_day.error:
                    logger.debug(ver_day.errorText)
                    result.error = True
                    result.error_text_append(ver_day.errorText)
                    break
                bt_text, cb = ver_day.entity
                if cb:
                    callback_data = CalendarCallback(act="DAY", year=year, month=month, day=day).pack()
                else:
                    callback_data = ignore_callback.pack()
                buttons.append(InlineKeyboardButton(text=bt_text, callback_data=callback_data))
        # Last row - Button
        buttons.append(InlineKeyboardButton(text="❌ - нет свободных окошек",
                                            callback_data=ignore_callback.pack()))

        if not result.error:
            result.entity = result.entity.row(*buttons).adjust(3, 7).as_markup()
        return result

    async def process_selection(self, query: CallbackQuery, data: CalendarCallback) -> ReturnEntity:
        """
        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by calendar_callback
        :return: ReturnEntity where entity is datetime, indicating if a date is selected and returning the date if so.
        """
        result: ReturnEntity = ReturnEntity(error=False)
        # processing empty buttons, answering with no action
        match data.act:
            # user picked a day button, return date
            case "DAY":
                result.entity = datetime(data.year, data.month, data.day)
            # user navigates to previous year, editing message with new calendar
            case "PREV-YEAR":
                result.entity = datetime(data.year - 1, data.month, 1)
            # user navigates to next year, editing message with new calendar
            case "NEXT-YEAR":
                result.entity = datetime(data.year + 1, data.month, 1)
            # user navigates to previous month, editing message with new calendar
            case "PREV-MONTH":
                result.entity = datetime(data.year, data.month, 1) - timedelta(days=1)
            # user navigates to next month, editing message with new calendar
            case "NEXT-MONTH":
                result.entity = datetime(data.year, data.month, 1) + timedelta(days=31)

        match data.act:
            case "IGNORE":
                await query.answer(cache_time=5)
            case "DAY":
                await query.message.delete_reply_markup()  # removing inline keyboard
            case "PREV-YEAR" | "NEXT-YEAR" | "PREV-MONTH" | "NEXT-MONTH":
                keyboard = await self.start_calendar(int(result.entity.year), int(result.entity.month))
                if keyboard.error:
                    result.error = True
                    result.error_text_append(keyboard.errorText)
                else:
                    await query.message.edit_reply_markup(reply_markup=keyboard.entity)
        # at some point user clicks DAY button, returning date
        return result


__all__ = (
    'SimpleCalendar',
    'CalendarCallback'
)
