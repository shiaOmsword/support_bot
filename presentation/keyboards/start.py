from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def role_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Я рекламодатель", callback_data="role:advertiser")
    kb.button(text="Я владелец канала", callback_data="role:owner")
    kb.adjust(1)
    return kb.as_markup()

def open_chat_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть чат", url=url)]
        ]
    )
