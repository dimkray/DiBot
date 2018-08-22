from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from DB.Worker import Worker
import Fixer

Testing.testService = 'Worker'

print('------- Запущены тесты сервиса %s --------' % Testing.testService)

Fixer.DB = 'Tests/Test.db'

# здесь тестовая обработка #
with Profiler() as p:
    # AddTable
    Testing.testDef = 'AddTable'
    data = [[0, 'Тест 1'], [1, 'Тест 2']]
    test = Worker.AddTable('test1', {'id': 'int nn', 'text': 'str'}, data)
    Test.Add('normal', test, 'OK')

    # UpdateTable
    Testing.testDef = 'UpdateTable'
    test = Worker.UpdateTable('test2', {'id': 'int nn u', 'text': 'text'}, data)
    Test.Add('normal', test, 'OK')

    # UpdateTableCSV
    Testing.testDef = 'UpdateTableCSV'
    test = Worker.UpdateTableCSV('Tests/region.csv', 'region', {'id': 'int nn u', 'type': 'text', 'name': 'text'})
    Test.Add('normal', test, 'OK')

    test = Worker.UpdateTableCSV('Tests/region.csv', 'region2', {'id': 'int nn u', 'name': 'text', 'type': 'text'})
    Test.Add('normal', test, 'OK')

    test = Worker.UpdateTableCSV('Tests/area.csv', 'area', {'id': 'int nn u', 'area': 'text', 'type_name': 'text'},
                                 {'id': 'id', 'type_name': 'type', 'area': 'name'})
    Test.Add('normal', test, 'OK')

    # ReadBlockCSV
    Testing.testDef = 'ReadBlockCSV'
    test = Worker.ReadBlockCSV('Tests/region.csv')
    Test.Add('normal', test, 239)

    #UpdateBlockCSV
    Testing.testDef = 'UpdateBlockCSV'
    for row in Worker.mDataCSV:
        row[1] = row[1].upper()
        row[2] = row[2].upper()
        row.append(row[2].lower())
    Worker.mTableCSV.append('name_lower')
    test = Worker.UpdateBlockCSV('region3', {'id': 'int nn u', 'type': 'text', 'name': 'text',
                                             'name_lower': 'text'})
    Test.Add('normal', test, 'OK')

print('------- Отчёт тестов сервиса %s --------' % Testing.testService)
print(Report.WriteAll(service=Testing.testService))
print('')
print('------- Найдены ошибки сервиса %s  --------' % Testing.testService)
print(Report.WriteFails(service=Testing.testService))
