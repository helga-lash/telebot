from tg.handlers.admin.registration import admin_registration_router
from tg.handlers.admin.calendar import admin_calendar_router
from tg.handlers.admin.records import admin_records_router
from tg.handlers.admin.info import admin_info_router


admin_routers_list = [admin_calendar_router, admin_records_router, admin_info_router, admin_registration_router]


__all__ = 'admin_routers_list'
