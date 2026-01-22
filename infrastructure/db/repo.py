from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.models import UserChoiceModel
from domain.entities import UserChoice

class UserChoiceRepository:
    async def add(self, session: AsyncSession, choice: UserChoice) -> None:
        session.add(
            UserChoiceModel(
                user_id=choice.user_id,
                username=choice.username,
                role=choice.role.value,
                created_at=choice.created_at,  # <-- добавили
            )
        )
