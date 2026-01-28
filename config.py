from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, Field, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
    )

    
    admin_ids_raw: str = Field(default="", alias="ADMIN_IDS")
    default_mute_seconds: int = Field(default=18000, alias="DEFAULT_MUTE_SECONDS")
    
    @property
    def admin_ids(self) -> set[int]:
        if not self.admin_ids_raw.strip():
            return set()
        return {int(x.strip()) for x in self.admin_ids_raw.split(",") if x.strip()}

    bot_token: str = Field(alias="BOT_TOKEN")
    database_url: str = Field(alias="DATABASE_URL")

    owner_deliver_chat_id: int = Field(alias="OWNER_DELIVER_CHAT_ID")
    owner_open_url: AnyUrl = Field(alias="OWNER_OPEN_URL")
    owner_thread_id: int | None = Field(default=None, alias="OWNER_THREAD_ID")

    adv_new_deliver_chat_id: int = Field(alias="ADV_NEW_DELIVER_CHAT_ID")
    adv_new_open_url: AnyUrl = Field(alias="ADV_NEW_OPEN_URL")
    adv_new_thread_id: int | None = Field(default=None, alias="ADV_NEW_THREAD_ID")
    
    adv_existing_deliver_chat_id: int = Field(alias="ADV_EXISTING_DELIVER_CHAT_ID")
    adv_existing_open_url: AnyUrl = Field(alias="ADV_EXISTING_OPEN_URL")
    adv_existing_thread_id: int | None = Field(default=None, alias="ADV_EXISTING_THREAD_ID")
    
    owner_accounting_open_url: AnyUrl = Field(alias="OWNER_ACCOUNTING_OPEN_URL")
    support_open_url: AnyUrl = Field(alias="SUPPORT_OPEN_URL")

settings = Settings()
