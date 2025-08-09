import logging
import asyncio
import re

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from typing import TYPE_CHECKING, Any
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.database import requests
from src.constants.constant import PoolingData as poolData, DialogData as DData, HeroData as HData
from src.database.models import Users
from src.states.dialog_state import AdminSG
from src.utils.calculate.calculations import calculate_accrual, get_coins_per_lvl
from src.handlers.dialogs.hero.handler import get_rating, get_progress_bar

if TYPE_CHECKING:
    from src.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def get_info_hero(dialog: DialogManager,
                        i18n: TranslatorRunner,
                        telegram_id: int) -> dict[str, Any]:
    session: async_sessionmaker = dialog.middleware_data[poolData.session.value]
    classes = {
        'fighter': i18n.hero.fighter(),
        'knight': i18n.hero.knight(),
        'wizard': i18n.hero.wizard(),
        'ranger': i18n.hero.ranger(),
        'sorcerer': i18n.hero.sorcerer()
    }
    hero: Users = await requests.get_user_by_tg_id(
        async_session=session,
        telegram_id=telegram_id)
    hero_name = hero.hero_name
    h_class = hero.hero_class
    lvl = hero.xp // 100
    xp = hero.xp
    coins = hero.coins
    progress_bar = get_progress_bar(xp=xp)
    school_stars = ["⭐️" if i < hero.school_lvl else "⚫️" for i in range(3)]
    school_stars = ''.join(school_stars)
    lesson_reward = get_coins_per_lvl(h_lvl=lvl,
                                      s_lvl=hero.school_lvl)
    return {
        HData.hero_name.value: hero_name,
        HData.hero_class_ru.value: classes[h_class],
        HData.hero_class_en.value: h_class,
        HData.hero_lvl.value: lvl,
        HData.hero_xp.value: xp,
        HData.coins.value: coins,
        HData.progress_bar.value: progress_bar,
        HData.school_stars.value: school_stars,
        HData.lesson_reward.value: lesson_reward,
    }


