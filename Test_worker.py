from Profiler import Profiler
from Tests.Testing import Test, Report
from DB.Worker import Worker
import Fixer

service = 'DB.Worker'

print('------- Запущены тесты сервиса %s --------' % service)

Fixer.DB = 'Tests/Test.db'

# здесь тестовая обработка #
with Profiler() as p:
    # AddTable
    data = [[0,'Тест 1'],[1,'Тест 2']]
    test = Worker.AddTable('test1', {'id':'int nn', 'text':'str'}, data)
    Test.Add(service+'.AddTable', 'normal', test, 'OK')

    # UpdateTable
    test = Worker.UpdateTable('test2', {'id':'int nn u', 'text':'text'}, data)
    Test.Add(service+'.UpdateTable', 'normal', test, 'OK')

    # UpdateTableCSV
    test = Worker.UpdateTableCSV('Tests/region.csv', 'region', {'id':'int nn u', 'type':'text', 'name':'text'})
    Test.Add(service+'.UpdateTableCSV', 'normal', test, 'OK')

    test = Worker.UpdateTableCSV('Tests/region.csv', 'region2', {'id':'int nn u', 'name':'text', 'type':'text'})
    Test.Add(service+'.UpdateTableCSV', 'normal', test, 'OK')

    test = Worker.UpdateTableCSV('Tests/area.csv', 'area', {'id':'int nn u', 'area':'text', 'type_name':'text'},
                                 {'id': 'id', 'type_name': 'type', 'area': 'name'})
    Test.Add(service+'.UpdateTableCSV', 'normal', test, 'OK')

    # ReadBlockCSV
    test = Worker.ReadBlockCSV('Tests/region.csv')
    Test.Add(service+'.ReadBlockCSV', 'normal', test, 239)

    #UpdateBlockCSV
    for row in Worker.mDataCSV:
        row[1] = row[1].upper()
        row[2] = row[2].upper()
        row.append(row[2].lower())
    Worker.mTableCSV.append('name_lower')
    test = Worker.UpdateBlockCSV('region3', {'id':'int nn u', 'type':'text', 'name':'text',
                                             'name_lower':'text'})
    Test.Add(service+'.UpdateBlockCSV', 'normal', test, 'OK')

print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
