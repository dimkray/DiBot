# -*- coding: utf-8 -*-
# Сервис автотестирования бота
import Fixer
from Tests.Testing import Report

# Автотестирование
def Alltests():
    try:
        import Tests.Test_Testing
        import Tests.Test_Yandex
        # ....
        print('------- Запущены тесты --------')
        print(Report.WriteAll())
        print('')
        print('------- Найдены ошибки --------')
        print(Report.WriteFails())
    except Exception as e:
        Fixer.errlog('Autotest.Alltests', str(e))
        return '#bug: ' + str(e) 
