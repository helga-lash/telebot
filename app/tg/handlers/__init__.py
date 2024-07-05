from tg.handlers.command import command_router
from tg.handlers.not_match import not_match_router
from tg.handlers.info import info_router
from tg.handlers.records import records_router
from tg.handlers.admin import admin_router
from tg.handlers.confirmation import confirmation_router


__all__ = (
    'command_router',
    'not_match_router',
    'info_router',
    'records_router',
    'admin_router',
    'confirmation_router'
)
