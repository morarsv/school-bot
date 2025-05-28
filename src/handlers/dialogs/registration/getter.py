import logging
from dataclasses import dataclass
from aiogram.types import User
from typing import TYPE_CHECKING
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from src.constants.constant import DialogData as DData

if TYPE_CHECKING:
    from src.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


@dataclass
class Hero:
    id: str
    h_class: str


def hero_id_getter(hero: Hero) -> str:
    return hero.id


async def preview_getter(dialog_manager: DialogManager,
                         event_from_user: User,
                         i18n: TranslatorRunner,
                         **_kwargs):
    menu_text = i18n.registration.preview()
    return {
        'menu_text': menu_text,
        'btn_next': i18n.btn.next()
    }


async def select_hero_getter(dialog_manager: DialogManager,
                             event_from_user: User,
                             i18n: TranslatorRunner,
                             **_kwargs):
    widget_data = dialog_manager.current_context().widget_data
    hero_key = [
        Hero(id=i18n.hero.id.knight(), h_class=i18n.hero.knight()),
        Hero(id=i18n.hero.id.ranger(), h_class=i18n.hero.ranger()),
        Hero(id=i18n.hero.id.sorcerer(), h_class=i18n.hero.sorcerer()),
        Hero(id=i18n.hero.id.wizard(), h_class=i18n.hero.wizard()),
        Hero(id=i18n.hero.id.fighter(), h_class=i18n.hero.fighter())
    ]
    description_hero = {
        i18n.hero.id.knight(): i18n.registration.hero.knight(),
        i18n.hero.id.ranger(): i18n.registration.hero.ranger(),
        i18n.hero.id.sorcerer(): i18n.registration.hero.sorcerer(),
        i18n.hero.id.wizard(): i18n.registration.hero.wizard(),
        i18n.hero.id.fighter(): i18n.registration.hero.fighter()
    }
    selected_hero_id = widget_data.get(DData.selected_hero.value, i18n.hero.id.knight())
    menu_text = description_hero.get(selected_hero_id)
    return {
        'heroes': hero_key,
        'menu_text': menu_text,
        'h_class': selected_hero_id,
        'btn_next': i18n.btn.next()
    }


async def input_getter(dialog_manager: DialogManager,
                       event_from_user: User,
                       i18n: TranslatorRunner,
                       **_kwargs):
    widget_data = dialog_manager.current_context().widget_data
    if widget_data.get(DData.err_input.value, False):
        widget_data[DData.err_input.value] = False
        input_hero_name = i18n.err.input.name()
    else:
        input_hero_name = i18n.registration.name()

    return {
        'input_hero_name': input_hero_name,
        'btn_back': i18n.btn.back()
    }
