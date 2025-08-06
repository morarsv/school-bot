import pytz
import re
from datetime import datetime, timedelta, timezone


def bot_current_time() -> str:
    current_time_zone = datetime.now(pytz.utc)
    utc_plus_7 = current_time_zone.astimezone(pytz.timezone("Asia/Novosibirsk"))
    time = utc_plus_7.strftime("%Y-%m-%d %H:%M:%S")
    return time


def logging_custom_time(*args):
    utc_dt = datetime.now(timezone.utc)
    converted = utc_dt.astimezone(timezone(timedelta(hours=7)))
    return converted.timetuple()


def check_format_hero_name(text: str) -> str:
    pattern = r'^[а-яА-Я0-9_]{4,20}$'
    if re.match(pattern, text):
        return text
    raise ValueError


def check_format_summ(text: str) -> str:
    pattern = r'^[0-9]+$'
    if re.match(pattern, text):
        return text
    raise ValueError
