from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

MENU_MESSAGE_ID_KEY = "menu_message_id"

async def send_or_edit_menu(
    chat_message: Message,
    state: FSMContext,
    text: str,
    reply_markup=None,
    disable_web_page_preview:bool=True,
):
    data = await state.get_data()
    menu_message_id = data.get(MENU_MESSAGE_ID_KEY)

    # 1) Пытаемся отредактировать существующее меню
    if menu_message_id:
        try:
            await chat_message.bot.edit_message_text(
                chat_id=chat_message.chat.id,
                message_id=menu_message_id,
                text=text,
                reply_markup=reply_markup,
                disable_web_page_preview=disable_web_page_preview,
            )
            return
        except TelegramBadRequest:
            # сообщение удалено / слишком старое / нет прав / “message is not modified” и т.д.
            pass

    # 2) Если редактирование не удалось — отправляем новое
    msg = await chat_message.answer(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=disable_web_page_preview,
    )
    await state.update_data({MENU_MESSAGE_ID_KEY: msg.message_id})
