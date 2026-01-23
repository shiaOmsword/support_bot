import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from config import settings
from presentation.keyboards.start import role_keyboard, advertiser_type_keyboard
from presentation.texts.common import start_message, help_message, about_message

router = Router()
log = logging.getLogger(__name__)


async def safe_edit(message: Message, text: str, reply_markup=None):
    try:
        await message.edit_text(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except TelegramBadRequest:
        await message.answer(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )


@router.message(F.text == "/start")
async def start_cmd(message: Message):
    await message.answer(
        start_message(),
        reply_markup=role_keyboard(str(settings.owner_open_url)),
        disable_web_page_preview=True,
    )


@router.message(F.text == "/help")
async def help_cmd(message: Message):
    await message.answer(help_message())


@router.message(F.text == "/about")
async def about_cmd(message: Message):
    await message.answer(about_message())


# Если пользователь пишет "здрасьте" или что угодно — просто показываем меню выбора
@router.message()
async def any_text_show_menu(message: Message):
    await message.answer(
        "Выберите, куда перейти:",
        reply_markup=role_keyboard(str(settings.owner_open_url)),
        disable_web_page_preview=True,
    )


@router.callback_query(F.data == "role:advertiser")
async def advertiser_clicked(callback: CallbackQuery):
    await callback.answer()
    await safe_edit(
        callback.message,
        "Уточните, пожалуйста:",
        reply_markup=advertiser_type_keyboard(
            str(settings.adv_new_open_url),
            str(settings.adv_existing_open_url),
        )
    )


@router.callback_query(F.data == "back:roles")
async def back_to_roles(callback: CallbackQuery):
    await callback.answer()
    await safe_edit(
        callback.message,
        start_message(),
        reply_markup=role_keyboard(str(settings.owner_open_url)),
    )
