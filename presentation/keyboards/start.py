from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def role_keyboard(owner_url: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    # ССЫЛКА: сразу уводит в чат
    kb.button(text="Я — владелец/менеджер канала", url=owner_url)

    # CALLBACK: нужен, чтобы показать следующее меню
    kb.button(text="Я — рекламодатель", callback_data="role:advertiser")

    kb.adjust(1)
    return kb.as_markup()


def advertiser_type_keyboard(new_advertiser_url: str, old_advertiser_url: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    # ССЫЛКИ: сразу уводят в нужный чат
    kb.button(text="Я — новый рекламодатель", url=new_advertiser_url)
    kb.button(text="Я — действующий рекламодатель", url=old_advertiser_url)

    # CALLBACK: вернуться назад в главное меню
    kb.button(text="⬅️ Назад", callback_data="back:roles")

    kb.adjust(1)
    return kb.as_markup()
