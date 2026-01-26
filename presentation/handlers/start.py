import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from application.services.routing_service import RoutingService
from presentation.ui.callbacks import RoleCb, NavCb, ActCb
from domain.enums import UserRole
from presentation.texts.common import send_message_to_chat
from presentation.ui.nav import get_nav, set_nav
from presentation.ui.render import safe_edit
from presentation.ui import screens
from presentation.texts.common import start_message, help_message, about_message
from presentation.ui.screens import SCREEN_REGISTRY

router = Router()
log = logging.getLogger(__name__)


@router.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext):
    await state.update_data(nav_stack=["roles"])
    text, kb = screens.roles_screen()
    await message.answer(start_message(), reply_markup=kb, disable_web_page_preview=True)


@router.message(F.text == "/help")
async def help_cmd(message: Message):
    await message.answer(help_message())


@router.message(F.text == "/about")
async def about_cmd(message: Message):
    await message.answer(about_message())


@router.message()
async def any_text_show_menu(message: Message, state: FSMContext):
    await state.update_data(nav_stack=["roles"])
    text, kb = screens.roles_screen()
    await message.answer("Выберите, куда перейти:", reply_markup=kb, disable_web_page_preview=True)


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
    await safe_edit(cq.message, text, reply_markup=kb)


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
    await safe_edit(cq.message, text, reply_markup=kb)



