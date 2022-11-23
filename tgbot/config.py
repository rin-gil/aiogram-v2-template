"""Configuration settings for the bot"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from environs import Env


BASE_DIR: Path = Path(__file__).resolve().parent


@dataclass
class DbConfig:
    """Database configuration"""

    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    """Bot data"""

    token: str
    admin_ids: tuple[int, ...]


@dataclass
class Miscellaneous:
    """Other settings"""

    other_params: Optional[str] = None


@dataclass
class Config:
    """Bot config"""

    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: Optional[str] = None) -> Config:
    """Loads settings from environment variables"""
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=tuple(map(int, env.list("ADMINS"))),
        ),
        db=DbConfig(
            host=env.str("DB_HOST"), password=env.str("DB_PASS"), user=env.str("DB_USER"), database=env.str("DB_NAME")
        ),
        misc=Miscellaneous(),
    )
