from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def role_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Я — владелец/менеджер канала", callback_data="role:channel_owner")
    kb.button(text="Я — рекламодатель", callback_data="role:advertiser")
    kb.adjust(1)
    return kb.as_markup()

def advertiser_type_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Я — новый рекламодатель", callback_data="adv_type:new")
    kb.button(text="Я — действующий рекламодатель", callback_data="adv_type:existing")
    kb.button(text="⬅️ Назад", callback_data="back:roles")
    kb.adjust(1)
    return kb.as_markup()
