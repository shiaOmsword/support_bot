from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from presentation.keyboards.start import role_keyboard, open_chat_keyboard
from domain.enums import UserRole
from application.services.routing_service import RoutingService

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "Здравствуйте. Выберите, кем вы являетесь — и я дам ссылку на нужный чат поддержки.",
        reply_markup=role_keyboard(),
    )

@router.callback_query(F.data.startswith("role:"))
async def role_selected(callback: CallbackQuery, routing: RoutingService):
    _, raw_role = callback.data.split(":", 1)

    role = UserRole(raw_role)
    url = routing.get_target_url(role)

    user = callback.from_user
    await routing.register_choice(user_id=user.id, username=user.username, role=role)

    role_label = "рекламодателя" if role == UserRole.ADVERTISER else "владельца канала"
    await callback.message.answer(
        f"Понял. Для обращения в поддержку по линии {role_label} нажмите кнопку ниже:",
        reply_markup=open_chat_keyboard(url),
    )
    await callback.answer()
