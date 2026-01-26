from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def role_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    # ССЫЛКА: сразу уводит в чат
    kb.button(text="Я — владелец/менеджер канала", callback_data="role:owner")

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

def owner_type_keyboard(accounting_url:str,support_url:str) ->InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Как получить выплату?", callback_data="role:owner:how_to_payment")
    kb.button(text="Бухгалтерия", url=accounting_url)
    kb.button(text="Поддержка", url=support_url)
    
    kb.button(text="⬅️ Назад", callback_data="back:roles")

    kb.adjust(1)
    return kb.as_markup()

def how_to_payment_keyboard(accounting_url:str) ->InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Остались вопросы?",  url=accounting_url)
    
    kb.button(text="⬅️ Назад", callback_data="back:roles:owner")

    kb.adjust(1)
    return kb.as_markup()
    