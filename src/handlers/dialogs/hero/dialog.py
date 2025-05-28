import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Back, Button
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from src.states.dialog_state import HeroSG
from src.handlers.dialogs.hero.handler import btn_daily_reward, btn_upgrade_school
from src.handlers.dialogs.hero.getter import preview_getter, rating_getter, school_getter
from src.middlewares.authorization_monitor import AuthorizationMiddleware
from src.middlewares.message_monitor import MessageMonitorMiddleware

logger = logging.getLogger(__name__)


preview = Window(
    Format(text='{menu_text}'),
    StaticMedia(path=Format(
        text='src/data/img/classes/{h_class}_lvl{h_lvl}.jpg'
    )),
    Column(
        Button(
            text=Format(text='{btn_daily_reward}'),
            on_click=btn_daily_reward,
            id='b_daily_reward',
            when='reward'
        ),
        SwitchTo(
            text=Format(text='{btn_school}'),
            id='b_school',
            state=HeroSG.SCHOOL
        ),
        SwitchTo(
            text=Format(text='{btn_rating}'),
            id='b_rating',
            state=HeroSG.RATING
        )

    ),
    state=HeroSG.PREVIEW,
    getter=preview_getter
)

school = Window(
    Format(text='{menu_text}'),
    StaticMedia(path=Format(
        text='src/data/img/school/school_lvl{lvl}.jpg'
    )),
    Button(
        text=Format(text='{btn_upgrade_school}'),
        on_click=btn_upgrade_school,
        id='b_upgrade_school',
        when='upgrade'
    ),
    Back(
        text=Format(text='{btn_back}')
    ),
    state=HeroSG.SCHOOL,
    getter=school_getter
)

rating = Window(
    Format(text='{menu_text}'),
    SwitchTo(
        text=Format(text='{btn_back}'),
        id='b_back',
        state=HeroSG.PREVIEW
    ),
    state=HeroSG.RATING,
    getter=rating_getter
)

hero_dialog = Dialog(
    preview, school, rating
)

hero_dialog.callback_query.middleware(AuthorizationMiddleware())
hero_dialog.message.middleware(AuthorizationMiddleware())
hero_dialog.message.middleware(MessageMonitorMiddleware())
