from enum import Enum


class PoolingData(Enum):
    event_from_user = 'event_from_user'
    online_users = '_online_users'
    i18n = 'i18n'
    session = 'session'


class StartData(Enum):
    pass


class HeroData(Enum):
    hero_name = 'hero_name'
    hero_class_ru = 'hero_class_ru'
    hero_class_en = 'hero_class_en'
    hero_lvl = 'hero_lvl'
    hero_xp = 'hero_xp'
    coins = 'coins'
    progress_bar = 'progress_bar'
    school_stars = 'school_stars'
    school_lvl = 'school_lvl'
    lesson_reward = 'lesson_reward'
    daily_reward = 'reward'
    cost_school = 'cost_school'
    upgrade_school = 'upgrade_school'


class DialogData(Enum):
    err_input = 'err_input'
    telegram_id = 'telegram_id'
    input_hero_name = 'input_hero_name'
    input_summ = 'input_summ'
    input_accrual_coins = 'input_accrual_coins'
    list_heroes = 'list_heroes'
    hero = 'hero'
    heroes = 'heroes'
    selected_hero = 'selected_hero'
    xp = 'xp'
    coins = 'coins'
    none = 'none'
    upgrade_school_costs = 'upgrade_school_costs'
    usernames = 'usernames'
    users = 'users'
    users_not_found = 'users_not_found'
    rating = 'rating'
    is_accrual_coins = 'is_accrual_coins'
