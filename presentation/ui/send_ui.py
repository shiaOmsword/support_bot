from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


async def send_ui(
    *,
    bot: Bot,
    message: Message,
    state: FSMContext,
    text: str,
    reply_markup=None,
    try_edit: bool = True,
) -> None:
    """
    UI-ответ:
    - если это business-чат (есть business_connection_id) -> отвечаем через send_message с business_connection_id
      (самый стабильный способ)
    - иначе -> пытаемся edit_text, если не получилось -> answer()
    """

    data = await state.get_data()
    bc_id = data.get("business_connection_id") or getattr(message, "business_connection_id", None)

    # BUSINESS MODE: отвечаем как бизнес-аккаунт
    if bc_id:
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            business_connection_id=bc_id,
        )
        return

    # NORMAL MODE: редактируем как раньше
    if try_edit:
        try:
            await message.edit_text(
                text=text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
            return
        except TelegramBadRequest:
            pass

    await message.answer(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )
