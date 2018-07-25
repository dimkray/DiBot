from Profiler import Profiler
from Tests.Testing import Test, Report
from Services.DaData import strData, DData

service = 'DaData'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #
with Profiler() as p:
    # isWork
    # test = DData.Address('Пермская обл, пос. Звёздный, ул Бабичева, 2Г')
    # test = strData.Name('Алеrсандр', False)
    # print(test)
    # Test.Add(service+'.Name', 'normal', test, 'Александр')

    # test = strData.Organization('ООО Такском', False, False)
    # print(test)
    # Test.Add(service+'.Name', 'normal', test, 'ООО Такском')

    # test = strData.Organization('7704211201', True, False)
    # print(test)
    # Test.Add(service+'.Name', 'normal', test, '7704211201')

    test = strData.Address('мск Михевская, 7 к1', False)
    print(test)
    Test.Add(service+'.Name', 'normal', test, '7704211201')

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
