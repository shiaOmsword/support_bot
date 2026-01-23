import time
from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message

class MessageThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit_seconds: float = 1.0):
        self._rate = rate_limit_seconds
        self._last: dict[int, float] = {}  # user_id -> timestamp

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.monotonic()
        last = self._last.get(user_id, 0.0)

        if now - last < self._rate:
            # Молча игнорируем (чтобы не отвечать спамеру ещё больше)
            return None

        self._last[user_id] = now
        return await handler(event, data)
