import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from application.services.routing_service import RoutingService
from presentation.ui.callbacks import RoleCb, NavCb, ActCb

from presentation.ui.nav import get_nav, set_nav
from presentation.ui.send_ui import send_ui
from presentation.ui import screens
from presentation.texts.common import start_message, help_message, about_message
from presentation.ui.screens import SCREEN_REGISTRY
#from presentation.ui.root_ui import ensure_root_message, edit_root_message
from aiogram.filters import CommandStart
from presentation.ui.menu_ui import show_new_menu
from presentation.ui.menu_ui_edit import edit_menu

HAS_SEEN_START_KEY = "has_seen_start"
router = Router()
log = logging.getLogger(__name__)

@router.business_message(CommandStart())
@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    # сохраняем business_connection_id если пришёл
    if getattr(message, "business_connection_id", None):
        await state.update_data(business_connection_id=message.business_connection_id)

    # payload после /start
    payload = (message.text or "").split(maxsplit=1)
    start_arg = payload[1] if len(payload) > 1 else ""

    # если это вход из панели business (“Управление ботом”)
    # тебе может пригодиться user_chat_id, но хотя бы не ломаемся
    # start_arg будет вида "bizChat<user_chat_id>"
    await state.update_data(nav_stack=["roles"])

    text, kb = screens.roles_screen()
    # ВАЖНО: дальше не answer(), а через root-UI (см. пункт 3)
    await message.answer(
        start_message(),
        reply_markup=kb,
        disable_web_page_preview=True,
    )
    await state.update_data(**{HAS_SEEN_START_KEY: True})
    
@router.business_message(F.text == "/help")   
@router.message(F.text == "/help")
async def help_cmd(message: Message, state: FSMContext):
        # если это бизнес-диалог — сохраняем connection id
    if message.business_connection_id:
        await state.update_data(business_connection_id=message.business_connection_id)
    await message.answer(help_message())

@router.business_message(F.text == "/about")
@router.message(F.text == "/about")
async def about_cmd(message: Message, state: FSMContext):
    if message.business_connection_id:
        await state.update_data(business_connection_id=message.business_connection_id)
    await message.answer(about_message())

@router.business_message()
@router.message()
async def any_text_show_menu(message: Message, state: FSMContext):
    if getattr(message, "business_connection_id", None):
        await state.update_data(business_connection_id=message.business_connection_id)
    
    text = (message.text or "").strip()
    if text.startswith("/"):
        return

    data = await state.get_data()
    if data.get(HAS_SEEN_START_KEY):
        return

    await state.update_data(nav_stack=["roles"], **{HAS_SEEN_START_KEY: True})

    _, kb = screens.roles_screen()

    await show_new_menu(
        bot=message.bot,
        message=message,
        state=state,
        text=start_message(),   # <-- вместо "Выберите, куда перейти:"
        reply_markup=kb,
    )


@router.callback_query(RoleCb.filter())
async def on_role(cq: CallbackQuery, callback_data: RoleCb, state: FSMContext, routing: RoutingService):
    await cq.answer()

    nav = await get_nav(state)
    if callback_data.role == "advertiser":
        nav = nav.push("advertiser_type")
        text, kb = screens.advertiser_type_screen(routing)
    else:
        nav = nav.push("owner_menu")
        text, kb = screens.owner_menu_screen(routing)

    await set_nav(state, nav)
    await edit_menu(
        bot = cq.bot,
        message = cq.message,
        state = state,
        text = text,
        reply_markup=kb,
        )


@router.callback_query(NavCb.filter())
async def on_nav(cq: CallbackQuery, callback_data: NavCb, state: FSMContext, routing: RoutingService):
    await cq.answer()

    nav = await get_nav(state)
    if callback_data.action == "open":
        nav = nav.push(callback_data.screen)
    else:
        nav = nav.back()
    await set_nav(state, nav)

    screen_fn = SCREEN_REGISTRY.get(nav.current, SCREEN_REGISTRY["roles"])
    text, kb = screen_fn(routing)
    
    await edit_menu(
        bot = cq.bot,
        message = cq.message,
        state = state,
        text = text,
        reply_markup=kb,
        )



