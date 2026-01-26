from enum import Enum

class UserRole(str, Enum):
    CHANNEL_OWNER = "channel_owner"
    ADVERTISER = "advertiser"
    ACCOUNTING = "accounting"
    SUPPORT = "support"


class AdvertiserType(str, Enum):
    NEW = "new"
    EXISTING = "existing"
