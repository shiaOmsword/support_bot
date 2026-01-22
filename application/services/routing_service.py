from datetime import datetime, timezone
from domain.enums import UserRole
from domain.entities import UserChoice
from infrastructure.db.repo import UserChoiceRepository
from infrastructure.db.uow import UnitOfWork

class RoutingService:
    def __init__(
        self,
        advertiser_url: str,
        owner_url: str,
        uow: UnitOfWork,
        repo: UserChoiceRepository,
    ):
        self._advertiser_url = advertiser_url
        self._owner_url = owner_url
        self._uow = uow
        self._repo = repo

    def get_target_url(self, role: UserRole) -> str:
        if role == UserRole.ADVERTISER:
            return self._advertiser_url
        if role == UserRole.OWNER:
            return self._owner_url
        raise ValueError(f"Unsupported role: {role}")

    async def register_choice(self, user_id: int, username: str | None, role: UserRole) -> None:
        choice = UserChoice(
            user_id=user_id,
            username=username,
            role=role,
            created_at=datetime.now(timezone.utc),
        )
        async with self._uow.session() as session:
            await self._repo.add(session, choice)
