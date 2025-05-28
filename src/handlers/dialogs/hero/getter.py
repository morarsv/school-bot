import logging

from aiogram.types import User
from typing import TYPE_CHECKING
from aiogram_dialog import DialogManager, ShowMode
from fluentogram import TranslatorRunner
from src.handlers.dialogs.hero.handler import get_info_hero, get_info_school, get_rating
from src.constants.constant import HeroData as HData, DialogData as DData

if TYPE_CHECKING:
    from src.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         event_from_user: User,
                         i18n: TranslatorRunner,
                         **_kwargs):
    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')
    widget_data = dialog_manager.current_context().widget_data
    telegram_id = int(event_from_user.id)
    widget_data[DData.telegram_id.value] = telegram_id
    hero_data = await get_info_hero(
        dialog=dialog_manager,
        i18n=i18n,
        telegram_id=telegram_id
    )
    menu_text = i18n.my.hero.preview(
        h_name=hero_data[HData.hero_name.value],
        h_class=hero_data[HData.hero_class_ru.value],
        lvl=hero_data[HData.hero_lvl.value],
        xp=hero_data[HData.hero_xp.value],
        progress=hero_data[HData.progress_bar.value],
        coins=hero_data[HData.coins.value],
        school_stars=hero_data[HData.school_stars.value],
        reward=hero_data[HData.lesson_reward.value]
    )

    return {
        'menu_text': menu_text,
        'h_class': hero_data[HData.hero_class_en.value],
        'h_lvl': hero_data[HData.hero_lvl.value],
        'btn_daily_reward': i18n.btn.daily.reward(),
        'btn_school': i18n.btn.school(),
        'btn_rating': i18n.btn.rating(),
        'reward': hero_data[HData.daily_reward.value]
    }


async def school_getter(dialog_manager: DialogManager,
                        event_from_user: User,
                        i18n: TranslatorRunner,
                        **_kwargs):
    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')
    widget_data = dialog_manager.current_context().widget_data
    telegram_id = widget_data[DData.telegram_id.value]
    school_data = await get_info_school(
        dialog=dialog_manager,
        i18n=i18n,
        telegram_id=telegram_id
    )
    menu_text = i18n.my.hero.school(
        school_stars=school_data[HData.school_stars.value],
        cost=school_data[HData.cost_school.value]
    )
    return {
        'menu_text': menu_text,
        'lvl': school_data[HData.school_lvl.value],
        'upgrade': school_data[HData.upgrade_school.value],
        'btn_upgrade_school': i18n.btn.upgrade.school(),
        'btn_back': i18n.btn.back()
    }


async def rating_getter(dialog_manager: DialogManager,
                        event_from_user: User,
                        i18n: TranslatorRunner,
                        **_kwargs):
    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')
    rating = await get_rating(dialog=dialog_manager)
    menu_text = i18n.my.hero.rating(
        heroes=rating
    )
    return {
        'menu_text': menu_text,
        'btn_back': i18n.btn.back()
    }
