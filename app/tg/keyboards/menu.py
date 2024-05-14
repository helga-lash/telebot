from aiogram import Bot
from aiogram.types import BotCommand

from tg.lexicon import lex_commands


async def set_menu(bot: Bot) -> None:
    """
    Function that sets the bot menu
    :param bot: aiogram.Bot
    :return: None
    """
    main_menu_commands = [BotCommand(command=f'/{lex_commands.start.command}', description=lex_commands.start.descr),
                          BotCommand(command=f'/{lex_commands.help.command}', description=lex_commands.help.descr),
                          BotCommand(command=f'/{lex_commands.cancel.command}', description=lex_commands.cancel.descr)]
    await bot.set_my_commands(main_menu_commands)


__all__ = 'set_menu'
