from aiogram.types import InlineKeyboardMarkup


from domain.enums import UserRole, AdvertiserType
from presentation.ui.keyboard import Btn, build_kb
from presentation.ui.callbacks import NavCb, RoleCb
from application.services.routing_service import RoutingService

def how_to_payment_screen(routing: RoutingService) -> tuple[str, InlineKeyboardMarkup]:
    text = (
        "Теперь все выплаты начисляются напрямую на ваш личный счёт «Телепорт» в рамках нашей платформы.\n\n"
        "<b>Как вывести средства?</b>\n\n"
        "1) Зайдите в личный кабинет: <a href='https://tele-port.me'>tele-port.me</a>\n"
        "2) Откройте вкладку «Настройки».\n"
        "3) В блоке «Расписание выплат» нажмите «Вывести средства».\n"
        "4) Выплата приходит в течение <b>1–3 банковских дней</b>.\n"
    )

    accounting_url = routing.get_target(UserRole.ACCOUNTING).open_url
    kb = build_kb(
        [
            Btn("Остались бухгалтерские вопросы?", url=accounting_url),  # временно
        ],
        columns=1,
        back=Btn("⬅️ Назад", cb=NavCb(action="back", screen="owner_menu").pack()),
    )
    return text, kb