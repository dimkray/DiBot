# -*- coding: utf-8 -*-
# Сервис автотестирования бота
import Fixer
from Tests.Testing import Report

# Основной класс по автотестированию всех модулей/сервисов
Fixer.AddDef('AutoTest', 'Основной класс по автотестированию всех модулей/сервисов', sclass='AutoTest')

class AutoTest:

    # Автотестирование всех классов
    Fixer.AddDef('Alltests', 'Получение списка всех функций указанного класса (включая системные)',
                 {},
                 'Наполняется Tests. Возвращается состояние тестирования [string]')

    def Alltests():
        try:
            import Tests.Test_Testing
            import Tests.Test_Yandex
            # ....
            print('------- Alltests - Запущены тесты --------')
            print(Report.WriteAll())
            print('')
            print('------- Alltests - Найдены ошибки --------')
            print(Report.WriteFails())
            return 'Ok'
        except Exception as e:
            Fixer.errlog('Autotest.Alltests', str(e))
            return '#bug: ' + str(e)

    # Вывод результатов автотестирования определённого модуля/класса
    def Tests(module):
        s = 'Тесты сервиса/модуля ' + module + '\n'
        s += Report.WriteAll(service=module)
        return s

    # Вывод ошибок автотестирования определённого модуля/класса
    def Fails(module):
        s = 'Найденные ошибки сервиса/модуля ' + module + '\n'
        s += Report.WriteFails(service=module)
        return s