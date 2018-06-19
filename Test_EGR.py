from Profiler import Profiler
from Tests.Testing import Test, Report
from DB.SQLite import SQL

service = 'EGR'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #
with Profiler() as p:
    test = SQL.ReadRow('organizations', 'orgn', '1027700071530')['id']
    etalon = '4249295'
    Test.Add(service+'.Organizations','тестирование скорости обращения', test, etalon)

with Profiler() as p:
    test = SQL.ReadRow('organizations', 'id', '15680004')['ogrn']
    etalon = '1024600970591'
    Test.Add(service+'.Organizations','тестирование скорости обращения', test, etalon)

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
