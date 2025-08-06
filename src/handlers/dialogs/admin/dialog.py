import logging
from _operator import itemgetter

from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Column, Back, Button, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Format
from src.states.dialog_state import AdminSG
from src.constants.constant import DialogData as DData
from src.handlers.dialogs.admin.handler import (btn_back, btn_switch_to_hero, success_input_summ, err_input_summ,
                                                btn_accrual, success_input_usernames, btn_rating, btn_btn_list_heroes,
                                                btn_back_to_input_usernames, btn_coins_accrual,
                                                success_input_accrual_coins, err_input_accrual_coins,
                                                send_msg_handler)
from src.handlers.dialogs.admin.getter import (input_getter, heroes_getter, found_heroes_getter,
                                               preview_getter, info_hero_getter, rating_getter,
                                               input_accrual_getter)
from src.utils.func import check_format_summ
from src.middlewares.authorization_monitor import AuthorizationMiddleware

logger = logging.getLogger(__name__)

preview = Window(
    Format(text='{menu_text}'),
    Button(
        text=Format(text='{btn_list_heroes}'),
        id='btn_list_heroes',
        on_click=btn_btn_list_heroes
    ),
    SwitchTo(
        text=Format(text='{btn_settings_heroes}'),
        id='btn_settings_heroes',
        state=AdminSG.INPUT_USERNAMES
    ),
    SwitchTo(
        text=Format(text='{btn_coins_accrual}'),
        id='btn_coins_accrual',
        on_click=btn_coins_accrual,
        state=AdminSG.INPUT_USERNAMES
    ),
    SwitchTo(
        text=Format(text='{btn_write_everyone}'),
        id='btn_write_everyone',
        state=AdminSG.INPUT_MSG
    ),
    Button(
        text=Format(text='{btn_rating}'),
        id='btn_rating',
        on_click=btn_rating
    ),
    state=AdminSG.MENU,
    getter=preview_getter
)

input_usernames = Window(
    Format(text='{input_usernames}'),
    TextInput(
        id=DData.usernames.value,
        on_success=success_input_usernames,
    ),
    Button(
        text=Format(text='{btn_cancel}'),
        id='btn_cancel',
        on_click=btn_back
    ),
    state=AdminSG.INPUT_USERNAMES,
    getter=input_getter
)

found_usernames = Window(
    Format(text='{menu_text}'),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='usernames',
                item_id_getter=itemgetter(1),
                when='usernames'
            )
        ),
        width=1,
        height=5,
        id='scroll_list_usernames',
    ),
    Button(
        text=Format(text='{btn_accrual}'),
        id='btn_accrual',
        on_click=btn_accrual,
        when='usernames'
    ),
    SwitchTo(
        text=Format(text='{btn_write_off}'),
        id='btn_write_off',
        state=AdminSG.INPUT_SUMM,
        when='usernames'
    ),
    Button(
        text=Format(text='{btn_back}'),
        id='btn_back',
        on_click=btn_back_to_input_usernames
    ),
    state=AdminSG.FOUND_HEROES,
    getter=found_heroes_getter
)

input_summ = Window(
    Format(text='{input_summ}'),
    TextInput(
        id=DData.input_summ.value,
        type_factory=check_format_summ,
        on_success=success_input_summ,
        on_error=err_input_summ
    ),
    Back(
        text=Format(text='{btn_cancel}'),
        id='btn_cancel',
    ),
    state=AdminSG.INPUT_SUMM,
    getter=input_getter
)

list_heroes = Window(
    Format(text='{menu_text}'),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='heroes',
                when='heroes',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_hero
            )
        ),
        width=1,
        height=5,
        id='scroll_list_heroes',
    ),
    Button(
        text=Format(text='{btn_back}'),
        id='btn_back',
        on_click=btn_back
    ),
    state=AdminSG.LIST_HEROES,
    getter=heroes_getter
)

info_hero = Window(
    Format(text='{menu_text}'),
    Back(
        text=Format(text='{btn_back}'),
        id='btn_back',
    ),
    state=AdminSG.INFO_HERO,
    getter=info_hero_getter
)

rating = Window(
    Format(text='{menu_text}'),
    Button(
        text=Format(text='{btn_back}'),
        id='btn_back',
        on_click=btn_back
    ),
    state=AdminSG.RATING,
    getter=rating_getter
)

input_coins_accrual = Window(
    Format(text='{menu_text}'),
    TextInput(
        id=DData.input_accrual_coins.value,
        type_factory=check_format_summ,
        on_success=success_input_accrual_coins,
        on_error=err_input_accrual_coins
    ),
    SwitchTo(
        text=Format(text='{btn_cancel}'),
        id='btn_cancel_accrual_coins',
        state=AdminSG.MENU
    ),
    state=AdminSG.INPUT_COINS_ACCRUAL,
    getter=input_accrual_getter
)

input_msg = Window(
    Format(text='{input_msg}'),
    MessageInput(
        func=send_msg_handler,
        content_types=[ContentType.PHOTO, ContentType.TEXT],
    ),
    SwitchTo(
        text=Format(text='{btn_cancel}'),
        id='btn_cancel_input_msg',
        state=AdminSG.MENU
    ),
    state=AdminSG.INPUT_MSG,
    getter=input_getter
)

admin_dialog = Dialog(
    preview, input_usernames, found_usernames, input_summ, list_heroes, info_hero, rating, input_coins_accrual,
    input_msg
)

admin_dialog.message.middleware(AuthorizationMiddleware())
admin_dialog.callback_query.middleware(AuthorizationMiddleware())
