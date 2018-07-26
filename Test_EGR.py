from Profiler import Profiler
from Tests.Testing import Test, Report
from DB.SQLite import SQL

service = 'EGR2'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #
with Profiler() as p:
    test = SQL.ReadRow('organization', 'ogrn', '1027700071530')[0] #['id']
    etalon = 4249295
    Test.Add(service, service+'.Organizations','тестирование скорости обращения', test, etalon)

with Profiler() as p:
    test = SQL.ReadRow('organization', 'id', '15680004')[2] #['ogrn']
    etalon = '1024600970591'
    Test.Add(service, service+'.Organizations','тестирование скорости обращения', test, etalon)

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
