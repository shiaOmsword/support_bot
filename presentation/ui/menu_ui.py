from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

MENU_KEY = "menu_message_id"
BC_KEY = "business_connection_id"


async def show_new_menu(
    *,
    bot: Bot,
    message: Message,
    state: FSMContext,
    text: str,
    reply_markup: InlineKeyboardMarkup,
) -> int:
    bc_id = (await state.get_data()).get(BC_KEY) or getattr(message, "business_connection_id", None)
    if bc_id:
        await state.update_data(**{BC_KEY: bc_id})

    kwargs = dict(
        chat_id=message.chat.id,
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )
    if bc_id:
        kwargs["business_connection_id"] = bc_id

    sent = await bot.send_message(**kwargs)
    await state.update_data(**{MENU_KEY: sent.message_id})
    return sent.message_id
