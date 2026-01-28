from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from infrastructure.db.uow import UnitOfWork
from infrastructure.db.state_repo import UserStateRepository, BotStateRepository
from config import settings

from datetime import timezone

def ensure_aware_utc(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def _is_command(text: str | None) -> bool:
    return bool(text) and text.strip().startswith("/")


class SupportGateMiddleware(BaseMiddleware):
    def __init__(self, uow: UnitOfWork, user_repo: UserStateRepository, bot_repo: BotStateRepository):
        self.uow = uow
        self.user_repo = user_repo
        self.bot_repo = bot_repo

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        username = event.from_user.username
        text = event.text

        # 1) Админы: не запускаем клиентский флоу на их сообщения (кроме команд)
        if user_id in settings.admin_ids and not _is_command(text):
            return None

        now = datetime.now(timezone.utc)

        async with self.uow.session() as session:
            bot_state = await self.bot_repo.get_singleton(session)
            sleep_until = ensure_aware_utc(bot_state.sleep_until)

            if sleep_until and now < sleep_until:
                if user_id in settings.admin_ids and _is_command(text):
                    return await handler(event, data)
                return None

            st = await self.user_repo.get_or_create(session, user_id=user_id, username=username)
            blocked_until = ensure_aware_utc(getattr(st, "blocked_until", None))
            if blocked_until and now < blocked_until:
                # блокировка режет вообще всё, включая команды
                return None            

            bc_id = getattr(event, "business_connection_id", None)
            if bc_id:
                st.business_connection_id = bc_id

            muted_until = ensure_aware_utc(st.muted_until)
            if muted_until and now < muted_until:
                if _is_command(text):
                    return await handler(event, data)
                return None

            if not _is_command(text):
                st.muted_until = now + timedelta(seconds=settings.default_mute_seconds)

        return await handler(event, data)
