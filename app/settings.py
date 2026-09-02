from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    site_phone: str = "+7 900 000-00-00"
    site_phone_tel: str = "+79000000000"
    site_city: str = "Иркутск и Иркутская область"
    site_name: str = "Камаз. Щебень"

    vk_access_token: str = ""
    vk_peer_id: str = ""

    max_bot_token: str = ""
    max_user_id: str = ""
    max_chat_id: str = ""

    database_path: Path = ROOT / "data" / "leads.db"


settings = Settings()
