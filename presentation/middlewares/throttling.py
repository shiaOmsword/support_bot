import time
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit_seconds: float = 1.0):
        self._rate = rate_limit_seconds
        self._last: dict[int, float] = {}  # user_id -> timestamp

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        now = time.monotonic()
        last = self._last.get(user_id, 0.0)

        if now - last < self._rate:
            # Ничего не выполняем, просто отвечаем на callback (чтобы убрать "часики")
            await event.answer("Слишком часто. Подождите секунду.", show_alert=False)
            return None

        self._last[user_id] = now
        return await handler(event, data)
