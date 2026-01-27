from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


ROOT_KEY = "root_message_id"
BC_KEY = "business_connection_id"


async def _get_bc_id(message: Message, state: FSMContext) -> str | None:
    data = await state.get_data()
    return data.get(BC_KEY) or getattr(message, "business_connection_id", None)


async def ensure_root_message(
    *,
    bot: Bot,
    message: Message,
    state: FSMContext,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> int:
    """
    Гарантирует, что у нас есть root_message_id.
    Если нет — отправляет первое root-сообщение и сохраняет его id в FSM.
    """
    # запоминаем business_connection_id, если он есть
    bc_id = await _get_bc_id(message, state)
    if bc_id:
        await state.update_data(**{BC_KEY: bc_id})

    data = await state.get_data()
    root_id = data.get(ROOT_KEY)
    if root_id:
        return int(root_id)

    # создаём root-сообщение (как бизнес, если bc_id есть)
    kwargs = dict(
        chat_id=message.chat.id,
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )
    if bc_id:
        kwargs["business_connection_id"] = bc_id  # важно для business :contentReference[oaicite:1]{index=1}

    sent = await bot.send_message(**kwargs)
    await state.update_data(**{ROOT_KEY: sent.message_id})
    return sent.message_id


async def edit_root_message(
    *,
    bot: Bot,
    message: Message,
    state: FSMContext,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Строго редактирует одно root-сообщение.
    Если редактирование невозможно (удалили/не найдено) — пересоздаёт root и обновляет FSM.
    """
    root_id = await ensure_root_message(bot=bot, message=message, state=state, text=text, reply_markup=reply_markup)
    bc_id = await _get_bc_id(message, state)

    try:
        kwargs = dict(
            chat_id=message.chat.id,
            message_id=root_id,
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
        if bc_id:
            kwargs["business_connection_id"] = bc_id

        await bot.edit_message_text(**kwargs)
    except TelegramBadRequest:
        # root сообщение могли удалить/устарело/нельзя редактировать -> пересоздаём
        data = await state.get_data()
        data.pop(ROOT_KEY, None)
        await state.set_data(data)

        await ensure_root_message(bot=bot, message=message, state=state, text=text, reply_markup=reply_markup)
