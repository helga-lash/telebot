from tg.handlers.user.confirmation import user_confirmation_router
from tg.handlers.user.info import user_info_router
from tg.handlers.user.registration import user_registration_router
from tg.handlers.user.records import user_records_router


user_routers_list = [
    user_confirmation_router,
    user_info_router,
    user_registration_router,
    user_records_router
]


__all__ = user_routers_list
