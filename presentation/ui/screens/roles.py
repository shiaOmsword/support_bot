from aiogram.types import InlineKeyboardMarkup
from domain.enums import UserRole, AdvertiserType
from presentation.ui.keyboard import Btn, build_kb
from presentation.ui.callbacks import NavCb, RoleCb

def roles_screen() -> tuple[str, InlineKeyboardMarkup]:
    text = "Выберите, кем вы являетесь:"
    kb = build_kb(
        [
            Btn("Я — владелец/админ канала", cb=RoleCb(role=UserRole.CHANNEL_OWNER.value).pack()),
            Btn("Я — рекламодатель", cb=RoleCb(role=UserRole.ADVERTISER.value).pack()),
        ],
        columns=1,
    )
    return text, kb