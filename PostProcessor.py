# -*- coding: utf-8 -*-
# ПостПроцессор - финальный обработчик пользовательских запросов, реагирует на ошибки
from fixer import DB
from config import QUERY, PROCESS
from system.string import str_find
from system.logging import err_log
from datetime import datetime

BUGS = {'#bug:': ['ошибка', 1],
        '#problem:': ['проблема', 2],
        '#critical:': ['критическая ошибка', 9],
        '#err:': ['некорректность', None]}


def error_processor(text):
    """Постпроцессорный обработчик пользовательских запросов, где есть ошибки"""
    try:
        bug, text = str_find(text, ['#bug:', '#problem:', '#err:', ' #critical:'])
        number = 0
        if bug != '':  # если обработан
            number = DB.count('bugs') + 1  # число строк -> порядковый номер
        if BUGS[bug][1]:
            DB.write_row('bugs', [number, 1, QUERY, PROCESS, text, str(datetime.today())])
        text = "Извини! Но при работе возникла %s в сервисе {%s}: %s\nОшибка зарегестрирована под номером %i.\n" \
               "Попробуй по-другому сформулировать свой вопрос или запрос!" % \
               (BUGS[bug][0], PROCESS, text, number)
        return text
    except Exception as e: 
        err_log('ErrorProcessor', str(e))
        return text
