import Fixer
from Profiler import Profiler
from Tests.Testing import Test, Report
from DB.SQLite import SQL

service = 'SQLite'
Fixer.DB = 'DB/Geo.db'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #
with Profiler() as p:
    # isWork
    desc = { 'table=': 'cities',
                 'cityName': 'name',
                 'cityNameLat': 'name_ascii',
                 'cityNameRus': 'name_ru',
                 'Location': ['lat', 'lon'],
                 'Population': 'population',
                 'Names': {'table=': 'names',
                    'ISO': 'iso',
                    'alternativeName': 'name',
                    'Parameters': 'params',
                    'where=': ['geo_id', 'id']},
                 'obj=': ['id']}
    
    test = SQL.Dict(desc, [511196])
    Test.Add(service+'.Dict','normal', test, None)

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
