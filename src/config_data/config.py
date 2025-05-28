from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class AdminData:
    id: list[int]


@dataclass
class Redis:
    host: str
    port: int


@dataclass
class DatabaseConfig:
    url: str


@dataclass
class Config:
    database: DatabaseConfig
    redis: Redis
    bot_token: TgBot
    admin_data: AdminData


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)

    raw_admin_ids = env.str('ADMIN_ID')
    admin_ids = [int(i.strip()) for i in raw_admin_ids.split(',') if i.strip().isdigit()]
    return Config(
        database=DatabaseConfig(url=env.str('URL_SQLITE')),
        redis=Redis(host=env.str('HOST_REDIS'), port=env.int('PORT_REDIS')),
        bot_token=TgBot(token=env.str('BOT_TOKEN')),
        admin_data=AdminData(id=admin_ids)
    )
