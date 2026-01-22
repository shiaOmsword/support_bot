import asyncio
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command

from domain.enums import UserRole, AdvertiserType
from application.services.routing_service import RoutingService
from presentation.keyboards.start import role_keyboard, advertiser_type_keyboard
from presentation.states import IntakeFlow
from presentation.texts.common import (
    start_message,
    choose_role_message,
    processing_message,
    role_result_message,
    help_message,
    about_message,
    send_message_to_chat,
)

router = Router()
log = logging.getLogger(__name__)

async def safe_edit(message: Message, text: str, reply_markup=None):
    try:
        await message.edit_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)
    except TelegramBadRequest:
        await message.answer(text=text, reply_markup=reply_markup, disable_web_page_preview=True)

@router.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(IntakeFlow.waiting_initial_text)
    await message.answer(about_message())
    
@router.message(F.text == "/help")
async def help_cmd(message: Message):
    await message.answer(help_message())
    
@router.message(F.text == "/about")
async def about_cmd(message: Message):
    await message.answer(about_message())        

@router.message(IntakeFlow.waiting_initial_text)
async def intake_initial_text(message: Message, state: FSMContext):
    await state.update_data(initial_text=message.text)
    await state.set_state(IntakeFlow.waiting_role)
    await message.answer(start_message(), reply_markup=role_keyboard())

@router.callback_query(IntakeFlow.waiting_role, F.data == "back:roles")
async def back_roles_from_role(callback: CallbackQuery):
    await callback.answer()
    await safe_edit(callback.message, start_message(), reply_markup=role_keyboard())

@router.callback_query(IntakeFlow.waiting_role, F.data.startswith("role:"))
async def choose_role(callback: CallbackQuery, state: FSMContext, routing: RoutingService):
    await callback.answer()
    _, raw_role = callback.data.split(":", 1)
    role = UserRole(raw_role)
    await state.update_data(role=role.value)

    if role == UserRole.ADVERTISER:
        await state.set_state(IntakeFlow.waiting_adv_type)
        await safe_edit(callback.message, "Уточните, пожалуйста:", reply_markup=advertiser_type_keyboard())
    else:
        await route_and_send(callback, state, routing, role=role, adv_type=None)

@router.callback_query(IntakeFlow.waiting_adv_type, F.data == "back:roles")
async def back_to_roles(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(IntakeFlow.waiting_role)
    await safe_edit(callback.message, start_message() , reply_markup=role_keyboard())

@router.callback_query(IntakeFlow.waiting_adv_type, F.data.startswith("adv_type:"))
async def choose_adv_type(callback: CallbackQuery, state: FSMContext, routing: RoutingService):
    await callback.answer()
    _, raw_type = callback.data.split(":", 1)
    adv_type = AdvertiserType(raw_type)

    data = await state.get_data()
    role = UserRole(data["role"])  # advertiser

    await route_and_send(callback, state, routing, role=role, adv_type=adv_type)

async def route_and_send(
    callback: CallbackQuery,
    state: FSMContext,
    routing: RoutingService,
    role: UserRole,
    adv_type: AdvertiserType | None,
):
    data = await state.get_data()
    initial_text = data.get("initial_text", "")

    await safe_edit(callback.message, processing_message())
    await asyncio.sleep(0.7)

    target = routing.get_target(role, adv_type)
    kwargs = {}
    
    if target.thread_id is not None:
        kwargs["message_thread_id"] = target.thread_id
    
    user = callback.from_user
    user_ref = f"@{user.username}" if user.username else f"user_id={user.id}"
    
    log.info(
        "role_selected user_id=%s username=%s role=%s",
        user.id,
        user.username,
        role.value,
    )

    # Отправляем менеджеру в личку (менеджер должен был нажать /start у бота)
    await callback.bot.send_message(
        chat_id=target.deliver_chat_id,
        text=send_message_to_chat(initial_text,user_ref),
        **kwargs,
    )

    # Без кнопки: только текст + кликабельная ссылка (клик всё равно нужен)
    await safe_edit(
        callback.message,
        "Готово. Я передал ваше сообщение менеджеру.\n"
        "Откройте чат с менеджером по ссылке:\n"
        f"{target.open_url}"
    )

    await state.clear()