async def btn_btn_list_heroes(callback: CallbackQuery,
                              button: Button,
                              dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    session: async_sessionmaker = middleware_data[poolData.session.value]

    users: list[Users] = await requests.get_all_users(async_session=session)
    heroes = [(hero.hero_name, str(hero.telegram_id)) for hero in users]
    widget_data[DData.heroes.value] = heroes

    try:
        await dialog_manager.switch_to(state=AdminSG.LIST_HEROES,
                                       show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=AdminSG.LIST_HEROES,
                                       show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')


async def btn_rating(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data

    rating: str = await get_rating(dialog=dialog_manager)
    widget_data[DData.rating.value] = rating

    try:
        await dialog_manager.switch_to(state=AdminSG.RATING,
                                       show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=AdminSG.RATING,
                                       show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[DData.rating.value] = []
    widget_data[DData.heroes.value] = []
    widget_data[DData.users_not_found.value] = False
    try:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')


async def btn_coins_accrual(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[DData.is_accrual_coins.value] = True


async def success_input_usernames(message: Message,
                                  widget: ManagedTextInput,
                                  dialog_manager: DialogManager,
                                  text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    session: async_sessionmaker = middleware_data[poolData.session.value]
    usernames = re.split(r',\s*', text)
    users: list[Users] = await requests.find_heroes(async_session=session,
                                                    hero_name=usernames)
    if users:
        heroes = [(hero.hero_name, str(hero.telegram_id)) for hero in users]
        widget_data[DData.heroes.value] = heroes
        widget_data[DData.users_not_found.value] = False
        if widget_data.get(DData.is_accrual_coins.value, False):
            widget_data[DData.is_accrual_coins.value] = False
            try:
                await dialog_manager.switch_to(state=AdminSG.INPUT_COINS_ACCRUAL,
                                               show_mode=ShowMode.DELETE_AND_SEND)
            except AttributeError as e:
                await dialog_manager.switch_to(state=AdminSG.INPUT_COINS_ACCRUAL,
                                               show_mode=ShowMode.SEND)
                logger.error(f'Error deleting message: {e}')
        else:
            try:
                await dialog_manager.switch_to(state=AdminSG.FOUND_HEROES,
                                               show_mode=ShowMode.DELETE_AND_SEND)
            except AttributeError as e:
                await dialog_manager.switch_to(state=AdminSG.FOUND_HEROES,
                                               show_mode=ShowMode.SEND)
                logger.error(f'Error deleting message: {e}')
    else:
        widget_data[DData.users_not_found.value] = True
        try:
            await dialog_manager.switch_to(state=AdminSG.INPUT_USERNAMES,
                                           show_mode=ShowMode.DELETE_AND_SEND)
        except AttributeError as e:
            await dialog_manager.switch_to(state=AdminSG.INPUT_USERNAMES,
                                           show_mode=ShowMode.SEND)
            logger.error(f'Error deleting message: {e}')


async def btn_accrual(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    session: async_sessionmaker = middleware_data[poolData.session.value]
    i18n: TranslatorRunner = middleware_data[poolData.i18n.value]
    heroes = widget_data[DData.heroes.value]
    heroes_names = [hero[0] for hero in heroes]
    users: list[Users] = await requests.find_heroes(async_session=session,
                                                    hero_name=heroes_names)
    async_requests = []
    async_send_message = []
    for user in users:
        user.xp, coins = calculate_accrual(xp=user.xp, s_lvl=user.school_lvl)
        user.coins += coins
        async_requests.append(requests.update_coins_and_xp_by_tg_id(
            async_session=session,
            telegram_id=user.telegram_id,
            xp=user.xp,
            coins=user.coins
        ))
        async_send_message.append(callback.message.bot.send_message(chat_id=user.telegram_id,
                                                                    text=i18n.admin.msg.lessons.accrual(coins=coins)))
    await asyncio.gather(*async_send_message)
    await asyncio.gather(*async_requests)
    widget_data[DData.users.value] = []
    try:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')


async def err_input_accrual_coins(message: Message,
                                  widget: ManagedTextInput,
                                  dialog_manager: DialogManager,
                                  error: ValueError):
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    await dialog_manager.switch_to(state=AdminSG.INPUT_COINS_ACCRUAL,
                                   show_mode=ShowMode.EDIT)


async def err_input_summ(message: Message,
                         widget: ManagedTextInput,
                         dialog_manager: DialogManager,
                         error: ValueError):
    widget_data = dialog_manager.current_context().widget_data
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    widget_data[DData.err_input.value] = True
    await dialog_manager.switch_to(state=AdminSG.INPUT_SUMM,
                                   show_mode=ShowMode.EDIT)


async def success_input_accrual_coins(message: Message,
                                      widget: ManagedTextInput,
                                      dialog_manager: DialogManager,
                                      text: str) -> None:
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    i18n: TranslatorRunner = middleware_data[poolData.i18n.value]
    summ = int(text)
    session: async_sessionmaker = middleware_data[poolData.session.value]
    heroes = widget_data[DData.heroes.value]
    heroes_names = [hero[0] for hero in heroes]
    users: list[Users] = await requests.find_heroes(async_session=session,
                                                    hero_name=heroes_names)
    async_requests = []
    async_send_message = []
    for user in users:
        user.coins += summ
        async_requests.append(requests.update_coins_by_tg_id(
            async_session=session,
            telegram_id=user.telegram_id,
            coins=user.coins
        ))
        async_send_message.append(message.bot.send_message(chat_id=user.telegram_id,
                                                           text=i18n.admin.msg.accrual(coins=summ)))
    await asyncio.gather(*async_send_message)
    await asyncio.gather(*async_requests)
    widget_data[DData.users.value] = []
    try:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')


async def success_input_summ(message: Message,
                             widget: ManagedTextInput,
                             dialog_manager: DialogManager,
                             text: str) -> None:
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    i18n: TranslatorRunner = middleware_data[poolData.i18n.value]
    summ = int(text)
    session: async_sessionmaker = middleware_data[poolData.session.value]
    heroes = widget_data[DData.heroes.value]
    heroes_names = [hero[0] for hero in heroes]
    users: list[Users] = await requests.find_heroes(async_session=session,
                                                    hero_name=heroes_names)
    async_requests = []
    async_send_message = []
    for user in users:
        user.coins -= summ
        async_requests.append(requests.update_coins_by_tg_id(
            async_session=session,
            telegram_id=user.telegram_id,
            coins=user.coins
        ))
        async_send_message.append(message.bot.send_message(chat_id=user.telegram_id,
                                                           text=i18n.admin.msg.debt(coins=summ)))
    await asyncio.gather(*async_send_message)
    await asyncio.gather(*async_requests)
    widget_data[DData.users.value] = []
    try:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')


async def btn_switch_to_hero(callback: CallbackQuery,
                             widget: Any,
                             dialog_manager: DialogManager,
                             selected_item: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    i18n: TranslatorRunner = middleware_data[poolData.i18n.value]
    hero = await get_info_hero(dialog=dialog_manager,
                               i18n=i18n,
                               telegram_id=int(selected_item))
    widget_data[DData.hero.value] = hero
    try:
        await dialog_manager.switch_to(state=AdminSG.INFO_HERO,
                                       show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=AdminSG.INFO_HERO,
                                       show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')


async def send_msg_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    middleware_data = dialog_manager.middleware_data
    session: async_sessionmaker = middleware_data[poolData.session.value]
    list_tg_id: list[int] = await requests.get_all_users_tg_id(async_session=session)

    if message.photo:
        photo = message.photo[-1]
        caption = message.caption if message.caption else ''
        file_id = photo.file_id
        try:
            async_send_message = [message.bot.send_photo(chat_id=tg_id,
                                                         photo=file_id,
                                                         caption=caption) for tg_id in list_tg_id]
            await asyncio.gather(*async_send_message)
        except AttributeError as e:
            logger.error(f'Error send message: {e}')

    elif message.text:
        text = message.text
        try:
            async_send_message = [message.bot.send_message(chat_id=tg_id,
                                                           text=text) for tg_id in list_tg_id]
            await asyncio.gather(*async_send_message)
        except AttributeError as e:
            logger.error(f'Error send message: {e}')

    try:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=AdminSG.MENU,
                                       show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')
