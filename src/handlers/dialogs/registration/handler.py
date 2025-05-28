import logging

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.types import CallbackQuery
from typing import TYPE_CHECKING
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import DatabaseError
from src.database import requests
from src.constants.constant import PoolingData as poolData, DialogData as DData
from src.database.models import Users
from src.session_models.session_model import SessionUser
from src.states.dialog_state import HeroSG, RegistrationSG

if TYPE_CHECKING:
    from src.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def error_input_name(message: Message,
                           widget: ManagedTextInput,
                           dialog_manager: DialogManager,
                           error: ValueError):
    widget_data = dialog_manager.current_context().widget_data
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    widget_data[DData.err_input.value] = True
    await dialog_manager.switch_to(state=RegistrationSG.INPUT_NAME,
                                   show_mode=ShowMode.EDIT)


async def btn_next_to_hero(callback: CallbackQuery,
                           button: Button,
                           dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data
    i18n: TranslatorRunner = middleware_data[poolData.i18n.value]
    widget_data[DData.selected_hero.value] = i18n.hero.id.knight()
    await dialog_manager.switch_to(state=RegistrationSG.HERO_IMG, show_mode=ShowMode.EDIT)


async def success_input_name(message: Message,
                             widget: ManagedTextInput,
                             dialog_manager: DialogManager,
                             text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data
    tg_id = int(message.from_user.id)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    session: async_sessionmaker = middleware_data[poolData.session.value]
    online_users = middleware_data[poolData.online_users.value]

    hero_name = text
    user: Users = await requests.get_user_by_hero_name(
        async_session=session,
        hero_name=hero_name
    )
    if user:
        widget_data[DData.err_input.value] = True
        await dialog_manager.switch_to(state=RegistrationSG.INPUT_NAME,
                                       show_mode=ShowMode.EDIT)
    else:
        hero_class = widget_data.get(DData.selected_hero.value)
        i18n: TranslatorRunner = middleware_data[poolData.i18n.value]
        new_hero: Users = Users()
        new_hero.telegram_id = tg_id
        new_hero.hero_name = hero_name
        new_hero.hero_class = hero_class

        online_users[tg_id] = SessionUser(
            hero_name=hero_name
        )
        middleware_data[poolData.online_users.value] = online_users

        try:
            await requests.add_user(
                async_session=session,
                user=new_hero
            )
        except DatabaseError as e:
            logger.error(f"Общая ошибка базы данных: {e}")
            await message.answer(text=i18n.err.add.hero())
            await dialog_manager.switch_to(state=RegistrationSG.INPUT_NAME,
                                           show_mode=ShowMode.EDIT)
        await dialog_manager.start(state=HeroSG.PREVIEW,
                                   mode=StartMode.RESET_STACK,
                                   show_mode=ShowMode.DELETE_AND_SEND)
