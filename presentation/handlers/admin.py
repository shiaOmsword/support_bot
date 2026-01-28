import logging
from datetime import datetime, timedelta, timezone

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import settings
from infrastructure.db.uow import UnitOfWork
from infrastructure.db.state_repo import UserStateRepository, BotStateRepository
from typing import Tuple

router = Router()
log = logging.getLogger(__name__)


def _is_admin(message: Message) -> bool:
    return bool(message.from_user) and message.from_user.id in settings.admin_ids

def _parse_target(s: str) -> tuple[str, str]:
    """
    Возвращает ("id", "123") или ("username", "vasya")
    """
    s = s.strip()
    if s.startswith("@"):
        return ("username", s.lstrip("@"))
    return ("id", s)

def _parse_duration_to_seconds(arg: str) -> int:
    """
    Поддержка:
      300        -> 300 секунд
      15m        -> 15 минут
      2h         -> 2 часа
      1d         -> 1 день
    """
    s = arg.strip().lower()
    if not s:
        raise ValueError("empty duration")

    # чистое число = секунды
    if s.isdigit():
        return int(s)

    unit = s[-1]
    num = s[:-1]
    if not num.isdigit():
        raise ValueError("bad duration")

    n = int(num)
    if unit == "s":
        return n
    if unit == "m":
        return n * 60
    if unit == "h":
        return n * 3600
    if unit == "d":
        return n * 86400

    raise ValueError("bad unit")


@router.business_message(Command("sleep"))
@router.message(Command("sleep"))
async def sleep_cmd(
    message: Message,
    state: FSMContext,
    uow: UnitOfWork,
    bot_state_repo: BotStateRepository,
):
    if not _is_admin(message):
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /sleep 2h  | /sleep 15m | /sleep 300")
        return

    try:
        seconds = _parse_duration_to_seconds(parts[1])
    except ValueError:
        await message.answer("Не понял длительность. Примеры: /sleep 2h, /sleep 15m, /sleep 300")
        return

    now = datetime.now(timezone.utc)
    sleep_until = now + timedelta(seconds=seconds)

    async with uow.session() as session:
        await bot_state_repo.set_sleep_until(session, sleep_until=sleep_until)
    
    local = sleep_until.astimezone(timezone(timedelta(hours=3)))
    await message.answer(f"Ок. Усыпил бота до {local:%Y-%m-%d %H:%M:%S} (MSK)")



@router.business_message(Command("wake"))
@router.message(Command("wake"))
async def wake_cmd(
    message: Message,
    state: FSMContext,
    uow: UnitOfWork,
    bot_state_repo: BotStateRepository,
):
    if not _is_admin(message):
        return

    async with uow.session() as session:
        await bot_state_repo.set_sleep_until(session, sleep_until=None)

    await message.answer("Ок. Бот проснулся ✅")


@router.business_message(Command("status"))
@router.message(Command("status"))
async def status_cmd(
    message: Message,
    uow: UnitOfWork,
    bot_state_repo: BotStateRepository,
):
    if not _is_admin(message):
        return

    async with uow.session() as session:
        st = await bot_state_repo.get_singleton(session)
        
    sleep_until =  f"{st.sleep_until.astimezone(timezone(timedelta(hours=3))):%Y-%m-%d %H:%M:%S}" if st.sleep_until else "нет"

    await message.answer(f"Состояние бота:\nспит до: {sleep_until} (MSK)")


# ---- опционально: mute / unmute конкретного пользователя ----

@router.business_message(Command("mute"))
@router.message(Command("mute"))
async def mute_user_cmd(
    message: Message,
    uow: UnitOfWork,
    user_state_repo: UserStateRepository,
):
    if not _is_admin(message):
        return

    # /mute <user_id> 5h
    parts = (message.text or "").split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Использование: /mute <user_id> 5h  |  /mute <user_id> 15m")
        return

    try:
        user_id = int(parts[1])
        seconds = _parse_duration_to_seconds(parts[2])
    except ValueError:
        await message.answer("Не понял аргументы. Пример: /mute 123456 5h")
        return

    muted_until = datetime.now(timezone.utc) + timedelta(seconds=seconds)

    async with uow.session() as session:
        await user_state_repo.set_muted_until(session, user_id=user_id, muted_until=muted_until)

    local = muted_until.astimezone(timezone(timedelta(hours=3)))
    
    await message.answer(f"Ок. Замьютил user_id={user_id} до {local:%Y-%m-%d %H:%M:%S} (MSK)")


