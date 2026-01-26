from aiogram.filters.callback_data import CallbackData


class NavCb(CallbackData, prefix="nav"):
    action: str  # "open" | "back"
    screen: str  # "roles" | "advertiser_type" | "owner_menu" | "how_to_payment"


class RoleCb(CallbackData, prefix="role"):
    role: str  # UserRole.value ("advertiser" | "channel_owner")

class ActCb(CallbackData, prefix="act"):
    name: str  # например: "send_support_ping"
