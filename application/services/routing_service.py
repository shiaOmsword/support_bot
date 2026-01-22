from dataclasses import dataclass
from domain.enums import UserRole, AdvertiserType

@dataclass(frozen=True)
class RouteTarget:
    deliver_chat_id: int
    open_url: str
    thread_id: int | None = None
    
class RoutingService:
    def __init__(
        self,
        owner_deliver_chat_id: int,
        owner_open_url: str,
        owner_thread_id: int | None,
        adv_new_deliver_chat_id: int,
        adv_new_open_url: str,
        adv_new_thread_id: int | None,
        adv_existing_deliver_chat_id: int,
        adv_existing_open_url: str,
        adv_existing_thread_id: int | None,
    ):
        self._targets = {
            ("channel_owner", None): RouteTarget(owner_deliver_chat_id, owner_open_url, owner_thread_id),
            ("advertiser", "new"): RouteTarget(adv_new_deliver_chat_id, adv_new_open_url, adv_new_thread_id),
            ("advertiser", "existing"): RouteTarget(adv_existing_deliver_chat_id, adv_existing_open_url, adv_existing_thread_id),
        }

    def get_target(self, role: UserRole, adv_type: AdvertiserType | None = None) -> RouteTarget:
        key = (role.value, adv_type.value if adv_type else None)
        try:
            return self._targets[key]
        except KeyError:
            raise ValueError(f"No target for role={role} adv_type={adv_type}")
