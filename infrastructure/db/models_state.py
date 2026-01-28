from datetime import datetime
from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.db.base import Base


class UserStateModel(Base):
    __tablename__ = "user_state"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)

    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # “не беспокоить до”
    muted_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # для редактирования текущего меню
    menu_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # бизнес-режим
    business_connection_id: Mapped[str | None] = mapped_column(String(128), nullable=True)


class BotStateModel(Base):
    __tablename__ = "bot_state"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sleep_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
