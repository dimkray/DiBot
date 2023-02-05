# -*- coding: utf-8 -*-
# ПостПроцессор - финальный обработчик пользовательских запросов, реагирует на ошибки
import fixer
from datetime import datetime
from DB.SQLite import SQL

# постпроцессорный обработчик пользовательских запросов, где есть ошибки
def ErrorProcessor(text):
    try:
        bug, text = Fixer.strfind(text, ['#bug:', '#problem:', '#err:',' #critical:'])
        iNum = 0
        if bug != '':  # если обработан
            iNum = SQL.Count('bugs')+1  # число строк -> порядковый номер
        if bug == '#bug:':
            SQL.WriteRow('bugs', [iNum, 1, Fixer.Query, Fixer.Process, text, str(datetime.today())])
            text = """Извини! Но при работе возникла ошибка в сервисе {%s}: %s
Ошибка зарегестрирована под номером %i.
Попробуй по-другому сформулировать свой вопрос или запрос!""" % (Fixer.Process, text, iNum)
            print(text)
        elif bug == '#problem:':
            SQL.WriteRow('bugs', [iNum, 2, Fixer.Query, Fixer.Process, text, str(datetime.today())])
            text = """Ой! При обработке запроса возникла проблема в сервисе {%s}: %s
Проблема зарегестрирована под номером %i.
Попробуй по-другому сформулировать свой вопрос или запрос!""" % (Fixer.Process, text, iNum)
        elif bug == '#critical:':
            SQL.WriteRow('bugs', [iNum, 9, Fixer.Query, Fixer.Process, text, str(datetime.today())])
            text = """При обработке запроса возникла критическая ошибка в сервисе {%s}: %s
Ошибка зарегестрирована под номером %i.
Попробуй по-другому сформулировать свой вопрос или запрос!""" % (Fixer.Process, text, iNum)
        elif bug == '#err:':
            text = 'Некорректный запрос в сервисе {%s}: %s\n' % (Fixer.Process, text)
        return text
    except Exception as e: 
        Fixer.errlog('ErrorProcessor', str(e))
        return text
