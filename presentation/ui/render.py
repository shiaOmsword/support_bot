from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest


async def safe_edit(message: Message, text: str, reply_markup=None):
    try:
        await message.edit_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)
    except TelegramBadRequest:
        await message.answer(text=text, reply_markup=reply_markup, disable_web_page_preview=True)
