import logging
from datetime import datetime, timedelta, timezone

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import settings
from infrastructure.db.uow import UnitOfWork
from infrastructure.db.state_repo import UserStateRepository, BotStateRepository

router = Router()
log = logging.getLogger(__name__)


def _is_admin(message: Message) -> bool:
    return bool(message.from_user) and message.from_user.id in settings.admin_ids


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
