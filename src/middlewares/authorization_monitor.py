import logging

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from aiogram_dialog import DialogManager, StartMode, ShowMode
from src.database import requests
from src.database.models import Users
from src.constants.constant import PoolingData as poolData
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.session_models.session_model import SessionUser
from src.states.dialog_state import RegistrationSG
from src.config_data.config import load_config, Config


logger = logging.getLogger(__name__)
config: Config = load_config()


class AuthorizationMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_data: User = data.get(poolData.event_from_user.value)
        bot = event.bot
        tg_id = int(user_data.id)
        online: dict[int, SessionUser] = data.get(poolData.online_users.value)
        session: async_sessionmaker = data.get(poolData.session.value)
        if tg_id in config.admin_data.id:
            return await handler(event, data)
        if tg_id in online:
            return await handler(event, data)
        else:
            user: Users = await requests.get_user_by_tg_id(async_session=session,
                                                           telegram_id=tg_id)
            if user is not None:
                online[tg_id] = SessionUser(
                    hero_name=user.hero_name
                )
                data[poolData.online_users.value] = online
                return await handler(event, data)
            else:
                try:
                    await bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)
                except AttributeError as e:
                    logger.error(f'Error deleting message: {e}')

                dialog: DialogManager = data['dialog_manager']
                try:
                    await dialog.start(state=RegistrationSG.PREVIEW,
                                       mode=StartMode.RESET_STACK,
                                       show_mode=ShowMode.DELETE_AND_SEND)
                except AttributeError as e:
                    await dialog.start(state=RegistrationSG.PREVIEW,
                                       mode=StartMode.RESET_STACK,
                                       show_mode=ShowMode.SEND)

                return
