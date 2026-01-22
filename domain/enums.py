from enum import Enum

class UserRole(str, Enum):
    ADVERTISER = "advertiser"
    OWNER = "owner"