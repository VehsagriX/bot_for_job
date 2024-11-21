from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

CHANNEL_ID_ADMIN = '-4555803331'
CHANNEL_ID_USER = '-4546613771'
all_company = [
    'KOINOTI NAV',
    'EVOLET',
    'ТаджМоторс',
    'JAC',
    'Chery',
    'BYD',
    'Ёвар',
    'Хонаи Ман',
    'АРВИС',
    'Мармари',
    'Авесто Групп',
    'ATS',
]

class Settings(BaseSettings):
    bot_token: SecretStr

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
        env_file_encoding='UTF-8',
    )


settings = Settings()
