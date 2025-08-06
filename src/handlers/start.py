import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode, ShowMode
from src.states.dialog_state import HeroSG, AdminSG
from src.middlewares.authorization_monitor import AuthorizationMiddleware
from src.config_data.config import load_config, Config

start_router = Router()
start_router.message.middleware(AuthorizationMiddleware())
start_router.callback_query.middleware(AuthorizationMiddleware())
config: Config = load_config()

logger = logging.getLogger(__name__)


@start_router.message(CommandStart())
async def command_start_process(message: Message,
                                dialog_manager: DialogManager,
                                bot: Bot):
    dialog_manager.show_mode = ShowMode.SEND
    try:
        await bot.delete_message(message_id=message.message_id,
                                 chat_id=message.chat.id)
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    tg_id = int(message.from_user.id)

    if tg_id in config.admin_data.id:

        try:
            await dialog_manager.start(state=AdminSG.MENU,
                                       mode=StartMode.RESET_STACK,
                                       show_mode=ShowMode.DELETE_AND_SEND)
        except AttributeError:
            await dialog_manager.start(state=AdminSG.MENU,
                                       mode=StartMode.RESET_STACK,
                                       show_mode=ShowMode.SEND)
    else:
        try:
            await dialog_manager.start(state=HeroSG.PREVIEW,
                                       mode=StartMode.RESET_STACK,
                                       show_mode=ShowMode.DELETE_AND_SEND)
        except AttributeError:
            await dialog_manager.start(state=HeroSG.PREVIEW,
                                       mode=StartMode.RESET_STACK,
                                       show_mode=ShowMode.SEND)
