from collections.abc import Callable
from aiogram.types import InlineKeyboardMarkup
from application.services.routing_service import RoutingService

from .roles import roles_screen
from .advertiser import advertiser_type_screen
from .owner import owner_menu_screen
from .how_to_payment import how_to_payment_screen
from .old_advertiser import old_advertiser_type_screen
from .support import support_menu_screen
ScreenFn = Callable[[RoutingService], tuple[str, InlineKeyboardMarkup]]

def _wrap_no_routing(fn):
    def inner(_routing: RoutingService):
        return fn()
    return inner

SCREEN_REGISTRY: dict[str, ScreenFn] = {
    "roles": _wrap_no_routing(roles_screen),
    "advertiser_type": advertiser_type_screen,
    "owner_menu": owner_menu_screen,
    "how_to_payment": how_to_payment_screen,
    "old_advertiser_type": old_advertiser_type_screen,
    "support_menu": support_menu_screen,
}
