import asyncio
import logging
import os
from typing import Optional

from asyncio.exceptions import CancelledError
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis
from fluentogram import TranslatorHub
from src.config_data.config import Config, load_config
from src.utils.i18n import create_translator_hub
from src.database.models import async_database_run, async_session
from src.session_models.session_model import SessionUser
from src.utils.cmd_menu import set_main_menu
from src.utils.func import bot_current_time, logging_custom_time
from src.middlewares.i18n import TranslatorRunnerMiddleware
# Роутеры и диалоги
from src.handlers.start import start_router
from src.handlers.dialogs.registration.dialog import registration_dialog
from src.handlers.dialogs.hero.dialog import hero_dialog
from src.handlers.dialogs.admin.dialog import admin_dialog


def setup_dp(storage: Optional[RedisStorage] = None):
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        start_router,
        registration_dialog,
        hero_dialog, admin_dialog
    )
    setup_dialogs(dp)
    return dp


async def main():
    config: Config = load_config()

    log_directory = 'src/logs/'
    time = bot_current_time()
    os.makedirs(log_directory, exist_ok=True)
    log_file_path = os.path.join(log_directory, f'err_bot_{time[:10]}.log')
    logging.basicConfig(level=logging.INFO,
                        format='[{asctime}] #{levelname:<8} {filename}'
                               ' - {lineno} - {name} - {message}',
                        style='{'
                        )
    file_handler = logging.FileHandler(filename=log_file_path, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(fmt='[{asctime}] #{levelname:<8} {filename}'
                                      ' - {lineno} - {name} - {message}',
                                  style='{')
    formatter.converter = logging_custom_time
    file_handler.setFormatter(formatter)

    logging.getLogger().addHandler(file_handler)

    translator_hub: TranslatorHub = create_translator_hub()
    redis = Redis(host=config.redis.host, port=config.redis.port)
    key_builder = DefaultKeyBuilder(with_destiny=True)
    storage = RedisStorage(redis=redis, key_builder=key_builder)

    bot = Bot(token=config.bot_token.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = setup_dp(storage=storage)
    dp.update.middleware(TranslatorRunnerMiddleware())

    online_users: dict[int, SessionUser] = {}
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await async_database_run()
    try:
        await dp.start_polling(bot,
                               _translator_hub=translator_hub,
                               _online_users=online_users,
                               session=async_session)
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt or CancelledError:
        logging.error("Shutting down...")
