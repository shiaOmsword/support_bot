from domain.enums import UserRole


def start_message() -> str:
    return (
        "Добрый день! Я ваш помощник Чуня.\n\n"
        "Выберите, в какой чат перейти:"
    )


def choose_role_message() -> str:
    return "Выберите, кем вы являетесь:"


def processing_message() -> str:
    return "Перенаправляю вас к сотруднику поддержки. Пожалуйста, ожидайте…"


def role_result_message(role: UserRole, url: str) -> str:
    role_label = (
        "рекламодателя"
        if role == UserRole.ADVERTISER
        else "владельца канала"
    )

    return (
        f"Вы выбрали поддержку для {role_label}.\n\n"
        f"Нажмите «Открыть чат», чтобы перейти к сотруднику.\n\n"
        f"Если кнопка не открылась — напишите менеджеру по ссылке:\n"
        f"{url}"
    )

def send_message_to_chat(initial_text:str, user_ref:str) -> str:
    return (
            f"Новый запрос от {user_ref}\n"
            f"Текст: {initial_text}"
    )
    

def help_message() -> str:
    return (
        "Помощь по боту:\n\n"
        "/start — начать работу с ботом\n"
        "/help — справка\n"
        "/about — информация о боте\n\n"
        "Для обращения в поддержку выберите роль кнопками."
    )


def about_message() -> str:
    return (
        "Бот технической поддержки.\n\n"
        "Назначение бота — быстро перевести вас в нужный чат с сотрудником поддержки "
        "в зависимости от типа запроса."
    )
