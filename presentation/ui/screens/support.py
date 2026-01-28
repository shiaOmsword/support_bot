from aiogram.types import InlineKeyboardMarkup
from domain.enums import UserRole, AdvertiserType
from presentation.ui.keyboard import Btn, build_kb
from presentation.ui.callbacks import NavCb, RoleCb
from application.services.routing_service import RoutingService
from presentation.texts.common import support_screen_text
def support_menu_screen(routing: RoutingService) -> tuple[str, InlineKeyboardMarkup]:
    text = support_screen_text()

    support_url = routing.get_target(UserRole.SUPPORT).open_url

    kb = build_kb(
        [

        ],
        columns=1,
        back=Btn("⬅️ Назад", cb=NavCb(action="back", screen="owner_menu").pack()),
    )
    return text, kb