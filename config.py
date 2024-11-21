from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

CHANNEL_ID_ADMIN = '-4555803331'
CHANNEL_ID_USER = '-4546613771'
all_company = [
    'KOINOTI NAV',
    'EVOLET',
    'ТаджМоторс',
    'JAC Motors',
    'CHERY',
    'BYD',
    'ЁВАР',
    'ХОНАМ МАН',
    'АРВИС',
    'Мармари',
    'Авесто Групп',
    'ATS',
    'Склад МЧС',
    'Склад МЯМО',
    'Склад Худжанд',
    'Склад Курган',
    'АСД',
    'ИАС',
    'РАЗЕС',
    'BYD Кова',
    'ДАСТРАС',
    'МЕДСИ',
    'SPEY MEDICAL',
    'Lady Healthcare',
    'Belinda',
    'Belinda Ophtalmology',
    'VEGAPHARM',
    'NEO UNIVERSE',
]


class Settings(BaseSettings):
    bot_token: SecretStr

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
        env_file_encoding='UTF-8',
    )


settings = Settings()