@router.business_message(Command("unmute"))
@router.message(Command("unmute"))
async def unmute_user_cmd(
    message: Message,
    uow: UnitOfWork,
    user_state_repo: UserStateRepository,
):
    if not _is_admin(message):
        return

    # /unmute <user_id>
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /unmute <user_id>")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("user_id должен быть числом. Пример: /unmute 123456")
        return

    async with uow.session() as session:
        await user_state_repo.set_muted_until(session, user_id=user_id, muted_until=None)

    await message.answer(f"Ок. Размьютил user_id={user_id} ✅")


@router.business_message(Command("user"))
@router.message(Command("user"))
async def user_status_cmd(
    message: Message,
    uow: UnitOfWork,
    user_state_repo: UserStateRepository,
):
    if not _is_admin(message):
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /user <user_id>  или  /user @username")
        return

    kind, val = _parse_target(parts[1])

    async with uow.session() as session:
        if kind == "id":
            try:
                user_id = int(val)
            except ValueError:
                await message.answer("user_id должен быть числом. Или укажи @username.")
                return
            st = await user_state_repo.get(session, user_id=user_id)
        else:
            st = await user_state_repo.get_by_username(session, username=val)

    if not st:
        await message.answer("Не нашёл пользователя в базе (он ещё не писал боту).")
        return

    muted = st.muted_until.isoformat() if st.muted_until else "нет"
    blocked = st.blocked_until.isoformat() if getattr(st, "blocked_until", None) else "нет"
    await message.answer(
        "Состояние пользователя:\n"
        f"user_id: {st.user_id}\n"
        f"username: @{st.username}" if st.username else f"user_id: {st.user_id}\nusername: нет"
    )
    await message.answer(
        f"muted_until: {muted}\n"
        f"blocked_until: {blocked}\n"
        f"menu_message_id: {st.menu_message_id or 'нет'}\n"
        f"business_connection_id: {st.business_connection_id or 'нет'}"
    )
    
    
@router.business_message(Command("block"))
@router.message(Command("block"))
async def block_cmd(
    message: Message,
    uow: UnitOfWork,
    user_state_repo: UserStateRepository,
):
    if not _is_admin(message):
        return

    parts = (message.text or "").split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Использование: /block <user_id|@username> 5h  |  /block 123456 15m")
        return

    kind, val = _parse_target(parts[1])

    try:
        seconds = _parse_duration_to_seconds(parts[2])
    except ValueError:
        await message.answer("Не понял длительность. Примеры: 15m, 2h, 1d, 300")
        return

    now = datetime.now(timezone.utc)
    blocked_until = now + timedelta(seconds=seconds)

    async with uow.session() as session:
        if kind == "id":
            try:
                user_id = int(val)
            except ValueError:
                await message.answer("user_id должен быть числом. Или укажи @username.")
                return
            await user_state_repo.set_blocked_until(session, user_id=user_id, blocked_until=blocked_until)
        else:
            st = await user_state_repo.get_by_username(session, username=val)
            if not st:
                await message.answer("Не нашёл этого @username в базе (он ещё не писал боту).")
                return
            await user_state_repo.set_blocked_until(session, user_id=st.user_id, blocked_until=blocked_until)
            user_id = st.user_id

    await message.answer(f"Ок. Заблокировал user_id={user_id} до {blocked_until.isoformat()}")
    
    
@router.business_message(Command("unblock"))
@router.message(Command("unblock"))
async def unblock_cmd(
    message: Message,
    uow: UnitOfWork,
    user_state_repo: UserStateRepository,
):
    if not _is_admin(message):
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /unblock <user_id|@username>")
        return

    kind, val = _parse_target(parts[1])

    async with uow.session() as session:
        if kind == "id":
            try:
                user_id = int(val)
            except ValueError:
                await message.answer("user_id должен быть числом. Или укажи @username.")
                return
            await user_state_repo.set_blocked_until(session, user_id=user_id, blocked_until=None)
        else:
            st = await user_state_repo.get_by_username(session, username=val)
            if not st:
                await message.answer("Не нашёл этого @username в базе.")
                return
            await user_state_repo.set_blocked_until(session, user_id=st.user_id, blocked_until=None)
            user_id = st.user_id

    await message.answer(f"Ок. Разблокировал user_id={user_id} ✅")
        