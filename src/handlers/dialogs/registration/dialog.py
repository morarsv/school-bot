import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Radio, Column, Next, Back, Button
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from src.states.dialog_state import RegistrationSG
from src.constants.constant import DialogData as DData
from src.utils.func import check_format_hero_name
from src.handlers.dialogs.registration.handler import success_input_name, error_input_name, btn_next_to_hero
from src.handlers.dialogs.registration.getter import (preview_getter, hero_id_getter,
                                                      select_hero_getter, input_getter)

logger = logging.getLogger(__name__)


preview = Window(
    Format(text='{menu_text}'),
    Button(
        text=Format(text='{btn_next}'),
        id='__next__1',
        on_click=btn_next_to_hero
    ),
    state=RegistrationSG.PREVIEW,
    getter=preview_getter
)


select_hero = Window(
    Format(text='{menu_text}'),
    StaticMedia(path=Format(
        text='src/data/img/classes/{h_class}_lvl0.jpg'
    )),
    Column(
        Radio(
            checked_text=Format(text="🔘 {item.h_class}"),
            unchecked_text=Format(text="⚪️ {item.h_class}"),
            id=DData.selected_hero.value,
            items="heroes",
            item_id_getter=hero_id_getter,
        ),
    ),
    Next(
        text=Format(text='{btn_next}'),
    ),
    state=RegistrationSG.HERO_IMG,
    getter=select_hero_getter
)


input_hero_name = Window(
    Format(text='{input_hero_name}'),
    TextInput(
        id=DData.input_hero_name.value,
        on_success=success_input_name,
        on_error=error_input_name,
        type_factory=check_format_hero_name
    ),
    Back(
        Format(text='{btn_back}')
    ),
    state=RegistrationSG.INPUT_NAME,
    getter=input_getter
)


registration_dialog = Dialog(
    preview, select_hero, input_hero_name
)
