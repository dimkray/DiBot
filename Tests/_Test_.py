from Services.DefProcess import Run
from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from Services import _Service_
from Services._Service_ import _Serv_


service = '_Service_'
print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #

Testing.testService = service

# _Def_
Testing.testDef = '_Def_'
with Profiler() as p:
    test = _Service_._Def_('Русский')
    etalon = 'ru'
Test.Add('normal', test, etalon)

with Profiler() as p:
    test = _Service_._Def_('Элийский')
    etalon = ''
Test.Add('unreal', test, etalon)


Testing.testService = '_Serv_'
# Добавляем все функции класса
for idef in Run.GetMemberList(_Serv_):
    Test.AddDef(idef)

Testing.testDef = '_Def_'
with Profiler() as p:
    test = _Serv_._Def_('taxcom')
    etalon = ""
Test.Add('normal', test, etalon)

with Profiler() as p:
    test = _Serv_._Def_('xxxx')
    etalon = ""
Test.Add('unreal', test, etalon)

with Profiler() as p:
    test = _Serv_._Def_(0)
    etalon = "#bug: ..."
Test.Add('crush', test, etalon)


print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll(service=service))
print(Report.WriteAll(service=Testing.testService))

print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails(service=service))
print(Report.WriteFails(service=Testing.testService))
