import asyncio
from typing import Callable, Awaitable, Any

from aiogram import Bot, Dispatcher
from aiogram.types import TelegramObject
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from di.container import build_container, Container
from presentation.routers import build_root_router

from infrastructure.db.base import Base

class DIMiddleware:
    def __init__(self, container: Container):
        self._container = container

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["routing"] = self._container.routing
        return await handler(event, data)

async def on_startup(container: Container) -> None:
    async with container.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main() -> None:
    container = build_container()
    await on_startup(container)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(DIMiddleware(container))
    dp.include_router(build_root_router())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
