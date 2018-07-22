from Profiler import Profiler, decorator
from Tests.Testing import Test, Report
from Services import Yandex
import DefProcess


@decorator.benchmark
def summ():
    return 800 / 3

summ()

service = 'Yandex'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #

print(DefProcess.GetMemberList(Yandex))
#  DefProcess.GetClass(service)
#  print(DefProcess.GetAllMembers(service))

# FindLang
with Profiler() as p:
    test = Yandex.FindLang('Русский')
    ptime = p.getTime
etalon = 'ru'
Test.Add(service+'.FindLang', 'normal', test, etalon, time=ptime)

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
