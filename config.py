from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

CHANNEL_ID = '-4555803331'


class Settings(BaseSettings):
    bot_token: SecretStr

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
        env_file_encoding='UTF-8',
    )


settings = Settings()
