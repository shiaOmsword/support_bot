from dataclasses import dataclass
from domain.enums import UserRole, AdvertiserType

@dataclass(frozen=True)
class RouteTarget:
    open_url: str
    deliver_chat_id: int | None = None
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
        owner_accounting_open_url:str,
        support_open_url:str,
    ):
        self._targets = {
            ("channel_owner", None): RouteTarget(
                open_url=owner_open_url , 
                deliver_chat_id=owner_deliver_chat_id, 
                thread_id=owner_thread_id
                ),
            ("advertiser", "new"): RouteTarget(
                open_url=adv_new_open_url, 
                deliver_chat_id=adv_new_deliver_chat_id,
                thread_id=adv_new_thread_id
                ),
            ("advertiser", "existing"): RouteTarget(
                open_url=adv_existing_open_url ,
                deliver_chat_id=adv_existing_deliver_chat_id, 
                thread_id=adv_existing_thread_id
                ),
            ("accounting", None):RouteTarget(
                open_url=owner_accounting_open_url
                ),
            ("support", None):RouteTarget(open_url=support_open_url),
        }

    def get_target(self, role: UserRole, adv_type: AdvertiserType | None = None) -> RouteTarget:
        key = (role.value, adv_type.value if adv_type else None)
        try:
            return self._targets[key]
        except KeyError:
            raise ValueError(f"No target for role={role} adv_type={adv_type}")
