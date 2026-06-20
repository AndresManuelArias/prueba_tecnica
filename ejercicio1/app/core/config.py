from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    meta_whatsapp_token: str = "mock_token_dev"
    meta_phone_number_id: str = "mock_phone_id_dev"
    meta_version_api: str = "v20.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()