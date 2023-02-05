from datetime import datetime, timedelta


def time_now(time_zone: float) -> datetime:
    """Узнать текущее время пользователя"""
    return datetime.utcnow() + timedelta(hours=time_zone)


def time_str() -> str:
    """Запись времени и даты"""
    s = str(datetime.today())
    return s[0:s.find('.')]


def good_time(time_zone: float):
    """Определить текущее приветствие по времени"""
    now = time_now(time_zone)
    if now.hour < 6: return 'Доброй ночи'
    if now.hour < 13: return 'Доброе утро'
    if now.hour < 19: return 'Добрый день'
    return 'Добрый вечер'
