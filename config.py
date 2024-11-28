from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

CHANNEL_ID_ADMIN = '-4555803331'
CHANNEL_ID_USER = '-4546613771'
CHANNEL_TEST_ADMIN = '-4578540724'
CHANNEL_TEST_USER = '-4528923908'

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

users_for_voucher = [
    '6972606957',
    '283943400',
    '174628526'
]

super_admin = [
    6972606957,
    174628526,

]

class Settings(BaseSettings):
    bot_test_token: SecretStr
    bot_job_token: SecretStr
    bot_kit_support_token: SecretStr

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
        env_file_encoding='UTF-8',
    )


settings = Settings()
