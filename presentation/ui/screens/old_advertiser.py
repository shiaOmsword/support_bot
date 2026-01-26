from aiogram.types import InlineKeyboardMarkup
from domain.enums import UserRole, AdvertiserType
from presentation.ui.keyboard import Btn, build_kb
from presentation.ui.callbacks import NavCb, RoleCb
from application.services.routing_service import RoutingService

def old_advertiser_type_screen(routing: RoutingService) -> tuple[str, InlineKeyboardMarkup]:
    text = "Выбрите, пожалуйста к кому написать:"
    old_url1 = routing.get_target(UserRole.ADVERTISER, AdvertiserType.EXISTING).open_url
    old_url2 = routing.get_target(UserRole.CHANNEL_OWNER).open_url
    kb = build_kb(
        [
            Btn("Максим", url=old_url2),
            Btn("Надежда", url=old_url1),
        ],
        columns=1,
        back=Btn("⬅️ Назад", cb=NavCb(action="back", screen="roles").pack()),
    )
    return text, kb