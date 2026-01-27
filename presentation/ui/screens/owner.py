from aiogram.types import InlineKeyboardMarkup
from domain.enums import UserRole, AdvertiserType
from presentation.ui.keyboard import Btn, build_kb
from presentation.ui.callbacks import NavCb, RoleCb
from application.services.routing_service import RoutingService

def owner_menu_screen(routing: RoutingService) -> tuple[str, InlineKeyboardMarkup]:
    text = "Уточните, пожалуйста:"
    accounting_url = routing.get_target(UserRole.ACCOUNTING).open_url
    support_url = routing.get_target(UserRole.SUPPORT).open_url

    kb = build_kb(
        [
            Btn("Как получить выплату?", cb=NavCb(action="open", screen="how_to_payment").pack()),
            Btn("Бухгалтерия", url=accounting_url),
            Btn("Поддержка", url=support_url),
        ],
        columns=1,
        back=Btn("⬅️ Назад", cb=NavCb(action="back", screen="roles").pack()),
    )
    return text, kb