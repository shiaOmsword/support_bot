from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dataclass(frozen=True, slots=True)
class Btn:
    text: str
    cb: Optional[str] = None
    url: Optional[str] = None

    def __post_init__(self):
        if (self.cb is None) == (self.url is None):
            raise ValueError("Btn must have exactly one of: cb or url")


def build_kb(
    buttons: Sequence[Btn],
    *,
    columns: int = 1,
    back: Optional[Btn] = None,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for b in buttons:
        if b.cb:
            kb.button(text=b.text, callback_data=b.cb)
        else:
            kb.button(text=b.text, url=b.url)

    if back:
        kb.button(text=back.text, callback_data=back.cb)

    kb.adjust(columns)
    return kb.as_markup()
