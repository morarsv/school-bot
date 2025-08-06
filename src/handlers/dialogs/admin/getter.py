import logging

from aiogram.types import User
from typing import TYPE_CHECKING
from aiogram_dialog import DialogManager, ShowMode
from fluentogram import TranslatorRunner

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
    return {
        'menu_text': i18n.admin.panel.menu(),
        'btn_list_heroes': i18n.btn.list.heroes(),
        'btn_settings_heroes': i18n.btn.settings.heroes(),
        'btn_rating': i18n.btn.rating(),
        'btn_coins_accrual': i18n.btn.coins.accrual(),
        'btn_write_everyone': i18n.btn.write.everyone()
    }


async def input_getter(dialog_manager: DialogManager,
                       event_from_user: User,
                       i18n: TranslatorRunner,
                       **_kwargs):
    widget_data = dialog_manager.current_context().widget_data
    input_summ = i18n.err.input.summ() if widget_data.get(DData.err_input.value, False) \
        else i18n.admin.panel.input.summ()
    widget_data[DData.err_input.value] = False
    input_usernames = (i18n.admin.panel.input.usernames() + '\n\n' +
                       i18n.admin.panel.list.empty.usernames()) if widget_data.get(DData.users_not_found.value,
                                                                                   False) else (i18n.admin.panel.
                                                                                                input.usernames())
    return {
        'input_usernames': input_usernames,
        'input_summ': input_summ,
        'input_msg': i18n.admin.panel.input.msg(),
        'btn_cancel': i18n.btn.cancel()
    }


async def found_heroes_getter(dialog_manager: DialogManager,
                              event_from_user: User,
                              i18n: TranslatorRunner,
                              **_kwargs):
    widget_data = dialog_manager.current_context().widget_data
    usernames = widget_data[DData.heroes.value]
    menu_text = i18n.admin.panel.list.fill.usernames() if usernames else \
        i18n.admin.panel.list.empty.usernames()
    return {
        'menu_text': menu_text,
        'usernames': usernames,
        'btn_accrual': i18n.btn.accrual(),
        'btn_write_off': i18n.btn.write.off(),
        'btn_back': i18n.btn.back()
    }


async def heroes_getter(dialog_manager: DialogManager,
                        event_from_user: User,
                        i18n: TranslatorRunner,
                        **_kwargs):
    widget_data = dialog_manager.current_context().widget_data
    heroes = widget_data[DData.heroes.value]
    menu_text = i18n.admin.panel.list.heroes()
    return {
        'menu_text': menu_text,
        'heroes': heroes,
        'btn_back': i18n.btn.back()
    }


async def rating_getter(dialog_manager: DialogManager,
                        event_from_user: User,
                        i18n: TranslatorRunner,
                        **_kwargs):
    widget_data = dialog_manager.current_context().widget_data
    rating = widget_data[DData.rating.value]
    menu_text = i18n.my.hero.rating(
        heroes=rating
    )
    return {
        'menu_text': menu_text,
        'btn_back': i18n.btn.back()
    }


async def input_accrual_getter(dialog_manager: DialogManager,
                               event_from_user: User,
                               i18n: TranslatorRunner,
                               **_kwargs):
    widget_data = dialog_manager.current_context().widget_data
    heroes = widget_data[DData.heroes.value]
    users = ', '.join([hero[0] for hero in heroes])
    return {
        'menu_text': i18n.admin.panel.input.accrual.summ(users=users),
        'btn_cancel': i18n.btn.cancel()
    }


async def info_hero_getter(dialog_manager: DialogManager,
                           event_from_user: User,
                           i18n: TranslatorRunner,
                           **_kwargs):
    widget_data = dialog_manager.current_context().widget_data
    hero_data = widget_data[DData.hero.value]
    menu_text = i18n.admin.panel.info.hero(
        h_class=hero_data[HData.hero_class_ru.value],
        h_name=hero_data[HData.hero_name.value],
        lvl=hero_data[HData.hero_lvl.value],
        xp=hero_data[HData.hero_xp.value],
        progress=hero_data[HData.progress_bar.value],
        coins=hero_data[HData.coins.value],
        school_stars=hero_data[HData.school_stars.value],
        reward=hero_data[HData.lesson_reward.value]
    )
    return {
        'menu_text': menu_text,
        'btn_back': i18n.btn.back()
    }
