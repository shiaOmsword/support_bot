from aiogram.types import InlineKeyboardMarkup
from domain.enums import UserRole, AdvertiserType
from presentation.ui.keyboard import Btn, build_kb
from presentation.ui.callbacks import NavCb, RoleCb
from application.services.routing_service import RoutingService

def advertiser_type_screen(routing: RoutingService) -> tuple[str, InlineKeyboardMarkup]:
    text = "Уточните, пожалуйста:"
    new_url = routing.get_target(UserRole.ADVERTISER, AdvertiserType.NEW).open_url

    kb = build_kb(
        [
            Btn("Я — новый рекламодатель", url=new_url),
            Btn("Я — действующий рекламодатель", cb=NavCb(action="open", screen="old_advertiser_type").pack()),
        ],
        columns=1,
        back=Btn("⬅️ Назад", cb=NavCb(action="back", screen="roles").pack()),
    )
    return text, kb