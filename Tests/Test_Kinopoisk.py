from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from services.Kinopoisk import Movies, Persons
from services.DefProcess import Runner

service = 'Kinopoisk'
print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #

Testing.testService = service
# Добавляем все функции класса
for idef in Runner.GetMemberList(Movies):
    Test.AddDef(idef)

# Find movie
Testing.testDef = 'Find'
with Profiler() as p:
    test = Movies.Find('Хан Соло')
    etalon = 'Solo: A Star Wars Story'
Test.Add('normal', test[0][2], etalon)

with Profiler() as p:
    test = Movies.Find('Элийский')
    etalon = []
Test.Add('unreal', test, etalon)

# GetContent movie
Testing.testDef = 'GetContent'
with Profiler() as p:
    test = Movies.GetContent(841277)
    etalon = 'Хан Соло: Звёздные войны. Истории'
Test.Add('normal', test['title'], etalon)

# Find person
Testing.testDef = 'Find'
with Profiler() as p:
    test = Persons.Find('Том Круз')
    etalon = 'Tom Cruise'
Test.Add('normal', test[0][2], etalon)

# GetContent person
Testing.testDef = 'GetContent'
with Profiler() as p:
    test = Persons.GetContent(20302)
    etalon = 'Том Круз'
Test.Add('normal', test['name'], etalon)

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll(service=service))
print(Report.WriteAll(service=Testing.testService))

print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails(service=service))
print(Report.WriteFails(service=Testing.testService))
