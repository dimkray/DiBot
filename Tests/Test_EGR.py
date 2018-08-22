from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from DB.SQLite import SQL

Testing.testService = 'EGR2'

print('------- Запущены тесты сервиса %s --------' % Testing.testService)

# здесь тестовая обработка #
with Profiler() as p:
    Testing.testDef = 'Organizations'
    test = SQL.ReadRow('organization', 'ogrn', '1027700071530')[0]  #['id']
    etalon = 4249295
    Test.Add('тестирование скорости обращения', test, etalon)

with Profiler() as p:
    test = SQL.ReadRow('organization', 'id', '15680004')[2]  #['ogrn']
    etalon = '1024600970591'
    Test.Add('тестирование скорости обращения', test, etalon)

print('')
print('------- Отчёт тестов сервиса %s --------' % Testing.testService)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % Testing.testService)
print(Report.WriteFails())
