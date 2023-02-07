import fixer
from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from services import Yandex
from services.Yandex import Ya
from services.DefProcess import Runner

Testing.testService = 'Yandex'
print('------- Запущены тесты сервиса %s --------' % Testing.testService)

# здесь тестовая обработка #

sdef = '.FindLang'
with Profiler() as p:
    Testing.testDef = 'FindLang'
    test = Yandex.FindLang('Русский')
    etalon = 'ru'
Test.Add('normal 1', test, etalon)

with Profiler() as p:
    test = Yandex.FindLang(' Английский ')
    etalon = 'en'
Test.Add('normal 2', test, etalon)

with Profiler() as p:
    test = Yandex.FindLang('Элийский')
    etalon = ''
Test.Add('unreal', test, etalon)


Testing.testDef = 'isStation'
with Profiler() as p:
    test = Yandex.isStation('Нижний Тагил')
    etalon = True
Test.Add('normal 1', test, etalon)

with Profiler() as p:
    test = Yandex.isStation(' МСК ')
    etalon = True
Test.Add('normal 2', test, etalon)

with Profiler() as p:
    test = Yandex.isStation('Элийский')
    etalon = False
Test.Add('unreal', test, etalon)


Testing.testDef = 'isStational'
with Profiler() as p:
    Fixer.region = ''
    test = Yandex.isStational('Нижний Тагил')
    etalon = 'Свердловская область'
Test.Add('normal 1', test, True)
Test.Add('normal 2', Fixer.region, etalon)

with Profiler() as p:
    Fixer.region = ''
    test = Yandex.isStational(' МСК ')
    etalon = 'Москва и Московская область'
Test.Add('normal 3', Fixer.region, etalon)

with Profiler() as p:
    Fixer.region = ''
    test = Yandex.isStational('Элийский')
    etalon = ''
Test.Add('unreal', Fixer.region, etalon)


Testing.testDef = 'eStation'
with Profiler() as p:
    test = Yandex.eStation('Звёздный')
    etalon = 'Г. Звёздный '
Test.Add('normal 1', test, etalon)

with Profiler() as p:
    test = Yandex.eStation('Нижние котлы')
    etalon = 'Нижние котлы '
Test.Add('normal 2', test, etalon)

with Profiler() as p:
    test = Yandex.eStation('Элийский')
    etalon = ''
Test.Add('unreal', test, etalon)


Testing.testService = 'Ya'
# Добавляем все функции класса Ya
for idef in Runner.GetMemberList(Ya):
    Test.AddDef(idef)


Testing.testDef = 'Catalog'
with Profiler() as p:
    test = Ya.Catalog('taxcom')
    etalon = """Найдено совпадений: 1:
[1] http://taxcom.ru/ - «Такском» — системы электронного документооборота (ТИЦ: 1200)
Раздел: Business -> Corporate_Services -> Automation -> Office_Automation
Регион:  -> Russia"""
Test.Add('normal', test, etalon)

with Profiler() as p:
    test = Ya.Catalog('xxxx')
    etalon = """Сайт или часть сайта "xxxx" не найдена :(
Следует уточнить строку поиска или убедиться, что сайт существует."""
Test.Add('unreal', test, etalon)

with Profiler() as p:
    test = Ya.Catalog(0)
    etalon = "#bug: 'int' object has no attribute 'strip'"
Test.Add('crush', test, etalon)


print('')
print('------- Отчёт тестов сервиса Yandex --------')
print(Report.WriteAll(service='Yandex'))
print(Report.WriteAll(service='Ya'))

print('')
print('------- Найдены ошибки сервиса Yandex  --------')
print(Report.WriteFails(service='Yandex'))
print(Report.WriteFails(service='Ya'))
