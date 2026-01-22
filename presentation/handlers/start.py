import asyncio
import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from presentation.keyboards.start import role_keyboard, support_keyboard
from domain.enums import UserRole
from application.services.routing_service import RoutingService
from presentation.texts.common import (
    start_message,
    choose_role_message,
    processing_message,
    role_result_message,
    help_message,
    about_message,
)
router = Router()
log = logging.getLogger(__name__)


async def _safe_edit_or_answer(message: Message, text: str, reply_markup=None, disable_web_page_preview: bool = True):
    """
    Пытаемся отредактировать текущее сообщение.
    Если нельзя — отправляем новое (fallback).
    """
    try:
        await message.edit_text(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview,
        )
    except TelegramBadRequest:
        await message.answer(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview,
        )


@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        start_message(),
        reply_markup=role_keyboard(),
    )


@router.message(F.text == "/help")
async def help_cmd(message: Message):
    await message.answer(help_message())


@router.message(F.text == "/about")
async def about_cmd(message: Message):
    await message.answer(about_message())


@router.callback_query(F.data == "back:roles")
async def back_to_roles(callback: CallbackQuery):
    await callback.answer()
    await _safe_edit_or_answer(
        callback.message,
        choose_role_message(),
        reply_markup=role_keyboard(),
    )


@router.callback_query(F.data.startswith("role:"))
async def role_selected(callback: CallbackQuery, routing: RoutingService):
    await callback.answer()

    # Шаг 1 — сообщение ожидания
    await _safe_edit_or_answer(
        callback.message,
        processing_message(),
        reply_markup=None,
    )

    await asyncio.sleep(0.7)

    _, raw_role = callback.data.split(":", 1)
    role = UserRole(raw_role)
    url = routing.get_target_url(role)

    user = callback.from_user

    log.info(
        "role_selected user_id=%s username=%s role=%s",
        user.id,
        user.username,
        role.value,
    )

    await routing.register_choice(
        user_id=user.id,
        username=user.username,
        role=role,
    )

    # Шаг 2 — финальный текст
    await _safe_edit_or_answer(
        callback.message,
        role_result_message(role, url),
        reply_markup=support_keyboard(url),
    )
