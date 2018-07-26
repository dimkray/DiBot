import DefProcess
import Fixer
from Profiler import Profiler
from Tests.Testing import Test, Report
from Services import Yandex
from Services.Yandex import Ya


service = 'Yandex'
print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #

sdef = '.FindLang'
with Profiler() as p:
    test = Yandex.FindLang('Русский')
    etalon = 'ru'
Test.Add(service + sdef, 'normal 1', test, etalon)

with Profiler() as p:
    test = Yandex.FindLang(' Английский ')
    etalon = 'en'
Test.Add(service + sdef, 'normal 2', test, etalon)

with Profiler() as p:
    test = Yandex.FindLang('Элийский')
    etalon = ''
Test.Add(service + sdef, 'unreal', test, etalon)


sdef = '.isStation'
with Profiler() as p:
    test = Yandex.isStation('Нижний Тагил')
    etalon = True
Test.Add(service + sdef, 'normal 1', test, etalon)

with Profiler() as p:
    test = Yandex.isStation(' МСК ')
    etalon = True
Test.Add(service + sdef, 'normal 2', test, etalon)

with Profiler() as p:
    test = Yandex.isStation('Элийский')
    etalon = False
Test.Add(service + sdef, 'unreal', test, etalon)


sdef = '.isStational'
with Profiler() as p:
    Fixer.region = ''
    test = Yandex.isStational('Нижний Тагил')
    etalon = 'Свердловская область'
Test.Add(service + sdef, 'normal 1', test, True)
Test.Add(service + sdef, 'normal 2', Fixer.region, etalon)

with Profiler() as p:
    Fixer.region = ''
    test = Yandex.isStational(' МСК ')
    etalon = 'Москва и Московская область'
Test.Add(service + sdef, 'normal 3', Fixer.region, etalon)

with Profiler() as p:
    Fixer.region = ''
    test = Yandex.isStational('Элийский')
    etalon = ''
Test.Add(service + sdef, 'unreal', Fixer.region, etalon)


sdef = '.eStation'
with Profiler() as p:
    test = Yandex.eStation('Звёздный')
    etalon = 'Г. Звёздный '
Test.Add(service + sdef, 'normal 1', test, etalon)

with Profiler() as p:
    test = Yandex.eStation('Нижние котлы')
    etalon = 'Нижние котлы '
Test.Add(service + sdef, 'normal 2', test, etalon)

with Profiler() as p:
    test = Yandex.eStation('Элийский')
    etalon = ''
Test.Add(service + sdef, 'unreal', test, etalon)


service = 'Ya'
# Добавляем все функции класса Ya
for idef in DefProcess.GetMemberList(Ya):
    Test.AddDef(service + '.' + idef)

sdef = '.Catalog'
with Profiler() as p:
    test = Ya.Catalog('taxcom')
    etalon = """Найдено совпадений: 1:
[1] http://taxcom.ru/ - «Такском» — системы электронного документооборота (ТИЦ: 1200)
Раздел: Business -> Corporate_Services -> Automation -> Office_Automation
Регион:  -> Russia"""
Test.Add(service + sdef, 'normal', test, etalon)

with Profiler() as p:
    test = Ya.Catalog('xxxx')
    etalon = """Сайт или часть сайта "xxxx" не найдена :(
Следует уточнить строку поиска или убедиться, что сайт существует."""
Test.Add(service + sdef, 'unreal', test, etalon)

with Profiler() as p:
    test = Ya.Catalog(0)
    etalon = "#bug: 'int' object has no attribute 'strip'"
Test.Add(service + sdef, 'crush', test, etalon)


print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())

print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
