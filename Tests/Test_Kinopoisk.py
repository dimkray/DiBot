from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from Services.Kinopoisk import Movies
from Services.DefProcess import Runner

service = 'Kinopoisk'
print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #

Testing.testService = service
# Добавляем все функции класса
for idef in Runner.GetMemberList(Movies):
    Test.AddDef(idef)

# Find
Testing.testDef = 'Find'
with Profiler() as p:
    test = Movies.Find('Хан Соло')
    etalon = 'ru'
Test.Add('normal', test, etalon)

# with Profiler() as p:
#     test = Movie.Find('Элийский')
#     etalon = ''
# Test.Add('unreal', test, etalon)

# GetContent
Testing.testDef = 'GetContent'
with Profiler() as p:
    test = Movies.GetContent('Интердевочка')
    etalon = ""
Test.Add('normal', test, etalon)

# with Profiler() as p:
#     test = Movie.GetContent('xxxx')
#     etalon = ""
# Test.Add('unreal', test, etalon)
#
# with Profiler() as p:
#     test = Movie.GetContent(0)
#     etalon = "#bug: ..."
# Test.Add('crush', test, etalon)


print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll(service=service))
print(Report.WriteAll(service=Testing.testService))

print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails(service=service))
print(Report.WriteFails(service=Testing.testService))
