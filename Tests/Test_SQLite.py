import fixer
from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from DB.SQLite import SQL

Testing.testService = 'SQL'
Fixer.DB = 'Tests/test.db'

print('------- Запущены тесты сервиса %s --------' % Testing.testService)

# здесь тестовая обработка #
with Profiler() as p:
    # Read
    Testing.testDef = 'ReadAll'
    test = SQL.ReadAll('test1')
    etalon = [(0, 'Тест 1'), (1, 'Тест 2')]
    Test.Add('normal', test, etalon)
    
    # Dict
    Testing.testDef = 'Dict'
    desc = { 'table=': 'test1',
             'Text': 'text',
             'Region': {'table=': 'region',
                        'typeRegion': 'type',
                        'nameRegion': 'name',
                        'where=': ['id', 'id']},
             'col+': [{'table=': 'test2',
                       'Text2': 'text',
                       'where=': ['id', 'id']},
                      {'table=': 'region2',
                       'typeRegion2': 'type',
                       'nameRegion2': 'name',
                       'where=': ['id', 'id']}]}

    test = SQL.Dict(desc, {'id': 1, 'text': 'Тест 2'})
    etalon = [{'Text': 'Тест 2',
               'Region': [{'typeRegion': 'ГОРОД', 'nameRegion': 'МОСКВА'}],
               'Text2': 'Тест 2', 'typeRegion2': 'ГОРОД', 'nameRegion2': 'МОСКВА'}]
    Test.Add('normal', test, etalon)

    test = SQL.Dict({'table=': 'test1', 'key': 'id'}, {'text': 'Тест 1'})
    Test.Add('normal simple', test, [{'key': 0}])

print('')
print('------- Отчёт тестов сервиса %s --------' % Testing.testService)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % Testing.testService)
print(Report.WriteFails())
