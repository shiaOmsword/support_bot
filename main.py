import asyncio
from typing import Callable, Awaitable, Any

from aiogram import Bot, Dispatcher
from aiogram.types import TelegramObject
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from di.container import build_container, Container
from presentation.routers import build_root_router
from presentation.middlewares.throttling import ThrottlingMiddleware
from presentation.middlewares.message_throttling import MessageThrottlingMiddleware
from presentation.middlewares.support_gate import SupportGateMiddleware
from infrastructure.db.base import Base
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

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
        data["uow"] = self._container.uow
        data["user_state_repo"] = self._container.user_state_repo
        data["bot_state_repo"] = self._container.bot_state_repo
        return await handler(event, data)

async def on_startup(container: Container) -> None:
    async with container.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main() -> None:
    container = build_container()
    await on_startup(container)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(DIMiddleware(container))
    
    dp.message.middleware(MessageThrottlingMiddleware(rate_limit_seconds=1.0))
    dp.callback_query.middleware(ThrottlingMiddleware(rate_limit_seconds=1.0)) 
    
    dp.message.middleware(SupportGateMiddleware(container.uow, container.user_state_repo, container.bot_state_repo))
    dp.business_message.middleware(SupportGateMiddleware(container.uow, container.user_state_repo, container.bot_state_repo))
    
    
    
    dp.include_router(build_root_router())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
