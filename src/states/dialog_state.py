from aiogram.fsm.state import State, StatesGroup


class AdminSG(StatesGroup):
    MENU = State()
    RATING = State()
    INPUT_USERNAMES = State()
    FOUND_HEROES = State()
    INPUT_SUMM = State()
    LIST_HEROES = State()
    INFO_HERO = State()
    INPUT_COINS_ACCRUAL = State()
    INPUT_MSG = State()


class RegistrationSG(StatesGroup):
    PREVIEW = State()
    HERO_IMG = State()
    INPUT_NAME = State()


class HeroSG(StatesGroup):
    PREVIEW = State()
    RATING = State()
    SCHOOL = State()
