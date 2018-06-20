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
##    data = [[0,'Тест 1'],[1,'Тест 2']]
##    test = Worker.AddTable('test1', {'id':'int nn u', 'text':'str'}, data)
##    Test.Add(service+'.AddTable', 'normal', test, 'OK')
##
##    # UpdateTable
##    test = Worker.UpdateTable('test2', {'id':'int nn u', 'text':'text'}, data)
##    Test.Add(service+'.UpdateTable', 'normal', test, 'OK')

    # UpdateTableCSV
    test = Worker.UpdateTableCSV('region', {'id':'int nn u', 'type':'text', 'name':'text'}
                                 , 'Tests/region.csv')
    Test.Add(service+'.UpdateTableCSV', 'normal', test, 'OK')

    test = Worker.UpdateTableCSV('region2', {'id':'int nn u', 'name':'text', 'type':'text'}
                                 , 'Tests/region.csv')
    Test.Add(service+'.UpdateTableCSV', 'normal', test, 'OK')

    test = Worker.UpdateTableCSV('area', {'id':'int nn u', 'area':'text', 'type_name':'text'}
                                 , 'Tests/area.csv', {'id': 'id', 'type_name': 'type', 'area': 'name'})
    Test.Add(service+'.UpdateTableCSV', 'normal', test, 'OK')

print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
