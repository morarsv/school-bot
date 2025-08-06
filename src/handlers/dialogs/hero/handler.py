import logging
import random

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery
from typing import TYPE_CHECKING, Any
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import DatabaseError
from src.database import requests
from src.constants.constant import PoolingData as poolData, DialogData as DData, HeroData as HData
from src.database.models import Users
from src.states.dialog_state import HeroSG
from src.utils.func import bot_current_time
from src.utils.calculate.calculations import get_coins_per_lvl, get_cost_upgrade_school

from datetime import datetime

if TYPE_CHECKING:
    from src.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


def get_progress_bar(xp: int) -> str:
    current_xp = xp % 100
    filled = current_xp * 10 // 100
    return "[" + "█" * filled + "░" * (10 - filled) + f"] {current_xp}/100"


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
    school_stars = ["⭐️" if i < hero.school_lvl else "⚫️" for i in range(3)]
    school_stars = ''.join(school_stars)
    progress_bar = get_progress_bar(xp=xp)

    last_daily_reward_date = str(hero.last_daily_reward_date) if hero.last_daily_reward_date else '2025-01-01'

    last_reward = datetime.strptime(last_daily_reward_date[:10], '%Y-%m-%d')
    current_time = datetime.strptime(bot_current_time()[:10], '%Y-%m-%d')
    lesson_reward = get_coins_per_lvl(h_lvl=lvl,
                                      s_lvl=hero.school_lvl)
    reward = None if current_time <= last_reward else 1
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
        HData.daily_reward.value: reward
    }


async def get_info_school(dialog: DialogManager,
                          i18n: TranslatorRunner,
                          telegram_id: int) -> dict[str, Any]:
    session: async_sessionmaker = dialog.middleware_data[poolData.session.value]
    hero: Users = await requests.get_user_by_tg_id(
        async_session=session,
        telegram_id=telegram_id)
    school_stars = ["⭐️" if i < hero.school_lvl else "⚫️" for i in range(3)]
    school_stars = ''.join(school_stars)
    cost = get_cost_upgrade_school(s_lvl=hero.school_lvl)
    upgrade = None if hero.coins < cost else 1
    upgrade = None if hero.school_lvl >= 3 else upgrade
    coins = hero.coins
    dialog.current_context().widget_data[DData.upgrade_school_costs.value] = cost
    if cost == 99999:
        cost = i18n.max.lvl.school()
    return {
        HData.school_stars.value: school_stars,
        HData.coins.value: coins,
        HData.school_lvl.value: hero.school_lvl,
        HData.cost_school.value: cost,
        HData.upgrade_school.value: upgrade
    }


async def get_rating(dialog: DialogManager) -> str:
    middleware_data = dialog.middleware_data
    session: async_sessionmaker = middleware_data[poolData.session.value]
    i18n: TranslatorRunner = middleware_data[poolData.i18n.value]
    classes = {
        'fighter': i18n.hero.fighter(),
        'knight': i18n.hero.knight(),
        'wizard': i18n.hero.wizard(),
        'ranger': i18n.hero.ranger(),
        'sorcerer': i18n.hero.sorcerer()
    }
    top_heroes: list[Users] = await requests.get_rating_names_30(async_session=session)
    names = [(f'<b>{hero.hero_name}</b>—{classes[hero.hero_class]}—{i18n.lvl.hero(lvl=(hero.xp // 100))}—'
              f'{i18n.coins.lessons(coins=get_coins_per_lvl(h_lvl=(hero.xp // 100), s_lvl=hero.school_lvl))}') for \
             hero in top_heroes]
    return '\n'.join([f'{i + 1}.  {name}' for i, name in enumerate(names)])


async def btn_daily_reward(callback: CallbackQuery,
                           button: Button,
                           dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    session: async_sessionmaker = middleware_data[poolData.session.value]
    telegram_id = widget_data[DData.telegram_id.value]
    i18n: TranslatorRunner = middleware_data[poolData.i18n.value]
    hero: Users = await requests.get_user_by_tg_id(
        async_session=session,
        telegram_id=telegram_id
    )

    reward_type = random.choice([DData.xp.value, DData.coins.value, DData.none.value])

    if reward_type == DData.xp.value:
        amount = random.randint(1, 7)
        old_lvl = hero.xp // 100
        xp = amount + hero.xp
        await callback.answer(text=i18n.ur.reward.xp(xp=amount), show_alert=True)
        current_lvl = xp // 100

        if old_lvl < current_lvl < 10:
            await callback.answer(text=i18n.lvl.up(lvl=current_lvl))

        xp = 1099 if xp >= 1099 else xp
        try:
            await requests.update_xp_by_tg_id(
                async_session=session,
                telegram_id=telegram_id,
                xp=xp
            )
        except DatabaseError as e:
            logger.error(f"Общая ошибка базы данных: {e}")

    elif reward_type == DData.coins.value:
        amount = random.randint(1, 7)
        hero.coins += amount
        await callback.answer(text=i18n.ur.reward.coins(coins=amount), show_alert=True)
        try:
            await requests.update_coins_by_tg_id(
                async_session=session,
                telegram_id=telegram_id,
                coins=hero.coins
            )
        except DatabaseError as e:
            logger.error(f"Общая ошибка базы данных: {e}")
    else:
        await callback.answer(text=i18n.ur.reward.none(), show_alert=True)

    try:
        current_time = datetime.strptime(bot_current_time()[:10], '%Y-%m-%d')
        await requests.update_last_daily_reward_date_by_tg_id(
            async_session=session,
            telegram_id=telegram_id,
            date=current_time
        )
    except DatabaseError as e:
        logger.error(f"Общая ошибка базы данных: {e}")

    try:
        await dialog_manager.switch_to(state=HeroSG.PREVIEW, show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=HeroSG.PREVIEW, show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')


async def btn_upgrade_school(callback: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    session: async_sessionmaker = middleware_data[poolData.session.value]
    telegram_id = widget_data[DData.telegram_id.value]
    hero: Users = await requests.get_user_by_tg_id(
        async_session=session,
        telegram_id=telegram_id
    )
    upgrade_school_costs = widget_data[DData.upgrade_school_costs.value]
    coins = hero.coins - upgrade_school_costs
    school_lvl = hero.school_lvl + 1
    try:
        await requests.update_school_lvl_and_coins_by_tg_id(
            async_session=session,
            telegram_id=telegram_id,
            school_lvl=school_lvl,
            coins=coins
        )
    except DatabaseError as e:
        logger.error(f"Общая ошибка базы данных: {e}")

    try:
        await dialog_manager.switch_to(state=HeroSG.SCHOOL, show_mode=ShowMode.DELETE_AND_SEND)
    except AttributeError as e:
        await dialog_manager.switch_to(state=HeroSG.SCHOOL, show_mode=ShowMode.SEND)
        logger.error(f'Error deleting message: {e}')
