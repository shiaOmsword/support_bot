from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models_state import UserStateModel, BotStateModel


class UserStateRepository:
    async def get(self, session: AsyncSession, *, user_id: int) -> UserStateModel | None:
        return await session.get(UserStateModel, user_id)

    async def get_by_username(self, session: AsyncSession, *, username: str) -> UserStateModel | None:
        # username храним без "@"
        username = username.lstrip("@")
        q = await session.execute(
            select(UserStateModel).where(UserStateModel.username == username).limit(1)
        )
        return q.scalar_one_or_none()

    async def set_blocked_until(self, session: AsyncSession, *, user_id: int, blocked_until) -> None:
        obj = await session.get(UserStateModel, user_id)
        if not obj:
            obj = UserStateModel(user_id=user_id, username=None)
            session.add(obj)
        obj.blocked_until = blocked_until
            
    async def get_or_create(self, session: AsyncSession, *, user_id: int, username: str | None) -> UserStateModel:
        obj = await session.get(UserStateModel, user_id)
        if obj:
            # обновим username/last_seen
            obj.username = username
            return obj

        obj = UserStateModel(user_id=user_id, username=username)
        session.add(obj)
        return obj

    async def set_muted_until(self, session: AsyncSession, *, user_id: int, muted_until: datetime | None) -> None:
        obj = await session.get(UserStateModel, user_id)
        if not obj:
            obj = UserStateModel(user_id=user_id, username=None)
            session.add(obj)
        obj.muted_until = muted_until

    async def set_menu_message_id(self, session: AsyncSession, *, user_id: int, menu_message_id: int | None) -> None:
        obj = await session.get(UserStateModel, user_id)
        if not obj:
            obj = UserStateModel(user_id=user_id, username=None)
            session.add(obj)
        obj.menu_message_id = menu_message_id

    async def set_business_connection_id(self, session: AsyncSession, *, user_id: int, bc_id: str | None) -> None:
        obj = await session.get(UserStateModel, user_id)
        if not obj:
            obj = UserStateModel(user_id=user_id, username=None)
            session.add(obj)
        obj.business_connection_id = bc_id


class BotStateRepository:
    async def get_singleton(self, session: AsyncSession) -> BotStateModel:
        q = await session.execute(select(BotStateModel).limit(1))
        obj = q.scalar_one_or_none()
        if obj:
            return obj
        obj = BotStateModel()
        session.add(obj)
        return obj

    async def set_sleep_until(self, session: AsyncSession, *, sleep_until: datetime | None) -> None:
        obj = await self.get_singleton(session)
        obj.sleep_until = sleep_until
