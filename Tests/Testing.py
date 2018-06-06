# -*- coding: utf-8 -*-
# Процессы тестирования сервисов/функций и самого бота
import Fixer

# Сравнение с эталонным
def Equal(test, etalon):
    if test == etalon: return True
    else: return False

# Сравнение с эталонным (для строк)
def strEqual(stest, setalon):
    from Service.StrMorth import Word
    if stest == setalon: return 1
    else:
        if stest.strip() == setalon.strip(): return 0.95
        if stest.strip().upper() == setalon.strip().upper(): return 0.9
        # if Word.Words ....
    return 0
