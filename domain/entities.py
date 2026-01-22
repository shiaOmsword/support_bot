from dataclasses import dataclass
from datetime import datetime
from domain.enums import UserRole

@dataclass(frozen=True)
class UserChoice:
    user_id: int
    username: str | None
    role: UserRole
    created_at: datetime
