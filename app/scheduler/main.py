import asyncio

from datetime import datetime, date, time
from aiogram import Bot
from aiogram.utils.formatting import Text

from configuration import logger
from database import select_confirmation, lock_reg_row
from tg.keyboards import Keyboard
from tg.lexicon import lex_buttons, lex_messages
from tg.helpers_functions import send_message


async def schedule(bot: Bot) -> None:
    while True:
        await asyncio.sleep(60)
        now = datetime.now()
        records = await select_confirmation(
            date(now.year, now.month, now.day), time(now.hour, now.minute, now.second), True
        )
        if records.error:
            logger.warning('Skipping a loop iteration')
            continue
        for record in records.entity:
            if record.lock or record.user.admin:
                continue
            lock = await lock_reg_row(record.id)
            if lock.error:
                logger.warning(f'Unable to lock record ID={record.id}')
                continue
            keyboard = Keyboard(2, f'-confirmation_day:{record.id}').create_inline(lex_buttons.yes, lex_buttons.no)
            await send_message(
                bot,
                record.user.tg_id,
                Text(lex_messages.confirmationDay.format(
                    date=record.date.strftime("%d-%m-%Y"),
                    time=record.time.strftime("%H:%M"),
                    name=record.user.name)).as_markdown(),
                keyboard
            )
        records = await select_confirmation(
            date(now.year, now.month, now.day), time(now.hour, now.minute, now.second), False
        )
        if records.error:
            logger.warning('Skipping a loop iteration')
            continue
        for record in records.entity:
            if record.user.admin or (record.lock and record.confirmation_day):
                continue
            lock = await lock_reg_row(record.id)
            if lock.error:
                logger.warning(f'Unable to lock record ID={record.id}')
                continue
            keyboard = Keyboard(2, f'-confirmation_two_hours:{record.id}').create_inline(lex_buttons.yes,
                                                                                         lex_buttons.no)
            await send_message(
                bot,
                record.user.tg_id,
                Text(lex_messages.confirmationDay.format(
                    day=record.date.strftime("%d-%m-%Y"),
                    time=record.time.strftime("%H:%M"),
                    name=record.user.name)).as_markdown(),
                keyboard
            )


__all__ = 'schedule'
