from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from services.IATA import IATA

Testing.testService = 'IATA'

print('------- Запущены тесты сервиса %s --------' % Testing.testService)

# здесь тестовая обработка #
with Profiler() as p:
    # Airport
    Testing.testDef = 'GetAirport'
    test = IATA.GetAirport(code='ACM')
    Test.Add('normal code', test, {'code': 'ACM', 'name': 'Арика'})

    test = IATA.GetAirport(code='AR')
    Test.Add('unreal code', test, {})

    Testing.testDef = 'Airport'
    test = IATA.Airport(code='ACM')
    etalon = [('ACM', 'Арика', 'Арика', 5.0, 'Колумбия', -2.133, -71.783, '', '', '', '', '')]
    Test.Add('normal code db', test, etalon)

    test = IATA.Airport(code='ACM', name='Шереметьево')
    Test.Add('normal code-name db', test, etalon)

    test = IATA.Airport(name='Шереметьево')
    etalon = [('SVO', 'Шереметьево', 'Москва', 3.0, 'Россия',
               55.972642, 37.414589, 3700, 190, '+7 (495) 232 65 65', '', 'http://www.svo.aero')]
    Test.Add('normal name db', test, etalon)
    
    test = IATA.Airport(name='ьево')
    etalon = [('BQS', 'Игнатьево', 'Благовещенск', 9.0, 'Россия', 50.425394, 127.412478, '', 194, '', '', ''),
              ('SVO', 'Шереметьево', 'Москва', 3.0, 'Россия', 55.972642, 37.414589, 3700, 190,
               '+7 (495) 232 65 65', '', 'http://www.svo.aero')]
    Test.Add('normal name db', test, etalon)

    test = IATA.Airport(code='ACCN')
    Test.Add('unreal code db', test, [])

    test = IATA.Airport(name='Перьмь')
    Test.Add('unreal name db', test, [])

    test = IATA.Airport()
    Test.Add('crash db', test, [])

    # City
    Testing.testDef = 'GetCity'
    test = IATA.GetCity(code='PEE')
    Test.Add('normal code', test, {'code': 'PEE', 'country_code': 'RU', 'name': 'Пермь'})

    test = IATA.GetCity(code='EEE')
    Test.Add('unreal code', test, {})

    Testing.testDef = 'City'
    test = IATA.City(code='PEE')
    etalon = [('PEE', 'Большое Савино', 'Пермь', -2.0, 'Россия',
               57.914517, 56.021214, 3200, 123, '+7 (342) 294-97-71',
               '', 'http://www.aviaperm.ru')]
    Test.Add('normal code db', test, etalon)

    test = IATA.City(code='PEE', name='Москва')
    Test.Add('normal code-name db', test, etalon)

    test = IATA.City(name='Екат')
    etalon = [('SVX', 'Кольцово', 'Екатеринбург', 5.0, 'Россия',
               56.743108, 60.802728, 3026, 233, '+7 (343) 264-42-02', '',
               'http://www.koltsovo.ru')]
    Test.Add('normal name db', test, etalon)

    test = IATA.City(name='Нью-Йорк') # 11 аэропортов
    Test.Add('normal name big db', len(test), 11)

    test = IATA.City(code='EEE')
    Test.Add('unreal code db', test, [])

    test = IATA.City(name='Перьмь')
    Test.Add('unreal name db', test, [])

    test = IATA.City()
    Test.Add('crash db', test, [])

    # Country
    Testing.testDef = 'GetCountry'
    test = IATA.GetCountry(code='RU')
    Test.Add('normal code',
             test, {'code': 'RU', 'code3': 'RUS', 'iso_numeric': 643, 'name': 'Россия', 'languages': []})

    test = IATA.GetCountry(code='RUU')
    Test.Add('unreal code', test, {})

    Testing.testDef = 'Country'
    test = IATA.Country(code='RU')
    etalon = [('RU', 'RUS', '643', 'Россия')]
    Test.Add('normal code db', test, etalon)

    test = IATA.Country(name='росс')
    Test.Add('normal name db', test, etalon)

    test = IATA.Country(code='EST', name='Россия')
    Test.Add('normal code-name db', test, [('EE', 'EST', '233', 'Эстония')])

    test = IATA.Country(code='WW')
    etalon = [('RU', 'RUS', '643', 'Россия')]
    Test.Add('unreal code db', test, [])

    test = IATA.Country(name='еее')
    Test.Add('unreal name db', test, [])

    test = IATA.Country()
    Test.Add('crush db', test, [])


print('')
print('------- Отчёт тестов сервиса %s --------' % Testing.testService)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % Testing.testService)
print(Report.WriteFails())
