from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

MENU_KEY = "menu_message_id"
BC_KEY = "business_connection_id"


async def edit_menu(
    *,
    bot: Bot,
    message: Message,
    state: FSMContext,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    data = await state.get_data()
    menu_id = data.get(MENU_KEY)
    bc_id = data.get(BC_KEY) or getattr(message, "business_connection_id", None)

    # Фоллбек: если меню-id ещё нет, редактируем текущее сообщение (кнопки нажали на нём)
    if not menu_id:
        try:
            await message.edit_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)
            return
        except TelegramBadRequest:
            # если не получилось — пусть вызывающий покажет новое меню
            raise

    kwargs = dict(
        chat_id=message.chat.id,
        message_id=int(menu_id),
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )
    if bc_id:
        kwargs["business_connection_id"] = bc_id

    await bot.edit_message_text(**kwargs)
