from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from Processor import Run
import fixer


service = 'Fixer'
print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #

Testing.testService = service
# Добавляем все функции класса
for idef in Run.get_member_list(Fixer):
    Test.AddDef(idef)
    #print(idef)

with Profiler() as p:
    # WriteClasses
    Testing.testDef = 'WriteClasses'
    test = Run.write_classes()
    etalon = 'ru'
    Test.Add('normal', test, etalon)



print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll(service=service))

print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails(service=service))
