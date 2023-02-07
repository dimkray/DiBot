from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from services.DaData import strData, DData

Testing.testService = 'DaData.strData'

print('------- Запущены тесты сервиса %s --------' % Testing.testService)

# здесь тестовая обработка #
with Profiler() as p:

    Testing.testDef = 'Name'
    test = strData.Name('Алеrсандр', False)
    print(test)
    Test.Add('normal', test, 'Александр')

    Testing.testDef = 'Organization'
    test = strData.Organization('ООО Такском', False, False)
    print(test)
    Test.Add('normal', test, 'ООО Такском')

    test = strData.Organization('5036045205', True, False)
    print(test)
    Test.Add('normal', test, '7704211201')

    Testing.testDef = '.Address'
    test = strData.Address('мск Михевская, 7 к1', False)
    print(test)
    Test.Add('normal', test, '7704211201')

print('')
print('------- Отчёт тестов сервиса %s --------' % Testing.testService)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % Testing.testService)
print(Report.WriteFails())
